"""Oracle WMS Focused Discovery - REAL Implementation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import json as _stdlib_json
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, cast

from flext_tests import r

from flext_oracle_wms import FlextOracleWmsSettings
from flext_oracle_wms.utilities import FlextOracleWmsUtilitiesClient
from tests.typings import t
from tests.utilities import u

if TYPE_CHECKING:
    from collections.abc import (
        MutableMapping,
        MutableSequence,
    )

    from tests.protocols import p

logger = u.fetch_logger(__name__)

_API_VERSION_LGF_V10 = "LGF_V10"


class FocusedOracleWmsDiscovery:
    """Focused Oracle WMS Discovery - find entities with data FAST."""

    def __init__(self) -> None:
        """Initialize with ADMINISTRATOR credentials."""
        settings = FlextOracleWmsSettings(
            base_url="https://invalid.wms.ocs.oraclecloud.com",
            username="user",
            password="xyz",
            timeout=30.0,
            max_retries=2,
            api_version=_API_VERSION_LGF_V10,
            verify_ssl=True,
            enable_logging=True,
        )
        self.client = FlextOracleWmsUtilitiesClient.Client(settings=settings)
        self.quick_test_entities: t.StrSequence = [
            "company",
            "facility",
            "item",
            "location",
            "inventory",
            "user_def",
            "container",
            "carrier",
            "zone",
            "area",
            "order_hdr",
            "order_dtl",
            "allocation",
            "pick_hdr",
            "pick_dtl",
            "lpn",
            "task",
            "shipment",
            "receipt",
            "manifest",
        ]
        self.entities_with_data: t.MutableJsonMapping = {}
        self.complete_schemas: t.MutableJsonMapping = {}

    def execute_focused_discovery(self) -> p.Result[t.JsonMapping]:
        """Execute complete focused discovery."""
        try:
            return self._execute_focused_discovery_unchecked()
        except Exception as e:
            logger.exception("Focused discovery failed")
            return r[t.JsonMapping].fail(f"Discovery failed: {e}")
        finally:
            self.client.stop()

    def _execute_focused_discovery_unchecked(self) -> p.Result[t.JsonMapping]:
        """Execute focused discovery while allowing client failures upward."""
        self.client.start()
        entities_result = self.client.discover_entities()
        if not entities_result.success:
            return r[t.JsonMapping].fail(
                f"Entity discovery failed: {entities_result.error}",
            )
        all_entities = entities_result.value
        available_quick = [e for e in self.quick_test_entities if e in all_entities]
        data_entities = self._quick_data_scan(available_quick)
        if data_entities and len(all_entities) > len(available_quick):
            remaining = [e for e in all_entities if e not in available_quick][:30]
            data_entities.update(self._quick_data_scan(remaining))
        self.entities_with_data = data_entities
        schemas = self._generate_focused_schemas(data_entities, available_quick)
        self.complete_schemas = schemas
        save_result = self._save_focused_results()
        self._summarize_data_entities(data_entities)
        self._visit_schemas(schemas)
        summary_payload: t.MutableJsonMapping = {
            "total_entities": len(all_entities),
            "entities_with_data": len(data_entities),
            "schemas_generated": len(schemas),
            "results_path": save_result.value if save_result.success else None,
            "data_entities": cast("t.JsonValue", data_entities),
            "schemas": cast("t.JsonValue", schemas),
        }
        return r[t.JsonMapping].ok(summary_payload)

    def _generate_focused_schemas(
        self,
        data_entities: t.JsonMapping,
        available_quick: t.StrSequence,
    ) -> t.MutableJsonMapping:
        """Generate focused schemas from available data or structure probes."""
        if data_entities:
            return self._generate_schemas_from_data(data_entities)
        structure_entities = self._get_entity_structures(available_quick[:5])
        return self._generate_schemas_from_structures(structure_entities)

    @staticmethod
    def _entity_count(pair: tuple[str, t.JsonValue]) -> int:
        """Return the count field for a discovered entity."""
        meta = pair[1]
        if isinstance(meta, dict):
            count = meta.get("count")
            if isinstance(count, int):
                return count
        return 0

    def _summarize_data_entities(self, data_entities: t.JsonMapping) -> None:
        """Sort data entities by count to exercise deterministic ordering."""
        if not data_entities:
            return
        sorted_entities = sorted(
            data_entities.items(),
            key=self._entity_count,
            reverse=True,
        )
        for _entity_name, _data in sorted_entities:
            pass

    @staticmethod
    def _visit_schemas(schemas: t.JsonMapping) -> None:
        """Iterate generated schemas for deterministic coverage."""
        if schemas:
            for _schema in schemas.values():
                pass

    def _quick_data_scan(self, entities: t.StrSequence) -> t.MutableJsonMapping:
        """Quick scan to find entities with actual data."""
        data_entities: t.MutableJsonMapping = {}
        for entity_name in entities:
            try:
                entity_info = self._scan_entity_data(entity_name)
                if entity_info is not None:
                    data_entities[entity_name] = cast("t.JsonValue", entity_info)
            except (RuntimeError, OSError, ValueError, KeyError):
                logger.debug("Failed to process entity %s", entity_name)
        return data_entities

    def _scan_entity_data(self, entity_name: str) -> t.MutableJsonMapping | None:
        """Scan one entity and return sample metadata when data exists."""
        result = self.client.get_entity_data(entity_name, limit=1)
        if not result.success or not result.value:
            return None
        detailed_result = self.client.get_entity_data(entity_name, limit=3)
        if not detailed_result.success:
            return None
        detailed_records = detailed_result.value
        entity_info: t.MutableJsonMapping = {
            "count": len(detailed_records),
            "has_data": True,
            "sample_size": len(detailed_records),
        }
        if detailed_records:
            sample = detailed_records[0]
            if isinstance(sample, dict):
                entity_info.update(self._entity_info_extra(sample))
        return entity_info

    def _entity_info_extra(self, sample: t.StrMapping) -> t.MutableJsonMapping:
        """Build extra metadata for an entity sample record."""
        return {
            "field_count": len(sample.keys()),
            "sample_fields": cast("t.JsonValue", list(sample.keys())),
            "field_types": cast(
                "t.JsonValue",
                {k: type(v).__name__ for k, v in sample.items()},
            ),
            "sample_record": cast("t.JsonValue", self._safe_sample(sample)),
        }

    def _get_entity_structures(
        self,
        entities: t.StrSequence,
    ) -> t.MutableJsonMapping:
        """Get entity structures even without data."""
        structures: t.MutableJsonMapping = {}
        for entity_name in entities:
            try:
                structure_payload = self._get_entity_structure(entity_name)
                if structure_payload is not None:
                    structures[entity_name] = cast("t.JsonValue", structure_payload)
            except (RuntimeError, OSError, ValueError, KeyError):
                logger.debug("Failed to get structure for entity %s", entity_name)
        return structures

    def _get_entity_structure(self, entity_name: str) -> t.MutableJsonMapping | None:
        """Return structure metadata for one entity when a sample exists."""
        result = self.client.get_entity_data(entity_name, limit=1)
        if not result.success or not result.value:
            return None
        sample = result.value[0]
        if not isinstance(sample, dict):
            return None
        return {
            "fields": cast("t.JsonValue", list(sample.keys())),
            "field_types": cast(
                "t.JsonValue",
                {k: type(v).__name__ for k, v in sample.items()},
            ),
            "sample_record": cast("t.JsonValue", self._safe_sample(sample)),
            "has_data": False,
        }

    def _safe_sample(
        self,
        record: t.StrMapping,
    ) -> MutableMapping[str, bool | float | int | str | None]:
        """Create safe sample record."""
        safe: MutableMapping[str, bool | float | int | str | None] = {}
        for k, v in list(record.items())[:10]:
            safe[k] = v if len(v) < 50 else f"<{len(v)}chars>"
        return safe

    def _generate_schemas_from_data(
        self,
        data_entities: t.JsonMapping,
    ) -> t.MutableJsonMapping:
        """Generate Singer schemas from entities with data."""
        schemas: t.MutableJsonMapping = {}
        for entity_name, entity_data in data_entities.items():
            if isinstance(entity_data, dict):
                schema = self._create_singer_schema(entity_name, entity_data)
                if schema:
                    schemas[entity_name] = cast("t.JsonValue", schema)
        return schemas

    def _generate_schemas_from_structures(
        self,
        structure_entities: t.JsonMapping,
    ) -> t.MutableJsonMapping:
        """Generate Singer schemas from structures."""
        schemas: t.MutableJsonMapping = {}
        for entity_name, structure_data in structure_entities.items():
            if isinstance(structure_data, dict):
                schema = self._create_singer_schema(entity_name, structure_data)
                if schema:
                    schemas[entity_name] = cast("t.JsonValue", schema)
        return schemas

    def _create_singer_schema(
        self,
        entity_name: str,
        entity_data: t.JsonMapping,
    ) -> t.JsonMapping | None:
        """Create Singer schema with proper Oracle WMS typing."""
        try:
            return self._create_singer_schema_unchecked(entity_name, entity_data)
        except (RuntimeError, OSError, ValueError, KeyError):
            logger.exception("Schema creation failed for %s", entity_name)
            return None

    def _create_singer_schema_unchecked(
        self,
        entity_name: str,
        entity_data: t.JsonMapping,
    ) -> t.JsonMapping | None:
        """Create a Singer schema while allowing data errors upward."""
        fields = entity_data.get("sample_fields", entity_data.get("fields", []))
        field_types = entity_data.get("field_types", {})
        sample_record = entity_data.get("sample_record", {})
        if not fields or not isinstance(fields, list):
            return None
        properties = self._create_schema_properties(
            entity_name,
            fields,
            field_types,
            sample_record,
        )
        key_properties = self._get_oracle_key_properties(
            entity_name,
            [f for f in fields if isinstance(f, str)],
        )
        schema_result: t.MutableJsonMapping = {
            "type": "object",
            "properties": cast("t.JsonValue", properties),
            "additionalProperties": False,
            "key_properties": cast("t.JsonValue", key_properties),
            "oracle_wms_entity": entity_name,
            "oracle_wms_environment": settings.base_url,
        }
        return schema_result

    def _create_schema_properties(
        self,
        entity_name: str,
        fields: t.SequenceOf[t.JsonValue],
        field_types: t.JsonValue,
        sample_record: t.JsonValue,
    ) -> t.MutableJsonMapping:
        """Create Singer schema properties for one entity."""
        properties: t.MutableJsonMapping = {}
        for field in fields:
            if not isinstance(field, str):
                continue
            python_type = (
                field_types[field]
                if isinstance(field_types, dict) and field in field_types
                else "str"
            )
            sample_value: t.JsonValue = (
                sample_record[field]
                if isinstance(sample_record, dict) and field in sample_record
                else None
            )
            singer_type = self._oracle_field_to_singer_type(
                field,
                str(python_type),
                sample_value,
                entity_name,
            )
            properties[field] = cast("t.JsonValue", singer_type)
        self._add_schema_metadata_properties(properties)
        return properties

    @staticmethod
    def _add_schema_metadata_properties(properties: t.MutableJsonMapping) -> None:
        """Add Singer metadata properties."""
        properties["_sdc_extracted_at"] = cast(
            "t.JsonValue",
            {"type": "string", "format": "date-time"},
        )
        properties["_sdc_entity"] = cast("t.JsonValue", {"type": "string"})
        properties["_sdc_record_hash"] = cast(
            "t.JsonValue",
            {"type": ["string", "null"]},
        )

    def _oracle_field_to_singer_type(
        self,
        field_name: str,
        python_type: str,
        sample_value: t.JsonValue,
        entity_name: str,
    ) -> t.JsonMapping:
        """Convert Oracle WMS field to Singer type with context."""
        if sample_value is not None:
            if isinstance(sample_value, bool):
                return {"type": ["boolean", "null"]}
            if isinstance(sample_value, int):
                if self._is_oracle_id_field(field_name):
                    return {
                        "type": ["integer", "null"],
                        "description": f"Oracle WMS {entity_name} ID field",
                    }
                return {"type": ["integer", "null"]}
            if isinstance(sample_value, float):
                return {"type": ["number", "null"]}
            if isinstance(sample_value, str):
                if self._is_oracle_timestamp(field_name, sample_value):
                    return {
                        "type": ["string", "null"],
                        "format": "date-time",
                        "description": "Oracle WMS timestamp",
                    }
                if self._is_oracle_code(field_name):
                    return {
                        "type": ["string", "null"],
                        "description": f"Oracle WMS {entity_name} code",
                    }
                if self._is_oracle_url(field_name, sample_value):
                    return {
                        "type": ["string", "null"],
                        "format": "uri",
                        "description": "Oracle WMS API URL",
                    }
                return {"type": ["string", "null"]}
            if isinstance(sample_value, dict):
                return {"type": ["object", "null"]}
            if isinstance(sample_value, list):
                return {"type": ["array", "null"]}
        _ = python_type  # used for future type-based fallback
        return {"type": ["string", "null"]}

    def _is_oracle_id_field(self, field_name: str) -> bool:
        """Check if field is Oracle ID."""
        return field_name.lower().endswith("_id") or field_name.lower() == "id"

    def _is_oracle_timestamp(self, field_name: str, value: str) -> bool:
        """Check if field is Oracle timestamp."""
        ts_indicators = ["_ts", "timestamp", "_time", "_at"]
        name_check = any(indicator in field_name.lower() for indicator in ts_indicators)
        value_check = (
            "T" in value and ":" in value and ("+" in value or "-" in value[-6:])
        )
        return name_check or value_check

    def _is_oracle_code(self, field_name: str) -> bool:
        """Check if field is Oracle code."""
        code_indicators = ["_code", "code", "_cd", "_nbr", "number"]
        return any(indicator in field_name.lower() for indicator in code_indicators)

    def _is_oracle_url(self, field_name: str, value: str) -> bool:
        """Check if field is Oracle URL."""
        return field_name.lower() == "url" and value.startswith("http")

    def _get_oracle_key_properties(
        self,
        entity_name: str,
        fields: t.StrSequence,
    ) -> t.StrSequence:
        """Get Oracle WMS key properties for entity."""
        keys: MutableSequence[str] = []
        if "id" in fields:
            keys.append("id")
        entity_keys: t.MappingKV[str, list[str]] = {
            "company": ["code", "company_code"],
            "facility": ["code", "facility_code"],
            "item": ["code", "item_code"],
            "location": ["code", "location_code"],
            "order_hdr": ["order_nbr"],
            "order_dtl": ["order_nbr", "line_nbr"],
            "allocation": ["id"],
            "pick_hdr": ["pick_nbr"],
            "pick_dtl": ["pick_nbr", "line_nbr"],
            "lpn": ["lpn_nbr"],
            "container": ["container_nbr"],
            "shipment": ["shipment_nbr"],
            "receipt": ["receipt_nbr"],
        }
        specific_keys = entity_keys.get(entity_name, [])
        for key in specific_keys:
            if key in fields and key not in keys:
                keys.append(key)
        return keys or (["id"] if "id" in fields else [])

    def _save_focused_results(self) -> p.Result[str]:
        """Save focused discovery results."""
        results_dir = Path("oracle_wms_focused_results")
        results_dir.mkdir(exist_ok=True)
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        if self.entities_with_data:
            entities_file = results_dir / f"entities_with_data_{timestamp}.json"
            with entities_file.open("w", encoding="utf-8") as f:
                f.write(_stdlib_json.dumps(dict(self.entities_with_data), indent=2))
        if self.complete_schemas:
            schemas_file = results_dir / f"singer_schemas_{timestamp}.json"
            with schemas_file.open("w", encoding="utf-8") as f:
                f.write(_stdlib_json.dumps(dict(self.complete_schemas), indent=2))
            catalog = self._create_singer_catalog()
            catalog_file = results_dir / f"singer_catalog_{timestamp}.json"
            with catalog_file.open("w", encoding="utf-8") as f:
                f.write(_stdlib_json.dumps(dict(catalog), indent=2))
        summary = {
            "timestamp": timestamp,
            "mode": "FOCUSED_ADMINISTRATOR_DISCOVERY",
            "oracle_environment": settings.base_url,
            "entities_with_data_count": len(self.entities_with_data),
            "schemas_generated_count": len(self.complete_schemas),
            "entities_with_data": list(self.entities_with_data.keys()),
            "schema_entities": list(self.complete_schemas.keys()),
        }
        summary_file = results_dir / f"summary_{timestamp}.json"
        with summary_file.open("w", encoding="utf-8") as f:
            f.write(_stdlib_json.dumps(dict(summary), indent=2))
        return r[str].ok(str(results_dir))

    def _create_singer_catalog(self) -> t.JsonMapping:
        """Create Singer catalog."""
        streams: MutableSequence[t.MutableJsonMapping] = []
        for entity_name, schema in self.complete_schemas.items():
            if not isinstance(schema, dict):
                continue
            key_properties = schema.get("key_properties", [])
            schema_without_keys: t.MutableJsonMapping = {
                k: v for k, v in schema.items() if k != "key_properties"
            }
            breadcrumb: t.StrSequence = []
            stream: t.MutableJsonMapping = {
                "tap_stream_id": entity_name,
                "stream": entity_name,
                "schema": cast("t.JsonValue", schema_without_keys),
                "key_properties": cast("t.JsonValue", key_properties),
                "metadata": cast(
                    "t.JsonValue",
                    [
                        {
                            "breadcrumb": breadcrumb,
                            "metadata": {
                                "inclusion": "available",
                                "selected": True,
                                "replication-method": "FULL_TABLE",
                            },
                        },
                    ],
                ),
            }
            streams.append(stream)
        return {"version": 1, "streams": cast("t.JsonValue", streams)}


def main() -> None:
    """Main execution."""
    discovery = FocusedOracleWmsDiscovery()
    result = discovery.execute_focused_discovery()
    if result.success:
        _data = result.value


if __name__ == "__main__":
    main()
