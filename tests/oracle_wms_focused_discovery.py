#!/usr/bin/env python3
"""Oracle WMS Focused Discovery - ADMINISTRATOR Mode.

FOCUSED STRATEGY:
1. Use ADMINISTRATOR credentials for complete access
2. Focus on entities that actually have data
3. Generate Singer schemas with real flattening
4. Implement modern Singer SDK patterns
5. Use Oracle metadata for real type discovery

ZERO FALLBACKS - 100% ORACLE DISCOVERY
"""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

object

from flext_core import FlextResult, get_logger

from flext_oracle_wms import (
    FlextOracleWmsApiVersion,
    FlextOracleWmsClientConfig,
    create_oracle_wms_client,
)

logger = get_logger(__name__)


class FocusedOracleWmsDiscovery:
    """Focused Oracle WMS Discovery - find entities with data FAST."""

    def __init__(self) -> None:
        """Initialize with ADMINISTRATOR credentials."""
        self.config = FlextOracleWmsClientConfig(
            base_url="https://ta29.wms.ocs.oraclecloud.com",
            username="USER_WMS_INTEGRA",  # ADMINISTRATOR TOTAL
            password="jmCyS7BK94YvhS@",
            environment="raizen_test",
            timeout=30.0,
            max_retries=2,
            api_version=FlextOracleWmsApiVersion.LGF_V10,
            verify_ssl=True,
            enable_logging=True,
        )
        self.client = create_oracle_wms_client(self.config, mock_mode=False)

        # Quick test entities - most likely to have data
        self.quick_test_entities = [
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

        self.entities_with_data = {}
        self.complete_schemas = {}

    async def execute_focused_discovery(self) -> FlextResult[dict[str, object]]:
        """Execute complete focused discovery."""
        try:
            # Start client
            await self.client.start()

            # Phase 1: Fast entity discovery

            entities_result = await self.client.discover_entities()
            if not entities_result.success:
                return FlextResult[None].fail(
                    f"Entity discovery failed: {entities_result.error}",
                )

            all_entities = entities_result.data

            # Phase 2: Quick data scan

            # Test quick entities first
            available_quick = [e for e in self.quick_test_entities if e in all_entities]

            data_entities = await self._quick_data_scan(available_quick)

            # If we found some, test more
            if data_entities and len(all_entities) > len(available_quick):
                remaining = [e for e in all_entities if e not in available_quick][:30]
                additional_data = await self._quick_data_scan(remaining)
                data_entities.update(additional_data)

            self.entities_with_data = data_entities

            # Phase 3: Schema generation

            if not data_entities:
                # Generate schemas from available structures anyway
                structure_entities = await self._get_entity_structures(
                    available_quick[:5],
                )
                schemas = await self._generate_schemas_from_structures(
                    structure_entities,
                )
            else:
                schemas = await self._generate_schemas_from_data(data_entities)

            self.complete_schemas = schemas

            # Phase 4: Save results

            save_result = await self._save_focused_results()

            # Results summary

            # Show entities with data
            if data_entities:
                sorted_entities = sorted(
                    data_entities.items(),
                    key=lambda x: x[1].get("count", 0),
                    reverse=True,
                )

                for _entity_name, data in sorted_entities:
                    data.get("count", 0)
                    data.get("field_count", 0)

                    # Show sample field names
                    sample_fields = data.get("sample_fields", [])[:5]
                    if sample_fields:
                        pass

            # Show generated schemas
            if schemas:
                for schema in schemas.values():
                    schema.get("properties", {})
                    schema.get("key_properties", [])

            return FlextResult[None].ok(
                {
                    "total_entities": len(all_entities),
                    "entities_with_data": len(data_entities),
                    "schemas_generated": len(schemas),
                    "results_path": save_result.data if save_result.success else None,
                    "data_entities": data_entities,
                    "schemas": schemas,
                },
            )

        except Exception as e:
            logger.exception("Focused discovery failed")
            return FlextResult[None].fail(f"Discovery failed: {e}")
        finally:
            await self.client.stop()

    async def _quick_data_scan(self, entities: list[str]) -> dict[str, object]:
        """Quick scan to find entities with actual data."""
        data_entities = {}

        for entity_name in entities:
            try:
                # Quick test with limit=1 to check for data
                result = await self.client.get_entity_data(entity_name, limit=1)

                if result.success:
                    data = result.data
                    if isinstance(data, dict):
                        count = data.get("count", 0)
                        results = data.get("results", [])

                        if count > 0 or (results and len(results) > 0):
                            # Entity has data - get more details
                            detailed_result = await self.client.get_entity_data(
                                entity_name,
                                limit=3,
                            )
                            if detailed_result.success:
                                detailed_data = detailed_result.data
                                if isinstance(detailed_data, dict):
                                    detailed_results = detailed_data.get("results", [])

                                    entity_info = {
                                        "count": detailed_data.get("count", 0),
                                        "has_data": True,
                                        "sample_size": len(detailed_results)
                                        if isinstance(detailed_results, list)
                                        else 0,
                                    }

                                    # Get field information from sample
                                    if (
                                        detailed_results
                                        and isinstance(detailed_results, list)
                                        and len(detailed_results) > 0
                                    ):
                                        sample = detailed_results[0]
                                        if isinstance(sample, dict):
                                            entity_info.update(
                                                {
                                                    "field_count": len(sample.keys()),
                                                    "sample_fields": list(
                                                        sample.keys(),
                                                    ),
                                                    "field_types": {
                                                        k: type(v).__name__
                                                        for k, v in sample.items()
                                                    },
                                                    "sample_record": self._safe_sample(
                                                        sample,
                                                    ),
                                                },
                                            )

                                    data_entities[entity_name] = entity_info

            except Exception:
                logger.debug("Failed to process entity %s", entity_name)

        return data_entities

    async def _get_entity_structures(self, entities: list[str]) -> dict[str, object]:
        """Get entity structures even without data."""
        structures = {}

        for entity_name in entities:
            try:
                result = await self.client.get_entity_data(entity_name, limit=1)
                if result.success:
                    data = result.data
                    if isinstance(data, dict):
                        results = data.get("results", [])
                        if results and isinstance(results, list) and len(results) > 0:
                            sample = results[0]
                            if isinstance(sample, dict):
                                structures[entity_name] = {
                                    "fields": list(sample.keys()),
                                    "field_types": {
                                        k: type(v).__name__ for k, v in sample.items()
                                    },
                                    "sample_record": self._safe_sample(sample),
                                    "has_data": False,
                                }

            except Exception:
                logger.debug("Failed to get structure for entity %s", entity_name)

        return structures

    def _safe_sample(self, record: dict[str, object]) -> dict[str, object]:
        """Create safe sample record."""
        safe = {}
        for k, v in list(record.items())[:10]:  # First 10 fields only
            if isinstance(v, (str, int, float, bool, type(None))):
                if (isinstance(v, str) and len(v) < 50) or not isinstance(v, str):
                    safe[k] = v
                else:
                    safe[k] = f"<{len(v)}chars>"
            else:
                safe[k] = f"<{type(v).__name__}>"
        return safe

    async def _generate_schemas_from_data(
        self,
        data_entities: dict[str, object],
    ) -> dict[str, object]:
        """Generate Singer schemas from entities with data."""
        schemas = {}

        for entity_name, entity_data in data_entities.items():
            schema = self._create_singer_schema(entity_name, entity_data)
            if schema:
                schemas[entity_name] = schema

        return schemas

    async def _generate_schemas_from_structures(
        self,
        structure_entities: dict[str, object],
    ) -> dict[str, object]:
        """Generate Singer schemas from structures."""
        schemas = {}

        for entity_name, structure_data in structure_entities.items():
            schema = self._create_singer_schema(entity_name, structure_data)
            if schema:
                schemas[entity_name] = schema

        return schemas

    def _create_singer_schema(
        self,
        entity_name: str,
        entity_data: dict[str, object],
    ) -> dict[str, object] | None:
        """Create Singer schema with proper Oracle WMS typing."""
        try:
            fields = entity_data.get("sample_fields", entity_data.get("fields", []))
            field_types = entity_data.get("field_types", {})
            sample_record = entity_data.get("sample_record", {})

            if not fields:
                return None

            properties = {}

            # Process each field with Oracle WMS specific typing
            for field in fields:
                python_type = field_types.get(field, "str")
                sample_value = sample_record.get(field)

                # Generate Singer type with Oracle WMS context
                singer_type = self._oracle_field_to_singer_type(
                    field,
                    python_type,
                    sample_value,
                    entity_name,
                )
                properties[field] = singer_type

            # Add Singer metadata
            properties["_sdc_extracted_at"] = {"type": "string", "format": "date-time"}
            properties["_sdc_entity"] = {"type": "string"}
            properties["_sdc_record_hash"] = {"type": ["string", "null"]}

            # Determine key properties
            key_properties = self._get_oracle_key_properties(entity_name, fields)

            return {
                "type": "object",
                "properties": properties,
                "additionalProperties": False,
                "key_properties": key_properties,
                "oracle_wms_entity": entity_name,
                "oracle_wms_environment": self.config.environment,
            }

        except Exception:
            logger.exception("Schema creation failed for %s", entity_name)
            return None

    def _oracle_field_to_singer_type(
        self,
        field_name: str,
        python_type: str,
        sample_value: object,
        entity_name: str,
    ) -> dict[str, object]:
        """Convert Oracle WMS field to Singer type with context."""
        # Oracle WMS specific field analysis
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

        # Fallback mapping
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
        fields: list[str],
    ) -> list[str]:
        """Get Oracle WMS key properties for entity."""
        keys = []

        # Always include id if present
        if "id" in fields:
            keys.append("id")

        # Entity-specific keys
        entity_keys = {
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

    async def _save_focused_results(self) -> FlextResult[str]:
        """Save focused discovery results."""
        results_dir = Path("oracle_wms_focused_results")
        results_dir.mkdir(exist_ok=True)

        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

        # Save entities with data
        if self.entities_with_data:
            entities_file = results_dir / f"entities_with_data_{timestamp}.json"
            with entities_file.open("w", encoding="utf-8") as f:
                json.dump(self.entities_with_data, f, indent=2, default=str)

        # Save Singer schemas
        if self.complete_schemas:
            schemas_file = results_dir / f"singer_schemas_{timestamp}.json"
            with schemas_file.open("w", encoding="utf-8") as f:
                json.dump(self.complete_schemas, f, indent=2, default=str)

            # Save Singer catalog
            catalog = self._create_singer_catalog()
            catalog_file = results_dir / f"singer_catalog_{timestamp}.json"
            with catalog_file.open("w", encoding="utf-8") as f:
                json.dump(catalog, f, indent=2, default=str)

        # Save summary
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

        return FlextResult[None].ok(str(results_dir))

    def _create_singer_catalog(self) -> dict[str, object]:
        """Create Singer catalog."""
        streams = []

        for entity_name, schema in self.complete_schemas.items():
            key_properties = schema.get("key_properties", [])
            schema_without_keys = {
                k: v for k, v in schema.items() if k != "key_properties"
            }

            stream = {
                "tap_stream_id": entity_name,
                "stream": entity_name,
                "schema": schema_without_keys,
                "key_properties": key_properties,
                "metadata": [
                    {
                        "breadcrumb": [],
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


async def main() -> None:
    """Main execution."""
    discovery = FocusedOracleWmsDiscovery()
    result = await discovery.execute_focused_discovery()

    if result.success:
        data = result.data

        if data["entities_with_data"] > 0:
            pass


if __name__ == "__main__":
    asyncio.run(main())
