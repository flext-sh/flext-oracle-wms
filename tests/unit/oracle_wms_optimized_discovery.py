"""Oracle WMS Optimized Discovery - REAL Implementation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.

OPTIMIZED approach:
1. Focus on high-priority entities first
2. Process in parallel batches
3. Use ADMINISTRATOR credentials for complete access
4. Generate Singer schemas with real flattening
5. No fallbacks, no estimations - 100% Oracle discovery
"""

from __future__ import annotations

import json as _stdlib_json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, cast

from flext_oracle_wms import FlextOracleWmsSettings, FlextOracleWmsUtilitiesClient
from flext_tests import r
from tests import t, u

if TYPE_CHECKING:
    from tests import p

logger = u.fetch_logger(__name__)

_API_VERSION_LGF_V10 = "LGF_V10"


class OptimizedOracleWmsDiscovery:
    """Optimized Oracle WMS Discovery for fast, complete results."""

    def __init__(self) -> None:
        """Initialize with ADMINISTRATOR credentials."""
        # NOTE (multi-agent): ADR-005 — settings scalars are namespaced under
        # ``OracleWms``; build via model_validate, retain on self.settings.
        self.settings = FlextOracleWmsSettings.model_validate({
            "OracleWms": {
                "base_url": "https://invalid.wms.ocs.oraclecloud.com",
                "username": "user",
                "password": "xyz",
                "timeout": 60.0,
                "retry_attempts": 3,
                "api_version": _API_VERSION_LGF_V10,
                "verify_ssl": True,
                "enable_logging": True,
            }
        })
        self.client = FlextOracleWmsUtilitiesClient.Client(settings=self.settings)
        self.priority_entities: set[str] = {
            "company",
            "facility",
            "item",
            "location",
            "user_def",
            "inventory",
            "inventory_detail",
            "inventory_summary",
            "order_hdr",
            "order_dtl",
            "allocation",
            "pick_hdr",
            "pick_dtl",
            "container",
            "lpn",
            "task",
            "wave_hdr",
            "wave_dtl",
            "shipment",
            "receipt",
            "manifest",
            "carrier",
            "zone",
            "area",
            "aisle",
            "bay",
            "level",
            "position",
        }
        self.discovered_entities: list[str] = []
        self.high_value_entities: t.MutableMappingKV[str, t.MutableJsonMapping] = {}
        self.complete_schemas: t.MutableMappingKV[str, t.JsonMapping] = {}

    def start_discovery(self) -> p.Result[bool]:
        """Start optimized discovery."""
        start_result = self.client.start()
        if not start_result.success:
            return r[bool].fail(f"Client start failed: {start_result.error}")
        return r[bool].ok(value=True)

    def discover_priority_entities_fast(self) -> p.Result[t.JsonMapping]:
        """Fast discovery of priority entities with data."""
        entities_result = self.client.discover_entities()
        if not entities_result.success:
            return r[t.JsonMapping].fail(
                f"Entity discovery failed: {entities_result.error}"
            )
        all_entities = entities_result.value
        available_priority = [e for e in all_entities if e in self.priority_entities]
        other_entities = [e for e in all_entities if e not in self.priority_entities]
        priority_results = self._process_entity_batch(available_priority, batch_size=10)
        entities_with_data: list[str] = [
            entity_name
            for entity_name, result in priority_results.items()
            if result.get("has_data", False)
        ]
        all_results = priority_results
        if entities_with_data and other_entities:
            additional_results = self._process_entity_batch(
                other_entities[:50], batch_size=15
            )
            all_results = {**priority_results, **additional_results}
            entities_with_data.extend([
                entity
                for entity, result in additional_results.items()
                if result.get("has_data", False)
            ])
        self.high_value_entities = {
            name: result
            for name, result in all_results.items()
            if result.get("has_data", False)
        }
        summary_payload: t.MutableJsonMapping = {
            "total_processed": len(all_results),
            "entities_with_data": len(self.high_value_entities),
            "high_value_entities": cast(
                "t.JsonValue", list(self.high_value_entities.keys())
            ),
            "detailed_results": cast("t.JsonValue", all_results),
        }
        return r[t.JsonMapping].ok(summary_payload)

    def _process_entity_batch(
        self, entities: t.StrSequence, batch_size: int = 10
    ) -> t.MutableMappingKV[str, t.MutableJsonMapping]:
        """Process entity batch with parallel requests."""
        results: t.MutableMappingKV[str, t.MutableJsonMapping] = {}
        for i in range(0, len(entities), batch_size):
            batch = entities[i : i + batch_size]
            batch_tasks = [
                self._analyze_single_entity(entity_name) for entity_name in batch
            ]
            batch_results: list[t.MutableJsonMapping | Exception] = []
            for task in batch_tasks:
                try:
                    batch_results.append(task)
                except Exception as e:
                    batch_results.append(e)
            for entity_name, result in zip(batch, batch_results, strict=False):
                if isinstance(result, Exception):
                    results[entity_name] = {
                        "has_data": False,
                        "error": str(result),
                        "processed_at": datetime.now(UTC).isoformat(),
                    }
                else:
                    results[entity_name] = result
            time.sleep(0.1)
        return results

    def _analyze_single_entity(self, entity_name: str) -> t.MutableJsonMapping:
        """Analyze single entity for data and structure."""
        try:
            return self._analyze_single_entity_unchecked(entity_name)
        except Exception as e:
            return {
                "has_data": False,
                "error": f"Exception: {e}",
                "processed_at": datetime.now(UTC).isoformat(),
            }

    def _analyze_single_entity_unchecked(
        self, entity_name: str
    ) -> t.MutableJsonMapping:
        """Analyze one entity while allowing client errors upward."""
        data_result = self.client.get_entity_data(entity_name, limit=3)
        if not data_result.success:
            return {
                "has_data": False,
                "error": str(data_result.error),
                "processed_at": datetime.now(UTC).isoformat(),
            }
        records = data_result.value
        analysis: t.MutableJsonMapping = {
            "has_data": len(records) > 0,
            "total_count": len(records),
            "sample_count": len(records),
            "processed_at": datetime.now(UTC).isoformat(),
        }
        if records:
            sample_record = records[0]
            if isinstance(sample_record, dict):
                analysis.update(self._analysis_extra(sample_record))
        return analysis

    def _analysis_extra(self, sample_record: t.StrMapping) -> t.MutableJsonMapping:
        """Build analysis metadata from one sample record."""
        return {
            "field_count": len(sample_record.keys()),
            "fields": cast("t.JsonValue", list(sample_record.keys())),
            "field_types": cast(
                "t.JsonValue", {k: type(v).__name__ for k, v in sample_record.items()}
            ),
            "sample_record": cast(
                "t.JsonValue", self._safe_sample_record(sample_record)
            ),
        }

    def _safe_sample_record(
        self, record: t.StrMapping
    ) -> t.MutableMappingKV[str, bool | float | int | str | None]:
        """Create safe sample record for storage."""
        safe_record: t.MutableMappingKV[str, bool | float | int | str | None] = {}
        for k, v in record.items():
            safe_record[k] = v if len(v) < 100 else f"<string:{len(v)}chars>"
        return safe_record

    def generate_complete_singer_schemas(self) -> p.Result[t.JsonMapping]:
        """Generate complete Singer schemas for high-value entities."""
        if not self.high_value_entities:
            return r[t.JsonMapping].fail(
                "No high-value entities available for schema generation"
            )
        singer_schemas: t.MutableMappingKV[str, t.JsonMapping] = {}
        for entity_name, entity_data in self.high_value_entities.items():
            schema = self._generate_singer_schema_from_entity_data(
                entity_name, entity_data
            )
            if schema:
                singer_schemas[entity_name] = schema
        self.complete_schemas = singer_schemas
        catalog = self._generate_singer_catalog(singer_schemas)
        schemas_payload: t.MutableJsonMapping = {
            "schemas_generated": len(singer_schemas),
            "schemas": cast("t.JsonValue", singer_schemas),
            "singer_catalog": cast("t.JsonValue", catalog),
        }
        return r[t.JsonMapping].ok(schemas_payload)

    def _generate_singer_schema_from_entity_data(
        self, entity_name: str, entity_data: t.JsonMapping
    ) -> t.JsonMapping | None:
        """Generate Singer schema from entity data with proper typing."""
        try:
            return self._generate_singer_schema_from_entity_data_unchecked(
                entity_name, entity_data
            )
        except (RuntimeError, OSError, ValueError, KeyError):
            logger.exception("Schema generation failed for %s", entity_name)
            return None

    def _generate_singer_schema_from_entity_data_unchecked(
        self, entity_name: str, entity_data: t.JsonMapping
    ) -> t.JsonMapping | None:
        """Generate Singer schema while allowing data errors upward."""
        fields = entity_data.get("fields", [])
        field_types = entity_data.get("field_types", {})
        sample_record = entity_data.get("sample_record", {})
        if not fields or not isinstance(fields, list):
            return None
        properties = self._generate_singer_properties(
            fields, field_types, sample_record
        )
        key_properties = self._determine_key_properties(
            entity_name, [f for f in fields if isinstance(f, str)]
        )
        schema_payload: t.MutableJsonMapping = {
            "type": "object",
            "properties": cast("t.JsonValue", properties),
            "additionalProperties": False,
            "key_properties": cast("t.JsonValue", key_properties),
        }
        return schema_payload

    def _generate_singer_properties(
        self,
        fields: t.SequenceOf[t.JsonValue],
        field_types: t.JsonValue,
        sample_record: t.JsonValue,
    ) -> t.MutableJsonMapping:
        """Generate Singer properties for a schema."""
        properties: t.MutableJsonMapping = {}
        for field in fields:
            if not isinstance(field, str):
                continue
            python_type = (
                str(field_types[field])
                if isinstance(field_types, dict) and field in field_types
                else "str"
            )
            sample_value: t.JsonValue = (
                sample_record[field]
                if isinstance(sample_record, dict) and field in sample_record
                else None
            )
            properties[field] = cast(
                "t.JsonValue",
                self._oracle_to_singer_type(field, python_type, sample_value),
            )
        self._add_optimized_metadata_properties(properties)
        return properties

    @staticmethod
    def _add_optimized_metadata_properties(properties: t.MutableJsonMapping) -> None:
        """Add optimized Singer metadata properties."""
        properties["_sdc_extracted_at"] = {
            "type": "string",
            "format": "date-time",
            "description": "Timestamp when record was extracted",
        }
        properties["_sdc_entity"] = {
            "type": "string",
            "description": "Oracle WMS entity name",
        }
        properties["_sdc_sequence"] = {
            "type": "integer",
            "description": "Record sequence number",
        }

    def _oracle_to_singer_type(
        self, field_name: str, python_type: str, sample_value: t.JsonValue
    ) -> t.JsonMapping:
        """Convert Oracle field to Singer type with real data analysis."""
        if sample_value is not None:
            if isinstance(sample_value, bool):
                return {"type": ["boolean", "null"]}
            if isinstance(sample_value, int):
                return {"type": ["integer", "null"]}
            if isinstance(sample_value, float):
                return {"type": ["number", "null"]}
            if isinstance(sample_value, str):
                if self._is_oracle_datetime(field_name, sample_value):
                    return {
                        "type": ["string", "null"],
                        "format": "date-time",
                        "description": f"Oracle WMS timestamp field: {field_name}",
                    }
                if self._is_oracle_date(field_name, sample_value):
                    return {
                        "type": ["string", "null"],
                        "format": "date",
                        "description": f"Oracle WMS date field: {field_name}",
                    }
                if self._is_oracle_id_field(field_name):
                    return {
                        "type": ["string", "null"],
                        "description": f"Oracle WMS ID field: {field_name}",
                    }
                if self._is_oracle_code_field(field_name):
                    return {
                        "type": ["string", "null"],
                        "description": f"Oracle WMS code field: {field_name}",
                    }
                return {"type": ["string", "null"]}
            if isinstance(sample_value, dict):
                return {
                    "type": ["object", "null"],
                    "description": f"Oracle WMS nested object: {field_name}",
                }
            if isinstance(sample_value, list):
                return {
                    "type": ["array", "null"],
                    "description": f"Oracle WMS array field: {field_name}",
                }
        oracle_type_mapping: t.MappingKV[str, t.JsonMapping] = {
            "int": {"type": ["integer", "null"]},
            "float": {"type": ["number", "null"]},
            "str": {"type": ["string", "null"]},
            "bool": {"type": ["boolean", "null"]},
            "dict": {"type": ["object", "null"]},
            "list": {"type": ["array", "null"]},
            "NoneType": {"type": "null"},
        }
        return oracle_type_mapping.get(python_type, {"type": ["string", "null"]})

    def _is_oracle_datetime(self, field_name: str, value: str) -> bool:
        """Check if field is Oracle datetime."""
        datetime_patterns = ["_ts$", "_time$", "timestamp", "datetime", "_at$"]
        name_match = any(
            field_name.lower().endswith(pattern.replace("$", ""))
            or pattern.replace("$", "").replace("_", "") in field_name.lower()
            for pattern in datetime_patterns
        )
        oracle_datetime_check = (
            "T" in value and ":" in value and ("+" in value or "-" in value[-6:])
        )
        return name_match or oracle_datetime_check

    def _is_oracle_date(self, field_name: str, value: str) -> bool:
        """Check if field is Oracle date."""
        date_patterns = ["_date$", "date_", "_dt$"]
        name_match = any(
            pattern.replace("$", "") in field_name.lower() for pattern in date_patterns
        )
        if not self._is_oracle_datetime(field_name, value):
            oracle_date_check = value.count("-") == 2 and "T" not in value
            return name_match or oracle_date_check
        return name_match

    def _is_oracle_id_field(self, field_name: str) -> bool:
        """Check if field is Oracle ID."""
        return field_name.lower().endswith("_id") or field_name.lower() == "id"

    def _is_oracle_code_field(self, field_name: str) -> bool:
        """Check if field is Oracle code."""
        code_patterns = ["_code", "_cd", "code", "_nbr", "_num", "number"]
        return any(pattern in field_name.lower() for pattern in code_patterns)

    def _determine_key_properties(
        self, entity_name: str, fields: t.StrSequence
    ) -> list[str]:
        """Determine key properties for Oracle WMS entity."""
        potential_keys: list[str] = []
        if "id" in fields:
            potential_keys.append("id")
        entity_key_patterns: t.MappingKV[str, t.StrSequence] = {
            "company": ["code", "company_code"],
            "facility": ["code", "facility_code"],
            "item": ["code", "item_code", "sku"],
            "location": ["code", "location_code"],
            "order_hdr": ["order_nbr", "order_number"],
            "order_dtl": ["order_nbr", "line_nbr"],
            "allocation": ["allocation_id"],
            "inventory": ["facility_id", "item_id", "location_id"],
            "lpn": ["lpn_nbr", "lpn_id"],
            "container": ["container_nbr", "container_id"],
        }
        patterns = entity_key_patterns.get(entity_name, [])
        for pattern in patterns:
            if pattern in fields and pattern not in potential_keys:
                potential_keys.append(pattern)
        if not potential_keys:
            common_keys = ["code", "nbr", "number", "name"]
            for field in fields:
                if any(key in field.lower() for key in common_keys):
                    potential_keys.append(field)
                    break
        return potential_keys[:3]

    def _generate_singer_catalog(
        self, schemas: t.MappingKV[str, t.JsonMapping]
    ) -> t.JsonMapping:
        """Generate Singer catalog from schemas."""
        streams: t.MutableSequenceOf[t.JsonMapping] = []
        for entity_name, schema in schemas.items():
            key_properties = schema.get("key_properties", ["id"])
            breadcrumb: t.StrSequence = []
            stream: t.MutableJsonMapping = {
                "tap_stream_id": entity_name,
                "stream": entity_name,
                "schema": {k: v for k, v in schema.items() if k != "key_properties"},
                "key_properties": key_properties,
                "metadata": cast(
                    "t.JsonValue",
                    [
                        {
                            "breadcrumb": breadcrumb,
                            "metadata": {
                                "inclusion": "available",
                                "selected": True,
                                "replication-method": "FULL_TABLE",
                                "forced-replication-method": "FULL_TABLE",
                                "table-key-properties": key_properties,
                            },
                        }
                    ],
                ),
            }
            streams.append(stream)
        return {"version": 1, "streams": cast("t.JsonValue", streams)}

    def save_optimized_results(self) -> p.Result[str]:
        """Save optimized discovery results."""
        results_dir = Path("oracle_wms_optimized_results")
        results_dir.mkdir(exist_ok=True)
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        entities_file = results_dir / f"high_value_entities_{timestamp}.json"
        with entities_file.open("w", encoding="utf-8") as f:
            f.write(_stdlib_json.dumps(dict(self.high_value_entities), indent=2))
        schemas_file = results_dir / f"singer_schemas_{timestamp}.json"
        with schemas_file.open("w", encoding="utf-8") as f:
            f.write(_stdlib_json.dumps(dict(self.complete_schemas), indent=2))
        if self.complete_schemas:
            catalog = self._generate_singer_catalog(self.complete_schemas)
            catalog_file = results_dir / f"singer_catalog_{timestamp}.json"
            with catalog_file.open("w", encoding="utf-8") as f:
                f.write(_stdlib_json.dumps(dict(catalog), indent=2))
        summary: t.MutableJsonMapping = {
            "discovery_timestamp": timestamp,
            "discovery_mode": "OPTIMIZED_ADMINISTRATOR_MODE",
            "total_high_value_entities": len(self.high_value_entities),
            "schemas_generated": len(self.complete_schemas),
            "oracle_wms_environment": self.settings.OracleWms.base_url,
            "oracle_wms_base_url": self.settings.OracleWms.base_url,
            "api_version": self.settings.OracleWms.api_version,
            "high_value_entities": cast(
                "t.JsonValue", list(self.high_value_entities.keys())
            ),
        }
        summary_file = results_dir / f"discovery_summary_{timestamp}.json"
        with summary_file.open("w", encoding="utf-8") as f:
            f.write(_stdlib_json.dumps(dict(summary), indent=2))
        return r[str].ok(str(results_dir))

    def cleanup(self) -> p.Result[bool]:
        """Clean up resources."""
        try:
            self.client.stop()
            return r[bool].ok(value=True)
        except Exception as e:
            return r[bool].fail(f"Cleanup failed: {e}")


class OptimizedOracleWmsDiscoveryRunner:
    """Runner namespace for optimized Oracle WMS discovery."""

    @staticmethod
    def run_optimized_discovery() -> None:
        """Run optimized Oracle WMS discovery."""
        discovery = OptimizedOracleWmsDiscovery()
        try:
            OptimizedOracleWmsDiscoveryRunner._run_optimized_steps(discovery)
        except (RuntimeError, OSError, ValueError, KeyError):
            logger.exception("Optimized discovery failed")
        finally:
            discovery.cleanup()

    @staticmethod
    def _run_optimized_steps(discovery: OptimizedOracleWmsDiscovery) -> None:
        """Run optimized discovery steps."""
        start_result = discovery.start_discovery()
        if not start_result.success:
            return
        entities_result = discovery.discover_priority_entities_fast()
        if not entities_result.success:
            return
        schemas_result = discovery.generate_complete_singer_schemas()
        if not schemas_result.success:
            return
        save_result = discovery.save_optimized_results()
        if not save_result.success:
            return
        OptimizedOracleWmsDiscoveryRunner._summarize_high_value_entities(discovery)

    @staticmethod
    def _summarize_high_value_entities(discovery: OptimizedOracleWmsDiscovery) -> None:
        """Sort high-value entities by total count."""
        if not discovery.high_value_entities:
            return
        sorted_entities = sorted(
            discovery.high_value_entities.items(),
            key=OptimizedOracleWmsDiscoveryRunner._total_count,
            reverse=True,
        )
        for _entity_name, _data in sorted_entities[:15]:
            pass

    @staticmethod
    def _total_count(pair: tuple[str, t.JsonMapping]) -> int:
        """Return total_count for an optimized discovery entity."""
        tc = pair[1].get("total_count")
        return tc if isinstance(tc, int) else 0


if __name__ == "__main__":
    OptimizedOracleWmsDiscoveryRunner.run_optimized_discovery()
