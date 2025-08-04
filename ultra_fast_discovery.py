#!/usr/bin/env python3
"""Ultra-Fast Oracle WMS Discovery - FOCUS ON RESULTS.

STRATEGY:
1. Test only TOP 20 most important WMS entities
2. Find those with REAL DATA quickly
3. Generate Singer schemas only for entities with data
4. Create complete Singer catalog for Meltano
5. Complete in under 30 seconds

ZERO WASTE - MAXIMUM EFFICIENCY
"""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from flext_core import FlextResult, get_logger

from flext_oracle_wms import FlextOracleWmsClientConfig, create_oracle_wms_client
from flext_oracle_wms.api_catalog import FlextOracleWmsApiVersion

logger = get_logger(__name__)


class UltraFastDiscovery:
    """Ultra-fast Oracle WMS discovery - focus on results."""

    def __init__(self) -> None:
        """Initialize with ADMINISTRATOR credentials."""
        self.config = FlextOracleWmsClientConfig(
            base_url="https://ta29.wms.ocs.oraclecloud.com",
            username="USER_WMS_INTEGRA",  # ADMINISTRATOR
            password="jmCyS7BK94YvhS@",
            environment="raizen_test",
            timeout=10.0,  # FAST
            max_retries=1,  # MINIMAL RETRIES
            api_version=FlextOracleWmsApiVersion.LGF_V10,
            verify_ssl=True,
            enable_logging=True,
        )
        self.client = create_oracle_wms_client(self.config, mock_mode=False)

        # TOP 20 most critical WMS entities
        self.critical_entities = [
            "company",
            "facility",
            "item",
            "location",
            "inventory",
            "order_hdr",
            "order_dtl",
            "allocation",
            "container",
            "lpn",
            "pick_hdr",
            "pick_dtl",
            "task",
            "shipment",
            "receipt",
            "carrier",
            "zone",
            "area",
            "user_def",
            "manifest",
        ]

        self.entities_with_data = {}
        self.singer_schemas = {}

    async def ultra_fast_run(self) -> FlextResult[dict[str, Any]]:
        """Ultra-fast discovery execution."""
        start_time = datetime.now(UTC)

        try:
            await self.client.start()

            # Test critical entities for data

            data_entities = await self._scan_for_data()

            if data_entities:
                # Generate Singer schemas only for entities with data
                schemas = await self._generate_singer_schemas(data_entities)

                # Create Singer catalog
                catalog = self._create_singer_catalog(schemas)

                # Save results
                results_path = await self._save_results(data_entities, schemas, catalog)

            else:
                # Still generate schemas from structures
                structure_schemas = await self._generate_structure_schemas()
                catalog = self._create_singer_catalog(structure_schemas)
                results_path = await self._save_results({}, structure_schemas, catalog)

            end_time = datetime.now(UTC)
            duration = (end_time - start_time).total_seconds()

            # Final results

            if self.entities_with_data:
                for data in self.entities_with_data.values():
                    data.get("count", 0)
                    data.get("field_count", 0)

            return FlextResult.ok(
                {
                    "duration_seconds": duration,
                    "entities_with_data": len(self.entities_with_data),
                    "schemas_generated": len(self.singer_schemas),
                    "results_path": results_path.data if results_path.success else None,
                },
            )

        except Exception as e:
            logger.exception("Ultra-fast discovery failed")
            return FlextResult.fail(f"Discovery failed: {e}")
        finally:
            await self.client.stop()

    async def _scan_for_data(self) -> dict[str, Any]:
        """Scan entities for real data quickly."""
        data_entities = {}

        # Test entities in parallel batches of 5
        for i in range(0, len(self.critical_entities), 5):
            batch = self.critical_entities[i : i + 5]

            tasks = [self._test_entity_data(entity) for entity in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for entity, result in zip(batch, results, strict=False):
                if isinstance(result, dict) and result.get("has_data", False):
                    data_entities[entity] = result
                elif isinstance(result, Exception):
                    pass

        return data_entities

    async def _test_entity_data(self, entity_name: str) -> dict[str, Any]:
        """Test single entity for data."""
        try:
            result = await self.client.get_entity_data(entity_name, limit=1)

            if result.success:
                data = result.data
                if isinstance(data, dict):
                    count = data.get("count", 0)
                    results = data.get("results", [])

                    if count > 0 or (results and len(results) > 0):
                        # Get more details for entities with data
                        detail_result = await self.client.get_entity_data(
                            entity_name,
                            limit=2,
                        )
                        if detail_result.success:
                            detail_data = detail_result.data
                            if isinstance(detail_data, dict):
                                detail_results = detail_data.get("results", [])

                                if detail_results and len(detail_results) > 0:
                                    sample = detail_results[0]
                                    if isinstance(sample, dict):
                                        return {
                                            "has_data": True,
                                            "count": detail_data.get("count", 0),
                                            "field_count": len(sample.keys()),
                                            "fields": list(sample.keys()),
                                            "field_types": {
                                                k: type(v).__name__
                                                for k, v in sample.items()
                                            },
                                            "sample": dict(
                                                list(sample.items())[:5],
                                            ),  # First 5 fields
                                        }

                    return {"has_data": False, "count": count}
                return {
                    "has_data": False,
                    "error": f"Invalid response: {type(data)}",
                }
            return {"has_data": False, "error": str(result.error)}

        except Exception as e:
            return {"has_data": False, "error": f"Exception: {e}"}

    async def _generate_singer_schemas(
        self,
        data_entities: dict[str, Any],
    ) -> dict[str, Any]:
        """Generate Singer schemas for entities with data."""
        schemas = {}

        for entity_name, entity_data in data_entities.items():
            schema = self._create_singer_schema(entity_name, entity_data)
            if schema:
                schemas[entity_name] = schema

        self.singer_schemas = schemas
        return schemas

    async def _generate_structure_schemas(self) -> dict[str, Any]:
        """Generate schemas from structures when no data available."""
        schemas = {}

        # Test first 5 entities for structure
        for entity_name in self.critical_entities[:5]:
            try:
                result = await self.client.get_entity_data(entity_name, limit=1)
                if result.success:
                    data = result.data
                    if isinstance(data, dict):
                        results = data.get("results", [])
                        if results and len(results) > 0:
                            sample = results[0]
                            if isinstance(sample, dict):
                                schema = self._create_singer_schema_from_structure(
                                    entity_name,
                                    sample,
                                )
                                if schema:
                                    schemas[entity_name] = schema
            except Exception:
                pass

        self.singer_schemas = schemas
        return schemas

    def _create_singer_schema(
        self,
        entity_name: str,
        entity_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Create Singer schema from entity data."""
        fields = entity_data.get("fields", [])
        field_types = entity_data.get("field_types", {})

        if not fields:
            return None

        properties = {}

        # Convert each field to Singer type
        for field in fields:
            python_type = field_types.get(field, "str")
            properties[field] = self._python_to_singer_type(python_type)

        # Add Singer metadata
        properties.update(
            {
                "_sdc_extracted_at": {"type": "string", "format": "date-time"},
                "_sdc_entity": {"type": "string"},
                "_sdc_sequence": {"type": "integer"},
            },
        )

        # Determine key properties
        key_properties = self._get_key_properties(entity_name, fields)

        return {
            "type": "object",
            "properties": properties,
            "additionalProperties": False,
            "key_properties": key_properties,
        }

    def _create_singer_schema_from_structure(
        self,
        entity_name: str,
        sample: dict[str, Any],
    ) -> dict[str, Any]:
        """Create Singer schema from sample structure."""
        properties = {}

        for field, value in sample.items():
            if isinstance(value, bool):
                properties[field] = {"type": ["boolean", "null"]}
            elif isinstance(value, int):
                properties[field] = {"type": ["integer", "null"]}
            elif isinstance(value, float):
                properties[field] = {"type": ["number", "null"]}
            elif isinstance(value, str):
                properties[field] = {"type": ["string", "null"]}
            elif isinstance(value, dict):
                properties[field] = {"type": ["object", "null"]}
            elif isinstance(value, list):
                properties[field] = {"type": ["array", "null"]}
            else:
                properties[field] = {"type": ["string", "null"]}

        # Add Singer metadata
        properties.update(
            {
                "_sdc_extracted_at": {"type": "string", "format": "date-time"},
                "_sdc_entity": {"type": "string"},
                "_sdc_sequence": {"type": "integer"},
            },
        )

        key_properties = self._get_key_properties(entity_name, list(sample.keys()))

        return {
            "type": "object",
            "properties": properties,
            "additionalProperties": False,
            "key_properties": key_properties,
        }

    def _python_to_singer_type(self, python_type: str) -> dict[str, Any]:
        """Convert Python type to Singer type."""
        type_mapping = {
            "int": {"type": ["integer", "null"]},
            "float": {"type": ["number", "null"]},
            "str": {"type": ["string", "null"]},
            "bool": {"type": ["boolean", "null"]},
            "dict": {"type": ["object", "null"]},
            "list": {"type": ["array", "null"]},
            "NoneType": {"type": "null"},
        }
        return type_mapping.get(python_type, {"type": ["string", "null"]})

    def _get_key_properties(self, entity_name: str, fields: list[str]) -> list[str]:
        """Get key properties for entity."""
        # Always include id if present
        if "id" in fields:
            return ["id"]

        # Entity-specific keys
        entity_keys = {
            "company": ["code", "company_code"],
            "facility": ["code", "facility_code"],
            "item": ["code", "item_code"],
            "location": ["code", "location_code"],
            "order_hdr": ["order_nbr"],
            "order_dtl": ["order_nbr", "line_nbr"],
            "allocation": ["id"],
            "container": ["container_nbr"],
            "lpn": ["lpn_nbr"],
        }

        keys = entity_keys.get(entity_name, [])
        return [key for key in keys if key in fields][:2]  # Max 2 keys

    def _create_singer_catalog(self, schemas: dict[str, Any]) -> dict[str, Any]:
        """Create complete Singer catalog."""
        streams = []

        for entity_name, schema in schemas.items():
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
                            "forced-replication-method": "FULL_TABLE",
                        },
                    },
                ],
            }
            streams.append(stream)

        return {"version": 1, "streams": streams}

    async def _save_results(
        self,
        data_entities: dict[str, Any],
        schemas: dict[str, Any],
        catalog: dict[str, Any],
    ) -> FlextResult[str]:
        """Save results quickly."""
        results_dir = Path("ultra_fast_results")
        results_dir.mkdir(exist_ok=True)

        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

        # Save entities with data
        if data_entities:
            entities_file = results_dir / f"data_entities_{timestamp}.json"
            with entities_file.open("w", encoding="utf-8") as f:
                json.dump(data_entities, f, indent=2, default=str)

        # Save Singer schemas
        if schemas:
            schemas_file = results_dir / f"singer_schemas_{timestamp}.json"
            with schemas_file.open("w", encoding="utf-8") as f:
                json.dump(schemas, f, indent=2, default=str)

        # Save Singer catalog
        catalog_file = results_dir / f"singer_catalog_{timestamp}.json"
        with catalog_file.open("w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2, default=str)

        # Save summary
        summary = {
            "discovery_mode": "ULTRA_FAST",
            "timestamp": timestamp,
            "duration_target": "30_seconds",
            "entities_tested": len(self.critical_entities),
            "entities_with_data": len(data_entities),
            "schemas_generated": len(schemas),
            "catalog_streams": len(catalog.get("streams", [])),
            "oracle_environment": self.config.environment,
        }

        summary_file = results_dir / f"summary_{timestamp}.json"
        with summary_file.open("w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, default=str)

        return FlextResult.ok(str(results_dir))


async def main() -> None:
    """Main execution."""
    discovery = UltraFastDiscovery()
    result = await discovery.ultra_fast_run()

    if result.success:
        pass


if __name__ == "__main__":
    asyncio.run(main())
