"""Real functional tests for Oracle WMS helpers module."""


import pytest

from flext_oracle_wms.exceptions import (
    FlextOracleWmsError,
)
from flext_oracle_wms.helpers import (
    flext_oracle_wms_build_entity_url,
    flext_oracle_wms_chunk_records,
    flext_oracle_wms_extract_environment_from_url,
    flext_oracle_wms_extract_pagination_info,
    flext_oracle_wms_format_timestamp,
    flext_oracle_wms_normalize_url,
    flext_oracle_wms_validate_api_response,
    flext_oracle_wms_validate_entity_name,
    handle_operation_exception,
    validate_dict_parameter,
    validate_records_list,
    validate_string_parameter,
)


class TestRealScenarios:
    """Test real-world scenarios with Oracle WMS helpers."""

    def test_real_oracle_wms_urls(self) -> None:
        """Test with real Oracle WMS URL patterns."""
        real_scenarios = [
            {
                "base": "https://company.oraclecloud.com",
                "env": "production",
                "entity": "order_hdr",
                "expected": "https://company.oraclecloud.com/production/wms/lgfapi/v10/entity/order_hdr/"
            },
            {
                "base": "https://dev-wms.company.com",
                "env": "dev",
                "entity": "item_master",
                "expected": "https://dev-wms.company.com/dev/wms/lgfapi/v10/entity/item_master/"
            },
            {
                "base": "https://internal.invalid/REDACTED",
                "env": "test",
                "entity": "inventory_balance",
                "expected": "https://internal.invalid/REDACTED"
            }
        ]

        for scenario in real_scenarios:
            result = flext_oracle_wms_build_entity_url(
                scenario["base"],
                scenario["env"],
                scenario["entity"]
            )
            assert result == scenario["expected"]

    def test_real_environment_extraction(self) -> None:
        """Test environment extraction from real Oracle WMS URLs."""
        real_urls = [
            ("https://company.oraclecloud.com/production/wms/lgfapi/v10", "production"),
            ("https://dev-wms.company.com/development/api", "development"),
            ("https://internal.invalid/REDACTED", "staging"),
            ("https://wms.company.com/qa/wms/lgfapi", "qa"),
            ("https://internal.wms/prod/system", "prod"),
        ]

        for url, expected_env in real_urls:
            result = flext_oracle_wms_extract_environment_from_url(url)
            assert result == expected_env

    def test_real_entity_validation(self) -> None:
        """Test validation with real Oracle WMS entity names."""
        valid_entities = [
            ("ORDER_HDR", "order_hdr"),
            ("order_dtl", "order_dtl"),
            ("ITEM_MASTER", "item_master"),
            ("inventory_balance", "inventory_balance"),
            ("shipment_hdr", "shipment_hdr"),
            ("receipt_dtl", "receipt_dtl"),
            ("location_master", "location_master"),
            ("company_config", "company_config"),
            ("facility_master", "facility_master"),
            ("wave_hdr", "wave_hdr"),
        ]

        for input_entity, expected in valid_entities:
            result = flext_oracle_wms_validate_entity_name(input_entity)
            assert result.is_success
            assert result.data == expected

    def test_real_api_responses(self) -> None:
        """Test validation with real Oracle WMS API response patterns."""
        # Success responses
        success_responses = [
            {
                "results": [
                    {"order_id": "ORD001", "status": "OPEN"},
                    {"order_id": "ORD002", "status": "RELEASED"}
                ],
                "page_nbr": 1,
                "page_count": 1,
                "result_count": 2
            },
            {
                "data": {"order_id": "ORD001", "status": "OPEN"},
                "message": "Order retrieved successfully"
            },
            {
                "status": "success",
                "entity_count": 150,
                "timestamp": "2025-01-15T10:30:00Z"
            }
        ]

        for response in success_responses:
            result = flext_oracle_wms_validate_api_response(response)
            assert result.is_success

        # Error responses
        error_responses = [
            {"error": "Order not found"},
            {"error": "Insufficient privileges", "error_code": "AUTH001"},
            {"message": "Error: Database connection failed"},
            {"message": "System error occurred during processing"},
            {"status": "error", "message": "Invalid entity name provided"},
        ]

        for response in error_responses:
            result = flext_oracle_wms_validate_api_response(response)
            assert result.is_failure

    def test_real_pagination_responses(self) -> None:
        """Test with real Oracle WMS pagination response structures."""
        real_pagination = {
            "results": [
                {"order_id": "ORD001", "status": "OPEN"},
                {"order_id": "ORD002", "status": "RELEASED"}
            ],
            "page_nbr": 2,
            "page_count": 5,
            "result_count": 500,
            "next_page": "https://wms.company.com/api/orders?page=3",
            "previous_page": "https://wms.company.com/api/orders?page=1"
        }

        result = flext_oracle_wms_extract_pagination_info(real_pagination)

        assert result["current_page"] == 2
        assert result["total_pages"] == 5
        assert result["total_results"] == 500
        assert result["has_next"] is True
        assert result["has_previous"] is True
        assert "page=3" in result["next_url"]
        assert "page=1" in result["previous_url"]

    def test_real_record_chunking(self) -> None:
        """Test chunking with real Oracle WMS record structures."""
        # Simulate real order records
        order_records = [
            {
                "order_id": f"ORD{i:04d}",
                "facility": "DC01",
                "status": "OPEN" if i % 2 == 0 else "RELEASED",
                "order_date": "2025-01-15",
                "total_lines": 5,
                "priority": "HIGH" if i % 3 == 0 else "NORMAL"
            }
            for i in range(1, 101)  # 100 records
        ]

        # Test with typical batch size
        chunks = flext_oracle_wms_chunk_records(order_records, 25)

        assert len(chunks) == 4
        assert all(len(chunk) == 25 for chunk in chunks[:3])
        assert len(chunks[3]) == 25  # Last chunk

        # Verify record integrity
        all_records = []
        for chunk in chunks:
            all_records.extend(chunk)

        assert len(all_records) == 100
        assert all_records[0]["order_id"] == "ORD0001"
        assert all_records[-1]["order_id"] == "ORD0100"

    def test_real_timestamp_formatting(self) -> None:
        """Test timestamp formatting with real Oracle WMS timestamp patterns."""
        real_timestamps = [
            "2025-01-15T10:30:00Z",
            "2025-01-15T10:30:00.123Z",
            "2025-01-15T10:30:00+00:00",
            "2025-01-15 10:30:00",
            "2025-01-15T10:30:00.123456Z",
        ]

        for timestamp in real_timestamps:
            result = flext_oracle_wms_format_timestamp(timestamp)
            assert result == timestamp

        # Test with None (should return current time)
        current_result = flext_oracle_wms_format_timestamp(None)
        assert isinstance(current_result, str)
        assert "T" in current_result
        assert current_result.endswith("Z") or "+" in current_result

    def test_real_url_normalization(self) -> None:
        """Test URL normalization with real Oracle WMS URL patterns."""
        real_scenarios = [
            ("https://company.oraclecloud.com", "wms/lgfapi/v10/entity/orders",
             "https://company.oraclecloud.com/wms/lgfapi/v10/entity/orders"),
            ("https://wms.company.com/", "/api/v2/orders/",
             "https://wms.company.com/api/v2/orders/"),
            ("https://internal.wms", "production/wms/lgfapi/v10/",
             "https://internal.wms/production/wms/lgfapi/v10/"),
        ]

        for base_url, path, expected in real_scenarios:
            result = flext_oracle_wms_normalize_url(base_url, path)
            assert result == expected

    def test_validation_with_real_data_types(self) -> None:
        """Test validation functions with real Oracle WMS data types."""
        # Test with real record structures
        real_orders = [
            {"order_id": "ORD001", "facility": "DC01"},
            {"order_id": "ORD002", "facility": "DC02"},
        ]
        validate_records_list(real_orders)  # Should pass

        # Test with real configuration structure
        real_config = {
            "base_url": "https://wms.company.com",
            "timeout": 30,
            "retry_count": 3,
            "environment": "production"
        }
        validate_dict_parameter(real_config, "wms_config")  # Should pass

        # Test with real entity names
        entity_names = ["order_hdr", "item_master", "inventory_balance"]
        for entity_name in entity_names:
            validate_string_parameter(entity_name, "entity_name")  # Should pass

    def test_error_handling_real_scenarios(self) -> None:
        """Test error handling with real-world exception scenarios."""
        # Simulate real database connection error
        db_error = ConnectionError("ORA-12541: TNS:no listener")

        with pytest.raises(FlextOracleWmsError) as exc_info:
            handle_operation_exception(
                db_error,
                "connect to Oracle WMS database",
                facility="DC01",
                retry_attempt=3
            )

        assert "TNS:no listener" in str(exc_info.value)
        assert exc_info.value.__cause__ == db_error

        # Simulate real API timeout error
        timeout_error = TimeoutError("Request timeout after 30 seconds")

        with pytest.raises(FlextOracleWmsError) as exc_info:
            handle_operation_exception(
                timeout_error,
                "retrieve order data",
                order_id="ORD001",
                endpoint="/api/orders"
            )

        assert "timeout" in str(exc_info.value).lower()

    def test_edge_cases_real_world(self) -> None:
        """Test edge cases that occur in real Oracle WMS environments."""
        # Very long entity names (should fail)
        long_entity = "a" * 200
        result = flext_oracle_wms_validate_entity_name(long_entity)
        assert result.is_failure

        # Entity names with special characters (should fail)
        invalid_entities = ["order@hdr", "item-master", "inv.balance", "order hdr"]
        for entity in invalid_entities:
            result = flext_oracle_wms_validate_entity_name(entity)
            assert result.is_failure

        # URLs with unusual but valid structures
        unusual_urls = [
            "https://internal.invalid/REDACTED.com/env1/api",
            "https://internal.invalid/REDACTED",
            "https://wms.company.co.uk/staging/v2",
        ]

        for url in unusual_urls:
            # Should not raise exceptions
            env = flext_oracle_wms_extract_environment_from_url(url)
            assert isinstance(env, str)
            assert len(env) > 0

    def test_performance_considerations(self) -> None:
        """Test performance considerations with large real-world datasets."""
        # Large record set (simulating real warehouse data)
        large_dataset = [
            {"order_id": f"ORD{i:06d}", "status": "OPEN"}
            for i in range(10000)
        ]

        # Test chunking large dataset
        chunks = flext_oracle_wms_chunk_records(large_dataset, 1000)
        assert len(chunks) == 10
        assert all(len(chunk) == 1000 for chunk in chunks)

        # Verify no data loss
        total_records = sum(len(chunk) for chunk in chunks)
        assert total_records == 10000
