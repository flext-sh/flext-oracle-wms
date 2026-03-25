"""Oracle WMS Focused Discovery - REAL Implementation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import json
from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from datetime import UTC, datetime
from pathlib import Path
from types import NoneType

from flext_core import FlextLogger, r

from flext_oracle_wms import (
    FlextOracleWmsClient,
    FlextOracleWmsClientSettings,
    create_oracle_wms_client,
)
from tests import t

logger = FlextLogger(__name__)

type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | Mapping[str, JsonValue] | Sequence[JsonValue]

_API_VERSION_LGF_V10 = "LGF_V10"


class FocusedOracleWmsDiscovery:
    """Focused Oracle WMS Discovery - find entities with data FAST."""

    def __init__(self) -> None:
        """Initialize with ADMINISTRATOR credentials."""
        self.config = FlextOracleWmsClientSettings(
            base_url="https://invalid.wms.ocs.oraclecloud.com",
            username="USER_WMS_INTEGRA",
            password="jmCyS7BK94YvhS@",
            environment="test",
            timeout=30.0,
            max_retries=2,
            api_version=_API_VERSION_LGF_V10,
            verify_ssl=True,
            enable_logging=True,
        )
        self.client: FlextOracleWmsClient = create_oracle_wms_client(
            self.config,
            mock_mode=False,
        )
        self.quick_test_entities: Sequence[str] = [
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
        self.entities_with_data: MutableMapping[str, t.NormalizedValue] = {}
        self.complete_schemas: MutableMapping[str, t.NormalizedValue] = {}

    def execute_focused_discovery(self) -> r[Mapping[str, t.NormalizedValue]]:
        """Execute complete focused discovery."""
        try:
            self.client.start()
            entities_result = self.client.discover_entities()
            if not entities_result.is_success:
                return r[Mapping[str, t.NormalizedValue]].fail(
                    f"Entity discovery failed: {entities_result.error}",
                )
            all_entities = entities_result.value
            available_quick = [e for e in self.quick_test_entities if e in all_entities]
            data_entities = self._quick_data_scan(available_quick)
            if data_entities and len(all_entities) > len(available_quick):
                remaining = [e for e in all_entities if e not in available_quick][:30]
                additional_data = self._quick_data_scan(remaining)
                data_entities.update(additional_data)
            self.entities_with_data = data_entities
            if not data_entities:
                structure_entities = self._get_entity_structures(available_quick[:5])
                schemas = self._generate_schemas_from_structures(structure_entities)
            else:
                schemas = self._generate_schemas_from_data(data_entities)
            self.complete_schemas = schemas
            save_result = self._save_focused_results()
            if data_entities:

                def _entity_count(
                    pair: tuple[str, t.NormalizedValue],
                ) -> int:
                    meta = pair[1]
                    if isinstance(meta, dict):
                        c = meta.get("count")
                        if isinstance(c, int):
                            return c
                    return 0

                sorted_entities = sorted(
                    data_entities.items(),
                    key=_entity_count,
                    reverse=True,
                )
                for _entity_name, _data in sorted_entities:
                    pass
            if schemas:
                for _schema in schemas.values():
                    pass
            return r[Mapping[str, t.NormalizedValue]].ok({
                "total_entities": len(all_entities),
                "entities_with_data": len(data_entities),
                "schemas_generated": len(schemas),
                "results_path": save_result.value if save_result.is_success else None,
                "data_entities": data_entities,
                "schemas": schemas,
            })
        except Exception as e:
            logger.exception("Focused discovery failed")
            return r[Mapping[str, t.NormalizedValue]].fail(f"Discovery failed: {e}")
        finally:
            self.client.stop()

    def _quick_data_scan(
        self, entities: t.StrSequence
    ) -> MutableMapping[str, t.NormalizedValue]:
        """Quick scan to find entities with actual data."""
        data_entities: MutableMapping[str, t.NormalizedValue] = {}
        for entity_name in entities:
            try:
                result = self.client.get_entity_data(entity_name, limit=1)
                if result.is_success:
                    records = result.value
                    if records:
                        detailed_result = self.client.get_entity_data(
                            entity_name,
                            limit=3,
                        )
                        if detailed_result.is_success:
                            detailed_records = detailed_result.value
                            entity_info: MutableMapping[str, t.NormalizedValue] = {
                                "count": len(detailed_records),
                                "has_data": True,
                                "sample_size": len(detailed_records),
                            }
                            if detailed_records:
                                sample = detailed_records[0]
                                if isinstance(sample, dict):
                                    entity_info.update({
                                        "field_count": len(sample.keys()),
                                        "sample_fields": list(sample.keys()),
                                        "field_types": {
                                            k: type(v).__name__
                                            for k, v in sample.items()
                                        },
                                        "sample_record": self._safe_sample(
                                            sample,
                                        ),
                                    })
                            data_entities[entity_name] = entity_info
            except (RuntimeError, OSError, ValueError, KeyError):
                logger.debug("Failed to process entity %s", entity_name)
        return data_entities

    def _get_entity_structures(
        self,
        entities: t.StrSequence,
    ) -> MutableMapping[str, t.NormalizedValue]:
        """Get entity structures even without data."""
        structures: MutableMapping[str, t.NormalizedValue] = {}
        for entity_name in entities:
            try:
                result = self.client.get_entity_data(entity_name, limit=1)
                if result.is_success:
                    records = result.value
                    if records:
                        sample = records[0]
                        if isinstance(sample, dict):
                            structures[entity_name] = {
                                "fields": list(sample.keys()),
                                "field_types": {
                                    k: type(v).__name__ for k, v in sample.items()
                                },
                                "sample_record": self._safe_sample(sample),
                                "has_data": False,
                            }
            except (RuntimeError, OSError, ValueError, KeyError):
                logger.debug("Failed to get structure for entity %s", entity_name)
        return structures

    def _safe_sample(
        self,
        record: t.StrMapping,
    ) -> MutableMapping[str, NoneType | bool | float | int | str]:
        """Create safe sample record."""
        safe: MutableMapping[str, NoneType | bool | float | int | str] = {}
        for k, v in list(record.items())[:10]:
            if isinstance(v, (str, int, float, bool, type(None))):
                if (isinstance(v, str) and len(v) < 50) or not isinstance(v, str):
                    safe[k] = v
                else:
                    safe[k] = f"<{len(v)}chars>"
            else:
                safe[k] = f"<{type(v).__name__}>"
        return safe

    def _generate_schemas_from_data(
        self,
        data_entities: Mapping[str, t.NormalizedValue],
    ) -> MutableMapping[str, t.NormalizedValue]:
        """Generate Singer schemas from entities with data."""
        schemas: MutableMapping[str, t.NormalizedValue] = {}
        for entity_name, entity_data in data_entities.items():
            if isinstance(entity_data, dict):
                schema = self._create_singer_schema(entity_name, entity_data)
                if schema:
                    schemas[entity_name] = schema
        return schemas

    def _generate_schemas_from_structures(
        self,
        structure_entities: Mapping[str, t.NormalizedValue],
    ) -> MutableMapping[str, t.NormalizedValue]:
        """Generate Singer schemas from structures."""
        schemas: MutableMapping[str, t.NormalizedValue] = {}
        for entity_name, structure_data in structure_entities.items():
            if isinstance(structure_data, dict):
                schema = self._create_singer_schema(entity_name, structure_data)
                if schema:
                    schemas[entity_name] = schema
        return schemas

    def _create_singer_schema(
        self,
        entity_name: str,
        entity_data: Mapping[str, t.NormalizedValue],
    ) -> Mapping[str, t.NormalizedValue] | None:
        """Create Singer schema with proper Oracle WMS typing."""
        try:
            fields = entity_data.get("sample_fields", entity_data.get("fields", []))
            field_types = entity_data.get("field_types", {})
            sample_record = entity_data.get("sample_record", {})
            if not fields or not isinstance(fields, list):
                return None
            properties: MutableMapping[str, t.NormalizedValue] = {}
            for field in fields:
                if not isinstance(field, str):
                    continue
                python_type = (
                    field_types[field]
                    if isinstance(field_types, dict) and field in field_types
                    else "str"
                )
                sample_value: t.NormalizedValue = (
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
                properties[field] = singer_type
            properties["_sdc_extracted_at"] = {"type": "string", "format": "date-time"}
            properties["_sdc_entity"] = {"type": "string"}
            properties["_sdc_record_hash"] = {"type": ["string", "null"]}
            str_fields: Sequence[str] = [f for f in fields if isinstance(f, str)]
            key_properties = self._get_oracle_key_properties(entity_name, str_fields)
            return {
                "type": "object",
                "properties": properties,
                "additionalProperties": False,
                "key_properties": key_properties,
                "oracle_wms_entity": entity_name,
                "oracle_wms_environment": str(self.config.environment),
            }
        except (RuntimeError, OSError, ValueError, KeyError):
            logger.exception("Schema creation failed for %s", entity_name)
            return None

    def _oracle_field_to_singer_type(
        self,
        field_name: str,
        python_type: str,
        sample_value: t.NormalizedValue,
        entity_name: str,
    ) -> Mapping[str, t.NormalizedValue]:
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
        if isinstance(value, str):
            value_check = (
                "T" in value and ":" in value and ("+" in value or "-" in value[-6:])
            )
            return name_check or value_check
        return name_check

    def _is_oracle_code(self, field_name: str) -> bool:
        """Check if field is Oracle code."""
        code_indicators = ["_code", "code", "_cd", "_nbr", "number"]
        return any(indicator in field_name.lower() for indicator in code_indicators)

    def _is_oracle_url(self, field_name: str, value: str) -> bool:
        """Check if field is Oracle URL."""
        return (
            field_name.lower() == "url"
            and isinstance(value, str)
            and value.startswith("http")
        )

    def _get_oracle_key_properties(
        self,
        entity_name: str,
        fields: Sequence[str],
    ) -> Sequence[str]:
        """Get Oracle WMS key properties for entity."""
        keys: MutableSequence[str] = []
        if "id" in fields:
            keys.append("id")
        entity_keys: Mapping[str, list[str]] = {
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

    def _save_focused_results(self) -> r[str]:
        """Save focused discovery results."""
        results_dir = Path("oracle_wms_focused_results")
        results_dir.mkdir(exist_ok=True)
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        if self.entities_with_data:
            entities_file = results_dir / f"entities_with_data_{timestamp}.json"
            with entities_file.open("w", encoding="utf-8") as f:
                json.dump(self.entities_with_data, f, indent=2, default=str)
        if self.complete_schemas:
            schemas_file = results_dir / f"singer_schemas_{timestamp}.json"
            with schemas_file.open("w", encoding="utf-8") as f:
                json.dump(self.complete_schemas, f, indent=2, default=str)
            catalog = self._create_singer_catalog()
            catalog_file = results_dir / f"singer_catalog_{timestamp}.json"
            with catalog_file.open("w", encoding="utf-8") as f:
                json.dump(catalog, f, indent=2, default=str)
        summary = {
            "timestamp": timestamp,
            "mode": "FOCUSED_ADMINISTRATOR_DISCOVERY",
            "oracle_environment": self.config.environment,
            "entities_with_data_count": len(self.entities_with_data),
            "schemas_generated_count": len(self.complete_schemas),
            "entities_with_data": list(self.entities_with_data.keys()),
            "schema_entities": list(self.complete_schemas.keys()),
        }
        summary_file = results_dir / f"summary_{timestamp}.json"
        with summary_file.open("w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, default=str)
        return r[str].ok(str(results_dir))

    def _create_singer_catalog(self) -> Mapping[str, t.NormalizedValue]:
        """Create Singer catalog."""
        streams: MutableSequence[MutableMapping[str, t.NormalizedValue]] = []
        for entity_name, schema in self.complete_schemas.items():
            if not isinstance(schema, dict):
                continue
            key_properties = schema.get("key_properties", [])
            schema_without_keys: MutableMapping[str, t.NormalizedValue] = {
                k: v for k, v in schema.items() if k != "key_properties"
            }
            breadcrumb: Sequence[str] = []
            stream: MutableMapping[str, t.NormalizedValue] = {
                "tap_stream_id": entity_name,
                "stream": entity_name,
                "schema": schema_without_keys,
                "key_properties": key_properties,
                "metadata": [
                    {
                        "breadcrumb": breadcrumb,
                        "metadata": {
                            "inclusion": "available",
                            "selected": True,
                            "replication-method": "FULL_TABLE",
                        },
                    },
                ],
            }
            streams.append(stream)
        return {"version": 1, "streams": streams}


def main() -> None:
    """Main execution."""
    discovery = FocusedOracleWmsDiscovery()
    result = discovery.execute_focused_discovery()
    if result.is_success:
        _data = result.value


if __name__ == "__main__":
    main()
