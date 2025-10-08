"""Comprehensive unit tests for Oracle WMS helpers module - targeting 90%+ coverage.

Based on working code patterns and real Oracle WMS URL structures.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import pytest
from flext_core import FlextTypes

from flext_oracle_wms import (
    flext_oracle_wms_build_entity_url,
    flext_oracle_wms_chunk_records,
    flext_oracle_wms_extract_environment_from_url,
    flext_oracle_wms_extract_pagination_info,
    flext_oracle_wms_format_timestamp,
    flext_oracle_wms_normalize_url,
    flext_oracle_wms_validate_api_response,
    flext_oracle_wms_validate_entity_name,
)


@pytest.mark.unit
class TestUrlHelpers:
    """Test URL manipulation helper functions."""

    def test_build_entity_url_basic(self) -> None:
        """Test basic entity URL building."""
        base_url = "https://test.wms.oraclecloud.com"
        environment = "test"
        entity_name = "facility"

        result = flext_oracle_wms_build_entity_url(base_url, environment, entity_name)

        expected = f"{base_url}/{environment}/wms/lgfapi/v10/entity/{entity_name}/"
        assert result == expected

    def test_build_entity_url_with_api_version(self) -> None:
        """Test entity URL building with API version."""
        base_url = "https://test.wms.oraclecloud.com"
        environment = "test"
        entity_name = "item"
        api_version = "v1.0"

        result = flext_oracle_wms_build_entity_url(
            base_url,
            environment,
            entity_name,
            api_version,
        )

        expected = (
            f"{base_url}/{environment}/wms/lgfapi/{api_version}/entity/{entity_name}/"
        )
        assert result == expected

    def test_build_entity_url_with_trailing_slash(self) -> None:
        """Test entity URL building with trailing slash in base URL."""
        base_url = "https://test.wms.oraclecloud.com/"
        environment = "test"
        entity_name = "company"

        result = flext_oracle_wms_build_entity_url(base_url, environment, entity_name)

        # Should handle trailing slash correctly
        assert "//" not in result.replace("https://", "")
        assert entity_name in result

    def test_build_entity_url_empty_entity(self) -> None:
        """Test entity URL building with empty entity name."""
        base_url = "https://test.wms.oraclecloud.com"
        environment = "test"

        with pytest.raises(
            Exception,
            match="All URL components must be non-empty strings",
        ):
            flext_oracle_wms_build_entity_url(base_url, environment, "")

    def test_build_entity_url_invalid_base_url(self) -> None:
        """Test entity URL building with invalid base URL."""
        environment = "test"
        entity_name = "facility"

        with pytest.raises(
            Exception,
            match="All URL components must be non-empty strings",
        ):
            flext_oracle_wms_build_entity_url("", environment, entity_name)

    def test_normalize_url_basic(self) -> None:
        """Test basic URL normalization."""
        base_url = "https://test.wms.oraclecloud.com/"
        path = "test/api"
        result = flext_oracle_wms_normalize_url(base_url, path)

        expected = "https://test.wms.oraclecloud.com/test/api"
        assert result == expected

    def test_normalize_url_no_trailing_slash(self) -> None:
        """Test URL normalization when base URL has no trailing slash."""
        base_url = "https://test.wms.oraclecloud.com"
        path = "test"
        result = flext_oracle_wms_normalize_url(base_url, path)

        expected = "https://test.wms.oraclecloud.com/test"
        assert result == expected

    def test_normalize_url_leading_slash_in_path(self) -> None:
        """Test URL normalization with leading slash in path."""
        base_url = "https://test.wms.oraclecloud.com/"
        path = "/test/api"
        result = flext_oracle_wms_normalize_url(base_url, path)

        expected = "https://test.wms.oraclecloud.com/test/api"
        assert result == expected

    def test_extract_environment_from_url_basic(self) -> None:
        """Test environment extraction from URL."""
        url = "https://invalid.wms.ocs.oraclecloud.com/company_unknow"
        result = flext_oracle_wms_extract_environment_from_url(url)

        assert result == "company_unknow"

    def test_extract_environment_from_url_with_path(self) -> None:
        """Test environment extraction from URL with additional path."""
        url = "https://invalid.wms.ocs.oraclecloud.com/company_unknow/scmRestApi/resources"
        result = flext_oracle_wms_extract_environment_from_url(url)

        assert result == "company_unknow"

    def test_extract_environment_from_url_no_environment(self) -> None:
        """Test environment extraction from URL without environment."""
        url = "https://invalid.wms.ocs.oraclecloud.com/"
        result = flext_oracle_wms_extract_environment_from_url(url)

        assert result == "default"

    def test_extract_environment_from_url_invalid_url(self) -> None:
        """Test environment extraction from invalid URL."""
        result = flext_oracle_wms_extract_environment_from_url("not-a-url")
        assert result == "not-a-url"  # Function parses the entire string as environment


@pytest.mark.unit
class TestValidationHelpers:
    """Test validation helper functions."""

    def test_validate_entity_name_valid(self) -> None:
        """Test entity name validation with valid names."""
        valid_names = [
            "facility",
            "item",
            "company",
            "order_hdr",
            "order_dtl",
            "action_code",
        ]

        for name in valid_names:
            result = flext_oracle_wms_validate_entity_name(name)
            assert result.success
            assert result.data == name.lower()

    def test_validate_entity_name_invalid(self) -> None:
        """Test entity name validation with invalid names."""
        invalid_names = [
            "",  # Empty
            "   ",  # Only whitespace
            "invalid name with spaces",  # Spaces
            "special!chars@",  # Special characters
        ]

        for name in invalid_names:
            result = flext_oracle_wms_validate_entity_name(name)
            assert result.is_failure

    def test_validate_api_response_valid(self) -> None:
        """Test API response validation with valid response."""
        response = {
            "results": [{"id": 1, "name": "Test 1"}],
            "status": "success",
            "message": "Data retrieved successfully",
        }

        result = flext_oracle_wms_validate_api_response(response)
        assert result.success
        assert result.data == response

    def test_validate_api_response_error_field(self) -> None:
        """Test API response validation with error field."""
        response = {"error": "Database connection failed", "status": "error"}

        result = flext_oracle_wms_validate_api_response(response)
        assert result.is_failure
        assert result.error is not None
        assert (
            result.error is not None
            and "API error: Database connection failed" in result.error
        )

    def test_validate_api_response_error_status(self) -> None:
        """Test API response validation with error status."""
        response = {"status": "error", "message": "Invalid authentication"}

        result = flext_oracle_wms_validate_api_response(response)
        assert result.is_failure
        assert result.error is not None
        assert (
            result.error is not None
            and "API error: Invalid authentication" in result.error
        )


@pytest.mark.unit
class TestDataProcessingHelpers:
    """Test data processing helper functions."""

    def test_chunk_records_basic(self) -> None:
        """Test basic record chunking."""
        records: list[FlextTypes.Dict] = [
            {"id": i, "value": f"item_{i}"} for i in range(10)
        ]
        chunk_size = 3

        chunks = list(flext_oracle_wms_chunk_records(records, chunk_size))

        assert len(chunks) == 4  # 3 full chunks + 1 partial
        assert len(chunks[0]) == 3
        assert len(chunks[1]) == 3
        assert len(chunks[2]) == 3
        assert len(chunks[3]) == 1

    def test_chunk_records_exact_division(self) -> None:
        """Test chunking when records divide evenly."""
        records: list[FlextTypes.Dict] = [
            {"id": i, "value": f"item_{i}"} for i in range(9)
        ]
        chunk_size = 3

        chunks = list(flext_oracle_wms_chunk_records(records, chunk_size))

        assert len(chunks) == 3
        assert len(chunks[0]) == 3
        assert len(chunks[1]) == 3
        assert len(chunks[2]) == 3

    def test_chunk_records_empty_list(self) -> None:
        """Test chunking empty list."""
        records: list[FlextTypes.Dict] = []
        chunk_size = 3

        chunks = list(flext_oracle_wms_chunk_records(records, chunk_size))

        assert len(chunks) == 0

    def test_chunk_records_single_chunk(self) -> None:
        """Test chunking when all records fit in one chunk."""
        records: list[FlextTypes.Dict] = [
            {"id": i, "value": f"item_{i}"} for i in [1, 2, 3]
        ]
        chunk_size = 5

        chunks = list(flext_oracle_wms_chunk_records(records, chunk_size))

        assert len(chunks) == 1
        assert len(chunks[0]) == 3

    def test_chunk_records_invalid_chunk_size(self) -> None:
        """Test chunking with invalid chunk size."""
        records: list[FlextTypes.Dict] = [
            {"id": i, "value": f"item_{i}"} for i in [1, 2, 3]
        ]

        with pytest.raises(Exception, match="Chunk size must be positive"):
            flext_oracle_wms_chunk_records(records, 0)

        with pytest.raises(Exception, match="Chunk size must be positive"):
            flext_oracle_wms_chunk_records(records, -1)

    def test_extract_pagination_info_complete(self) -> None:
        """Test extracting pagination info with all fields."""
        response = {
            "results": [{"id": 1}],
            "page_nbr": 2,
            "page_count": 5,
            "result_count": 50,
            "next_page": "page=3",
            "previous_page": "page=1",
        }

        result = flext_oracle_wms_extract_pagination_info(response)

        expected = {
            "current_page": 2,
            "total_pages": 5,
            "total_results": 50,
            "next_url": "page=3",
            "previous_url": "page=1",
            "has_next": True,
            "has_previous": True,
        }

        assert result == expected

    def test_extract_pagination_info_minimal(self) -> None:
        """Test extracting pagination info with minimal fields."""
        response: FlextTypes.Dict = {"results": [{"id": 1}, {"id": 2}]}

        result = flext_oracle_wms_extract_pagination_info(response)

        expected = {
            "current_page": 1,
            "total_pages": 1,
            "total_results": 0,
            "next_url": None,
            "previous_url": None,
            "has_next": False,
            "has_previous": False,
        }

        assert result == expected

    def test_extract_pagination_info_no_data(self) -> None:
        """Test extracting pagination info from response with no data."""
        response: FlextTypes.Dict = {}

        result = flext_oracle_wms_extract_pagination_info(response)

        expected = {
            "current_page": 1,
            "total_pages": 1,
            "total_results": 0,
            "next_url": None,
            "previous_url": None,
            "has_next": False,
            "has_previous": False,
        }

        assert result == expected


@pytest.mark.unit
class TestTimestampHelpers:
    """Test timestamp formatting helper functions."""

    def test_format_timestamp_string_iso(self) -> None:
        """Test formatting ISO timestamp string."""
        timestamp_str = "2025-01-01T12:30:45Z"
        result = flext_oracle_wms_format_timestamp(timestamp_str)

        assert result == timestamp_str

    def test_format_timestamp_string_non_iso(self) -> None:
        """Test formatting non-ISO timestamp string."""
        timestamp_str = "2025-01-01 12:30:45"
        result = flext_oracle_wms_format_timestamp(timestamp_str)

        # Should still return the string (might be processed differently)
        assert isinstance(result, str)
        assert result == timestamp_str

    def test_format_timestamp_none(self) -> None:
        """Test formatting None timestamp."""
        result = flext_oracle_wms_format_timestamp(None)

        # Should return current timestamp as ISO string
        assert isinstance(result, str)
        assert "T" in result  # ISO format contains T

    def test_format_timestamp_empty_string(self) -> None:
        """Test formatting empty timestamp string."""
        result = flext_oracle_wms_format_timestamp("")

        # Should return current timestamp for empty string
        assert isinstance(result, str)
        assert "T" in result
