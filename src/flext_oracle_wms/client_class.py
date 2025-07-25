"""FlextOracleWms Client Class - Single Responsibility Principle.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Oracle WMS client implementation with proper prefixing and
Clean Architecture principles - migrated from flext-tap-oracle-wms.
"""

from __future__ import annotations

import base64
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Self

import httpx

# Import from flext-core root namespace as required
from flext_core import FlextResult, get_logger

# Import enterprise cache manager for consistency
from flext_oracle_wms.infrastructure.flext_oracle_wms_cache import (
    FlextOracleWmsCacheManager,
)

if TYPE_CHECKING:
    from types import TracebackType

    from flext_oracle_wms.config_module import FlextOracleWmsModuleConfig


logger = get_logger(__name__)


class FlextOracleWmsClientError(Exception):
    """Base exception for Oracle WMS client errors."""


class FlextOracleWmsAuthenticationError(FlextOracleWmsClientError):
    """Exception raised for authentication errors."""


class FlextOracleWmsConnectionError(FlextOracleWmsClientError):
    """Exception raised for connection errors."""


class FlextOracleWmsClient:
    """FlextOracleWms HTTP client for Oracle WMS REST API operations.

    Provides comprehensive Oracle WMS integration capabilities following
    SOLID principles with proper error handling and type safety.
    """

    def __init__(self, config: FlextOracleWmsModuleConfig, metrics: Any = None) -> None:
        """Initialize Oracle WMS client.

        Args:
            config: WMS configuration
            metrics: Metrics tracking instance

        """
        self.config = config
        self.metrics = metrics

        # Create HTTP client with configuration
        self.client = httpx.Client(
            base_url=str(config.base_url).rstrip("/"),
            timeout=config.timeout_seconds,
            verify=getattr(config, "verify_ssl", True),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "flext-oracle-wms/2.0.0",
            },
        )

        # Apply authentication if configured
        if config.username and config.password:
            credentials = f"{config.username}:{config.password}"
            encoded = base64.b64encode(credentials.encode()).decode()
            self.client.headers["Authorization"] = f"Basic {encoded}"

        # Initialize enterprise cache manager for consistency with legacy client
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

        # Initialize operation tracking for consistency
        self._operation_tracker: dict[str, dict[str, Any]] = {}
        self._operation_counter = 0

        logger.debug("Oracle WMS client initialized for %s", config.base_url)

    def validate_entity_name(self, entity_name: str) -> str:
        """Validate Oracle WMS entity name.

        Args:
            entity_name: Entity name to validate

        Returns:
            Validated entity name

        Raises:
            ValueError: If entity name is invalid

        """
        from flext_oracle_wms.constants import FlextOracleWmsEntityTypes

        if entity_name not in FlextOracleWmsEntityTypes.ALL_ENTITIES:
            valid_entities = ", ".join(FlextOracleWmsEntityTypes.ALL_ENTITIES)
            msg = (
                f"Invalid entity name: {entity_name}. Must be one of: {valid_entities}"
            )
            raise ValueError(msg)

        return entity_name

    def build_api_url(self, entity_name: str, api_version: str | None = None) -> str:
        """Build complete API URL for Oracle WMS entity.

        Args:
            entity_name: WMS entity name
            api_version: API version (optional, uses config default)

        Returns:
            Complete API URL for the entity

        """
        # Validate entity name first
        validated_entity = self.validate_entity_name(entity_name)
        version = api_version or getattr(self.config, "api_version", "v10")

        base_url = str(self.config.base_url).rstrip("/")
        return f"{base_url}/wms/lgfapi/{version}/entity/{validated_entity}"

    def __enter__(self) -> Self:
        """Context manager entry."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Context manager exit - close client."""
        self.client.close()

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make GET request to Oracle WMS API.

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            API response data

        Raises:
            FlextOracleWmsConnectionError: Connection or timeout errors
            FlextOracleWmsClientError: Other API errors

        """
        if self.metrics:
            self.metrics.add_api_call()

        try:
            response = self.client.get(endpoint, params=params or {})

            # Handle common HTTP status codes
            self._handle_response_errors(response)

            response.raise_for_status()
            result = response.json()
            return result if isinstance(result, dict) else {"data": result}

        except httpx.ConnectError as e:
            msg = f"Connection failed: {e}"
            raise FlextOracleWmsConnectionError(msg) from e
        except httpx.TimeoutException as e:
            msg = f"Request timeout: {e}"
            raise FlextOracleWmsConnectionError(msg) from e
        except Exception as e:
            if isinstance(
                e,
                (
                    FlextOracleWmsAuthenticationError
                    | FlextOracleWmsConnectionError
                    | FlextOracleWmsClientError
                ),
            ):
                raise
            msg = f"Unexpected error: {e}"
            raise FlextOracleWmsClientError(msg) from e

    def discover_entities(self) -> FlextResult[list[dict[str, Any]]]:
        """Discover available Oracle WMS entities.

        Returns:
            FlextResult with list of discovered entity definitions

        """
        logger.info("Discovering Oracle WMS entities")

        try:
            # Try common WMS entity discovery endpoints
            endpoints = [
                "/api/entities",
                "/api/v1/entities",
                "/wms/lgfapi/v10/entity",
                "/wms/lgfapi/v11/entity",
            ]

            for endpoint in endpoints:
                try:
                    result = self.get(endpoint)
                    # Check if result contains data key with list
                    if "data" in result and isinstance(result["data"], list):
                        entities_list = result["data"]
                        if entities_list:
                            logger.info(
                                "Found %d entities via %s",
                                len(entities_list),
                                endpoint,
                            )
                            return FlextResult.ok(entities_list)
                    elif "entities" in result:
                        entities = result["entities"]
                        if isinstance(entities, list):
                            logger.info(
                                "Found %d entities via %s",
                                len(entities),
                                endpoint,
                            )
                            return FlextResult.ok(entities)
                except FlextOracleWmsClientError:
                    continue

            logger.warning("No entities discovered - will try common WMS endpoints")
            return FlextResult.ok([])

        except Exception as e:
            return FlextResult.fail(f"Entity discovery failed: {e}")

    def get_entity_data(
        self,
        entity_name: str,
        params: dict[str, str | int | float | bool] | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Get data for a specific Oracle WMS entity.

        Args:
            entity_name: Name of the entity to retrieve
            params: Additional query parameters

        Returns:
            FlextResult with entity data from WMS API

        """
        try:
            endpoint = f"/api/{entity_name}"

            # Add WMS scoping parameters from config
            query_params = {
                "page_size": self.config.batch_size,
                **(params or {}),
            }

            # Add company and facility codes if available
            if hasattr(self.config, "company_code"):
                query_params["company_code"] = self.config.company_code
            if hasattr(self.config, "facility_code"):
                query_params["facility_code"] = self.config.facility_code

            result = self.get(endpoint, query_params)
            return FlextResult.ok(result)

        except Exception as e:
            return FlextResult.fail(f"Entity data fetch failed: {e}")

    def test_connection(self) -> FlextResult[bool]:
        """Test connection to Oracle WMS API.

        Returns:
            FlextResult with connection test status

        """
        try:
            # Try a simple endpoint to test connectivity
            self.get("/api/ping")
            return FlextResult.ok(True)
        except (
            FlextOracleWmsAuthenticationError,
            FlextOracleWmsConnectionError,
            FlextOracleWmsClientError,
        ):
            return FlextResult.ok(False)
        except Exception as e:
            return FlextResult.fail(f"Connection test failed: {e}")

    def bulk_get_entities(
        self,
        entity_names: list[str],
        params: dict[str, Any] | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Get data for multiple Oracle WMS entities in batch.

        Args:
            entity_names: List of entity names to retrieve
            params: Common query parameters for all entities

        Returns:
            FlextResult with dict mapping entity names to their data

        """
        try:
            results: dict[str, dict[str, Any]] = {}
            failed_entities: list[str] = []

            for entity_name in entity_names:
                try:
                    # Validate entity name
                    validated_entity = self.validate_entity_name(entity_name)

                    # Build endpoint
                    api_version = getattr(self.config, "api_version", "v10")
                    endpoint = f"/wms/lgfapi/{api_version}/entity/{validated_entity}"

                    # Make request
                    response_data = self.get(endpoint, params)
                    results[entity_name] = response_data

                except Exception as e:
                    failed_entities.append(f"{entity_name}: {e!s}")
                    continue

            if failed_entities and not results:
                return FlextResult.fail(
                    f"All entities failed: {'; '.join(failed_entities)}",
                )
            if failed_entities:
                # Partial success - include failed entities in metadata
                return FlextResult.ok(
                    {
                        "data": results,
                        "failed_entities": failed_entities,
                        "partial_success": True,
                    },
                )
            return FlextResult.ok({"data": results, "partial_success": False})

        except Exception as e:
            return FlextResult.fail(f"Bulk get entities failed: {e}")

    def bulk_post_records(
        self,
        entity_name: str,
        records: list[dict[str, Any]],
        batch_size: int | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Post multiple records to Oracle WMS entity in batches.

        Args:
            entity_name: Target entity name
            records: List of records to post
            batch_size: Number of records per batch (uses config default if None)

        Returns:
            FlextResult with batch operation results

        """
        try:
            # Validate entity name
            validated_entity = self.validate_entity_name(entity_name)

            # Get batch size from config or use default
            batch_size_value = batch_size or getattr(self.config, "batch_size", 50)

            # Ensure batch_size is a positive integer
            if not isinstance(batch_size_value, int) or batch_size_value <= 0:
                return FlextResult.fail("Batch size must be a positive integer")

            effective_batch_size: int = batch_size_value

            # Split records into batches
            batches = [
                records[i : i + effective_batch_size]
                for i in range(0, len(records), effective_batch_size)
            ]

            results: dict[str, Any] = {
                "total_records": len(records),
                "total_batches": len(batches),
                "successful_batches": 0,
                "failed_batches": 0,
                "errors": [],
            }

            # Process each batch
            for batch_index, batch_records in enumerate(batches):
                try:
                    # Build endpoint
                    api_version = getattr(self.config, "api_version", "v10")
                    endpoint = f"/wms/lgfapi/{api_version}/entity/{validated_entity}"

                    # Post batch
                    response = self.client.post(
                        endpoint,
                        json={"records": batch_records},
                    )

                    # Handle response errors
                    self._handle_response_errors(response)
                    response.raise_for_status()

                    results["successful_batches"] += 1

                except Exception as e:
                    results["failed_batches"] += 1
                    results["errors"].append(f"Batch {batch_index}: {e!s}")

            if results["failed_batches"] == 0:
                return FlextResult.ok(results)
            if results["successful_batches"] > 0:
                return FlextResult.ok({**results, "partial_success": True})
            return FlextResult.fail(
                f"All batches failed: {'; '.join(results['errors'])}",
            )

        except Exception as e:
            return FlextResult.fail(f"Bulk post records failed: {e}")

    def bulk_update_records(
        self,
        entity_name: str,
        records: list[dict[str, Any]],
        id_field: str = "id",
        batch_size: int | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Update multiple records in Oracle WMS entity in batches.

        Args:
            entity_name: Target entity name
            records: List of records to update (must include id_field)
            id_field: Name of the ID field for updates
            batch_size: Number of records per batch

        Returns:
            FlextResult with batch update results

        """
        try:
            # Validate entity name
            validated_entity = self.validate_entity_name(entity_name)

            # Validate all records have ID field
            missing_id_records = [
                i for i, record in enumerate(records) if id_field not in record
            ]
            if missing_id_records:
                return FlextResult.fail(
                    f"Records missing {id_field}: {missing_id_records}",
                )

            # Get batch size
            batch_size_value = batch_size or getattr(self.config, "batch_size", 50)

            # Ensure batch_size is a positive integer
            if not isinstance(batch_size_value, int) or batch_size_value <= 0:
                return FlextResult.fail("Batch size must be a positive integer")

            effective_batch_size: int = batch_size_value

            # Split into batches
            batches = [
                records[i : i + effective_batch_size]
                for i in range(0, len(records), effective_batch_size)
            ]

            results: dict[str, Any] = {
                "total_records": len(records),
                "total_batches": len(batches),
                "successful_updates": 0,
                "failed_updates": 0,
                "errors": [],
            }

            # Process each batch
            for batch_records in batches:
                successful_in_batch = 0

                for record in batch_records:
                    try:
                        record_id = record[id_field]
                        api_version = getattr(self.config, "api_version", "v10")
                        endpoint = (
                            f"/wms/lgfapi/{api_version}/entity/{validated_entity}/"
                            f"{record_id}"
                        )

                        # Update individual record
                        response = self.client.put(endpoint, json=record)
                        self._handle_response_errors(response)
                        response.raise_for_status()

                        successful_in_batch += 1
                        results["successful_updates"] += 1

                    except Exception as e:
                        results["failed_updates"] += 1
                        results["errors"].append(f"Record {record_id}: {e!s}")

            if results["failed_updates"] == 0:
                return FlextResult.ok(results)
            if results["successful_updates"] > 0:
                return FlextResult.ok({**results, "partial_success": True})
            return FlextResult.fail(
                f"All updates failed: {len(results['errors'])} errors",
            )

        except Exception as e:
            return FlextResult.fail(f"Bulk update records failed: {e}")

    @staticmethod
    def _handle_response_errors(response: httpx.Response) -> None:
        """Handle HTTP response errors.

        Args:
            response: HTTP response to check

        Raises:
            FlextOracleWmsAuthenticationError: For 401/403 errors
            FlextOracleWmsConnectionError: For server errors
            FlextOracleWmsClientError: For client errors

        """
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            msg = "Authentication failed: Invalid credentials"
            raise FlextOracleWmsAuthenticationError(msg)
        if response.status_code == HTTPStatus.FORBIDDEN:
            msg = "Authentication failed: Access denied"
            raise FlextOracleWmsAuthenticationError(msg)
        if response.status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
            msg = f"Server error: {response.status_code}"
            raise FlextOracleWmsConnectionError(msg)
        if response.status_code >= HTTPStatus.BAD_REQUEST:
            msg = f"Client error: {response.status_code}"
            raise FlextOracleWmsClientError(msg)

    def get_bulk_cache_stats(self) -> dict[str, Any]:
        """Get cache statistics for consistency with legacy client.

        Returns:
            Dictionary with cache statistics

        """
        # Get comprehensive stats from enterprise cache manager
        enterprise_stats = self._cache_manager.flext_oracle_wms_get_stats()

        # Add configuration information
        return {
            "cache_enabled": getattr(self.config, "enable_cache", True),
            "enterprise_cache": True,
            **enterprise_stats,
        }

    def clear_bulk_cache(self) -> bool:
        """Clear the cache for consistency with legacy client.

        Returns:
            True if cache was cleared, False if no cache exists

        """
        # Use enterprise cache manager to clear all caches
        success = self._cache_manager.flext_oracle_wms_clear_all()
        if success:
            logger.info("Cleared enterprise cache")
        else:
            logger.warning("Failed to clear enterprise cache")
        return success

    def get_operation_tracking_stats(self) -> dict[str, Any]:
        """Get operation tracking statistics for consistency.

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

    def close(self) -> None:
        """Close the HTTP client connection for consistency."""
        if hasattr(self, "client") and self.client:
            self.client.close()
            logger.info("Oracle WMS client connection closed")

    def get_connection_info(self) -> dict[str, Any]:
        """Get connection information for consistency with legacy client.

        Returns:
            Dictionary with connection details

        """
        return {
            "base_url": self.config.base_url,
            "auth_method": "basic",  # Oracle WMS uses basic authentication
            "username": self.config.username,
            "timeout": self.config.timeout_seconds,
            "client_active": hasattr(self, "client") and self.client is not None,
        }
