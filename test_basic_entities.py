#!/usr/bin/env python3
"""Test Oracle WMS with Basic Entities.

Test with fundamental WMS entities that should have data.
"""

import asyncio
import operator

from flext_core import get_logger

from flext_oracle_wms import FlextOracleWmsClientConfig, create_oracle_wms_client
from flext_oracle_wms.api_catalog import FlextOracleWmsApiVersion

logger = get_logger(__name__)


async def test_basic_entities() -> None:
    """Test basic WMS entities that should contain data."""
    config = FlextOracleWmsClientConfig(
        base_url="https://ta29.wms.ocs.oraclecloud.com",
        username="USER_WMS_INTEGRA",
        password="jmCyS7BK94YvhS@",
        environment="raizen_test",
        timeout=60.0,
        max_retries=3,
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        verify_ssl=True,
        enable_logging=True,
    )

    real_client = create_oracle_wms_client(config, mock_mode=False)

    # Basic entities that should exist in any WMS
    basic_entities = [
        "company",
        "facility",
        "item",
        "location",
        "inventory",
        "user_def",
        "container",
        "carrier",
        "warehouse",
        "zone",
    ]

    try:
        await real_client.start()

        # Get all entities and find basic ones
        entities_result = await real_client.discover_entities()
        if entities_result.success:
            all_entities = entities_result.data
            available_basic = [e for e in basic_entities if e in all_entities]
        else:
            available_basic = basic_entities

        successful_extractions = []

        for entity_name in available_basic:
            try:
                # Test simple extraction without field filters
                data_result = await real_client.get_entity_data(entity_name, limit=2)

                if data_result.success:
                    data = data_result.data
                    if isinstance(data, dict):
                        count = data.get("count", 0)
                        results = data.get("results", [])

                        if results and len(results) > 0:
                            sample = results[0]
                            if isinstance(sample, dict):
                                fields = list(sample.keys())

                                # Show sample data (non-sensitive fields only)
                                safe_sample = {}
                                for k, v in list(sample.items())[:5]:
                                    if (
                                        isinstance(v, (str, int, float, bool))
                                        and len(str(v)) < 100
                                    ):
                                        safe_sample[k] = v
                                    else:
                                        safe_sample[k] = f"<{type(v).__name__}>"

                                successful_extractions.append(
                                    {
                                        "entity": entity_name,
                                        "count": count,
                                        "fields": fields,
                                        "sample": safe_sample,
                                    },
                                )

            except Exception:
                pass

        await real_client.stop()

        # Results Summary

        if successful_extractions:
            sum(ext["count"] for ext in successful_extractions)

            # Show successful entities
            for ext in successful_extractions:
                ext["entity"]
                count = ext["count"]
                len(ext["fields"])

            # Test a more complex query with a working entity
            if successful_extractions:
                best_entity = max(
                    successful_extractions,
                    key=operator.itemgetter("count"),
                )
                entity_name = best_entity["entity"]

                try:
                    # Test with larger limit
                    advanced_result = await real_client.start()
                    if advanced_result.success:
                        big_data_result = await real_client.get_entity_data(
                            entity_name,
                            limit=10,
                            offset=0,
                        )

                        if big_data_result.success:
                            big_data = big_data_result.data
                            if isinstance(big_data, dict):
                                big_data.get("count", 0)

                                # Check pagination info
                                page_info = {}
                                for key in [
                                    "page_number",
                                    "page_count",
                                    "next_page",
                                    "previous_page",
                                ]:
                                    if key in big_data:
                                        page_info[key] = big_data[key]

                                if page_info:
                                    pass

                        await real_client.stop()
                except Exception:
                    pass

        # Final honest assessment
        if successful_extractions:
            [ext["entity"] for ext in successful_extractions]

    except Exception:
        logger.exception("Basic entity test failed")


if __name__ == "__main__":
    asyncio.run(test_basic_entities())
