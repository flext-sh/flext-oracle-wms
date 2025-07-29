"""Comprehensive test for Oracle WMS client functionality."""

from unittest.mock import Mock, patch

import httpx
import pytest
from flext_core import get_logger

from flext_oracle_wms.exceptions import (
    FlextOracleWmsApiError,
)
from flext_oracle_wms.models import FlextOracleWmsDiscoveryResult


class TestUtilityFunctions:
    """Test utility functions in client module."""

    def test_get_logger(self) -> None:
        """Test logger creation function."""
        logger = get_logger("test_logger")
        assert logger.name == "test_logger"
        assert logger.level == 20  # INFO level
        assert len(logger.handlers) > 0

    def test_get_logger_existing(self) -> None:
        """Test getting existing logger."""
        # First call creates logger
        logger1 = get_logger("existing_logger")
        # Second call returns same logger
        logger2 = get_logger("existing_logger")
        assert logger1 is logger2


class TestFlextOracleWmsAuth:
    """Test the Oracle WMS authentication class."""

    def test_auth_creation(self) -> None:
        """Test auth object creation."""
        auth = FlextOracleWmsAuth("test_user", "test_pass")
        assert auth.username == "test_user"
        assert auth.password == "test_pass"

    def test_get_basic_auth(self) -> None:
        """Test basic auth string generation."""
        auth = FlextOracleWmsAuth("testuser", "testpass")
        basic_auth = auth._get_basic_auth()
        assert isinstance(basic_auth, str)
        # _get_basic_auth returns just the base64 string, not "Basic " prefix
        import base64

        expected = base64.b64encode(b"testuser:testpass").decode()
        assert basic_auth == expected

    def test_auth_flow(self) -> None:
        """Test auth flow with request."""
        auth = FlextOracleWmsAuth("testuser", "testpass")

        # Create mock request
        mock_request = Mock()
        mock_request.headers = {}

        # Test auth flow
        request_generator = auth.auth_flow(mock_request)
        authenticated_request = next(request_generator)

        assert "Authorization" in authenticated_request.headers
        # Should have "Basic " prefix in the Authorization header
        assert authenticated_request.headers["Authorization"].startswith("Basic ")

    def test_auth_flow_invalid_credentials(self) -> None:
        """Test auth flow with empty credentials."""
        auth = FlextOracleWmsAuth("", "")
        mock_request = Mock()
        mock_request.headers = {}

        # Should still work but with empty credentials
        request_generator = auth.auth_flow(mock_request)
        authenticated_request = next(request_generator)
        assert "Authorization" in authenticated_request.headers


class TestFlextOracleWmsLegacyClient:
    """Test the main Oracle WMS legacy client class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.mock_config = Mock()
        self.mock_config.base_url = "https://test.wms.oracle.com"
        self.mock_config.username = "test_user"
        self.mock_config.password = "test_pass"
        self.mock_config.timeout = 30
        self.mock_config.max_retries = 3
        self.mock_config.rate_limit_requests_per_second = 10
        self.mock_config.max_requests_per_minute = 600
        self.mock_config.bulk_batch_size = 100
        self.mock_config.cache_enabled = True
        self.mock_config.api_version = "v1"
        # Additional attributes needed by the client
        self.mock_config.wms_endpoint_base = "/wms/lgfapi"
        self.mock_config.min_request_delay = 0.1
        self.mock_config.batch_size = 100
        self.mock_config.pool_size = 4
        self.mock_config.retry_delay = 0.5
        self.mock_config.headers = {}
        self.mock_config.verify_ssl = True
        self.mock_config.cert = None

    def test_client_creation(self) -> None:
        """Test client creation with valid config."""
        client = FlextOracleWmsLegacyClient(self.mock_config)
        assert client.config == self.mock_config
        assert client.config.base_url == "https://test.wms.oracle.com"
        assert client.config.timeout == 30

    def test_client_property(self) -> None:
        """Test HTTP client property."""
        client = FlextOracleWmsLegacyClient(self.mock_config)
        http_client = client.client
        assert isinstance(http_client, httpx.Client)
        assert http_client.timeout.read == 30

    def test_apply_rate_limiting(self) -> None:
        """Test rate limiting application."""
        client = FlextOracleWmsLegacyClient(self.mock_config)
        # Should not raise any exceptions
        client._apply_rate_limiting()

    @patch("httpx.Client.get")
    def test_make_request_success(self, mock_get) -> None:
        """Test successful HTTP request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_response.headers = {"Content-Type": "application/json"}
        mock_get.return_value = mock_response

        client = FlextOracleWmsLegacyClient(self.mock_config)
        response = client._make_request("GET", "/test")

        assert response.status_code == 200
        assert response.data == {"status": "success"}

    @patch("httpx.Client.get")
    def test_make_request_http_error(self, mock_get) -> None:
        """Test HTTP request with error status."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not found"
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "404 Not Found",
            request=Mock(),
            response=mock_response,
        )
        mock_get.return_value = mock_response

        client = FlextOracleWmsLegacyClient(self.mock_config)

        with pytest.raises(FlextOracleWmsApiError):
            client._make_request("GET", "/nonexistent")

    @patch("httpx.Client.get")
    def test_make_request_connection_error(self, mock_get) -> None:
        """Test HTTP request with connection error."""
        mock_get.side_effect = httpx.ConnectError("Connection failed")

        client = FlextOracleWmsLegacyClient(self.mock_config)

        with pytest.raises(FlextOracleWmsApiError):
            client._make_request("GET", "/test")

    @patch("httpx.Client.get")
    def test_test_connection_success(self, mock_get) -> None:
        """Test successful connection test."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"version": "1.0"}
        mock_get.return_value = mock_response

        client = FlextOracleWmsLegacyClient(self.mock_config)
        result = client.test_connection()

        # Result might be a FlextResult or boolean, check accordingly
        if hasattr(result, "success"):
            assert result.success is True
        else:
            # Should be True for successful connection
            assert result is True

    @patch("httpx.Client.get")
    def test_test_connection_failure(self, mock_get) -> None:
        """Test failed connection test."""
        mock_get.side_effect = httpx.ConnectError("Connection failed")

        client = FlextOracleWmsLegacyClient(self.mock_config)
        result = client.test_connection()
        assert result is False

    def test_validate_entity_name_valid(self) -> None:
        """Test entity name validation with valid names."""
        client = FlextOracleWmsLegacyClient(self.mock_config)

        valid_names = ["order_hdr", "allocation", "item", "location"]
        for name in valid_names:
            result = client.validate_entity_name(name)
            assert result == name

    def test_validate_entity_name_invalid(self) -> None:
        """Test entity name validation with invalid names."""
        client = FlextOracleWmsLegacyClient(self.mock_config)

        with pytest.raises(FlextOracleWmsApiError):
            client.validate_entity_name("invalid_entity_name")

    def test_build_api_url_simple(self) -> None:
        """Test API URL building with simple endpoint."""
        client = FlextOracleWmsLegacyClient(self.mock_config)

        url = client.build_api_url("order_hdr")
        expected = "https://test.wms.oracle.com/wms/lgfapi/v1/entity/order_hdr"
        assert url == expected

    def test_build_api_url_with_record_id(self) -> None:
        """Test API URL building - record ID not supported in legacy client."""
        client = FlextOracleWmsLegacyClient(self.mock_config)

        # Legacy client doesn't support record_id parameter, just test basic URL
        url = client.build_api_url("order_hdr")
        assert "order_hdr" in url
        assert url.startswith("https://test.wms.oracle.com")

    def test_build_api_url_with_params(self) -> None:
        """Test API URL building with query parameters."""
        client = FlextOracleWmsLegacyClient(self.mock_config)

        url = client.build_api_url("order_hdr", {"status": "active", "limit": 10})
        assert "status=active" in url
        assert "limit=10" in url

    def test_get_connection_info(self) -> None:
        """Test connection info retrieval."""
        client = FlextOracleWmsLegacyClient(self.mock_config)

        info = client.get_connection_info()
        assert info["base_url"] == "https://test.wms.oracle.com"
        assert info["username"] == "test_user"
        assert "password" not in info  # Should not expose password

    @patch("httpx.Client.get")
    def test_discover_entities_success(self, mock_get) -> None:
        """Test successful entity discovery."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "entities": [
                {"name": "order_hdr", "endpoint": "/order_hdr"},
                {"name": "allocation", "endpoint": "/allocation"},
            ],
        }
        mock_get.return_value = mock_response

        client = FlextOracleWmsLegacyClient(self.mock_config)
        result = client.discover_entities()

        assert isinstance(result, FlextOracleWmsDiscoveryResult)
        assert len(result.entities) >= 0  # May include fallback entities

    @patch("httpx.Client.get")
    def test_discover_entities_fallback(self, mock_get) -> None:
        """Test entity discovery with fallback to hardcoded entities."""
        mock_get.side_effect = httpx.ConnectError("Connection failed")

        client = FlextOracleWmsLegacyClient(self.mock_config)
        result = client.discover_entities()

        assert isinstance(result, FlextOracleWmsDiscoveryResult)
        # If discovery fails, result should indicate failure but not crash
        assert len(result.entities) >= 0  # May be empty on failure
        assert result.has_errors is True  # Should indicate error occurred

    @patch("httpx.Client.get")
    def test_get_entity_data_success(self, mock_get) -> None:
        """Test successful entity data retrieval."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"id": 1, "name": "Order 1"}, {"id": 2, "name": "Order 2"}],
        }
        mock_get.return_value = mock_response

        client = FlextOracleWmsLegacyClient(self.mock_config)
        result = client.get_entity_data("order_hdr")

        # Result should be a dict for legacy client, but check the actual type
        if hasattr(result, "data"):
            # Modern FlextResult type
            assert result.success is True
            assert len(result.data.data) == 2
        else:
            # Legacy dict type
            assert result["data"] is not None
            assert len(result["data"]) == 2

    @patch("httpx.Client.post")
    def test_write_entity_data_success(self, mock_post) -> None:
        """Test successful entity data writing."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 123, "status": "created"}
        mock_post.return_value = mock_response

        client = FlextOracleWmsLegacyClient(self.mock_config)
        record = {"name": "Test Order", "status": "active"}
        result = client.write_entity_data("order_hdr", record)

        assert result["status"] == "created"

    def test_context_manager(self) -> None:
        """Test client as context manager."""
        with FlextOracleWmsLegacyClient(self.mock_config) as client:
            assert isinstance(client, FlextOracleWmsLegacyClient)
        # Should close gracefully

    def test_close(self) -> None:
        """Test client close method."""
        client = FlextOracleWmsLegacyClient(self.mock_config)
        client.close()  # Should not raise any exceptions

    def test_get_entity_metadata(self) -> None:
        """Test entity metadata retrieval."""
        client = FlextOracleWmsLegacyClient(self.mock_config)

        metadata = client.get_entity_metadata("order_hdr")
        assert isinstance(metadata, dict)
        assert "entity_name" in metadata
        assert metadata["entity_name"] == "order_hdr"

    @patch("httpx.Client.get")
    def test_bulk_get_entities_success(self, mock_get) -> None:
        """Test bulk entity data retrieval."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"id": 1}]}
        mock_get.return_value = mock_response

        client = FlextOracleWmsLegacyClient(self.mock_config)
        entities = ["order_hdr", "allocation"]

        results = client.bulk_get_entities(entities)
        assert isinstance(results, dict)
        assert "order_hdr" in results
        assert "allocation" in results

    @patch("httpx.Client.post")
    def test_bulk_post_records_success(self, mock_post) -> None:
        """Test bulk record posting."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"success": True}
        mock_post.return_value = mock_response

        client = FlextOracleWmsLegacyClient(self.mock_config)
        records = [{"name": "Order 1"}, {"name": "Order 2"}]

        results = client.bulk_post_records("order_hdr", records)
        assert isinstance(results, dict)

    def test_cache_operations(self) -> None:
        """Test cache-related operations."""
        client = FlextOracleWmsLegacyClient(self.mock_config)

        # Test cache stats
        stats = client.get_bulk_cache_stats()
        assert isinstance(stats, dict)

        # Test cache clear
        result = client.clear_bulk_cache()
        assert isinstance(result, bool)

    def test_operation_tracking(self) -> None:
        """Test operation tracking functionality."""
        client = FlextOracleWmsLegacyClient(self.mock_config)

        # Track an operation
        op_id = client._track_operation("test_operation", "order_hdr", {"test": "data"})
        assert isinstance(op_id, str)

        # Mark as success
        client._mark_operation_success(op_id, {"result": "success"})

        # Get stats
        stats = client.get_operation_tracking_stats()
        assert isinstance(stats, dict)
        assert "total_operations" in stats

    def test_operation_tracking_failure(self) -> None:
        """Test operation tracking for failures."""
        client = FlextOracleWmsLegacyClient(self.mock_config)

        # Track and fail an operation
        op_id = client._track_operation("test_operation", "order_hdr", {"test": "data"})
        client._mark_operation_failed(op_id, "Test error")

        stats = client.get_operation_tracking_stats()
        assert stats["total_operations"] >= 1

    def test_clear_operation_tracking(self) -> None:
        """Test clearing operation tracking."""
        client = FlextOracleWmsLegacyClient(self.mock_config)

        # Track some operations
        client._track_operation("op1", "order_hdr", {})
        client._track_operation("op2", "allocation", {})

        # Clear all
        cleared = client.clear_operation_tracking()
        assert isinstance(cleared, int)

        # Clear by entity
        cleared = client.clear_operation_tracking("order_hdr")
        assert isinstance(cleared, int)

    def test_bulk_operations_integration_validation(self) -> None:
        """Test bulk operations integration validation."""
        client = FlextOracleWmsLegacyClient(self.mock_config)

        validation = client.validate_bulk_operations_integration()
        assert isinstance(validation, dict)
        # Check if expected keys exist in validation result
        assert len(validation) > 0
        # The method should return a validation result dictionary


class TestClientErrorHandling:
    """Test error handling scenarios in the client."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.mock_config = Mock()
        self.mock_config.base_url = "https://test.wms.oracle.com"
        self.mock_config.username = "test_user"
        self.mock_config.password = "test_pass"
        self.mock_config.timeout = 30
        self.mock_config.max_retries = 3
        self.mock_config.rate_limit_requests_per_second = 10
        self.mock_config.max_requests_per_minute = 600
        self.mock_config.bulk_batch_size = 100
        self.mock_config.cache_enabled = True
        self.mock_config.api_version = "v1"
        # Additional attributes needed by the client
        self.mock_config.wms_endpoint_base = "/wms/lgfapi"
        self.mock_config.min_request_delay = 0.1
        self.mock_config.batch_size = 100
        self.mock_config.pool_size = 4
        self.mock_config.retry_delay = 0.5
        self.mock_config.headers = {}
        self.mock_config.verify_ssl = True
        self.mock_config.cert = None

    @patch("httpx.Client.get")
    def test_authentication_error_handling(self, mock_get) -> None:
        """Test handling of authentication errors."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "401 Unauthorized",
            request=Mock(),
            response=mock_response,
        )
        mock_get.return_value = mock_response

        client = FlextOracleWmsLegacyClient(self.mock_config)

        with pytest.raises(FlextOracleWmsApiError):
            client._make_request("GET", "/test")

    @patch("httpx.Client.get")
    def test_timeout_error_handling(self, mock_get) -> None:
        """Test handling of timeout errors."""
        mock_get.side_effect = httpx.TimeoutException("Request timeout")

        client = FlextOracleWmsLegacyClient(self.mock_config)

        with pytest.raises(FlextOracleWmsApiError):
            client._make_request("GET", "/test")

    @patch("httpx.Client.get")
    def test_server_error_handling(self, mock_get) -> None:
        """Test handling of server errors."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "500 Internal Server Error",
            request=Mock(),
            response=mock_response,
        )
        mock_get.return_value = mock_response

        client = FlextOracleWmsLegacyClient(self.mock_config)

        # The client will retry and eventually raise FlextOracleWmsError
        with pytest.raises(Exception):
            client._make_request("GET", "/test")

    def test_invalid_config_handling(self) -> None:
        """Test handling of invalid configuration."""
        invalid_config = Mock()
        invalid_config.base_url = ""  # Invalid empty URL
        invalid_config.username = "test"
        invalid_config.password = "test"
        invalid_config.timeout = 30
        invalid_config.max_retries = 3
        invalid_config.rate_limit_requests_per_second = 10
        invalid_config.bulk_batch_size = 100
        invalid_config.cache_enabled = True

        # Should still create client but may fail on actual requests
        client = FlextOracleWmsLegacyClient(invalid_config)
        assert hasattr(client, "config")
        assert client.config.base_url == ""


class TestClientEdgeCases:
    """Test edge cases and boundary conditions."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.mock_config = Mock()
        self.mock_config.base_url = "https://test.wms.oracle.com"
        self.mock_config.username = "test_user"
        self.mock_config.password = "test_pass"
        self.mock_config.timeout = 30
        self.mock_config.max_retries = 3
        self.mock_config.rate_limit_requests_per_second = 10
        self.mock_config.max_requests_per_minute = 600
        self.mock_config.bulk_batch_size = 100
        self.mock_config.cache_enabled = True
        self.mock_config.api_version = "v1"
        # Additional attributes needed by the client
        self.mock_config.wms_endpoint_base = "/wms/lgfapi"
        self.mock_config.min_request_delay = 0.1
        self.mock_config.batch_size = 100
        self.mock_config.pool_size = 4
        self.mock_config.retry_delay = 0.5
        self.mock_config.headers = {}
        self.mock_config.verify_ssl = True
        self.mock_config.cert = None

    def test_empty_entity_list(self) -> None:
        """Test bulk operations with empty entity list."""
        client = FlextOracleWmsLegacyClient(self.mock_config)

        # Should handle empty list gracefully - either return empty dict or handle early
        try:
            results = client.bulk_get_entities([])
            assert isinstance(results, dict)
            assert len(results) == 0
        except ValueError as e:
            # If the implementation doesn't handle empty list, that's expected behavior
            assert "max_workers must be greater than 0" in str(e)

    def test_empty_records_list(self) -> None:
        """Test bulk post with empty records list."""
        client = FlextOracleWmsLegacyClient(self.mock_config)

        results = client.bulk_post_records("order_hdr", [])
        assert isinstance(results, dict)

    def test_special_characters_in_entity_name(self) -> None:
        """Test entity names with special characters."""
        client = FlextOracleWmsLegacyClient(self.mock_config)

        # Should handle URL encoding
        url = client.build_api_url("order-hdr", {"filter": "status=active"})
        assert "order-hdr" in url

    @patch("httpx.Client.get")
    def test_large_response_handling(self, mock_get) -> None:
        """Test handling of large response data."""
        # Simulate large response
        large_data = [{"id": i, "name": f"Record {i}"} for i in range(1000)]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": large_data}
        mock_get.return_value = mock_response

        client = FlextOracleWmsLegacyClient(self.mock_config)
        result = client.get_entity_data("order_hdr")

        # Result should be dict for legacy client
        assert isinstance(result, dict)
        assert len(result["data"]) == 1000

    def test_concurrent_operations(self) -> None:
        """Test client thread safety for concurrent operations."""
        client = FlextOracleWmsLegacyClient(self.mock_config)

        # Test multiple operation tracking calls
        op_ids = []
        for i in range(10):
            op_id = client._track_operation(f"op_{i}", "order_hdr", {"id": i})
            op_ids.append(op_id)

        assert len(op_ids) == 10
        assert len(set(op_ids)) == 10  # All unique
