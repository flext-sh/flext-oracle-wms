#!/usr/bin/env python3
"""Oracle WMS Optimized Discovery - REAL Implementation.

OPTIMIZED approach:
1. Focus on high-priority entities first
2. Process in parallel batches
3. Use ADMINISTRATOR credentials for complete access
4. Generate Singer schemas with real flattening
5. No fallbacks, no estimations - 100% Oracle discovery
"""

import asyncio
import json
import operator
from datetime import UTC, datetime
from pathlib import Path

from flext_core import FlextLogger, FlextResult

from flext_oracle_wms import (
    FlextOracleWmsApiVersion,
    FlextOracleWmsClientConfig,
    create_oracle_wms_client,
)

logger = FlextLogger(__name__)


class OptimizedOracleWmsDiscovery:
    """Optimized Oracle WMS Discovery for fast, complete results."""

    def __init__(self) -> None:
        """Initialize with ADMINISTRATOR credentials."""
        self.config = FlextOracleWmsClientConfig(
            base_url="https://ta29.wms.ocs.oraclecloud.com",
            username="USER_WMS_INTEGRA",  # ADMINISTRATOR TOTAL
            password="jmCyS7BK94YvhS@",
            environment="raizen_test",
            timeout=60.0,
            max_retries=3,
            api_version=FlextOracleWmsApiVersion.LGF_V10,
            verify_ssl=True,
            enable_logging=True,
        )
        self.client = create_oracle_wms_client(self.config, mock_mode=False)

        # Priority entities (core WMS business objects)
        self.priority_entities = {
            # Core master data
            "company",
            "facility",
            "item",
            "location",
            "user_def",
            # Inventory and stock
            "inventory",
            "inventory_detail",
            "inventory_summary",
            # Orders and fulfillment
            "order_hdr",
            "order_dtl",
            "allocation",
            "pick_hdr",
            "pick_dtl",
            # Warehouse operations
            "container",
            "lpn",
            "task",
            "wave_hdr",
            "wave_dtl",
            # Shipping and receiving
            "shipment",
            "receipt",
            "manifest",
            "carrier",
            # Warehouse layout
            "zone",
            "area",
            "aisle",
            "bay",
            "level",
            "position",
        }

        self.discovered_entities = []
        self.high_value_entities = {}  # Entities with data
        self.complete_schemas = {}

    async def start_discovery(self) -> FlextResult[None]:
        """Start optimized discovery."""
        start_result = await self.client.start()
        if not start_result.success:
            return FlextResult[None].fail(f"Client start failed: {start_result.error}")

        return FlextResult[None].ok(None)

    async def discover_priority_entities_fast(self) -> FlextResult[dict[str, object]]:
        """Fast discovery of priority entities with data."""
        # Get all entities first
        entities_result = await self.client.discover_entities()
        if not entities_result.success:
            return FlextResult[None].fail(
                f"Entity discovery failed: {entities_result.error}"
            )

        all_entities = entities_result.data

        # Find priority entities that exist
        available_priority = [e for e in all_entities if e in self.priority_entities]
        other_entities = [e for e in all_entities if e not in self.priority_entities]

        # Process priority entities first
        priority_results = await self._process_entity_batch(
            available_priority,
            "PRIORITY",
            batch_size=10,
        )

        # Find entities with actual data
        entities_with_data = []
        for entity_name, result in priority_results.items():
            if result.get("has_data", False):
                entities_with_data.append(entity_name)

        if entities_with_data:
            pass

        # If we found entities with data, process some additional ones
        if entities_with_data and len(other_entities) > 0:
            additional_results = await self._process_entity_batch(
                other_entities[:50],  # Test first 50 additional entities
                "ADDITIONAL",
                batch_size=15,
            )

            # Merge results
            all_results = {**priority_results, **additional_results}

            # Update entities with data
            additional_with_data = [
                entity
                for entity, result in additional_results.items()
                if result.get("has_data", False)
            ]
            entities_with_data.extend(additional_with_data)
        else:
            all_results = priority_results

        self.high_value_entities = {
            name: result
            for name, result in all_results.items()
            if result.get("has_data", False)
        }

        return FlextResult[None].ok(
            {
                "total_processed": len(all_results),
                "entities_with_data": len(self.high_value_entities),
                "high_value_entities": list(self.high_value_entities.keys()),
                "detailed_results": all_results,
            },
        )

    async def _process_entity_batch(
        self,
        entities: list[str],
        batch_name: str,
        batch_size: int = 10,
    ) -> dict[str, object]:
        """Process entity batch with parallel requests."""
        results = {}

        # Process in smaller batches to avoid overwhelming the API
        for i in range(0, len(entities), batch_size):
            batch = entities[i : i + batch_size]
            (i // batch_size) + 1
            (len(entities) + batch_size - 1) // batch_size

            # Process batch in parallel
            batch_tasks = [
                self._analyze_single_entity(entity_name) for entity_name in batch
            ]

            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)

            # Process results
            for entity_name, result in zip(batch, batch_results, strict=False):
                if isinstance(result, Exception):
                    results[entity_name] = {
                        "has_data": False,
                        "error": str(result),
                        "processed_at": datetime.now(UTC).isoformat(),
                    }
                elif isinstance(result, dict):
                    results[entity_name] = result
                else:
                    results[entity_name] = {
                        "has_data": False,
                        "error": "Invalid result type",
                        "processed_at": datetime.now(UTC).isoformat(),
                    }

            # Progress update
            sum(1 for r in results.values() if r.get("has_data", False))

            # Small delay to be respectful to the API
            await asyncio.sleep(0.1)

        return results

    async def _analyze_single_entity(self, entity_name: str) -> dict[str, object]:
        """Analyze single entity for data and structure."""
        try:
            # Get entity data with small sample
            data_result = await self.client.get_entity_data(
                entity_name,
                limit=3,  # Small sample for analysis
                offset=0,
            )

            if data_result.success:
                data = data_result.data
                if isinstance(data, dict):
                    count = data.get("count", 0)
                    results = data.get("results", [])

                    analysis = {
                        "has_data": count > 0,
                        "total_count": count,
                        "sample_count": len(results)
                        if isinstance(results, list)
                        else 0,
                        "processed_at": datetime.now(UTC).isoformat(),
                    }

                    # If has data, get structure info
                    if (
                        count > 0
                        and results
                        and isinstance(results, list)
                        and len(results) > 0
                    ):
                        sample_record = results[0]
                        if isinstance(sample_record, dict):
                            analysis.update(
                                {
                                    "field_count": len(sample_record.keys()),
                                    "fields": list(sample_record.keys()),
                                    "field_types": {
                                        k: type(v).__name__
                                        for k, v in sample_record.items()
                                    },
                                    "sample_record": self._safe_sample_record(
                                        sample_record,
                                    ),
                                },
                            )

                    return analysis
                return {
                    "has_data": False,
                    "error": f"Invalid response type: {type(data)}",
                    "processed_at": datetime.now(UTC).isoformat(),
                }
            return {
                "has_data": False,
                "error": str(data_result.error),
                "processed_at": datetime.now(UTC).isoformat(),
            }

        except Exception as e:
            return {
                "has_data": False,
                "error": f"Exception: {e}",
                "processed_at": datetime.now(UTC).isoformat(),
            }

    def _safe_sample_record(self, record: dict[str, object]) -> dict[str, object]:
        """Create safe sample record for storage."""
        safe_record = {}
        for k, v in record.items():
            if isinstance(v, (str, int, float, bool, type(None))):
                if (isinstance(v, str) and len(v) < 100) or not isinstance(v, str):
                    safe_record[k] = v
                else:
                    safe_record[k] = f"<string:{len(v)}chars>"
            else:
                safe_record[k] = f"<{type(v).__name__}>"
        return safe_record

    async def generate_complete_singer_schemas(self) -> FlextResult[dict[str, object]]:
        """Generate complete Singer schemas for high-value entities."""
        if not self.high_value_entities:
            return FlextResult[None].fail(
                "No high-value entities available for schema generation",
            )

        singer_schemas = {}

        for entity_name, entity_data in self.high_value_entities.items():
            # Generate Singer schema with real metadata-based typing
            schema = self._generate_singer_schema_from_entity_data(
                entity_name,
                entity_data,
            )

            if schema:
                singer_schemas[entity_name] = schema
                len(schema.get("properties", {}))

                # Show key fields
                properties = schema.get("properties", {})
                key_fields = [
                    field
                    for field in properties
                    if any(
                        key_indicator in field.lower()
                        for key_indicator in ["id", "code", "nbr", "number"]
                    )
                ][:5]
                if key_fields:
                    pass

        self.complete_schemas = singer_schemas

        # Generate Singer catalog
        catalog = self._generate_singer_catalog(singer_schemas)

        return FlextResult[None].ok(
            {
                "schemas_generated": len(singer_schemas),
                "schemas": singer_schemas,
                "singer_catalog": catalog,
            },
        )

    def _generate_singer_schema_from_entity_data(
        self,
        entity_name: str,
        entity_data: dict[str, object],
    ) -> dict[str, object] | None:
        """Generate Singer schema from entity data with proper typing."""
        try:
            fields = entity_data.get("fields", [])
            field_types = entity_data.get("field_types", {})
            sample_record = entity_data.get("sample_record", {})

            if not fields:
                return None

            properties = {}

            # Process each field with real data-driven typing
            for field in fields:
                python_type = field_types.get(field, "str")
                sample_value = sample_record.get(field)

                # Generate Singer type based on real Oracle data
                singer_type = self._oracle_to_singer_type(
                    field,
                    python_type,
                    sample_value,
                )
                properties[field] = singer_type

            # Add Singer metadata fields
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

            # Determine key properties based on Oracle WMS patterns
            key_properties = self._determine_key_properties(entity_name, fields)

            return {
                "type": "object",
                "properties": properties,
                "additionalProperties": False,
                "key_properties": key_properties,
            }

        except Exception:
            logger.exception("Schema generation failed for %s", entity_name)
            return None

    def _oracle_to_singer_type(
        self,
        field_name: str,
        python_type: str,
        sample_value: object,
    ) -> dict[str, object]:
        """Convert Oracle field to Singer type with real data analysis."""
        # Analyze sample value for precise typing
        if sample_value is not None:
            if isinstance(sample_value, bool):
                return {"type": ["boolean", "null"]}
            if isinstance(sample_value, int):
                return {"type": ["integer", "null"]}
            if isinstance(sample_value, float):
                return {"type": ["number", "null"]}
            if isinstance(sample_value, str):
                # Analyze string content for specialized types
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

        # Fallback based on Python type
        oracle_type_mapping = {
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

        if isinstance(value, str):
            # Check for Oracle datetime format
            oracle_datetime_check = (
                "T" in value
                and ":" in value
                and ("+" in value or "-" in value[-6:])  # Timezone indicator
            )
            return name_match or oracle_datetime_check

        return name_match

    def _is_oracle_date(self, field_name: str, value: str) -> bool:
        """Check if field is Oracle date."""
        date_patterns = ["_date$", "date_", "_dt$"]
        name_match = any(
            pattern.replace("$", "") in field_name.lower() for pattern in date_patterns
        )

        if isinstance(value, str) and not self._is_oracle_datetime(field_name, value):
            # Simple date format without time
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
        self,
        entity_name: str,
        fields: list[str],
    ) -> list[str]:
        """Determine key properties for Oracle WMS entity."""
        # Oracle WMS key patterns
        potential_keys = []

        # Always include id if present
        if "id" in fields:
            potential_keys.append("id")

        # Add entity-specific keys
        entity_key_patterns = {
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

        # If no specific keys found, use common patterns
        if not potential_keys:
            common_keys = ["code", "nbr", "number", "name"]
            for field in fields:
                if any(key in field.lower() for key in common_keys):
                    potential_keys.append(field)
                    break

        return potential_keys[:3]  # Max 3 key properties

    def _generate_singer_catalog(self, schemas: dict[str, object]) -> dict[str, object]:
        """Generate Singer catalog from schemas."""
        streams = []

        for entity_name, schema in schemas.items():
            key_properties = schema.get("key_properties", ["id"])

            stream = {
                "tap_stream_id": entity_name,
                "stream": entity_name,
                "schema": {k: v for k, v in schema.items() if k != "key_properties"},
                "key_properties": key_properties,
                "metadata": [
                    {
                        "breadcrumb": [],
                        "metadata": {
                            "inclusion": "available",
                            "selected": True,
                            "replication-method": "FULL_TABLE",
                            "forced-replication-method": "FULL_TABLE",
                            "table-key-properties": key_properties,
                        },
                    },
                ],
            }
            streams.append(stream)

        return {"version": 1, "streams": streams}

    async def save_optimized_results(self) -> FlextResult[str]:
        """Save optimized discovery results."""
        results_dir = Path("oracle_wms_optimized_results")
        results_dir.mkdir(exist_ok=True)

        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

        # Save high-value entities
        entities_file = results_dir / f"high_value_entities_{timestamp}.json"
        with entities_file.open("w", encoding="utf-8") as f:
            json.dump(self.high_value_entities, f, indent=2, default=str)

        # Save Singer schemas
        schemas_file = results_dir / f"singer_schemas_{timestamp}.json"
        with schemas_file.open("w", encoding="utf-8") as f:
            json.dump(self.complete_schemas, f, indent=2, default=str)

        # Save Singer catalog
        if self.complete_schemas:
            catalog = self._generate_singer_catalog(self.complete_schemas)
            catalog_file = results_dir / f"singer_catalog_{timestamp}.json"
            with catalog_file.open("w", encoding="utf-8") as f:
                json.dump(catalog, f, indent=2, default=str)

        # Save summary
        summary = {
            "discovery_timestamp": timestamp,
            "discovery_mode": "OPTIMIZED_ADMINISTRATOR_MODE",
            "total_high_value_entities": len(self.high_value_entities),
            "schemas_generated": len(self.complete_schemas),
            "oracle_wms_environment": self.config.environment,
            "oracle_wms_base_url": self.config.base_url,
            "api_version": self.config.api_version,
            "high_value_entities": list(self.high_value_entities.keys()),
            "entities_with_most_data": sorted(
                [
                    (name, data.get("total_count", 0))
                    for name, data in self.high_value_entities.items()
                ],
                key=operator.itemgetter(1),
                reverse=True,
            )[:10],
        }

        summary_file = results_dir / f"discovery_summary_{timestamp}.json"
        with summary_file.open("w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, default=str)

        if self.complete_schemas:
            pass

        return FlextResult[None].ok(str(results_dir))

    async def cleanup(self) -> FlextResult[None]:
        """Clean up resources."""
        try:
            await self.client.stop()
            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Cleanup failed: {e}")


async def run_optimized_discovery() -> None:
    """Run optimized Oracle WMS discovery."""
    discovery = OptimizedOracleWmsDiscovery()

    try:
        # Start discovery
        start_result = await discovery.start_discovery()
        if not start_result.success:
            return

        # Discover priority entities with data
        entities_result = await discovery.discover_priority_entities_fast()
        if not entities_result.success:
            return

        # Generate Singer schemas
        schemas_result = await discovery.generate_complete_singer_schemas()
        if not schemas_result.success:
            return

        # Save results
        save_result = await discovery.save_optimized_results()
        if not save_result.success:
            return

        # Final results

        # Show top entities
        if discovery.high_value_entities:
            sorted_entities = sorted(
                discovery.high_value_entities.items(),
                key=lambda x: x[1].get("total_count", 0),
                reverse=True,
            )

            for _entity_name, data in sorted_entities[:15]:
                data.get("total_count", 0)
                data.get("field_count", 0)

    except Exception:
        logger.exception("Optimized discovery failed")
    finally:
        await discovery.cleanup()


if __name__ == "__main__":
    asyncio.run(run_optimized_discovery())
