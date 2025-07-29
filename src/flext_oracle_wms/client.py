"""Enterprise Oracle WMS HTTP client with REAL Oracle WMS integration.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
Modern Python 3.13 client with flext-core type integration.
"""

from __future__ import annotations

import base64
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, Self, cast

from flext_api import FlextApiClient, create_client
from flext_core import FlextResult, get_logger

from flext_oracle_wms.constants import FlextOracleWmsDefaults, FlextOracleWmsEntityTypes

if TYPE_CHECKING:
    from collections.abc import Generator

    from flext_oracle_wms.config import (
        FlextOracleWmsModuleConfig,
        WMSAPIVersion,
        WMSRetryAttempts,
    )
    from flext_oracle_wms.constants import OracleWMSEntityType
    from flext_oracle_wms.typedefs import (
        WMSPageSize,
        WMSRecordBatch,
    )
    from flext_oracle_wms.types import (
        OracleWMSPassword,
        OracleWMSUsername,
    )
import httpx
from httpx import Auth

from flext_oracle_wms.cache import (
    FlextOracleWmsCacheManager,
)
from flext_oracle_wms.exceptions import (
    FlextOracleWmsApiError,
    FlextOracleWmsAuthenticationError,
    FlextOracleWmsError,
)
from flext_oracle_wms.flattening import FlextOracleWmsFlattener
from flext_oracle_wms.models import (
    FlextOracleWmsDiscoveryResult,
    FlextOracleWmsEntity,
    FlextOracleWmsResponse,
)

logger = get_logger(__name__)


def _raise_auth_error() -> None:
    """Raise authentication error."""
    msg = "Authentication failed"
    raise FlextOracleWmsAuthenticationError(msg)


def _raise_permission_error() -> None:
    """Raise permission error."""
    msg = "Access forbidden"
    raise PermissionError(msg)


def _handle_response_errors(response: httpx.Response) -> None:
    """Handle HTTP response errors."""
    if response.status_code == FlextOracleWmsDefaults.HTTP_UNAUTHORIZED:
        _raise_auth_error()
    if response.status_code == FlextOracleWmsDefaults.HTTP_FORBIDDEN:
        _raise_permission_error()
    if response.status_code >= FlextOracleWmsDefaults.HTTP_BAD_REQUEST:
        msg = f"HTTP {response.status_code}: {response.text}"
        raise FlextOracleWmsApiError(msg)


if TYPE_CHECKING:
    from flext_oracle_wms.config import (
        FlextOracleWmsModuleConfig,
        WMSAPIVersion,
        WMSRetryAttempts,
    )
    from flext_oracle_wms.typedefs import (
        WMSPageSize,
        WMSRecordBatch,
    )
    from flext_oracle_wms.types import (
        OracleWMSPassword,
        OracleWMSUsername,
    )
logger = get_logger(__name__)


class FlextOracleWmsAuth(Auth):
    """Oracle WMS authentication handler."""

    def __init__(
        self,
        username: OracleWMSUsername,
        password: OracleWMSPassword,
    ) -> None:
        """Initialize Oracle WMS authentication with flext-core types.

        Args:
            username: WMS username using flext-core type validation
            password: WMS password using flext-core type validation

        """
        self.username = username
        self.password = password

    def auth_flow(
        self,
        request: httpx.Request,
    ) -> Generator[httpx.Request, httpx.Response]:
        """Apply Oracle WMS authentication to request."""
        auth_header = f"Basic {_get_basic_auth(self.username, self.password)}"
        request.headers["Authorization"] = auth_header
        yield request

def _get_basic_auth(username: str, password: str) -> str:
    """Generate basic auth string."""
    credentials = f"{username}:{password}"
    return base64.b64encode(credentials.encode()).decode()


class FlextOracleWmsClient:
    """Enterprise Oracle WMS client with REAL Oracle WMS API integration.

    This client provides:
    - Real Oracle WMS API connectivity
    - Authentication handling
    - Rate limiting and retry logic
    - Connection pooling
    - Comprehensive error handling.
    """

    def __init__(self, config: FlextOracleWmsModuleConfig) -> None:
        self.config = config
        self._client: httpx.Client | None = None
        self._last_request_time = 0.0
        self._request_count = 0
        self._session_start = time.time()

        # Initialize enterprise cache manager
        cache_config = {
            "cache_ttl_seconds": getattr(config, "cache_ttl_seconds", 300),
            "max_cache_entries": getattr(config, "max_cache_size", 1000),
            "cleanup_interval_seconds": getattr(
                config,
                "cleanup_interval_seconds",
                300,
            ),
        }
        self._cache_manager = FlextOracleWmsCacheManager(cache_config)

        # Initialize operation tracking for rollback support
        self._operation_tracker: dict[str, dict[str, Any]] = {}
        self._operation_counter = 0

        # Setup logging
        if config.enable_request_logging:
            get_logger("httpx").set_level("DEBUG")
        logger.info(
            "Initialized Oracle WMS client for %s with enterprise cache",
            config.base_url,
        )

    def _create_flext_api_client(self) -> FlextResult[FlextApiClient]:
        """Create FlextApiClient with proper configuration.

        Returns:
            FlextResult containing FlextApiClient or error

        """
        try:
            config = {
                "base_url": self.config.base_url,
                "timeout": self.config.timeout_seconds,
                "headers": {
                    "Authorization": f"Basic {_get_basic_auth(
                        self.config.username, self.config.password
                    )}"
                },
            }
            client = create_client(config)
            return FlextResult.ok(client)
        except Exception as e:
            return FlextResult.fail(f"Failed to create FlextApi client: {e}")

    @property
    def client(self) -> httpx.Client:
        """Get HTTP client instance with Oracle WMS authentication."""
        if self._client is None:
            auth = httpx.BasicAuth(self.config.username, self.config.password)
            self._client = httpx.Client(
                auth=auth,
                **self.config.connection_config,
                limits=httpx.Limits(
                    max_connections=self.config.pool_size,
                    max_keepalive_connections=self.config.pool_size // 2,
                ),
            )
            logger.info(
                "Created HTTP client with connection pool size: %d",
                self.config.pool_size,
            )
        return self._client

    def _apply_rate_limiting(self) -> None:
        """Apply rate limiting to Oracle WMS requests."""
        if not self.config.enable_rate_limiting:
            return
        current_time = time.time()
        # Check requests per minute limit
        time_limit = FlextOracleWmsDefaults.REQUESTS_PER_MINUTE_LIMIT
        if current_time - self._session_start < time_limit:
            if self._request_count >= self.config.max_requests_per_minute:
                sleep_time = time_limit - (current_time - self._session_start)
                logger.warning(
                    "Rate limit reached, sleeping for %.2f seconds",
                    sleep_time,
                )
                time.sleep(sleep_time)
                self._session_start = time.time()
                self._request_count = 0
        else:
            # Reset counters after a minute
            self._session_start = current_time
            self._request_count = 0
        # Apply minimum delay between requests
        time_since_last = current_time - self._last_request_time
        if time_since_last < self.config.min_request_delay:
            sleep_time = self.config.min_request_delay - time_since_last
            time.sleep(sleep_time)
        self._last_request_time = time.time()
        self._request_count += 1

    def _log_request_details(
        self,
        method: str,
        full_url: str,
        attempt: int,
        retries: int,
        *,
        request_data: dict[str, Any] | None = None,
    ) -> None:
        """Log request details if logging is enabled."""
        if not self.config.enable_request_logging:
            return

        logger.debug(
            "Making %s request to %s (attempt %d/%d)",
            method, full_url, attempt + 1, retries + 1,
        )
        if request_data:
            logger.debug("Request data: %s", request_data)

    def _log_response_details(self, response: httpx.Response) -> None:
        """Log response details if logging is enabled."""
        if not self.config.enable_request_logging:
            return

        logger.debug("Response status: %d", response.status_code)
        logger.debug("Response headers: %s", dict(response.headers))

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        retries: WMSRetryAttempts | None = None,
    ) -> httpx.Response:
        """Make a request to Oracle WMS API with retry logic."""
        if retries is None:
            retries = cast("WMSRetryAttempts", self.config.max_retries)
        self._apply_rate_limiting()
        full_url = f"{self.config.base_url}{endpoint}"
        for attempt in range(retries + 1):
            try:
                # Combine request data for logging
                request_data = {}
                if params:
                    request_data.update({"params": params})
                if json_data:
                    request_data.update({"json": json_data})

                self._log_request_details(
                    method, full_url, attempt, retries, request_data=request_data,
                )
                response = self.client.request(
                    method=method,
                    url=full_url,
                    params=params,
                    json=json_data,
                )
                self._log_response_details(response)
                # Handle Oracle WMS specific errors
                _handle_response_errors(response)
                response.raise_for_status()
                return response
            except (httpx.TimeoutException, httpx.ConnectError) as e:
                self._handle_retryable_error(e, attempt, retries)
            except (FlextOracleWmsAuthenticationError, FlextOracleWmsApiError):
                # Don't retry authentication or API errors
                raise
            except Exception as e:
                self._handle_retryable_error(e, attempt, retries)
        msg = f"Request failed after {retries + 1} attempts"
        raise FlextOracleWmsError(msg)

    def _handle_retryable_error(
        self,
        error: Exception,
        attempt: int,
        retries: int,
    ) -> None:
        """Handle retryable errors with logging and retry logic."""
        error_type = type(error).__name__
        logger.warning(
            "%s (attempt %d/%d): %s",
            error_type,
            attempt + 1,
            retries + 1,
            error,
        )
        if attempt == retries:
            msg = f"Request failed after {retries + 1} attempts"
            raise FlextOracleWmsError(msg) from error
        time.sleep(self.config.retry_delay * (attempt + 1))

    def test_connection(self) -> bool:
        """Test connection to Oracle WMS API.

        Returns:
            True if connection successful, False otherwise

        """
        try:
            # Test with a lightweight discovery call
            self._make_request(
                "GET", 
                self.config.wms_endpoint_base, 
                retries=cast("WMSRetryAttempts", 1)
            )
            logger.info("Connection test successful")
            return True
        except Exception:
            logger.exception("Connection test failed")
            return False

    def discover_entities(self) -> FlextOracleWmsDiscoveryResult:
        """Discover available entities from Oracle WMS API.

        Returns:
            Discovery result with available entities

        """
        try:
            logger.info("Starting entity discovery from Oracle WMS API")
            response = self._make_request("GET", self.config.wms_endpoint_base)
            data = response.json()
            entities = []
            if isinstance(data, list):
                # Direct list of entities
                for entity_name in data:
                    entity = FlextOracleWmsEntity(
                        name=entity_name,
                        description=f"Oracle WMS {entity_name} entity",
                        fields={},  # Will be populated by schema discovery
                        endpoint=self.config.get_entity_endpoint(entity_name),
                    )
                    entities.append(entity)
            elif isinstance(data, dict) and "entities" in data:
                # Structured response with entities list
                for entity_info in data["entities"]:
                    if isinstance(entity_info, str):
                        entity_name = entity_info
                    else:
                        entity_name = entity_info.get("name", str(entity_info))
                    entity = FlextOracleWmsEntity(
                        name=entity_name,
                        description=entity_info.get(
                            "description",
                            f"Oracle WMS {entity_name} entity",
                        ),
                        fields=entity_info.get("fields", {}),
                        endpoint=self.config.get_entity_endpoint(entity_name),
                    )
                    entities.append(entity)
            else:
                logger.warning("Unexpected discovery response format: %s", type(data))
                # Fallback to known entities
                entities = self._get_fallback_entities()
            return FlextOracleWmsDiscoveryResult(
                entities=entities,
                total_count=len(entities),
                timestamp=datetime.now(UTC).isoformat(),
            )
        except Exception as e:
            logger.exception("Entity discovery failed")
            return FlextOracleWmsDiscoveryResult(
                entities=[],
                total_count=0,
                timestamp=datetime.now(UTC).isoformat(),
                has_errors=True,
                errors=[str(e)],
            )

    def _get_fallback_entities(self) -> list[FlextOracleWmsEntity]:
        """Get fallback entities when discovery fails."""
        return [
            FlextOracleWmsEntity(
                name="allocation",
                description="WMS allocation records",
                fields={},
                endpoint=self.config.get_entity_endpoint("allocation"),
            ),
            FlextOracleWmsEntity(
                name="order_hdr",
                description="WMS order headers",
                fields={},
                endpoint=self.config.get_entity_endpoint("order_hdr"),
            ),
            FlextOracleWmsEntity(
                name="order_dtl",
                description="WMS order details",
                fields={},
                endpoint=self.config.get_entity_endpoint("order_dtl"),
            ),
            FlextOracleWmsEntity(
                name="inventory",
                description="WMS inventory records",
                fields={},
                endpoint=self.config.get_entity_endpoint("inventory"),
            ),
        ]

    def get_entity_data_safe(
        self,
        entity_name: str,
        params: dict[str, Any] | None = None,
        page_size: int | None = None,
        *,
        enable_flattening: bool = True,
    ) -> FlextResult[FlextOracleWmsResponse]:
        """Get entity data with FlextResult error handling.

        Args:
            entity_name: Oracle WMS entity name
            params: Query parameters
            page_size: Page size for pagination
            enable_flattening: Whether to flatten nested data

        Returns:
            FlextResult containing FlextOracleWmsResponse

        """
        try:
            # Convert page_size parameter to required type
            typed_page_size: WMSPageSize | None = page_size
            response = self.get_entity_data(
                cast("OracleWMSEntityType", entity_name),
                params,
                typed_page_size,
            )

            # Apply flattening if requested
            if enable_flattening and response.records:
                flattener = FlextOracleWmsFlattener()
                flattened_records: list[dict[str, Any]] = []
                for record in response.records:
                    flattened = self._flatten_single_record(
                        record, flattener, len(flattened_records), entity_name
                    )
                    flattened_records.append(flattened)
                response.records = flattened_records

            return FlextResult.ok(response)
        except Exception as e:
            error_msg = f"Failed to get data for entity {entity_name}: {e}"
            logger.exception(error_msg)
            return FlextResult.fail(error_msg)

    def get_entity_data_with_flext_api(
        self,
        entity_name: str,
        params: dict[str, Any] | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Get entity data using FlextApi client.

        Args:
            entity_name: Oracle WMS entity name
            params: Query parameters

        Returns:
            FlextResult containing response data

        """
        # Create FlextApi client
        client_result = self._create_flext_api_client()
        if not client_result.is_success:
            return FlextResult.fail(f"Client creation failed: {client_result.error}")

        # Get validated entity name
        try:
            validated_name = self.validate_entity_name(entity_name)
        except ValueError as e:
            return FlextResult.fail(str(e))

        # Build endpoint
        endpoint = self.build_api_url(validated_name)

        # Make request using FlextApi client
        try:
            # Since FlextApi client is async, we can't use it directly in sync method
            # Use the existing _make_request for now, but properly typed
            response = self._make_request("GET", endpoint, params=params)
            data = response.json()
            if isinstance(data, dict):
                return FlextResult.ok(data)
            return FlextResult.fail("Response is not a dictionary")
        except Exception as e:
            return FlextResult.fail(f"Request failed: {e}")

    async def get_entity_data_async(
        self,
        entity_name: str,
        params: dict[str, Any] | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Get entity data using async FlextApi client.

        Args:
            entity_name: Oracle WMS entity name
            params: Query parameters

        Returns:
            FlextResult containing response data

        """
        # Create FlextApi client
        client_result = self._create_flext_api_client()
        if not client_result.is_success:
            return FlextResult.fail(f"Client creation failed: {client_result.error}")

        client = client_result.data
        if client is None:
            return FlextResult.fail("FlextApi client creation returned None")

        # Get validated entity name
        try:
            validated_name = self.validate_entity_name(entity_name)
        except ValueError as e:
            return FlextResult.fail(str(e))

        # Build endpoint
        endpoint = self.build_api_url(validated_name)

        # Make request using FlextApi client
        try:
            # Convert params to proper type for FlextApi
            api_params = dict(params) if params else {}

            response_result = await client.get(endpoint, params=api_params)
            if not response_result.is_success:
                return FlextResult.fail(f"API request failed: {response_result.error}")

            response = response_result.data
            if response is None:
                return FlextResult.fail("API response data is None")
            data = response.json()
            if isinstance(data, dict):
                return FlextResult.ok(data)
            return FlextResult.fail("Response is not a dictionary")
        except Exception as e:
            return FlextResult.fail(f"Request failed: {e}")

    def get_entity_data(
        self,
        entity_name: OracleWMSEntityType,
        params: dict[str, Any] | None = None,
        page_size: WMSPageSize | None = None,
    ) -> FlextOracleWmsResponse:
        """Get data for an Oracle WMS entity via REAL API call using flext-core types.

        Args:
            entity_name: WMS entity name using flext-core validation
            params: Optional query parameters
            page_size: WMS page size using flext-core validation
        Returns:
            WMSResponse with entity data

        """
        endpoint = self.config.get_entity_endpoint(entity_name)
        request_params = self._build_request_params(params, page_size)

        try:
            logger.info("Fetching data for entity: %s", entity_name)
            response = self._make_request("GET", endpoint, params=request_params)
            data = response.json()

            records = self._extract_records_from_response(data, entity_name)
            processed_records = self._apply_flattening_if_enabled(records, entity_name)

            return self._create_success_response(processed_records)

        except Exception:
            logger.exception("Failed to get data for entity %s", entity_name)
            return self._create_error_response()

    def _build_request_params(
        self,
        params: dict[str, Any] | None,
        page_size: WMSPageSize | None,
    ) -> dict[str, Any]:
        """Build request parameters for entity data requests."""
        request_params = self.config.get_entity_params()
        if params:
            request_params.update(params)
        if page_size:
            request_params["page_size"] = min(page_size, self.config.batch_size)
        return request_params

    def _extract_records_from_response(
        self,
        data: dict[str, Any] | list[dict[str, Any]],
        entity_name: str,
    ) -> list[dict[str, Any]]:
        """Extract records from different response formats."""
        records: list[dict[str, Any]] = []
        if isinstance(data, list):
            records = data
        elif isinstance(data, dict):
            records_data = data.get(
                "data",
                data.get("results", data.get("records", [])),
            )
            records = records_data if isinstance(records_data, list) else []
        else:
            logger.warning(
                "Unexpected response format for %s: %s",
                entity_name,
                type(data),
            )
            records = []

        logger.info(
            "Retrieved %d records for entity: %s",
            len(records),
            entity_name,
        )
        return records

    def _apply_flattening_if_enabled(
        self,
        records: list[Any],
        entity_name: str,
    ) -> list[Any]:
        """Apply flattening to records if enabled."""
        flattening_enabled = getattr(self.config, "flattening_enabled", True)
        if not flattening_enabled or not records:
            return records

        logger.info(
            "Applying dynamic flattening to %d records for entity: %s",
            len(records),
            entity_name,
        )

        flattener = self._create_flattener()
        flattened_records = self._flatten_records_batch(records, flattener, entity_name)

        logger.info(
            "✅ Successfully flattened %d records for entity: %s",
            len(flattened_records),
            entity_name,
        )
        return flattened_records

    def _create_flattener(self) -> FlextOracleWmsFlattener:
        """Create Oracle WMS flattener with standard configuration."""
        return FlextOracleWmsFlattener(
            enabled=True,
            max_depth=5,  # Oracle WMS standard depth
            separator="__",  # Oracle WMS standard separator
            preserve_empty_arrays=False,
        )

    def _flatten_records_batch(
        self,
        records: list[Any],
        flattener: FlextOracleWmsFlattener,
        entity_name: str,
    ) -> list[Any]:
        """Flatten a batch of records with error handling."""
        flattened_records = []
        for i, record in enumerate(records):
            flattened_record = self._flatten_single_record(
                record, flattener, i, entity_name,
            )
            flattened_records.append(flattened_record)
        return flattened_records

    def _flatten_single_record(
        self,
        record: dict[str, Any],
        flattener: FlextOracleWmsFlattener,
        index: int,
        entity_name: str,
    ) -> dict[str, Any]:
        """Flatten a single record with error handling."""
        if not isinstance(record, dict):
            logger.warning(
                "Record %d for entity %s is not a dict, returning empty dict",
                index, entity_name
            )
            return {}

        flatten_result = flattener.flatten_record(record)
        if not flatten_result.is_success:
            logger.warning(
                "Failed to flatten record %d for entity %s: %s",
                index,
                entity_name,
                flatten_result.error,
            )
            return record

        flattening_data = flatten_result.data
        if flattening_data is None:
            logger.warning(
                "Flattening result data is None for record %d",
                index,
            )
            return record

        flattened_record_data = flattening_data["flattened_record"]
        flattened_record: dict[str, Any] = (
            flattened_record_data if isinstance(flattened_record_data, dict) else {}
        )

        # Log first record transformation for debugging
        if index == 0:
            original_fields = len(record)
            flattened_fields = len(flattened_record)
            logger.info(
                "🔄 Flattened sample record: %d -> %d fields",
                original_fields,
                flattened_fields,
            )

        return flattened_record

    def _create_success_response(self, records: list[Any]) -> FlextOracleWmsResponse:
        """Create successful response object."""
        return FlextOracleWmsResponse(
            data=records,
            records=records,
            total_count=len(records),
            page_size=self.config.batch_size,
            has_more=len(records) == self.config.batch_size,
        )

    def _create_error_response(self) -> FlextOracleWmsResponse:
        """Create error response object."""
        return FlextOracleWmsResponse(
            data=[],
            records=[],
            total_count=0,
            page_size=self.config.batch_size,
            has_more=False,
        )

    def write_entity_data(
        self,
        entity_name: OracleWMSEntityType,
        records: WMSRecordBatch,
        write_mode: str = "insert",
    ) -> dict[str, Any]:
        """Write data to Oracle WMS entity via REAL API call using flext-core types.

        Args:
            entity_name: WMS entity name using flext-core validation
            records: WMS record batch using flext-core validation
            write_mode: Write operation mode (insert, update, upsert)

        Returns:
            Dictionary with write operation results

        """
        endpoint = self.config.get_entity_endpoint(entity_name)
        results: dict[str, Any] = {
            "total_records": len(records),
            "successful": 0,
            "failed": 0,
            "errors": [],
        }
        try:
            logger.info(
                "Writing %d records to entity: %s (mode: %s)",
                len(records),
                entity_name,
                write_mode,
            )
            for i, record in enumerate(records):
                try:
                    # Track operation for potential rollback
                    original_data = None

                    # For updates, try to get original data first
                    if write_mode == "update" and "id" in record:
                        try:
                            get_endpoint = f"{endpoint}/{record['id']}"
                            get_response = self._make_request("GET", get_endpoint)
                            if (
                                get_response.status_code
                                == FlextOracleWmsDefaults.HTTP_OK
                            ):
                                original_data = get_response.json()
                        except Exception as e:
                            logger.warning(
                                "Could not fetch original data for record %s: %s",
                                record.get("id"),
                                e,
                            )

                    # Track the operation
                    operation_id = self._track_operation(
                        write_mode,
                        entity_name,
                        record,
                        original_data,
                    )

                    method = "POST" if write_mode == "insert" else "PUT"
                    response = self._make_request(method, endpoint, json_data=record)

                    if response.status_code in {200, 201, 204}:
                        results["successful"] += 1
                        # Mark operation as successful
                        result_data = response.json() if response.content else None
                        self._mark_operation_success(operation_id, result_data)
                    else:
                        results["failed"] += 1
                        error_msg = f"HTTP {response.status_code}: {response.text}"
                        results["errors"].append(
                            {
                                "record_index": i,
                                "error": error_msg,
                            },
                        )
                        # Mark operation as failed
                        self._mark_operation_failed(operation_id, error_msg)

                except Exception as e:
                    results["failed"] += 1
                    error_msg = str(e)
                    results["errors"].append({"record_index": i, "error": error_msg})
                    # Mark operation as failed if tracking was started
                    if "operation_id" in locals():
                        self._mark_operation_failed(operation_id, error_msg)
            logger.info(
                "Write operation completed: %d successful, %d failed",
                results["successful"],
                results["failed"],
            )
            return results
        except Exception as e:
            logger.exception("Write operation failed for entity %s", entity_name)
            # Return error results dict for write operation
            return {
                "total_records": len(records),
                "successful": 0,
                "failed": len(records),
                "errors": [{"error": f"Write operation failed: {e}"}],
            }

    def close(self) -> None:
        """Close the HTTP client connection."""
        if self._client:
            self._client.close()
            self._client = None
            logger.info("Oracle WMS client connection closed")

    def __enter__(self) -> Self:
        """Context manager entry."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Context manager exit."""
        self.close()

    # ==============================================================================
    # ULTRA-MODERN FLEXT-CORE INTEGRATION METHODS - Python 3.13 Enhanced
    # ==============================================================================
    def get_entity_metadata(self, entity_name: OracleWMSEntityType) -> dict[str, Any]:
        """Get Oracle WMS entity metadata using flext-core types.

        Args:
            entity_name: WMS entity name using flext-core validation
        Returns:
            Entity metadata dictionary

        """
        endpoint = f"{self.config.wms_endpoint_base}/{entity_name}/metadata"
        try:
            logger.info("Fetching metadata for entity: %s", entity_name)
            response = self._make_request("GET", endpoint)
            metadata_raw = response.json()
            # Ensure we return a dict[str, Any]
            if isinstance(metadata_raw, dict):
                metadata: dict[str, Any] = metadata_raw
            else:
                metadata = {
                    "error": "Invalid metadata format",
                    "raw_data": metadata_raw,
                }
            logger.info("Retrieved metadata for entity: %s", entity_name)
            return metadata
        except Exception:
            logger.exception("Failed to get metadata for entity %s", entity_name)
            # Return fallback metadata
            return {
                "entity_name": entity_name,
                "fields": {
                    "id": {"type": "integer", "primary_key": True},
                    "mod_ts": {"type": "string", "format": "date-time"},
                },
                "primary_key": ["id"],
                "replication_key": "mod_ts",
            }

    def validate_entity_name(self, entity_name: str) -> OracleWMSEntityType:
        """Validate entity name using flext-core types.

        Args:
            entity_name: Entity name to validate
        Returns:
            Validated WMS entity name
        Raises:
            ValueError: If entity name is invalid

        """
        # Check if entity name is valid
        if entity_name not in FlextOracleWmsEntityTypes.ALL_ENTITIES:
            msg = (
                f"Invalid entity name: {entity_name}. "
                f"Must be one of: {FlextOracleWmsEntityTypes.ALL_ENTITIES}"
            )
            raise ValueError(msg)

        # Safe to cast after validation since we've confirmed it's a valid literal value
        validated_name = cast("OracleWMSEntityType", entity_name)
        logger.debug("Validated entity name: %s", validated_name)
        return validated_name

    def build_api_url(
        self,
        entity_name: OracleWMSEntityType,
        api_version: WMSAPIVersion | None = None,
    ) -> str:
        """Build complete API URL using flext-core types.

        Args:
            entity_name: WMS entity name using flext-core validation
            api_version: WMS API version using flext-core validation
        Returns:
            Complete API URL for the entity

        """
        version = api_version or self.config.api_version
        url = f"{self.config.base_url}/wms/lgfapi/{version}/entity/{entity_name}"
        logger.debug("Built API URL for %s: %s", entity_name, url)
        return url

    def get_connection_info(self) -> dict[str, Any]:
        """Get connection information with flext-core type validation.

        Returns:
            Dictionary with connection details

        """
        return {
            "base_url": self.config.base_url,
            "api_version": self.config.api_version,
            "auth_method": "basic",  # Oracle WMS uses basic authentication
            "username": self.config.username,
            "timeout": self.config.timeout_seconds,
            "max_retries": self.config.max_retries,
            "page_size": self.config.batch_size,
            "client_active": self._client is not None,
        }

    # Bulk operations for legacy client compatibility
    def bulk_get_entities(
        self,
        entity_names: list[str],
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Get data for multiple Oracle WMS entities in batch with real parallelization.

        Args:
            entity_names: List of entity names to retrieve
            params: Common query parameters for all entities

        Returns:
            Dictionary with entity data results

        """
        # Use real parallel processing with connection pooling
        max_workers = min(len(entity_names), self.config.pool_size)
        results: dict[str, Any] = {}
        failed_entities: list[str] = []

        def fetch_entity(entity_name: str) -> tuple[str, Any]:
            """Fetch single entity data with error handling."""
            try:
                # Validate entity name first
                validated_name = self.validate_entity_name(entity_name)
                entity_data = self.get_entity_data(validated_name, params or {})
                # Convert WMSResponse to dict format for compatibility
                if hasattr(entity_data, "data") and entity_data.data is not None:
                    return entity_name, entity_data.data
                if hasattr(entity_data, "records") and entity_data.records is not None:
                    return entity_name, entity_data.records
                return entity_name, []
            except Exception as e:
                logger.warning("Failed to get entity %s: %s", entity_name, e)
                return entity_name, None

        # Execute parallel requests using thread pool
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_entity = {
                executor.submit(fetch_entity, entity_name): entity_name
                for entity_name in entity_names
            }

            # Collect results as they complete
            for future in as_completed(future_to_entity):
                entity_name = future_to_entity[future]
                try:
                    name, data = future.result()
                    if data is not None:
                        results[name] = data
                    else:
                        failed_entities.append(name)
                except Exception:
                    logger.exception("Failed to process entity %s", entity_name)
                    failed_entities.append(entity_name)

        logger.info(
            "Bulk get completed: %d successful, %d failed out of %d entities",
            len(results),
            len(failed_entities),
            len(entity_names),
        )

        return {
            "data": results,
            "partial_success": len(failed_entities) > 0,
            "failed_entities": failed_entities,
            "total_requested": len(entity_names),
            "successful_count": len(results),
            "failed_count": len(failed_entities),
        }

    def bulk_post_records(
        self,
        entity_name: str,
        records: list[dict[str, Any]],
        batch_size: int | None = None,
    ) -> dict[str, Any]:
        """Post multiple records to Oracle WMS entity in batches (legacy compatibility).

        Args:
            entity_name: Target entity name
            records: List of records to post
            batch_size: Number of records per batch

        Returns:
            Dictionary with batch operation results

        """
        try:
            validated_name = self.validate_entity_name(entity_name)
            batch_config = self._prepare_bulk_operation_config(records, batch_size)
            batches = self._create_record_batches(records, batch_config["batch_size"])

            results = self._initialize_bulk_results(records)
            return self._execute_bulk_post_batches(
                validated_name, batches, batch_config["max_workers"], results,
            )

        except ValueError as e:
            return self._create_bulk_error_response(e, records)

    def _prepare_bulk_operation_config(
        self,
        records: list[dict[str, Any]],
        batch_size: int | None,
    ) -> dict[str, Any]:
        """Prepare configuration for bulk operations."""
        batch_size_value = batch_size or self.config.batch_size
        max_workers = min(
            max(1, len(records) // batch_size_value),
            self.config.pool_size,
        )
        return {
            "batch_size": batch_size_value,
            "max_workers": max_workers,
        }

    def _create_record_batches(
        self,
        records: list[dict[str, Any]],
        batch_size: int,
    ) -> list[list[dict[str, Any]]]:
        """Create batches from records list."""
        return [
            records[i : i + batch_size]
            for i in range(0, len(records), batch_size)
        ]

    def _initialize_bulk_results(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        """Initialize results structure for bulk operations."""
        return {
            "total_records": len(records),
            "successful_batches": 0,
            "failed_batches": 0,
            "batch_results": [],
            "successful_records": [],
            "failed_records": [],
        }

    def _execute_bulk_post_batches(
        self,
        entity_name: str,
        batches: list[list[dict[str, Any]]],
        max_workers: int,
        results: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute bulk post operations with parallel processing."""
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_batch = {
                executor.submit(self._process_post_batch, entity_name, i, batch): i
                for i, batch in enumerate(batches)
            }

            self._collect_bulk_post_results(future_to_batch, results)

        logger.info(
            "Bulk post completed: %d batches successful, %d failed",
            results["successful_batches"],
            results["failed_batches"],
        )
        return results

    def _process_post_batch(
        self,
        entity_name: str,
        batch_index: int,
        batch: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Process a single batch for posting."""
        batch_result = {
            "batch_index": batch_index,
            "batch_size": len(batch),
            "successful": 0,
            "failed": 0,
            "errors": [],
        }

        try:
            write_result = self.write_entity_data(
                cast("OracleWMSEntityType", entity_name), batch, "insert"
            )
            batch_result.update(write_result)
            logger.debug(
                "Batch %d completed: %d successful, %d failed",
                batch_index,
                batch_result["successful"],
                batch_result["failed"],
            )
        except Exception as e:
            batch_result["failed"] = len(batch)
            errors_list = batch_result["errors"]
            if isinstance(errors_list, list):
                errors_list.append(f"Batch processing failed: {e}")
            logger.exception("Batch %d failed completely", batch_index)

        return batch_result

    def _collect_bulk_post_results(
        self,
        future_to_batch: dict[Any, int],
        results: dict[str, Any],
    ) -> None:
        """Collect results from parallel batch processing."""
        for future in as_completed(future_to_batch):
            batch_index = future_to_batch[future]
            try:
                batch_result = future.result()

                batch_results_list = results["batch_results"]
                if isinstance(batch_results_list, list):
                    batch_results_list.append(batch_result)

                self._update_batch_counters(results, batch_result)

            except Exception:
                logger.exception("Failed to process batch %d result", batch_index)
                self._increment_failed_batches(results)

    def _update_batch_counters(
        self,
        results: dict[str, Any],
        batch_result: dict[str, Any],
    ) -> None:
        """Update success/failure counters for batches."""
        if batch_result["successful"] > 0:
            current_successful = results["successful_batches"]
            if isinstance(current_successful, int):
                results["successful_batches"] = current_successful + 1

        if batch_result["failed"] > 0:
            self._increment_failed_batches(results)

    def _increment_failed_batches(self, results: dict[str, Any]) -> None:
        """Increment failed batches counter."""
        current_failed = results["failed_batches"]
        if isinstance(current_failed, int):
            results["failed_batches"] = current_failed + 1

    def _create_bulk_error_response(
        self,
        error: Exception,
        records: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Create error response for bulk operations."""
        return {
            "error": str(error),
            "total_records": len(records),
            "successful_batches": 0,
        }

    def bulk_update_records(
        self,
        entity_name: str,
        records: list[dict[str, Any]],
        id_field: str = "id",
        batch_size: int | None = None,
    ) -> dict[str, Any]:
        """Update multiple records in Oracle WMS entity in batches.

        Legacy compatibility method.

        Args:
            entity_name: Target entity name
            records: List of records to update
            id_field: Name of the ID field for updates
            batch_size: Number of records per batch

        Returns:
            Dictionary with batch update results

        """
        try:
            validated_name = self.validate_entity_name(entity_name)

            # Validate records have required ID field
            validation_result = self._validate_update_records(records, id_field)
            if validation_result["has_errors"]:
                error_response = validation_result["error_response"]
                return error_response if isinstance(error_response, dict) else {}

            batch_config = self._prepare_bulk_operation_config(records, batch_size)
            batches = self._create_record_batches(records, batch_config["batch_size"])

            results = self._initialize_bulk_update_results(records)
            return self._execute_bulk_update_batches(
                validated_name, batches, batch_config["max_workers"], results,
            )

        except ValueError as e:
            return self._create_bulk_update_error_response(e, records)

    def _validate_update_records(
        self,
        records: list[dict[str, Any]],
        id_field: str,
    ) -> dict[str, Any]:
        """Validate that all records have required ID field."""
        invalid_records = []
        for i, record in enumerate(records):
            if id_field not in record:
                invalid_records.append(
                    f"Record {i} missing required ID field '{id_field}'",
                )

        if invalid_records:
            return {
                "has_errors": True,
                "error_response": {
                    "error": (
                        f"Validation failed: {len(invalid_records)} "
                        "records missing ID field"
                    ),
                    "total_records": len(records),
                    "successful_updates": 0,
                    "validation_errors": invalid_records,
                },
            }

        return {"has_errors": False}

    def _initialize_bulk_update_results(
        self,
        records: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Initialize results structure for bulk update operations."""
        return {
            "total_records": len(records),
            "successful_updates": 0,
            "failed_updates": 0,
            "batch_results": [],
            "validation_errors": [],
        }

    def _execute_bulk_update_batches(
        self,
        entity_name: str,
        batches: list[list[dict[str, Any]]],
        max_workers: int,
        results: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute bulk update operations with parallel processing."""
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_batch = {
                executor.submit(self._process_update_batch, entity_name, i, batch): i
                for i, batch in enumerate(batches)
            }

            self._collect_bulk_update_results(future_to_batch, results, batches)

        logger.info(
            "Bulk update completed: %d successful, %d failed out of %d records",
            results["successful_updates"],
            results["failed_updates"],
            results["total_records"],
        )
        return results

    def _process_update_batch(
        self,
        entity_name: str,
        batch_index: int,
        batch: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Process a single batch for updating."""
        batch_result = {
            "batch_index": batch_index,
            "batch_size": len(batch),
            "successful": 0,
            "failed": 0,
            "errors": [],
        }

        try:
            write_result = self.write_entity_data(
                cast("OracleWMSEntityType", entity_name), batch, "update"
            )
            batch_result.update(write_result)
            logger.debug(
                "Update batch %d completed: %d successful, %d failed",
                batch_index,
                batch_result["successful"],
                batch_result["failed"],
            )
        except Exception as e:
            batch_result["failed"] = len(batch)
            errors_list = batch_result["errors"]
            if isinstance(errors_list, list):
                errors_list.append(f"Batch update failed: {e}")
            logger.exception("Update batch %d failed completely", batch_index)

        return batch_result

    def _collect_bulk_update_results(
        self,
        future_to_batch: dict[Any, int],
        results: dict[str, Any],
        batches: list[list[dict[str, Any]]],
    ) -> None:
        """Collect results from parallel update batch processing."""
        for future in as_completed(future_to_batch):
            batch_index = future_to_batch[future]
            try:
                batch_result = future.result()

                batch_results_list = results["batch_results"]
                if isinstance(batch_results_list, list):
                    batch_results_list.append(batch_result)

                self._accumulate_update_counters(results, batch_result)

            except Exception:
                logger.exception("Failed to process update batch %d result", batch_index)
                self._handle_failed_update_batch(results, batches, batch_index)

    def _accumulate_update_counters(
        self,
        results: dict[str, Any],
        batch_result: dict[str, Any],
    ) -> None:
        """Accumulate successful and failed update counters."""
        successful_count = batch_result.get("successful", 0)
        failed_count = batch_result.get("failed", 0)
        current_successful = results["successful_updates"]
        current_failed = results["failed_updates"]

        if isinstance(current_successful, int) and isinstance(successful_count, int):
            results["successful_updates"] = current_successful + successful_count

        if isinstance(current_failed, int) and isinstance(failed_count, int):
            results["failed_updates"] = current_failed + failed_count

    def _handle_failed_update_batch(
        self,
        results: dict[str, Any],
        batches: list[list[dict[str, Any]]],
        batch_index: int,
    ) -> None:
        """Handle failed update batch by adding entire batch as failed."""
        current_failed = results["failed_updates"]
        if isinstance(current_failed, int):
            batch_size = (
                len(batches[batch_index])
                if batch_index < len(batches)
                else self.config.batch_size
            )
            results["failed_updates"] = current_failed + batch_size

    def _create_bulk_update_error_response(
        self,
        error: Exception,
        records: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Create error response for bulk update operations."""
        return {
            "error": str(error),
            "total_records": len(records),
            "successful_updates": 0,
        }

    def validate_bulk_operations_integration(self) -> dict[str, Any]:
        """Validate that bulk operations can integrate with existing methods.

        This method performs a comprehensive check of the legacy client methods
        that bulk operations depend on, ensuring they work correctly.

        Returns:
            Dictionary with validation results

        """
        validation_results = self._initialize_validation_results()

        try:
            self._validate_client_and_config(validation_results)
            self._validate_method_availability(validation_results)
            self._validate_entity_operations(validation_results)
            self._validate_connection(validation_results)
            self._validate_configuration_consistency(validation_results)
            self._determine_overall_status(validation_results)

            logger.info(
                "Bulk operations integration validation completed: %s",
                validation_results["overall_status"],
            )
            return validation_results

        except Exception as e:
            validation_results["errors"].append(f"Validation process failed: {e}")
            validation_results["overall_status"] = "error"
            logger.exception("Integration validation failed")
            return validation_results

    def _initialize_validation_results(self) -> dict[str, Any]:
        """Initialize the validation results structure."""
        return {
            "timestamp": datetime.now(UTC).isoformat(),
            "client_status": "unknown",
            "config_validation": False,
            "method_availability": {},
            "entity_validation": {},
            "connection_test": False,
            "overall_status": "failed",
            "errors": [],
            "warnings": [],
        }

    def _validate_client_and_config(self, validation_results: dict[str, Any]) -> None:
        """Validate client and basic configuration."""
        validation_results["client_status"] = (
            "active" if self._client is not None else "inactive"
        )
        validation_results["config_validation"] = (
            hasattr(self.config, "base_url") and hasattr(self.config, "pool_size")
        )

    def _validate_method_availability(self, validation_results: dict[str, Any]) -> None:
        """Validate that required methods are available."""
        required_methods = [
            "validate_entity_name",
            "get_entity_data",
            "write_entity_data",
            "_make_request",
            "get_connection_info",
        ]

        for method_name in required_methods:
            method_exists = hasattr(self, method_name) and callable(
                getattr(self, method_name),
            )
            validation_results["method_availability"][method_name] = method_exists
            if not method_exists:
                validation_results["errors"].append(
                    f"Required method {method_name} not available",
                )

    def _validate_entity_operations(self, validation_results: dict[str, Any]) -> None:
        """Validate entity operations with known entities."""
        test_entities = ["allocation", "order_hdr", "inventory"]
        for entity in test_entities:
            try:
                validated = self.validate_entity_name(entity)
                validation_results["entity_validation"][entity] = (validated == entity)
            except Exception as e:
                validation_results["entity_validation"][entity] = False
                validation_results["warnings"].append(
                    f"Entity validation failed for {entity}: {e}",
                )

    def _validate_connection(self, validation_results: dict[str, Any]) -> None:
        """Validate connection status."""
        try:
            connection_test = self.test_connection()
            validation_results["connection_test"] = connection_test
            if not connection_test:
                validation_results["warnings"].append(
                    "Connection test failed - bulk operations may fail",
                )
        except Exception as e:
            validation_results["connection_test"] = False
            validation_results["errors"].append(f"Connection test error: {e}")

    def _validate_configuration_consistency(self, validation_results: dict[str, Any]) -> None:
        """Validate configuration consistency."""
        config_issues = []
        if not hasattr(self.config, "batch_size") or self.config.batch_size <= 0:
            config_issues.append("Invalid batch_size configuration")
        if not hasattr(self.config, "pool_size") or self.config.pool_size <= 0:
            config_issues.append("Invalid pool_size configuration")

        if config_issues:
            validation_results["errors"].extend(config_issues)

    def _determine_overall_status(self, validation_results: dict[str, Any]) -> None:
        """Determine the overall validation status."""
        all_methods_available = all(validation_results["method_availability"].values())
        config_valid = validation_results["config_validation"]
        some_entities_valid = any(validation_results["entity_validation"].values())

        if all_methods_available and config_valid and some_entities_valid:
            validation_results["overall_status"] = (
                "ready" if validation_results["connection_test"] else "ready_offline"
            )
        elif all_methods_available and config_valid:
            validation_results["overall_status"] = "partial"
        else:
            validation_results["overall_status"] = "failed"

    def _get_cached_entity_data(
        self,
        entity_name: str,
        params: dict[str, Any] | None = None,
    ) -> tuple[bool, Any]:
        """Get cached entity data if available using enterprise cache manager.

        Args:
            entity_name: Entity name
            params: Query parameters

        Returns:
            Tuple of (cache_hit, data)

        """
        # Create cache key from entity name and params

        params_str = str(sorted((params or {}).items()))
        cache_key = (
            f"entity_{entity_name}_"
            f"{hashlib.sha256(params_str.encode()).hexdigest()[:8]}"
        )

        # Try to get from enterprise cache if caching is enabled
        cache_enabled = getattr(self.config, "enable_cache", False)
        if not cache_enabled:
            return False, None

        # Use enterprise cache manager
        cached_data = self._cache_manager.flext_oracle_wms_get_entity(cache_key)
        if cached_data is not None:
            logger.debug("Enterprise cache hit for entity %s", entity_name)
            return True, cached_data

        return False, None

    def _cache_entity_data(
        self,
        entity_name: str,
        params: dict[str, Any] | None,
        data: object,
    ) -> None:
        """Cache entity data using enterprise cache manager.

        Args:
            entity_name: Entity name
            params: Query parameters
            data: Data to cache

        """
        cache_enabled = getattr(self.config, "enable_cache", False)
        if not cache_enabled:
            return

        params_str = str(sorted((params or {}).items()))
        cache_key = (
            f"entity_{entity_name}_"
            f"{hashlib.sha256(params_str.encode()).hexdigest()[:8]}"
        )

        # Use enterprise cache manager
        cache_ttl = getattr(self.config, "cache_ttl_seconds", 300)
        success = self._cache_manager.flext_oracle_wms_set_entity(
            cache_key,
            data,
            cache_ttl,
        )
        if success:
            logger.debug("Enterprise cached data for entity %s", entity_name)
        else:
            logger.warning("Failed to cache data for entity %s", entity_name)

    def get_bulk_cache_stats(self) -> dict[str, Any]:
        """Get cache statistics for bulk operations using enterprise cache manager.

        Returns:
            Dictionary with cache statistics

        """
        # Get comprehensive stats from enterprise cache manager
        enterprise_stats = self._cache_manager.flext_oracle_wms_get_stats()

        # Add configuration information
        return {
            "cache_enabled": getattr(self.config, "enable_cache", False),
            "enterprise_cache": True,
            **enterprise_stats,
        }

    def clear_bulk_cache(self) -> bool:
        """Clear the bulk operations cache using enterprise cache manager.

        Returns:
            True if cache was cleared, False if no cache exists

        """
        # Use enterprise cache manager to clear all caches
        success = self._cache_manager.flext_oracle_wms_clear_all()
        if success:
            logger.info("Cleared enterprise bulk operations cache")
        else:
            logger.warning("Failed to clear enterprise cache")
        return success

    def _track_operation(
        self,
        operation_type: str,
        entity_name: str,
        operation_data: dict[str, Any],
        original_data: dict[str, Any] | None = None,
    ) -> str:
        """Track operation for potential rollback.

        Args:
            operation_type: Type of operation ('insert', 'update', 'delete')
            entity_name: Target entity name
            operation_data: Data used in operation
            original_data: Original data before operation (for updates)

        Returns:
            Operation ID for tracking

        """
        self._operation_counter += 1
        operation_id = (
            f"{operation_type}_{entity_name}_{self._operation_counter}_"
            f"{int(time.time())}"
        )

        tracking_info = {
            "operation_id": operation_id,
            "operation_type": operation_type,
            "entity_name": entity_name,
            "operation_data": operation_data,
            "original_data": original_data,
            "timestamp": datetime.now(UTC).isoformat(),
            "status": "pending",
        }

        self._operation_tracker[operation_id] = tracking_info
        logger.debug("Tracking operation %s for entity %s", operation_id, entity_name)
        return operation_id

    def _mark_operation_success(
        self,
        operation_id: str,
        result_data: dict[str, Any] | None = None,
    ) -> None:
        """Mark operation as successful."""
        if operation_id in self._operation_tracker:
            self._operation_tracker[operation_id]["status"] = "success"
            if result_data:
                self._operation_tracker[operation_id]["result_data"] = result_data
            logger.debug("Marked operation %s as successful", operation_id)

    def _mark_operation_failed(self, operation_id: str, error: str) -> None:
        """Mark operation as failed."""
        if operation_id in self._operation_tracker:
            self._operation_tracker[operation_id]["status"] = "failed"
            self._operation_tracker[operation_id]["error"] = error
            logger.debug("Marked operation %s as failed: %s", operation_id, error)

    def _get_successful_operations(
        self,
        entity_name: str,
        operation_type: str,
    ) -> list[dict[str, Any]]:
        """Get successful operations for potential rollback."""
        return [
            tracking_info
            for tracking_info in self._operation_tracker.values()
            if (
                tracking_info["entity_name"] == entity_name
                and tracking_info["operation_type"] == operation_type
                and tracking_info["status"] == "success"
            )
        ]

    def bulk_rollback_batch_operation(
        self,
        entity_name: str,
        successful_operations: list[dict[str, Any]],
        operation_type: str = "insert",
    ) -> dict[str, Any]:
        """Rollback successful operations in case of partial batch failure.

        Args:
            entity_name: Target entity name
            successful_operations: List of operations that succeeded and need rollback
            operation_type: Type of operation to rollback ('insert', 'update', 'delete')

        Returns:
            Dictionary with rollback results

        """
        rollback_results = self._initialize_rollback_results(
            successful_operations, operation_type,
        )

        try:
            validated_name = self.validate_entity_name(entity_name)
            rollback_config = self._determine_rollback_strategy(operation_type)

            if "error" in rollback_config:
                rollback_results["rollback_errors"].append(rollback_config["error"])
                return rollback_results

            self._execute_rollback_operations(
                successful_operations,
                validated_name,
                rollback_config,
                rollback_results,
            )

            logger.info(
                "Rollback completed: %d successful, %d failed out of %d operations",
                rollback_results["successful_rollbacks"],
                rollback_results["failed_rollbacks"],
                rollback_results["total_rollbacks"],
            )
            return rollback_results

        except Exception as e:
            rollback_results["failed_rollbacks"] = len(successful_operations)
            rollback_results["rollback_errors"].append(f"Rollback process failed: {e}")
            logger.exception("Bulk rollback operation failed")
            return rollback_results

    def _initialize_rollback_results(
        self,
        successful_operations: list[dict[str, Any]],
        operation_type: str,
    ) -> dict[str, Any]:
        """Initialize rollback results structure."""
        return {
            "total_rollbacks": len(successful_operations),
            "successful_rollbacks": 0,
            "failed_rollbacks": 0,
            "rollback_errors": [],
            "rollback_type": operation_type,
        }

    def _determine_rollback_strategy(self, operation_type: str) -> dict[str, str]:
        """Determine rollback strategy based on operation type."""
        if operation_type == "insert":
            return {"rollback_operation": "delete", "id_field": "id"}
        if operation_type == "update":
            return {"rollback_operation": "restore", "id_field": "id"}
        if operation_type == "delete":
            return {"rollback_operation": "recreate", "id_field": "id"}
        return {"error": f"Unknown operation type: {operation_type}"}

    def _execute_rollback_operations(
        self,
        successful_operations: list[dict[str, Any]],
        validated_name: str,
        rollback_config: dict[str, str],
        rollback_results: dict[str, Any],
    ) -> None:
        """Execute rollback operations for all successful operations."""
        rollback_operation = rollback_config["rollback_operation"]
        id_field = rollback_config["id_field"]

        for operation in successful_operations:
            try:
                self._execute_single_rollback(
                    operation, validated_name, rollback_operation, id_field, rollback_results,
                )
            except Exception as e:
                rollback_results["failed_rollbacks"] += 1
                rollback_results["rollback_errors"].append(
                    f"Rollback failed for {operation}: {e}",
                )
                logger.exception("Rollback failed for operation %s", operation)

    def _execute_single_rollback(
        self,
        operation: dict[str, Any],
        validated_name: str,
        rollback_operation: str,
        id_field: str,
        rollback_results: dict[str, Any],
    ) -> None:
        """Execute a single rollback operation."""
        if rollback_operation == "delete":
            self._rollback_insert_operation(
                operation, validated_name, id_field, rollback_results,
            )
        elif rollback_operation == "restore":
            self._rollback_update_operation(
                operation, validated_name, id_field, rollback_results,
            )
        elif rollback_operation == "recreate":
            self._rollback_delete_operation(
                operation, validated_name, rollback_results,
            )
        else:
            rollback_results["failed_rollbacks"] += 1
            rollback_results["rollback_errors"].append(
                f"Cannot rollback {rollback_operation} operation: {operation}",
            )

    def _rollback_insert_operation(
        self,
        operation: dict[str, Any],
        validated_name: str,
        id_field: str,
        rollback_results: dict[str, Any],
    ) -> None:
        """Rollback insert by deleting created record."""
        if id_field in operation:
            record_id = operation[id_field]
            endpoint = self._build_record_endpoint(validated_name, record_id)

            response = self.client.delete(endpoint)
            response.raise_for_status()

            rollback_results["successful_rollbacks"] += 1
            logger.debug("Rolled back insert operation for record %s", record_id)
        else:
            self._handle_rollback_failure(
                rollback_results, f"Missing {id_field} in operation: {operation}",
            )

    def _rollback_update_operation(
        self,
        operation: dict[str, Any],
        validated_name: str,
        id_field: str,
        rollback_results: dict[str, Any],
    ) -> None:
        """Rollback update by restoring original values."""
        if "original_data" in operation:
            original_data = operation["original_data"]
            if original_data and id_field in original_data:
                record_id = original_data[id_field]
                endpoint = self._build_record_endpoint(validated_name, record_id)

                response = self.client.put(endpoint, json=original_data)
                response.raise_for_status()

                rollback_results["successful_rollbacks"] += 1
                logger.debug("Restored original data for record %s", record_id)
            else:
                self._handle_rollback_failure(
                    rollback_results, f"Missing original data for update rollback: {operation}",
                )
        else:
            self._handle_rollback_failure(
                rollback_results, f"Missing original_data in operation: {operation}",
            )

    def _rollback_delete_operation(
        self,
        operation: dict[str, Any],
        validated_name: str,
        rollback_results: dict[str, Any],
    ) -> None:
        """Rollback delete by recreating the record."""
        if "operation_data" in operation:
            recreate_data = operation["operation_data"]
            endpoint = self._build_entity_endpoint(validated_name)

            response = self.client.post(endpoint, json=recreate_data)
            response.raise_for_status()

            rollback_results["successful_rollbacks"] += 1
            logger.debug("Recreated deleted record for entity %s", validated_name)
        else:
            self._handle_rollback_failure(
                rollback_results, f"Missing operation_data for recreate: {operation}",
            )

    def _build_record_endpoint(self, entity_name: str, record_id: str) -> str:
        """Build endpoint for specific record operations."""
        api_version = getattr(self.config, "api_version", "v10")
        return f"/wms/lgfapi/{api_version}/entity/{entity_name}/{record_id}"

    def _build_entity_endpoint(self, entity_name: str) -> str:
        """Build endpoint for entity operations."""
        api_version = getattr(self.config, "api_version", "v10")
        return f"/wms/lgfapi/{api_version}/entity/{entity_name}"

    def _handle_rollback_failure(
        self,
        rollback_results: dict[str, Any],
        error_message: str,
    ) -> None:
        """Handle rollback failure by updating results."""
        rollback_results["failed_rollbacks"] += 1
        rollback_results["rollback_errors"].append(error_message)

    def bulk_rollback_tracked_operations(
        self,
        entity_name: str,
        operation_type: str = "insert",
    ) -> dict[str, Any]:
        """Rollback all successful tracked operations for an entity.

        Args:
            entity_name: Target entity name
            operation_type: Type of operation to rollback

        Returns:
            Dictionary with rollback results

        """
        # Get successful operations from tracker
        successful_operations = self._get_successful_operations(
            entity_name,
            operation_type,
        )

        if not successful_operations:
            return {
                "total_rollbacks": 0,
                "successful_rollbacks": 0,
                "failed_rollbacks": 0,
                "rollback_errors": [],
                "rollback_type": operation_type,
                "message": (
                    f"No successful {operation_type} operations found for entity "
                    f"{entity_name}"
                ),
            }

        # Use the enhanced rollback mechanism
        return self.bulk_rollback_batch_operation(
            entity_name,
            successful_operations,
            operation_type,
        )

    def clear_operation_tracking(self, entity_name: str | None = None) -> int:
        """Clear operation tracking data.

        Args:
            entity_name: Specific entity to clear, or None for all

        Returns:
            Number of operations cleared

        """
        cleared_count = 0

        if entity_name is None:
            # Clear all tracking
            cleared_count = len(self._operation_tracker)
            self._operation_tracker.clear()
            self._operation_counter = 0
            logger.info("Cleared all operation tracking (%d operations)", cleared_count)
        else:
            # Clear tracking for specific entity
            to_remove = []
            for op_id, tracking_info in self._operation_tracker.items():
                if tracking_info["entity_name"] == entity_name:
                    to_remove.append(op_id)

            for op_id in to_remove:
                del self._operation_tracker[op_id]
                cleared_count += 1

            logger.info(
                "Cleared operation tracking for entity %s (%d operations)",
                entity_name,
                cleared_count,
            )

        return cleared_count

    def get_operation_tracking_stats(self) -> dict[str, Any]:
        """Get operation tracking statistics.

        Returns:
            Dictionary with tracking statistics

        """
        stats: dict[str, Any] = {
            "total_operations": len(self._operation_tracker),
            "by_status": {"pending": 0, "success": 0, "failed": 0},
            "by_type": {},
            "by_entity": {},
            "oldest_operation": None,
            "newest_operation": None,
        }

        timestamps = []

        for tracking_info in self._operation_tracker.values():
            # Count by status
            status = tracking_info["status"]
            by_status = stats["by_status"]
            if isinstance(by_status, dict):
                by_status[status] = by_status.get(status, 0) + 1

            # Count by operation type
            op_type = tracking_info["operation_type"]
            by_type = stats["by_type"]
            if isinstance(by_type, dict):
                by_type[op_type] = by_type.get(op_type, 0) + 1

            # Count by entity
            entity = tracking_info["entity_name"]
            by_entity = stats["by_entity"]
            if isinstance(by_entity, dict):
                by_entity[entity] = by_entity.get(entity, 0) + 1

            # Track timestamps
            timestamps.append(tracking_info["timestamp"])

        if timestamps:
            timestamps.sort()
            stats["oldest_operation"] = timestamps[0]
            stats["newest_operation"] = timestamps[-1]

        return stats
