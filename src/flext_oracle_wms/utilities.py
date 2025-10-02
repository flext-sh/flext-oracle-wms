"""FlextOracleWmsUtilities - Oracle WMS Domain Utilities.

This module provides comprehensive utilities for Oracle Warehouse Management System (WMS)
operations, extending FlextUtilities with domain-specific nested classes for warehouse
management, inventory operations, authentication, and data validation.

All utilities use Python 3.13+ syntax, Pydantic 2.11+ features, and follow SOLID principles
without over-engineering. Each nested class provides specific functionality for Oracle WMS
domain operations.
"""

from __future__ import annotations

import base64
import re
from datetime import UTC, datetime
from typing import ClassVar
from urllib.parse import urlparse

from pydantic import SecretStr

from flext_core import FlextResult, FlextUtilities
from flext_oracle_wms.wms_constants import FlextOracleWmsConstants


class FlextOracleWmsUtilities(FlextUtilities):
    """Oracle WMS Domain Utilities.

    Comprehensive utilities for Oracle Warehouse Management System operations,
    providing domain-specific validation, data processing, and business logic
    utilities through nested classes.

    Extends FlextUtilities following the established [Project]Utilities pattern
    with Oracle WMS specific functionality for warehouse operations.
    """

    # Oracle WMS Domain Constants
    MIN_ENTITY_NAME_LENGTH: ClassVar[int] = 1
    MAX_ENTITY_NAME_LENGTH: ClassVar[int] = 255
    MIN_WAREHOUSE_ID_LENGTH: ClassVar[int] = 1
    MAX_WAREHOUSE_ID_LENGTH: ClassVar[int] = 50
    MIN_ITEM_ID_LENGTH: ClassVar[int] = 1
    MAX_ITEM_ID_LENGTH: ClassVar[int] = 100
    MIN_LOCATION_ID_LENGTH: ClassVar[int] = 1
    MAX_LOCATION_ID_LENGTH: ClassVar[int] = 50
    MIN_BATCH_SIZE: ClassVar[int] = 1
    MAX_BATCH_SIZE: ClassVar[int] = 1000
    MIN_TIMEOUT_SECONDS: ClassVar[int] = 1
    MAX_TIMEOUT_SECONDS: ClassVar[int] = 600
    MAX_RETRY_COUNT: ClassVar[int] = 10
    MIN_USERNAME_LENGTH: ClassVar[int] = 3
    MAX_USERNAME_LENGTH: ClassVar[int] = 100
    MIN_PASSWORD_LENGTH: ClassVar[int] = 8
    MAX_PASSWORD_LENGTH: ClassVar[int] = 128
    MAX_QUANTITY: ClassVar[float] = 1_000_000.0
    MAX_UOM_LENGTH: ClassVar[int] = 10
    MAX_ALERT_THRESHOLD: ClassVar[int] = 2

    class EntityValidation:
        """Oracle WMS Entity Validation Utilities.

        Provides validation methods for Oracle WMS entities including
        entity names, warehouse IDs, item IDs, location IDs, and other
        warehouse management identifiers.
        """

        @staticmethod
        def validate_entity_name(entity_name: str) -> FlextResult[str]:
            """Validate Oracle WMS entity name format.

            Args:
                entity_name: Entity name to validate

            Returns:
                FlextResult containing normalized entity name or error

            """
            if not entity_name or not entity_name.strip():
                return FlextResult[str].fail("Entity name cannot be empty")

            normalized = entity_name.strip().lower()

            if len(normalized) < FlextOracleWmsUtilities.MIN_ENTITY_NAME_LENGTH:
                return FlextResult[str].fail("Entity name too short")

            if len(normalized) > FlextOracleWmsUtilities.MAX_ENTITY_NAME_LENGTH:
                return FlextResult[str].fail(
                    f"Entity name too long (max {FlextOracleWmsUtilities.MAX_ENTITY_NAME_LENGTH} characters)"
                )

            # Validate pattern using constants
            pattern = FlextOracleWmsConstants.Entities.ENTITY_NAME_PATTERN
            if not re.match(pattern, normalized):
                return FlextResult[str].fail("Invalid entity name format")

            return FlextResult[str].ok(normalized)

        @staticmethod
        def validate_warehouse_id(warehouse_id: str) -> FlextResult[str]:
            """Validate Oracle WMS warehouse identifier.

            Args:
                warehouse_id: Warehouse ID to validate

            Returns:
                FlextResult containing validated warehouse ID or error

            """
            if not warehouse_id or not warehouse_id.strip():
                return FlextResult[str].fail("Warehouse ID cannot be empty")

            normalized = warehouse_id.strip().upper()

            if len(normalized) < FlextOracleWmsUtilities.MIN_WAREHOUSE_ID_LENGTH:
                return FlextResult[str].fail("Warehouse ID too short")

            if len(normalized) > FlextOracleWmsUtilities.MAX_WAREHOUSE_ID_LENGTH:
                return FlextResult[str].fail(
                    f"Warehouse ID too long (max {FlextOracleWmsUtilities.MAX_WAREHOUSE_ID_LENGTH} characters)"
                )

            # Validate alphanumeric with underscores and hyphens
            if not re.match(r"^[A-Z0-9_-]+$", normalized):
                return FlextResult[str].fail(
                    "Warehouse ID must contain only alphanumeric characters, underscores, and hyphens"
                )

            return FlextResult[str].ok(normalized)

        @staticmethod
        def validate_item_id(item_id: str) -> FlextResult[str]:
            """Validate Oracle WMS item identifier.

            Args:
                item_id: Item ID to validate

            Returns:
                FlextResult containing validated item ID or error

            """
            if not item_id or not item_id.strip():
                return FlextResult[str].fail("Item ID cannot be empty")

            normalized = item_id.strip()

            if len(normalized) < FlextOracleWmsUtilities.MIN_ITEM_ID_LENGTH:
                return FlextResult[str].fail("Item ID too short")

            if len(normalized) > FlextOracleWmsUtilities.MAX_ITEM_ID_LENGTH:
                return FlextResult[str].fail(
                    f"Item ID too long (max {FlextOracleWmsUtilities.MAX_ITEM_ID_LENGTH} characters)"
                )

            return FlextResult[str].ok(normalized)

        @staticmethod
        def validate_location_id(location_id: str) -> FlextResult[str]:
            """Validate Oracle WMS location identifier.

            Args:
                location_id: Location ID to validate

            Returns:
                FlextResult containing validated location ID or error

            """
            if not location_id or not location_id.strip():
                return FlextResult[str].fail("Location ID cannot be empty")

            normalized = location_id.strip().upper()

            if len(normalized) < FlextOracleWmsUtilities.MIN_LOCATION_ID_LENGTH:
                return FlextResult[str].fail("Location ID too short")

            if len(normalized) > FlextOracleWmsUtilities.MAX_LOCATION_ID_LENGTH:
                return FlextResult[str].fail(
                    f"Location ID too long (max {FlextOracleWmsUtilities.MAX_LOCATION_ID_LENGTH} characters)"
                )

            # Validate alphanumeric with underscores, hyphens, and dots for location hierarchy
            if not re.match(r"^[A-Z0-9._-]+$", normalized):
                return FlextResult[str].fail(
                    "Location ID must contain only alphanumeric characters, underscores, hyphens, and dots"
                )

            return FlextResult[str].ok(normalized)

    class ConnectionValidation:
        """Oracle WMS Connection Validation Utilities.

        Provides validation methods for Oracle WMS connection parameters
        including base URLs, authentication credentials, and connection settings.
        """

        @staticmethod
        def validate_base_url(base_url: str) -> FlextResult[str]:
            """Validate Oracle WMS base URL format.

            Args:
                base_url: Base URL to validate

            Returns:
                FlextResult containing validated URL or error

            """
            if not base_url or not base_url.strip():
                return FlextResult[str].fail("Base URL cannot be empty")

            normalized = base_url.strip().rstrip("/")

            try:
                parsed = urlparse(normalized)
                if not parsed.scheme or not parsed.netloc:
                    return FlextResult[str].fail("Invalid URL format")

                if parsed.scheme not in {"http", "https"}:
                    return FlextResult[str].fail("URL must use HTTP or HTTPS protocol")

                if "wms.ocs.oraclecloud.com" not in parsed.netloc:
                    return FlextResult[str].fail(
                        "URL must be an Oracle WMS cloud endpoint"
                    )

            except Exception as e:
                return FlextResult[str].fail(f"URL parsing error: {e}")

            return FlextResult[str].ok(normalized)

        @staticmethod
        def validate_timeout(timeout: int) -> FlextResult[int]:
            """Validate Oracle WMS request timeout value.

            Args:
                timeout: Timeout value in seconds

            Returns:
                FlextResult containing validated timeout or error

            """
            if timeout < FlextOracleWmsUtilities.MIN_TIMEOUT_SECONDS:
                return FlextResult[int].fail(
                    f"Timeout too short (minimum {FlextOracleWmsUtilities.MIN_TIMEOUT_SECONDS} seconds)"
                )

            if timeout > FlextOracleWmsUtilities.MAX_TIMEOUT_SECONDS:
                return FlextResult[int].fail(
                    f"Timeout too long (maximum {FlextOracleWmsUtilities.MAX_TIMEOUT_SECONDS} seconds)"
                )

            return FlextResult[int].ok(timeout)

        @staticmethod
        def validate_retry_count(retry_count: int) -> FlextResult[int]:
            """Validate Oracle WMS retry count value.

            Args:
                retry_count: Number of retry attempts

            Returns:
                FlextResult containing validated retry count or error

            """
            if retry_count < 0:
                return FlextResult[int].fail("Retry count cannot be negative")

            if retry_count > FlextOracleWmsUtilities.MAX_RETRY_COUNT:
                return FlextResult[int].fail(
                    "Retry count too high (maximum 10 retries)"
                )

            return FlextResult[int].ok(retry_count)

    class AuthenticationValidation:
        """Oracle WMS Authentication Validation Utilities.

        Provides validation methods for Oracle WMS authentication
        credentials including usernames, passwords, and auth methods.
        """

        @staticmethod
        def validate_username(username: str) -> FlextResult[str]:
            """Validate Oracle WMS username format.

            Args:
                username: Username to validate

            Returns:
                FlextResult containing validated username or error

            """
            if not username or not username.strip():
                return FlextResult[str].fail("Username cannot be empty")

            normalized = username.strip()

            if len(normalized) < FlextOracleWmsUtilities.MIN_USERNAME_LENGTH:
                return FlextResult[str].fail(
                    "Username too short (minimum 3 characters)"
                )

            if len(normalized) > FlextOracleWmsUtilities.MAX_USERNAME_LENGTH:
                return FlextResult[str].fail(
                    "Username too long (maximum 100 characters)"
                )

            # Basic format validation
            if not re.match(r"^[a-zA-Z0-9._@-]+$", normalized):
                return FlextResult[str].fail("Username contains invalid characters")

            return FlextResult[str].ok(normalized)

        @staticmethod
        def validate_password(password: str | SecretStr) -> FlextResult[SecretStr]:
            """Validate Oracle WMS password strength.

            Args:
                password: Password to validate (string or SecretStr)

            Returns:
                FlextResult containing validated SecretStr password or error

            """
            if isinstance(password, SecretStr):
                password_value = password.get_secret_value()
            else:
                password_value = password

            if not password_value or not password_value.strip():
                return FlextResult[SecretStr].fail("Password cannot be empty")

            if len(password_value) < FlextOracleWmsUtilities.MIN_PASSWORD_LENGTH:
                return FlextResult[SecretStr].fail(
                    "Password too short (minimum 8 characters)"
                )

            if len(password_value) > FlextOracleWmsUtilities.MAX_PASSWORD_LENGTH:
                return FlextResult[SecretStr].fail(
                    "Password too long (maximum 128 characters)"
                )

            return FlextResult[SecretStr].ok(SecretStr(password_value))

        @staticmethod
        def validate_auth_method(auth_method: str) -> FlextResult[str]:
            """Validate Oracle WMS authentication method.

            Args:
                auth_method: Authentication method to validate

            Returns:
                FlextResult containing validated auth method or error

            """
            if not auth_method or not auth_method.strip():
                return FlextResult[str].fail("Authentication method cannot be empty")

            normalized = auth_method.strip().upper()

            valid_methods = {"BASIC", "BEARER", "API_KEY", "OAUTH2"}
            if normalized not in valid_methods:
                return FlextResult[str].fail(
                    f"Invalid authentication method. Must be one of: {', '.join(valid_methods)}"
                )

            return FlextResult[str].ok(normalized)

    class DataProcessing:
        """Oracle WMS Data Processing Utilities.

        Provides utilities for processing Oracle WMS data including
        batch operations, pagination, filtering, and data transformation.
        """

        @staticmethod
        def validate_batch_size(batch_size: int) -> FlextResult[int]:
            """Validate Oracle WMS batch size for operations.

            Args:
                batch_size: Batch size to validate

            Returns:
                FlextResult containing validated batch size or error

            """
            if batch_size < FlextOracleWmsUtilities.MIN_BATCH_SIZE:
                return FlextResult[int].fail(
                    f"Batch size too small (minimum {FlextOracleWmsUtilities.MIN_BATCH_SIZE})"
                )

            if batch_size > FlextOracleWmsUtilities.MAX_BATCH_SIZE:
                return FlextResult[int].fail(
                    f"Batch size too large (maximum {FlextOracleWmsUtilities.MAX_BATCH_SIZE})"
                )

            return FlextResult[int].ok(batch_size)

        @staticmethod
        def chunk_records(
            records: list[dict[str, object]], chunk_size: int
        ) -> FlextResult[list[list[dict[str, object]]]]:
            """Chunk Oracle WMS records into batches for processing.

            Args:
                records: List of records to chunk
                chunk_size: Size of each chunk

            Returns:
                FlextResult containing list of record chunks or error

            """
            if not records:
                return FlextResult[list[list[dict[str, object]]]].ok([])

            chunk_validation = (
                FlextOracleWmsUtilities.DataProcessing.validate_batch_size(chunk_size)
            )
            if chunk_validation.is_failure:
                return FlextResult[list[list[dict[str, object]]]].fail(
                    chunk_validation.error
                )

            chunks: list[list[dict[str, object]]] = []
            for i in range(0, len(records), chunk_size):
                chunk = records[i : i + chunk_size]
                chunks.append(chunk)

            return FlextResult[list[list[dict[str, object]]]].ok(chunks)

        @staticmethod
        def validate_pagination_info(
            page: int, page_size: int
        ) -> FlextResult[dict[str, int]]:
            """Validate Oracle WMS pagination parameters.

            Args:
                page: Page number (1-based)
                page_size: Number of items per page

            Returns:
                FlextResult containing validated pagination info or error

            """
            if page < 1:
                return FlextResult[dict[str, int]].fail(
                    "Page number must be 1 or greater"
                )

            page_size_validation = (
                FlextOracleWmsUtilities.DataProcessing.validate_batch_size(page_size)
            )
            if page_size_validation.is_failure:
                return FlextResult[dict[str, int]].fail(
                    f"Invalid page size: {page_size_validation.error}"
                )

            pagination_info = {
                "page": page,
                "page_size": page_size,
                "offset": (page - 1) * page_size,
                "limit": page_size,
            }

            return FlextResult[dict[str, int]].ok(pagination_info)

        @staticmethod
        def normalize_filter_value(filter_value: object) -> FlextResult[str]:
            """Normalize Oracle WMS filter value for API queries.

            Args:
                filter_value: Filter value to normalize

            Returns:
                FlextResult containing normalized filter value or error

            """
            if filter_value is None:
                return FlextResult[str].fail("Filter value cannot be None")

            if isinstance(filter_value, str):
                normalized = filter_value.strip()
                if not normalized:
                    return FlextResult[str].fail("Filter value cannot be empty")
                return FlextResult[str].ok(normalized)

            if isinstance(filter_value, (int, float, bool)):
                return FlextResult[str].ok(str(filter_value))

            if isinstance(filter_value, datetime):
                # Use Python 3.13+ UTC constant
                iso_format = filter_value.replace(tzinfo=UTC).isoformat()
                return FlextResult[str].ok(iso_format)

            return FlextResult[str].fail(
                f"Unsupported filter value type: {type(filter_value)}"
            )

    class ApiRequestBuilder:
        """Oracle WMS API Request Builder Utilities.

        Provides utilities for building Oracle WMS API requests including
        endpoint construction, header building, and parameter validation.
        """

        @staticmethod
        def build_entity_endpoint(
            base_url: str,
            entity_name: str,
            entity_id: str | None = None,
            api_version: str = "v1",
        ) -> FlextResult[str]:
            """Build Oracle WMS entity API endpoint.

            Args:
                base_url: Oracle WMS base URL
                entity_name: Entity name for the endpoint
                entity_id: Optional entity ID for specific resource
                api_version: API version to use

            Returns:
                FlextResult containing constructed endpoint URL or error

            """
            # Validate base URL
            url_validation = (
                FlextOracleWmsUtilities.ConnectionValidation.validate_base_url(base_url)
            )
            if url_validation.is_failure:
                return FlextResult[str].fail(url_validation.error)

            # Validate entity name
            entity_validation = (
                FlextOracleWmsUtilities.EntityValidation.validate_entity_name(
                    entity_name
                )
            )
            if entity_validation.is_failure:
                return FlextResult[str].fail(entity_validation.error)

            # Build endpoint path
            normalized_base = url_validation.unwrap().rstrip("/")
            normalized_entity = entity_validation.unwrap()

            endpoint_parts = [normalized_base, "api", api_version, normalized_entity]

            if entity_id:
                # Validate entity ID if provided
                id_validation = (
                    FlextOracleWmsUtilities.EntityValidation.validate_item_id(entity_id)
                )
                if id_validation.is_failure:
                    return FlextResult[str].fail(
                        f"Invalid entity ID: {id_validation.error}"
                    )
                endpoint_parts.append(id_validation.unwrap())

            endpoint_url = "/".join(endpoint_parts)
            return FlextResult[str].ok(endpoint_url)

        @staticmethod
        def build_query_parameters(
            filters: dict[str, object],
        ) -> FlextResult[dict[str, str]]:
            """Build Oracle WMS API query parameters from filters.

            Args:
                filters: Dictionary of filter parameters

            Returns:
                FlextResult containing normalized query parameters or error

            """
            if not filters:
                return FlextResult[dict[str, str]].ok({})

            normalized_params: dict[str, str] = {}

            for key, value in filters.items():
                if not key or not key.strip():
                    return FlextResult[dict[str, str]].fail(
                        "Filter key cannot be empty"
                    )

                normalized_key = key.strip().lower()

                # Normalize filter value
                value_validation = (
                    FlextOracleWmsUtilities.DataProcessing.normalize_filter_value(value)
                )
                if value_validation.is_failure:
                    return FlextResult[dict[str, str]].fail(
                        f"Invalid filter value for '{key}': {value_validation.error}"
                    )

                normalized_params[normalized_key] = value_validation.unwrap()

            return FlextResult[dict[str, str]].ok(normalized_params)

        @staticmethod
        def build_request_headers(
            auth_method: str,
            username: str | None = None,
            password: str | SecretStr | None = None,
            api_key: str | None = None,
            bearer_token: str | None = None,
        ) -> FlextResult[dict[str, str]]:
            """Build Oracle WMS API request headers with authentication.

            Args:
                auth_method: Authentication method to use
                username: Username for basic auth
                password: Password for basic auth
                api_key: API key for API key auth
                bearer_token: Bearer token for bearer auth

            Returns:
                FlextResult containing request headers or error

            """
            # Validate auth method
            method_validation = (
                FlextOracleWmsUtilities.AuthenticationValidation.validate_auth_method(
                    auth_method
                )
            )
            if method_validation.is_failure:
                return FlextResult[dict[str, str]].fail(method_validation.error)

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "FlextOracleWms/1.0",
            }

            validated_method = method_validation.unwrap()

            if validated_method == "BASIC":
                if not username or not password:
                    return FlextResult[dict[str, str]].fail(
                        "Username and password required for basic auth"
                    )

                # Validate credentials
                username_validation = (
                    FlextOracleWmsUtilities.AuthenticationValidation.validate_username(
                        username
                    )
                )
                if username_validation.is_failure:
                    return FlextResult[dict[str, str]].fail(username_validation.error)

                password_validation = (
                    FlextOracleWmsUtilities.AuthenticationValidation.validate_password(
                        password
                    )
                )
                if password_validation.is_failure:
                    return FlextResult[dict[str, str]].fail(password_validation.error)

                # Build basic auth header
                credentials = f"{username_validation.unwrap()}:{password_validation.unwrap().get_secret_value()}"
                encoded_credentials = base64.b64encode(credentials.encode()).decode()
                headers["Authorization"] = f"Basic {encoded_credentials}"

            elif validated_method == "BEARER":
                if not bearer_token:
                    return FlextResult[dict[str, str]].fail(
                        "Bearer token required for bearer auth"
                    )
                headers["Authorization"] = f"Bearer {bearer_token}"

            elif validated_method == "API_KEY":
                if not api_key:
                    return FlextResult[dict[str, str]].fail(
                        "API key required for API key auth"
                    )
                headers["X-API-Key"] = api_key

            return FlextResult[dict[str, str]].ok(headers)

    class InventoryOperations:
        """Oracle WMS Inventory Operations Utilities.

        Provides utilities for Oracle WMS inventory management operations
        including stock validation, movement tracking, and inventory calculations.
        """

        @staticmethod
        def validate_quantity(quantity: float) -> FlextResult[float]:
            """Validate Oracle WMS inventory quantity.

            Args:
                quantity: Quantity value to validate

            Returns:
                FlextResult containing validated quantity or error

            """
            if not isinstance(quantity, (int, float)):
                return FlextResult[float].fail("Quantity must be a number")

            if quantity < 0:
                return FlextResult[float].fail("Quantity cannot be negative")

            if quantity > FlextOracleWmsUtilities.MAX_QUANTITY:
                return FlextResult[float].fail("Quantity too large (maximum 1,000,000)")

            return FlextResult[float].ok(float(quantity))

        @staticmethod
        def validate_unit_of_measure(uom: str) -> FlextResult[str]:
            """Validate Oracle WMS unit of measure.

            Args:
                uom: Unit of measure to validate

            Returns:
                FlextResult containing validated UOM or error

            """
            if not uom or not uom.strip():
                return FlextResult[str].fail("Unit of measure cannot be empty")

            normalized = uom.strip().upper()

            if len(normalized) > FlextOracleWmsUtilities.MAX_UOM_LENGTH:
                return FlextResult[str].fail(
                    "Unit of measure too long (maximum 10 characters)"
                )

            # Validate UOM format
            if not re.match(r"^[A-Z0-9]+$", normalized):
                return FlextResult[str].fail(
                    "Unit of measure must contain only alphanumeric characters"
                )

            return FlextResult[str].ok(normalized)

        @staticmethod
        def calculate_total_quantity(
            items: list[dict[str, object]], quantity_field: str = "quantity"
        ) -> FlextResult[float]:
            """Calculate total quantity from Oracle WMS inventory items.

            Args:
                items: List of inventory items
                quantity_field: Field name containing quantity values

            Returns:
                FlextResult containing total quantity or error

            """
            if not items:
                return FlextResult[float].ok(0.0)

            total_quantity = 0.0

            for item in items:
                if not isinstance(item, dict):
                    return FlextResult[float].fail("Each item must be a dictionary")

                if quantity_field not in item:
                    return FlextResult[float].fail(
                        f"Missing quantity field '{quantity_field}' in item"
                    )

                quantity_validation = (
                    FlextOracleWmsUtilities.InventoryOperations.validate_quantity(
                        item[quantity_field]
                    )
                )
                if quantity_validation.is_failure:
                    return FlextResult[float].fail(
                        f"Invalid quantity in item: {quantity_validation.error}"
                    )

                total_quantity += quantity_validation.unwrap()

            return FlextResult[float].ok(total_quantity)

    class MonitoringUtilities:
        """Oracle WMS Monitoring Utilities.

        Provides utilities for Oracle WMS monitoring and health checks
        including status validation, performance metrics, and error analysis.
        """

        @staticmethod
        def validate_health_status(
            status_data: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Validate Oracle WMS health check status data.

            Args:
                status_data: Health status data to validate

            Returns:
                FlextResult containing validated status data or error

            """
            if not status_data:
                return FlextResult[dict[str, object]].fail(
                    "Health status data cannot be empty"
                )

            required_fields = {"status", "timestamp", "service"}
            missing_fields = required_fields - set(status_data.keys())

            if missing_fields:
                return FlextResult[dict[str, object]].fail(
                    f"Missing required health status fields: {', '.join(missing_fields)}"
                )

            # Validate status value
            valid_statuses = {"healthy", "degraded", "unhealthy"}
            status = status_data["status"]
            if status not in valid_statuses:
                return FlextResult[dict[str, object]].fail(
                    f"Invalid health status '{status}'. Must be one of: {', '.join(valid_statuses)}"
                )

            # Validate service name
            service = status_data["service"]
            if not service or not str(service).strip():
                return FlextResult[dict[str, object]].fail(
                    "Service name cannot be empty"
                )

            validated_data = {
                "status": status,
                "timestamp": status_data["timestamp"],
                "service": str(service).strip(),
                "details": status_data.get("details", {}),
                "metrics": status_data.get("metrics", {}),
            }

            return FlextResult[dict[str, object]].ok(validated_data)

        @staticmethod
        def analyze_performance_metrics(
            metrics: dict[str, object], thresholds: dict[str, float] | None = None
        ) -> FlextResult[dict[str, object]]:
            """Analyze Oracle WMS performance metrics against thresholds.

            Args:
                metrics: Performance metrics data
                thresholds: Optional thresholds for metric analysis

            Returns:
                FlextResult containing metrics analysis or error

            """
            if not metrics:
                return FlextResult[dict[str, object]].fail(
                    "Performance metrics cannot be empty"
                )

            # Default thresholds
            default_thresholds = {
                "response_time_ms": 5000.0,
                "error_rate_percent": 5.0,
                "cpu_usage_percent": 80.0,
                "memory_usage_percent": 85.0,
                "throughput_requests_per_second": 100.0,
            }

            analysis_thresholds = thresholds or default_thresholds
            analysis_result: dict[str, object] = {
                "overall_status": "healthy",
                "alerts": [],
                "warnings": [],
                "analyzed_metrics": {},
            }

            for metric_name, metric_value in metrics.items():
                if not isinstance(metric_value, (int, float)):
                    continue

                analysis_result["analyzed_metrics"][metric_name] = {
                    "value": metric_value,
                    "status": "normal",
                }

                # Check against thresholds
                if metric_name in analysis_thresholds:
                    threshold = analysis_thresholds[metric_name]

                    if metric_value > threshold:
                        analysis_result["analyzed_metrics"][metric_name]["status"] = (
                            "exceeded"
                        )
                        analysis_result["alerts"].append(
                            f"{metric_name}: {metric_value} exceeds threshold {threshold}"
                        )
                        analysis_result["overall_status"] = "degraded"

                    elif metric_value > threshold * 0.8:  # Warning at 80% of threshold
                        analysis_result["analyzed_metrics"][metric_name]["status"] = (
                            "warning"
                        )
                        analysis_result["warnings"].append(
                            f"{metric_name}: {metric_value} approaching threshold {threshold}"
                        )

            # Set overall status based on alerts
            if analysis_result["alerts"]:
                analysis_result["overall_status"] = (
                    "unhealthy"
                    if len(analysis_result["alerts"])
                    > FlextOracleWmsUtilities.MAX_ALERT_THRESHOLD
                    else "degraded"
                )

            return FlextResult[dict[str, object]].ok(analysis_result)
