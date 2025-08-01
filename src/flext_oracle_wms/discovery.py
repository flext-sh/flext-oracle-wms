"""Enterprise Entity Discovery for Oracle WMS.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Advanced entity discovery system using flext-api client with caching and intelligent
discovery.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flext_api import FlextApiClientResponse

from flext_api import FlextApiClient
from flext_core import FlextResult, get_logger

from flext_oracle_wms.constants import FlextOracleWmsDefaults
from flext_oracle_wms.helpers import handle_operation_exception
from flext_oracle_wms.models import FlextOracleWmsDiscoveryResult, FlextOracleWmsEntity

if TYPE_CHECKING:
    from flext_api import FlextApiClient

logger = get_logger(__name__)

# Constants for FlextResult boolean values to avoid FBT003 lint errors
DISCOVERY_SUCCESS = True
DISCOVERY_FAILURE = False


# =============================================================================
# SOLID REFACTORING: Strategy + Command Patterns for complexity reduction
# =============================================================================


@dataclass
class DiscoveryContext:
    """Parameter Object: Encapsulates discovery operation context.

    SOLID REFACTORING: Reduces parameter passing and centralizes discovery state.
    """

    include_patterns: list[str] | None
    exclude_patterns: list[str] | None
    all_entities: list[FlextOracleWmsEntity]
    errors: list[str]


class DiscoveryStrategy(ABC):
    """Strategy Pattern: Abstract base for discovery strategies."""

    @abstractmethod
    async def execute_discovery_step(
        self,
        context: DiscoveryContext,
        api_client: FlextApiClient,
        endpoint: str,
    ) -> FlextResult[bool]:
        """Execute a discovery step and update context."""


class EndpointDiscoveryStrategy(DiscoveryStrategy):
    """Strategy Pattern: Handles endpoint discovery and entity collection."""

    def __init__(self, discovery_instance: FlextOracleWmsEntityDiscovery) -> None:
        """Initialize with discovery instance for delegation."""
        self.discovery = discovery_instance

    async def execute_discovery_step(
        self,
        context: DiscoveryContext,
        api_client: FlextApiClient,
        endpoint: str,
    ) -> FlextResult[bool]:
        """Execute endpoint discovery step using Railway-Oriented Programming.

        SOLID REFACTORING: Reduced multiple returns from 6 to 1 using Railway-Oriented.
        """
        try:
            logger.debug("Trying discovery endpoint", endpoint=endpoint)

            # Chain of validations using Railway-Oriented Programming
            response_result = await self._make_api_request(api_client, endpoint)
            if not response_result.is_success:
                return self._handle_discovery_error(
                    context, response_result.error or "Request failed", endpoint
                )

            validated_response = self._validate_response(response_result.data, endpoint)
            if not validated_response.is_success:
                return self._handle_discovery_error(
                    context,
                    validated_response.error or "Response validation failed",
                    endpoint,
                )

            # Parse and process entities - validated_response.data is guaranteed to be
            # FlextApiClientResponse
            if validated_response.data is None:
                return FlextResult.fail("Validated response data is None")
            return await self._process_entities_response(
                context,
                validated_response.data,
                endpoint
            )

        except Exception as e:
            error_msg = f"Exception calling {endpoint}: {e}"
            logger.exception(error_msg)
            context.errors.append(error_msg)
            return FlextResult.ok(DISCOVERY_FAILURE)


    async def _make_api_request(
        self,
        api_client: FlextApiClient,
        endpoint: str,
    ) -> FlextResult[FlextApiClientResponse]:
        """Make API request with proper error handling."""
        response_result = await api_client.get(endpoint)
        if not response_result.is_success:
            return FlextResult.fail(
                f"Failed to call {endpoint}: {response_result.error}"
            )
        # Type assertion: FlextApiClient.get() returns FlextResult[Response]
        # (guaranteed by flext_api contract)
        if response_result.data is None:
            return FlextResult.fail(f"No response data from {endpoint}")
        return FlextResult.ok(response_result.data)

    def _validate_response(
        self,
        response: FlextApiClientResponse | None,
        endpoint: str,
    ) -> FlextResult[FlextApiClientResponse]:
        """Validate API response structure and status."""
        if response is None:
            return FlextResult.fail(f"No response data from {endpoint}")

        if not hasattr(response, "status_code") or not hasattr(response, "data"):
            return FlextResult.fail(f"Invalid response structure from {endpoint}")

        if response.status_code != FlextOracleWmsDefaults.HTTP_OK:
            return FlextResult.fail(f"HTTP {response.status_code} from {endpoint}")

        return FlextResult.ok(response)

    async def _process_entities_response(
        self,
        context: DiscoveryContext,
        response: FlextApiClientResponse,
        endpoint: str,
    ) -> FlextResult[bool]:
        """Process entities from validated response."""
        parser = EntityResponseParser(self.discovery)
        entities_result = await parser.parse_entities_response(
            response.data,
            endpoint,
        )

        if entities_result.is_success and entities_result.data:
            context.all_entities.extend(entities_result.data)
            logger.info(
                "Successfully discovered entities",
                endpoint=endpoint,
                count=len(entities_result.data),
            )
            return FlextResult.ok(DISCOVERY_SUCCESS)

        context.errors.append(f"Failed to parse entities from {endpoint}")
        return FlextResult.ok(DISCOVERY_FAILURE)

    def _handle_discovery_error(
        self,
        context: DiscoveryContext,
        error_message: str,
        endpoint: str,  # noqa: ARG002
    ) -> FlextResult[bool]:
        """Handle discovery errors consistently."""
        logger.warning(error_message)
        context.errors.append(error_message)
        return FlextResult.ok(DISCOVERY_FAILURE)


class EntityResponseParser:
    """Command Pattern: Encapsulates entity parsing logic."""

    def __init__(self, discovery_instance: FlextOracleWmsEntityDiscovery) -> None:
        """Initialize with discovery instance for delegation."""
        self.discovery = discovery_instance

    async def parse_entities_response(
        self,
        response_data: object,
        endpoint: str,
    ) -> FlextResult[list[FlextOracleWmsEntity]]:
        """Parse entities from API response data using existing logic."""
        # Delegate to existing method to maintain functionality
        return await self.discovery._parse_entities_response(response_data, endpoint)


class FlextOracleWmsEntityDiscovery:
    """Enterprise entity discovery system for Oracle WMS using flext-api patterns.

    Provides comprehensive entity discovery with multiple endpoint support,
    pattern-based filtering, and intelligent caching.
    """

    def __init__(
        self,
        api_client: FlextApiClient,
        cache_manager: object | None = None,
        environment: str = "default",
    ) -> None:
        """Initialize entity discovery system.

        Args:
            api_client: FlextApiClient for API requests
            cache_manager: Optional cache manager for results
            environment: Oracle WMS environment name

        """
        self.api_client = api_client
        self.cache_manager = cache_manager
        self.environment = environment

        # Discovery endpoints to try (in order of preference)
        self.discovery_endpoints = [
            f"/{environment}/wms/lgfapi/v10/entity/",
            f"/{environment}/wms/lgfapi/v11/entity/",
            f"/{environment}/api/entities/",
            f"/{environment}/api/v1/entities/",
            f"/{environment}/entities/",
            f"/{environment}/metadata/entities/",
            f"/{environment}/schema/entities/",
        ]

        logger.info(
            "Oracle WMS entity discovery initialized",
            endpoints_count=len(self.discovery_endpoints),
            environment=environment,
        )

    async def discover_all_entities(
        self,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        *,
        use_cache: bool = True,
    ) -> FlextResult[FlextOracleWmsDiscoveryResult]:
        """Discover all available Oracle WMS entities.

        Args:
            include_patterns: Regex patterns for entities to include
            exclude_patterns: Regex patterns for entities to exclude
            use_cache: Whether to use cached results

        Returns:
            FlextResult with discovery results

        """
        try:
            start_time = datetime.now(UTC)

            # Generate cache key
            cache_key = (
                f"discovery_all_{hash(str(include_patterns))}_"
                f"{hash(str(exclude_patterns))}"
            )

            # Try cache first if enabled
            if use_cache and self.cache_manager:
                cached_result = await self._get_cached_discovery(cache_key)
                if cached_result.is_success:
                    logger.debug("Using cached discovery results")
                    return cached_result

            # Perform fresh discovery
            discovery_result = await self._perform_discovery(
                include_patterns,
                exclude_patterns,
            )

            if not discovery_result.is_success:
                return discovery_result

            # Calculate duration
            duration_ms = (datetime.now(UTC) - start_time).total_seconds() * 1000

            # Update result with timing info
            original_data = discovery_result.data
            if original_data is None:
                return FlextResult.fail("Discovery returned no data")

            result_data = FlextOracleWmsDiscoveryResult(
                entities=original_data.entities,
                total_count=original_data.total_count,
                timestamp=start_time.isoformat(),
                discovery_duration_ms=duration_ms,
                has_errors=original_data.has_errors,
                errors=original_data.errors,
            )

            # Cache the result
            if self.cache_manager:
                await self._cache_discovery_result(cache_key, result_data)

            logger.info(
                "Entity discovery completed successfully",
                entities_found=result_data.total_count,
                duration_ms=duration_ms,
            )

            return FlextResult.ok(result_data)

        except Exception as e:
            handle_operation_exception(e, "discover all entities")
            # Never reached due to handle_operation_exception always raising
            return FlextResult.fail(f"Discovery failed: {e}")

    async def discover_entity_schema(
        self,
        entity_name: str,
        *,
        use_cache: bool = True,
    ) -> FlextResult[FlextOracleWmsEntity]:
        """Discover schema for a specific Oracle WMS entity.

        Args:
            entity_name: Name of the entity to discover
            use_cache: Whether to use cached results

        Returns:
            FlextResult with entity schema information

        """
        try:
            cache_key = f"entity_schema_{entity_name}"

            # Try cache first
            if use_cache and self.cache_manager:
                cached_result = await self._get_cached_entity(cache_key)
                if cached_result.is_success:
                    return cached_result

            # Try to get entity details from different endpoints
            entity_result = await self._discover_single_entity(entity_name)

            if not entity_result.is_success:
                return entity_result

            # Cache the result
            if self.cache_manager and entity_result.data is not None:
                await self._cache_entity_result(cache_key, entity_result.data)

            return entity_result

        except Exception as e:
            handle_operation_exception(
                e,
                "discover entity schema",
                entity_name=entity_name,
            )
            # Never reached due to handle_operation_exception always raising
            return FlextResult.fail(f"Schema discovery failed: {e}")

    async def _perform_discovery(
        self,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
    ) -> FlextResult[FlextOracleWmsDiscoveryResult]:
        """Perform actual entity discovery using Strategy Pattern.

        SOLID REFACTORING: Reduced complexity from 19 to ~5 using Strategy Pattern
        and Command Pattern to separate concerns and improve maintainability.
        """
        # Create discovery context using Parameter Object Pattern
        context = DiscoveryContext(
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            all_entities=[],
            errors=[],
        )

        # Use Strategy Pattern for endpoint discovery
        discovery_strategy = EndpointDiscoveryStrategy(self)

        # Execute discovery across endpoints using strategy
        for endpoint in self.discovery_endpoints:
            result = await discovery_strategy.execute_discovery_step(
                context, self.api_client, endpoint
            )

            if result.is_success and result.data:
                # Break on first successful endpoint
                break

        # Apply post-processing using Command Pattern
        processed_entities = self._apply_post_processing(context)

        # Create and return discovery result
        return self._create_discovery_result(processed_entities, context)

    def _apply_post_processing(
        self,
        context: DiscoveryContext,
    ) -> list[FlextOracleWmsEntity]:
        """Apply filtering and deduplication using Command Pattern."""
        entities = context.all_entities

        # Filter entities based on patterns
        if context.include_patterns or context.exclude_patterns:
            entities = self._filter_entities(
                entities,
                context.include_patterns,
                context.exclude_patterns,
            )

        # Remove duplicates
        return self._deduplicate_entities(entities)

    def _create_discovery_result(
        self,
        entities: list[FlextOracleWmsEntity],
        context: DiscoveryContext,
    ) -> FlextResult[FlextOracleWmsDiscoveryResult]:
        """Create discovery result object."""
        discovery_result = FlextOracleWmsDiscoveryResult(
            entities=entities,
            total_count=len(entities),
            timestamp=datetime.now(UTC).isoformat(),
            has_errors=len(context.errors) > 0,
            errors=context.errors,
        )

        return FlextResult.ok(discovery_result)

    def _extract_entity_list_from_response(
        self,
        response_data: dict[str, object] | list[object] | object,
        endpoint: str,
    ) -> FlextResult[list[object]]:
        """Extract entity list from API response."""
        if isinstance(response_data, dict):
            # Handle different response formats with type validation
            if "entities" in response_data:
                entities_data = response_data["entities"]
                if isinstance(entities_data, list):
                    return FlextResult.ok(entities_data)
            if "results" in response_data:
                results_data = response_data["results"]
                if isinstance(results_data, list):
                    return FlextResult.ok(results_data)
            if "data" in response_data:
                data_data = response_data["data"]
                if isinstance(data_data, list):
                    return FlextResult.ok(data_data)
            # Try to extract entity names from keys
            return FlextResult.ok(list(response_data.keys()))
        if isinstance(response_data, list):
            return FlextResult.ok(response_data)
        return FlextResult.fail(f"Unexpected response format from {endpoint}")

    def _create_entity_from_string_name(self, name: str) -> FlextOracleWmsEntity:
        """Create entity from string name."""
        return FlextOracleWmsEntity(
            name=name,
            endpoint=f"/{self.environment}/wms/lgfapi/v10/entity/{name}/",
            description=f"Oracle WMS entity: {name}",
        )

    def _create_entity_from_metadata(
        self,
        item: dict[str, object],
    ) -> FlextOracleWmsEntity | None:
        """Create entity from metadata dictionary."""
        name = item.get("name", item.get("entity_name", ""))
        if not name:
            return None

        # Extract and validate fields with proper type casting
        fields_data = item.get("fields")
        entity_fields: dict[str, object] | None = (
            fields_data if isinstance(fields_data, dict) else None
        )

        return FlextOracleWmsEntity(
            name=str(name),
            endpoint=str(
                item.get(
                    "endpoint",
                    f"/{self.environment}/wms/lgfapi/v10/entity/{name}/",
                ),
            ),
            description=str(
                item.get(
                    "description",
                    f"Oracle WMS entity: {name}",
                ),
            ),
            primary_key=str(item.get("primary_key"))
            if item.get("primary_key")
            else None,
            replication_key=str(item.get("replication_key"))
            if item.get("replication_key")
            else None,
            supports_incremental=bool(item.get("supports_incremental")),
            fields=entity_fields,
        )

    async def _parse_entities_response(
        self,
        response_data: dict[str, object] | list[object] | object,
        endpoint: str,
    ) -> FlextResult[list[FlextOracleWmsEntity]]:
        """Parse entities from API response data."""
        try:
            # Extract entity list from response
            entity_list_result = self._extract_entity_list_from_response(
                response_data,
                endpoint,
            )
            if not entity_list_result.is_success:
                return FlextResult.fail(
                    entity_list_result.error or "Entity list extraction failed",
                )

            # Convert items to FlextOracleWmsEntity objects
            entities = []
            if entity_list_result.data is None:
                return FlextResult.ok([])

            for item in entity_list_result.data:
                if isinstance(item, str):
                    entity = self._create_entity_from_string_name(item)
                    entities.append(entity)
                elif isinstance(item, dict):
                    entity_result = self._create_entity_from_metadata(item)
                    if entity_result is not None:
                        entities.append(entity_result)

            logger.debug(
                "Parsed entities from response",
                count=len(entities),
                endpoint=endpoint,
            )
            return FlextResult.ok(entities)

        except Exception as e:
            handle_operation_exception(e, "parse entities response", endpoint=endpoint)
            # Never reached due to handle_operation_exception always raising
            return FlextResult.fail(f"Parse entities failed: {e}")

    async def _discover_single_entity(
        self,
        entity_name: str,
    ) -> FlextResult[FlextOracleWmsEntity]:
        """Discover details for a single entity."""
        # Try to get entity details from LGF API
        detail_endpoints = [
            f"/{self.environment}/wms/lgfapi/v10/entity/{entity_name}/",
            f"/{self.environment}/api/entities/{entity_name}/",
            f"/{self.environment}/metadata/entities/{entity_name}/",
        ]

        for endpoint in detail_endpoints:
            try:
                response_result = await self.api_client.get(endpoint)

                if (
                    response_result.is_success
                    and response_result.data is not None
                    and response_result.data.status_code
                    == FlextOracleWmsDefaults.HTTP_OK
                ):
                    # Try to extract schema information
                    schema_result = await self._extract_entity_schema(
                        response_result.data.data,
                        entity_name,
                        endpoint,
                    )
                    if schema_result.is_success:
                        return schema_result

            except Exception as e:
                logger.debug(
                    "Failed to get entity details",
                    entity_name=entity_name,
                    endpoint=endpoint,
                    error=str(e),
                )
                continue

        # Fallback: create basic entity
        entity = FlextOracleWmsEntity(
            name=entity_name,
            endpoint=f"/{self.environment}/wms/lgfapi/v10/entity/{entity_name}/",
            description=f"Oracle WMS entity: {entity_name}",
        )

        return FlextResult.ok(entity)

    async def _extract_entity_schema(
        self,
        response_data: dict[str, object] | list[object] | object,
        entity_name: str,
        endpoint: str,
    ) -> FlextResult[FlextOracleWmsEntity]:
        """Extract entity schema from response data."""
        try:
            fields: dict[str, object] = {}

            # Try to sample data to infer schema
            if isinstance(response_data, dict):
                results_data = response_data.get("results")
                if isinstance(results_data, list) and results_data:
                    sample_record = results_data[0]
                    if isinstance(sample_record, dict):
                        fields = {
                            key: {"type": self._infer_field_type(value)}
                            for key, value in sample_record.items()
                        }
                else:
                    data_data = response_data.get("data")
                    if isinstance(data_data, list) and data_data:
                        sample_record = data_data[0]
                        if isinstance(sample_record, dict):
                            fields = {
                                key: {"type": self._infer_field_type(value)}
                                for key, value in sample_record.items()
                            }

            entity = FlextOracleWmsEntity(
                name=entity_name,
                endpoint=endpoint,
                description=f"Oracle WMS entity: {entity_name}",
                fields=fields,
            )

            return FlextResult.ok(entity)

        except Exception as e:
            handle_operation_exception(
                e,
                "extract entity schema",
                entity_name=entity_name,
            )
            # Never reached due to handle_operation_exception always raising
            return FlextResult.fail(f"Extract schema failed: {e}")

    def _infer_field_type(self, value: object) -> str:
        """Infer field type from sample value."""
        if value is None:
            return "string"
        if isinstance(value, bool):
            return "boolean"
        if isinstance(value, int):
            return "integer"
        if isinstance(value, float):
            return "number"
        if isinstance(value, (dict, list)):
            return "object"
        return "string"

    def _filter_entities(
        self,
        entities: list[FlextOracleWmsEntity],
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
    ) -> list[FlextOracleWmsEntity]:
        """Filter entities based on include/exclude patterns."""
        filtered_entities = entities

        # Apply include patterns using list comprehension
        if include_patterns:
            filtered_entities = [
                entity
                for entity in filtered_entities
                if any(
                    re.search(pattern, entity.name, re.IGNORECASE)
                    for pattern in include_patterns
                )
            ]

        # Apply exclude patterns using list comprehension
        if exclude_patterns:
            filtered_entities = [
                entity
                for entity in filtered_entities
                if not any(
                    re.search(pattern, entity.name, re.IGNORECASE)
                    for pattern in exclude_patterns
                )
            ]

        return filtered_entities

    def _deduplicate_entities(
        self,
        entities: list[FlextOracleWmsEntity],
    ) -> list[FlextOracleWmsEntity]:
        """Remove duplicate entities based on name."""
        seen_names = set()
        unique_entities = []

        for entity in entities:
            if entity.name not in seen_names:
                seen_names.add(entity.name)
                unique_entities.append(entity)

        return unique_entities

    async def _get_cached_discovery(
        self,
        cache_key: str,
    ) -> FlextResult[FlextOracleWmsDiscoveryResult]:
        """Get cached discovery result."""
        # Implementation would depend on cache manager interface
        logger.debug("Cache lookup attempted", cache_key=cache_key)
        return FlextResult.fail("Cache not implemented")

    async def _cache_discovery_result(
        self,
        cache_key: str,
        result: FlextOracleWmsDiscoveryResult,
    ) -> None:
        """Cache discovery result."""
        # Implementation would depend on cache manager interface

    async def _get_cached_entity(
        self,
        cache_key: str,
    ) -> FlextResult[FlextOracleWmsEntity]:
        """Get cached entity result."""
        # Implementation would depend on cache manager interface
        logger.debug("Entity cache lookup attempted", cache_key=cache_key)
        return FlextResult.fail("Cache not implemented")

    async def _cache_entity_result(
        self,
        cache_key: str,
        entity: FlextOracleWmsEntity,
    ) -> None:
        """Cache entity result."""
        # Implementation would depend on cache manager interface


# Factory function for easy usage
def flext_oracle_wms_create_entity_discovery(
    api_client: FlextApiClient,
    environment: str,
    *,
    enable_caching: bool = True,
    cache_ttl: int = 300,
) -> FlextOracleWmsEntityDiscovery:
    """Create entity discovery.

    Args:
        api_client: FlextApiClient instance
        environment: Oracle WMS environment
        enable_caching: Whether to enable caching
        cache_ttl: Cache TTL in seconds

    Returns:
        Configured entity discovery

    """
    # Create cache manager if caching is enabled
    cache_manager = None
    if enable_caching:
        # Use basic object placeholder for cache manager
        cache_manager = {"enabled": True, "ttl": cache_ttl}

    return FlextOracleWmsEntityDiscovery(
        api_client=api_client,
        cache_manager=cache_manager,
        environment=environment,
    )
