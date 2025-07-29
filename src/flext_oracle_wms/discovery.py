"""Enterprise Entity Discovery for Oracle WMS.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Advanced entity discovery system using flext-api client with caching and intelligent
discovery.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from flext_core import FlextResult, get_logger

from flext_oracle_wms.constants import FlextOracleWmsDefaults
from flext_oracle_wms.models import FlextOracleWmsDiscoveryResult, FlextOracleWmsEntity

if TYPE_CHECKING:
    from flext_api import FlextApiClient

logger = get_logger(__name__)


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
                include_patterns, exclude_patterns
            )

            if not discovery_result.is_success:
                return discovery_result

            # Calculate duration
            duration_ms = (datetime.now(UTC) - start_time).total_seconds() * 1000

            # Update result with timing info
            result_data = discovery_result.data
            result_data = FlextOracleWmsDiscoveryResult(
                entities=result_data.entities,
                total_count=result_data.total_count,
                timestamp=start_time.isoformat(),
                discovery_duration_ms=duration_ms,
                has_errors=result_data.has_errors,
                errors=result_data.errors,
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
            logger.exception("Entity discovery failed")
            return FlextResult.fail(f"Discovery failed: {e}")

    async def discover_entity_schema(
        self, entity_name: str, *, use_cache: bool = True
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
            if self.cache_manager:
                await self._cache_entity_result(cache_key, entity_result.data)

            return entity_result

        except Exception as e:
            logger.exception("Entity schema discovery failed", entity_name=entity_name)
            return FlextResult.fail(f"Schema discovery failed for {entity_name}: {e}")

    async def _perform_discovery(
        self,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
    ) -> FlextResult[FlextOracleWmsDiscoveryResult]:
        """Perform actual entity discovery across multiple endpoints."""
        all_entities = []
        errors = []

        for endpoint in self.discovery_endpoints:
            try:
                logger.debug("Trying discovery endpoint", endpoint=endpoint)

                # Use FlextApiClient to make the request
                response_result = await self.api_client.get(endpoint)

                if not response_result.is_success:
                    error_msg = f"Failed to call {endpoint}: {response_result.error}"
                    logger.warning(error_msg)
                    errors.append(error_msg)
                    continue

                response = response_result.data

                if response.status_code != FlextOracleWmsDefaults.HTTP_OK:
                    error_msg = f"HTTP {response.status_code} from {endpoint}"
                    logger.warning(error_msg)
                    errors.append(error_msg)
                    continue

                # Parse entities from response
                entities_result = await self._parse_entities_response(
                    response.data, endpoint
                )

                if entities_result.is_success and entities_result.data:
                    all_entities.extend(entities_result.data)
                    logger.info(
                        "Successfully discovered entities",
                        endpoint=endpoint,
                        count=len(entities_result.data),
                    )
                    break  # Use first successful endpoint
                errors.append(f"Failed to parse entities from {endpoint}")

            except Exception as e:
                error_msg = f"Exception calling {endpoint}: {e}"
                logger.exception(error_msg)
                errors.append(error_msg)
                continue

        # Filter entities based on patterns
        if include_patterns or exclude_patterns:
            all_entities = self._filter_entities(
                all_entities, include_patterns, exclude_patterns
            )

        # Remove duplicates
        unique_entities = self._deduplicate_entities(all_entities)

        # Create discovery result
        discovery_result = FlextOracleWmsDiscoveryResult(
            entities=unique_entities,
            total_count=len(unique_entities),
            timestamp=datetime.now(UTC).isoformat(),
            has_errors=len(errors) > 0,
            errors=errors,
        )

        return FlextResult.ok(discovery_result)

    def _extract_entity_list_from_response(
        self, response_data: dict[str, object] | list[object] | object, endpoint: str
    ) -> FlextResult[list[object]]:
        """Extract entity list from API response."""
        if isinstance(response_data, dict):
            # Handle different response formats
            if "entities" in response_data:
                return FlextResult.ok(response_data["entities"])
            if "results" in response_data:
                return FlextResult.ok(response_data["results"])
            if "data" in response_data:
                return FlextResult.ok(response_data["data"])
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
        self, item: dict[str, object]
    ) -> FlextOracleWmsEntity | None:
        """Create entity from metadata dictionary."""
        name = item.get("name", item.get("entity_name", ""))
        if not name:
            return None

        return FlextOracleWmsEntity(
            name=str(name),
            endpoint=str(item.get(
                "endpoint",
                f"/{self.environment}/wms/lgfapi/v10/entity/{name}/",
            )),
            description=str(item.get(
                "description", f"Oracle WMS entity: {name}"
            )),
            primary_key=item.get("primary_key"),
            replication_key=item.get("replication_key"),
            supports_incremental=bool(item.get("supports_incremental", False)),
            fields=dict(item.get("fields", {})),
        )

    async def _parse_entities_response(
        self, response_data: dict[str, object] | list[object] | object, endpoint: str
    ) -> FlextResult[list[FlextOracleWmsEntity]]:
        """Parse entities from API response data."""
        try:
            # Extract entity list from response
            entity_list_result = self._extract_entity_list_from_response(response_data, endpoint)
            if not entity_list_result.is_success:
                return entity_list_result

            # Convert items to FlextOracleWmsEntity objects
            entities = []
            for item in entity_list_result.data:
                if isinstance(item, str):
                    entity = self._create_entity_from_string_name(item)
                    entities.append(entity)
                elif isinstance(item, dict):
                    entity = self._create_entity_from_metadata(item)
                    if entity:
                        entities.append(entity)

            logger.debug(
                "Parsed entities from response", count=len(entities), endpoint=endpoint
            )
            return FlextResult.ok(entities)

        except Exception as e:
            logger.exception("Failed to parse entities response", endpoint=endpoint)
            return FlextResult.fail(f"Failed to parse entities from {endpoint}: {e}")

    async def _discover_single_entity(
        self, entity_name: str
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
                    and response_result.data.status_code
                    == FlextOracleWmsDefaults.HTTP_OK
                ):
                    # Try to extract schema information
                    schema_result = await self._extract_entity_schema(
                        response_result.data.data, entity_name, endpoint
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
        endpoint: str
    ) -> FlextResult[FlextOracleWmsEntity]:
        """Extract entity schema from response data."""
        try:
            fields = {}

            # Try to sample data to infer schema
            if isinstance(response_data, dict):
                if response_data.get("results"):
                    sample_record = response_data["results"][0]
                    if isinstance(sample_record, dict):
                        fields = {
                            key: {"type": self._infer_field_type(value)}
                            for key, value in sample_record.items()
                        }
                elif response_data.get("data"):
                    sample_record = response_data["data"][0]
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
            logger.exception("Failed to extract entity schema", entity_name=entity_name)
            return FlextResult.fail(f"Schema extraction failed: {e}")

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

        # Apply include patterns
        if include_patterns:
            included = []
            for entity in filtered_entities:
                if any(
                    re.search(pattern, entity.name, re.IGNORECASE)
                    for pattern in include_patterns
                ):
                    included.append(entity)
            filtered_entities = included

        # Apply exclude patterns
        if exclude_patterns:
            excluded = []
            for entity in filtered_entities:
                if not any(
                    re.search(pattern, entity.name, re.IGNORECASE)
                    for pattern in exclude_patterns
                ):
                    excluded.append(entity)
            filtered_entities = excluded

        return filtered_entities

    def _deduplicate_entities(
        self, entities: list[FlextOracleWmsEntity]
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
        self, cache_key: str
    ) -> FlextResult[FlextOracleWmsDiscoveryResult]:
        """Get cached discovery result."""
        # Implementation would depend on cache manager interface
        return FlextResult.fail("Cache not implemented")

    async def _cache_discovery_result(
        self, cache_key: str, result: FlextOracleWmsDiscoveryResult
    ) -> None:
        """Cache discovery result."""
        # Implementation would depend on cache manager interface

    async def _get_cached_entity(
        self, cache_key: str
    ) -> FlextResult[FlextOracleWmsEntity]:
        """Get cached entity result."""
        # Implementation would depend on cache manager interface
        return FlextResult.fail("Cache not implemented")

    async def _cache_entity_result(
        self, cache_key: str, entity: FlextOracleWmsEntity
    ) -> None:
        """Cache entity result."""
        # Implementation would depend on cache manager interface


# Factory function for easy usage
def flext_oracle_wms_create_entity_discovery(
    api_client: FlextApiClient,
    environment: str,
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
    return FlextOracleWmsEntityDiscovery(
        api_client=api_client,
        environment=environment,
        enable_caching=enable_caching,
        cache_ttl=cache_ttl,
    )
