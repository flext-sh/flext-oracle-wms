"""Real functional tests for Oracle WMS helpers module."""


from flext_oracle_wms.helpers import (
    flext_oracle_wms_build_filter_query,
    flext_oracle_wms_calculate_pagination_info,
    flext_oracle_wms_extract_entity_metadata,
    flext_oracle_wms_format_wms_record,
    flext_oracle_wms_sanitize_entity_name,
    flext_oracle_wms_validate_connection,
)


class TestConnectionValidation:
    """Test connection validation with real scenarios."""

    def test_valid_connection_info(self) -> None:
        """Test validation with complete connection info."""
        connection_info = {
            "base_url": "https://test.wms.oraclecloud.com",
            "username": "test_user",
            "password": "test_pass",
        }
        result = flext_oracle_wms_validate_connection(connection_info)
        assert result.is_success is True

    def test_missing_base_url(self) -> None:
        """Test validation fails without base_url."""
        connection_info = {
            "username": "test_user",
            "password": "test_pass",
        }
        result = flext_oracle_wms_validate_connection(connection_info)
        assert result.is_success is False
        assert "Missing base_url" in result.error

    def test_missing_username(self) -> None:
        """Test validation fails without username."""
        connection_info = {
            "base_url": "https://test.wms.oraclecloud.com",
            "password": "test_pass",
        }
        result = flext_oracle_wms_validate_connection(connection_info)
        assert result.is_success is False
        assert "Missing username" in result.error

    def test_missing_password(self) -> None:
        """Test validation fails without password."""
        connection_info = {
            "base_url": "https://test.wms.oraclecloud.com",
            "username": "test_user",
        }
        result = flext_oracle_wms_validate_connection(connection_info)
        assert result.is_success is False
        assert "Missing password" in result.error

    def test_invalid_url_format(self) -> None:
        """Test validation fails with invalid URL."""
        connection_info = {
            "base_url": "not-a-valid-url",
            "username": "test_user",
            "password": "test_pass",
        }
        result = flext_oracle_wms_validate_connection(connection_info)
        assert result.is_success is False


class TestEntityNameSanitization:
    """Test entity name sanitization functionality."""

    def test_valid_entity_name(self) -> None:
        """Test sanitization of valid entity name."""
        result = flext_oracle_wms_sanitize_entity_name("order_hdr")
        assert result.is_success is True
        assert result.data == "order_hdr"

    def test_entity_name_with_spaces(self) -> None:
        """Test sanitization removes spaces."""
        result = flext_oracle_wms_sanitize_entity_name("order hdr")
        assert result.is_success is True
        assert " " not in result.data

    def test_entity_name_with_special_chars(self) -> None:
        """Test sanitization handles special characters."""
        result = flext_oracle_wms_sanitize_entity_name("order-hdr@test")
        assert result.is_success is True
        # Should remove or replace special characters
        assert "@" not in result.data

    def test_empty_entity_name(self) -> None:
        """Test sanitization fails with empty name."""
        result = flext_oracle_wms_sanitize_entity_name("")
        assert result.is_success is False

    def test_very_long_entity_name(self) -> None:
        """Test sanitization handles long names."""
        long_name = "a" * 100
        result = flext_oracle_wms_sanitize_entity_name(long_name)
        assert result.is_success is True
        # Function accepts long names - just verify it worked
        assert len(result.data) == 100


class TestFilterQueryBuilding:
    """Test filter query building functionality."""

    def test_simple_filter(self) -> None:
        """Test building simple equality filter."""
        filters = [{"field": "status", "operator": "eq", "value": "active"}]
        result = flext_oracle_wms_build_filter_query(filters)
        assert result.is_success is True

    def test_multiple_filters(self) -> None:
        """Test building multiple filters."""
        filters = [
            {"field": "status", "operator": "eq", "value": "active"},
            {"field": "priority", "operator": "eq", "value": "high"},
            {"field": "type", "operator": "eq", "value": "order"},
        ]
        result = flext_oracle_wms_build_filter_query(filters)
        assert result.is_success is True

    def test_range_filter(self) -> None:
        """Test building range-based filter."""
        filters = [
            {"field": "created_date", "operator": "gte", "value": "2025-01-01"},
            {"field": "created_date", "operator": "lte", "value": "2025-12-31"},
        ]
        result = flext_oracle_wms_build_filter_query(filters)
        assert result.is_success is True

    def test_list_filter(self) -> None:
        """Test building filter with list of values."""
        filters = [
            {"field": "status", "operator": "in", "value": ["active", "pending", "completed"]},
        ]
        result = flext_oracle_wms_build_filter_query(filters)
        assert result.is_success is True

    def test_empty_filters(self) -> None:
        """Test building query with no filters."""
        result = flext_oracle_wms_build_filter_query([])
        assert result.is_success is True


class TestEntityMetadataExtraction:
    """Test entity metadata extraction functionality."""

    def test_extract_basic_metadata(self) -> None:
        """Test extraction of basic entity metadata."""
        entity_data = {
            "name": "order_hdr",
            "description": "Order header entity",
            "primary_key": "order_id",
            "fields": {
                "order_id": {"type": "string", "primary_key": True},
                "status": {"type": "string"},
                "created_date": {"type": "datetime"},
            },
        }
        result = flext_oracle_wms_extract_entity_metadata(entity_data)
        assert result.is_success is True
        assert result.data["name"] == "order_hdr"
        assert result.data["primary_key"] == "order_id"

    def test_extract_with_relationships(self) -> None:
        """Test extraction with entity relationships."""
        entity_data = {
            "name": "order_hdr",
            "fields": {"order_id": {"type": "string"}},
            "relationships": {
                "lines": {"entity": "order_line", "type": "one_to_many"},
            },
        }
        result = flext_oracle_wms_extract_entity_metadata(entity_data)
        assert result.is_success is True

    def test_extract_missing_name(self) -> None:
        """Test extraction handles missing entity name."""
        entity_data = {
            "fields": {"id": {"type": "string"}},
        }
        result = flext_oracle_wms_extract_entity_metadata(entity_data)
        assert result.is_success is True
        assert result.data["name"] == "unknown"


class TestRecordFormatting:
    """Test WMS record formatting functionality."""

    def test_format_simple_record(self) -> None:
        """Test formatting simple WMS record."""
        record = {
            "order_id": "12345",
            "status": "active",
            "total_amount": 99.99,
        }
        result = flext_oracle_wms_format_wms_record(record, "order_hdr")
        assert result.is_success is True
        assert result.data["entity"] == "order_hdr"
        assert result.data["data"]["order_id"] == "12345"

    def test_format_record_with_dates(self) -> None:
        """Test formatting record with date fields."""
        record = {
            "order_id": "12345",
            "created_date": "2025-01-01T12:00:00Z",
            "modified_date": "2025-01-02T15:30:00Z",
        }
        result = flext_oracle_wms_format_wms_record(record, "order_hdr")
        assert result.is_success is True

    def test_format_record_with_nulls(self) -> None:
        """Test formatting record with null values."""
        record = {
            "order_id": "12345",
            "notes": None,
            "description": "",
        }
        result = flext_oracle_wms_format_wms_record(record, "order_hdr")
        assert result.is_success is True

    def test_format_empty_record(self) -> None:
        """Test formatting empty record."""
        result = flext_oracle_wms_format_wms_record({}, "order_hdr")
        assert result.is_success is True


class TestPaginationCalculation:
    """Test pagination info calculation functionality."""

    def test_calculate_basic_pagination(self) -> None:
        """Test calculation of basic pagination info."""
        result = flext_oracle_wms_calculate_pagination_info(
            current_page=1,
            page_size=50,
            total_records=250,
        )
        assert result.is_success is True
        assert result.data["total_pages"] == 5
        assert result.data["has_next"] is True
        assert result.data["has_previous"] is True

    def test_calculate_last_page(self) -> None:
        """Test calculation for last page."""
        result = flext_oracle_wms_calculate_pagination_info(
            current_page=4,  # 0-based, so page 4 is the last page (5 total pages)
            page_size=50,
            total_records=250,
        )
        assert result.is_success is True
        assert result.data["has_next"] is False
        assert result.data["has_previous"] is True

    def test_calculate_middle_page(self) -> None:
        """Test calculation for middle page."""
        result = flext_oracle_wms_calculate_pagination_info(
            current_page=2,  # 0-based, so page 2 is a middle page
            page_size=50,
            total_records=250,
        )
        assert result.is_success is True
        assert result.data["has_next"] is True
        assert result.data["has_previous"] is True

    def test_calculate_single_page(self) -> None:
        """Test calculation when all records fit in one page."""
        result = flext_oracle_wms_calculate_pagination_info(
            current_page=0,  # 0-based, so page 0 is the first page
            page_size=100,
            total_records=50,
        )
        assert result.is_success is True
        assert result.data["total_pages"] == 1
        assert result.data["has_next"] is False
        assert result.data["has_previous"] is False

    def test_calculate_invalid_page_size(self) -> None:
        """Test calculation fails with invalid page size."""
        result = flext_oracle_wms_calculate_pagination_info(
            current_page=0,
            page_size=0,
            total_records=100,
        )
        assert result.is_success is False
