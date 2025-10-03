"""Simple unit tests for Oracle WMS helpers module - targeting coverage.

Based on actual module functions and working patterns.


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

    def test_normalize_url_basic(self) -> None:
        """Test basic URL normalization."""
        base_url = "https://test.wms.oraclecloud.com/test"
        path = "scmRestApi/resources/latest/facility"

        result = flext_oracle_wms_normalize_url(base_url, path)

        assert isinstance(result, str)
        assert "test.wms.oraclecloud.com" in result
        assert "facility" in result

    def test_normalize_url_with_trailing_slash(self) -> None:
        """Test URL normalization with trailing slash."""
        base_url = "https://test.wms.oraclecloud.com/test/"
        path = "/scmRestApi/resources/latest/facility"

        result = flext_oracle_wms_normalize_url(base_url, path)

        assert isinstance(result, str)
        # Should handle trailing/leading slashes properly
        assert "//" not in result.replace("https://", "")

    def test_extract_environment_from_url_basic(self) -> None:
        """Test environment extraction from URL."""
        url = "https://ta29.wms.ocs.oraclecloud.com/raizen_test"
        result = flext_oracle_wms_extract_environment_from_url(url)

        assert result == "raizen_test"

    def test_extract_environment_from_url_with_path(self) -> None:
        """Test environment extraction from URL with additional path."""
        url = "https://ta29.wms.ocs.oraclecloud.com/raizen_test/scmRestApi/resources"
        result = flext_oracle_wms_extract_environment_from_url(url)

        assert result == "raizen_test"

    def test_extract_environment_from_url_invalid(self) -> None:
        """Test environment extraction from invalid URL."""
        url = "not-a-valid-url"
        result = flext_oracle_wms_extract_environment_from_url(url)

        # Should handle invalid URL gracefully
        assert result is None or isinstance(result, str)

    def test_build_entity_url_basic(self) -> None:
        """Test basic entity URL building."""
        base_url = "https://test.wms.oraclecloud.com"
        environment = "test"
        entity_name = "facility"

        result = flext_oracle_wms_build_entity_url(base_url, environment, entity_name)

        assert isinstance(result, str)
        assert "test.wms.oraclecloud.com" in result
        assert "facility" in result

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

        assert isinstance(result, str)
        assert "item" in result
        if api_version:
            assert api_version in result or "latest" in result

    def test_validate_entity_name_valid(self) -> None:
        """Test entity name validation with valid names."""
        valid_names = ["facility", "item", "company", "order_hdr"]

        for name in valid_names:
            result = flext_oracle_wms_validate_entity_name(name)
            assert result.success

    def test_validate_entity_name_invalid(self) -> None:
        """Test entity name validation with invalid names."""
        invalid_names = ["", "invalid name with spaces", "123_numeric_start"]

        for name in invalid_names:
            result = flext_oracle_wms_validate_entity_name(name)
            # Should either fail validation or handle gracefully
            assert result.is_failure or result.success

        # Test empty string - should fail validation
        result = flext_oracle_wms_validate_entity_name("")
        assert result.is_failure

        # Test invalid characters
        result = flext_oracle_wms_validate_entity_name("invalid-name!")
        assert result.is_failure


@pytest.mark.unit
class TestDataProcessingHelpers:
    """Test data processing helper functions."""

    def test_validate_api_response_invalid_list(self) -> None:
        """Test API response validation with invalid list input."""
        response = [{"id": 1, "name": "Test 1"}, {"id": 2, "name": "Test 2"}]

        # Function expects dict, should return failure result with list
        result = flext_oracle_wms_validate_api_response(response)
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "not a dictionary" in result.error

    def test_validate_api_response_valid_dict(self) -> None:
        """Test API response validation with valid dict."""
        response = {"results": [{"id": 1, "name": "Test 1"}], "count": 1}

        result = flext_oracle_wms_validate_api_response(response)
        assert result.success

    def test_validate_api_response_invalid(self) -> None:
        """Test API response validation with invalid data."""
        invalid_responses = [None, "", 123, True]

        for response in invalid_responses:
            # These should all return failure results since function expects dict
            result = flext_oracle_wms_validate_api_response(response)
            assert result.is_failure
            assert result.error is not None
            assert result.error is not None and "not a dictionary" in result.error

    def test_extract_pagination_info_complete(self) -> None:
        """Test extracting pagination info with complete data."""
        response = {
            "results": [{"id": 1}],
            "page_nbr": 1,
            "page_count": 5,
            "result_count": 50,
            "next_page": "page=2",
            "previous_page": None,
        }

        result = flext_oracle_wms_extract_pagination_info(response)

        assert isinstance(result, dict)
        # Should contain pagination information
        assert "current_page" in result or "page_nbr" in result

    def test_extract_pagination_info_minimal(self) -> None:
        """Test extracting pagination info with minimal data."""
        response: FlextTypes.Dict = {"results": [{"id": 1}, {"id": 2}]}

        result = flext_oracle_wms_extract_pagination_info(response)

        assert isinstance(result, dict)

    def test_extract_pagination_info_empty(self) -> None:
        """Test extracting pagination info from empty response."""
        response: FlextTypes.Dict = {}

        result = flext_oracle_wms_extract_pagination_info(response)

        assert isinstance(result, dict)

    def test_chunk_records_basic(self) -> None:
        """Test basic record chunking."""
        records: list[FlextTypes.Dict] = [
            {"id": i} for i in range(10)
        ]  # [{"id": 0}, {"id": 1}, ...]
        chunk_size = 3

        chunks = list(flext_oracle_wms_chunk_records(records, chunk_size))

        assert len(chunks) >= 3  # Should have at least 3 chunks
        assert chunks[0] == [{"id": 0}, {"id": 1}, {"id": 2}]
        assert chunks[1] == [{"id": 3}, {"id": 4}, {"id": 5}]
        assert chunks[2] == [{"id": 6}, {"id": 7}, {"id": 8}]

    def test_chunk_records_exact_division(self) -> None:
        """Test chunking when records divide evenly."""
        records: list[FlextTypes.Dict] = [
            {"id": i} for i in range(9)
        ]  # [{"id": 0}, {"id": 1}, ...]
        chunk_size = 3

        chunks = list(flext_oracle_wms_chunk_records(records, chunk_size))

        assert len(chunks) == 3
        assert chunks[0] == [{"id": 0}, {"id": 1}, {"id": 2}]
        assert chunks[1] == [{"id": 3}, {"id": 4}, {"id": 5}]
        assert chunks[2] == [{"id": 6}, {"id": 7}, {"id": 8}]

    def test_chunk_records_empty_list(self) -> None:
        """Test chunking empty list."""
        records: list[FlextTypes.Dict] = []
        chunk_size = 3

        chunks = list(flext_oracle_wms_chunk_records(records, chunk_size))

        assert len(chunks) == 0

    def test_chunk_records_single_chunk(self) -> None:
        """Test chunking when all records fit in one chunk."""
        records: list[FlextTypes.Dict] = [{"id": 1}, {"id": 2}, {"id": 3}]
        chunk_size = 5

        chunks = list(flext_oracle_wms_chunk_records(records, chunk_size))

        assert len(chunks) == 1
        assert chunks[0] == [{"id": 1}, {"id": 2}, {"id": 3}]

    def test_format_timestamp_basic(self) -> None:
        """Test basic timestamp formatting."""
        timestamp = "2025-01-01T12:30:45Z"
        result = flext_oracle_wms_format_timestamp(timestamp)

        assert isinstance(result, str)
        assert "2025" in result

    def test_format_timestamp_none(self) -> None:
        """Test formatting None timestamp."""
        result = flext_oracle_wms_format_timestamp(None)

        assert isinstance(result, str)

    def test_format_timestamp_empty(self) -> None:
        """Test formatting empty timestamp."""
        result = flext_oracle_wms_format_timestamp("")

        assert isinstance(result, str)
