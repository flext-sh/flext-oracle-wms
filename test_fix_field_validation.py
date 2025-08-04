#!/usr/bin/env python3
"""Fix Oracle WMS Field Validation Issue.

The test showed that 'create_ts' and 'mod_ts' are invalid fields.
Let's discover the correct field names from the real Oracle WMS API.
"""

import asyncio

from flext_core import get_logger

from flext_oracle_wms import FlextOracleWmsClientConfig, create_oracle_wms_client
from flext_oracle_wms.api_catalog import FlextOracleWmsApiVersion

logger = get_logger(__name__)


async def discover_real_fields() -> None:
    """Discover real field names from Oracle WMS API."""
    # Create REAL configuration
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

    try:
        await real_client.start()

        # Get entities
        entities_result = await real_client.discover_entities()
        if not entities_result.success:
            return

        entities = entities_result.data[:10]  # Test first 10 entities

        successful_extractions = []

        for entity_name in entities:
            # Try without field specification first
            try:
                data_result = await real_client.get_entity_data(
                    entity_name,
                    limit=1,  # Just 1 record to see structure
                )

                if data_result.success:
                    data = data_result.data
                    if isinstance(data, dict):
                        count = data.get("count", 0)
                        results = data.get("results", [])

                        if count > 0 and results:
                            sample_record = results[0]
                            if isinstance(sample_record, dict):
                                fields = list(sample_record.keys())

                                # Look for timestamp-like fields
                                timestamp_fields = [
                                    f
                                    for f in fields
                                    if any(
                                        t in f.lower()
                                        for t in [
                                            "ts",
                                            "time",
                                            "date",
                                            "created",
                                            "modified",
                                            "updated",
                                        ]
                                    )
                                ]
                                if timestamp_fields:
                                    pass

                                successful_extractions.append(
                                    {
                                        "entity": entity_name,
                                        "fields": fields,
                                        "timestamp_fields": timestamp_fields,
                                        "sample_data": dict(
                                            list(sample_record.items())[:3],
                                        ),
                                    },
                                )
                else:
                    error_msg = str(data_result.error)
                    if (
                        ("400" in error_msg and "VALIDATION_ERROR" in error_msg)
                        or "404" in error_msg
                        or "403" in error_msg
                        or "401" in error_msg
                    ):
                        pass

            except Exception:
                pass

        await real_client.stop()

        # Summary

        if successful_extractions:
            # Find common timestamp field patterns
            all_timestamp_fields = []
            for extraction in successful_extractions:
                all_timestamp_fields.extend(extraction["timestamp_fields"])

            unique_timestamp_patterns = set(all_timestamp_fields)
            for pattern in sorted(unique_timestamp_patterns):
                count = sum(
                    1
                    for ext in successful_extractions
                    if pattern in ext["timestamp_fields"]
                )

            # Show successful entities with their structures
            for extraction in successful_extractions[:5]:  # Show first 5
                extraction["entity"]
                len(extraction["fields"])
                extraction["timestamp_fields"]
                extraction["sample_data"]

        # Recommendation
        if successful_extractions:
            # Get the most common timestamp fields
            common_ts_fields = []
            for ext in successful_extractions:
                common_ts_fields.extend(ext["timestamp_fields"])

            if common_ts_fields:
                from collections import Counter

                Counter(common_ts_fields).most_common(3)

            successful_extractions[0]["entity"]

    except Exception:
        logger.exception("Field discovery failed")


if __name__ == "__main__":
    asyncio.run(discover_real_fields())
