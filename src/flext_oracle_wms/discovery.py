"""Enterprise Entity Discovery for Oracle WMS.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Advanced entity discovery system with multiple endpoint support and caching.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import TYPE_CHECKING, Any

# Import from flext-core root namespace as required
from flext_core import FlextResult, get_logger

from flext_oracle_wms.constants import FlextOracleWmsEntityTypes
from flext_oracle_wms.models import FlextOracleWmsDiscoveryResult, FlextOracleWmsEntity

if TYPE_CHECKING:
    import httpx

    from flext_oracle_wms.cache import (
        FlextOracleWmsCacheManager,
    )

logger = get_logger(__name__)


class FlextOracleWmsEntityDiscovery:
    """Enterprise entity discovery system for Oracle WMS.

    Provides comprehensive entity discovery with multiple endpoint support,
    pattern-based filtering, and intelligent caching.
    """

    def __init__(
        self,
        client: httpx.Client,
        cache_manager: FlextOracleWmsCacheManager | None = None,
    ) -> None:
        """Initialize entity discovery system.

        Args:
            client: HTTP client for API requests
            cache_manager: Optional cache manager for results

        """
        self.client = client
        self.cache_manager = cache_manager

        # Discovery endpoints to try (in order of preference)
        self.discovery_endpoints = [
            "/api/entities",
            "/api/v1/entities",
            "/wms/lgfapi/v10/entity",
            "/wms/lgfapi/v11/entity",
            "/entities",
            "/metadata/entities",
            "/schema/entities",
        ]

        logger.info(
            "FlextOracleWms entity discovery initialized with %d endpoints",
            len(self.discovery_endpoints),
        )

    def flext_oracle_wms_discover_all_entities(  # noqa: C901
        self,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
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
        cache_key = (
            f"discovery_all_{hash(str(include_patterns))}_{hash(str(exclude_patterns))}"
        )

        # Try cache first if enabled
        if use_cache and self.cache_manager:
            cached_result = self.cache_manager.flext_oracle_wms_get_metadata(cache_key)
            if cached_result:
                logger.debug("Using cached discovery results")
                return FlextResult.ok(cached_result)

        try:
            discovered_entities = []

            # Try each discovery endpoint
            for endpoint in self.discovery_endpoints:
                try:
                    logger.debug("Trying discovery endpoint: %s", endpoint)
                    response = self.client.get(endpoint)

                    if response.status_code == 200:
                        entities = self._parse_discovery_response(
                            response.json(),
                            endpoint,
                        )
                        if entities:
                            discovered_entities.extend(entities)
                            logger.info(
                                "Discovered %d entities from %s",
                                len(entities),
                                endpoint,
                            )
                            break  # Success, stop trying other endpoints

                except Exception as e:
                    logger.debug("Discovery endpoint %s failed: %s", endpoint, e)
                    continue

            # If no entities discovered via API, use fallback
            if not discovered_entities:
                logger.warning(
                    "No entities discovered via API, using fallback entities",
                )
                discovered_entities = self._get_fallback_entities()

            # Apply filters
            if include_patterns or exclude_patterns:
                discovered_entities = self._filter_entities(
                    discovered_entities,
                    include_patterns,
                    exclude_patterns,
                )

            # Create discovery result
            result = FlextOracleWmsDiscoveryResult(
                entities=discovered_entities,
                total_count=len(discovered_entities),
                timestamp=self._get_current_timestamp(),
                has_errors=False,
                errors=[],
            )

            # Cache result if cache manager available
            if use_cache and self.cache_manager:
                cache_result = self.cache_manager.flext_oracle_wms_set_metadata(
                    cache_key,
                    result,
                    ttl=3600,  # Cache for 1 hour
                )
                if not cache_result:
                    logger.warning("Failed to cache discovery results")

            logger.info(
                "Entity discovery completed: %d entities found",
                len(discovered_entities),
            )
            return FlextResult.ok(result)

        except Exception as e:
            logger.exception("Entity discovery failed: %s", e)
            return FlextResult.fail(f"Discovery failed: {e}")

    def flext_oracle_wms_discover_entity_details(  # noqa: C901
        self,
        entity_name: str,
        use_cache: bool = True,
    ) -> FlextResult[FlextOracleWmsEntity]:
        """Discover detailed information for a specific entity.

        Args:
            entity_name: Name of entity to discover
            use_cache: Whether to use cached results

        Returns:
            FlextResult with detailed entity information

        """
        cache_key = f"entity_details_{entity_name}"

        # Try cache first
        if use_cache and self.cache_manager:
            cached_result = self.cache_manager.flext_oracle_wms_get_metadata(cache_key)
            if cached_result:
                logger.debug("Using cached entity details for %s", entity_name)
                return FlextResult.ok(cached_result)

        try:
            # Try different metadata endpoints for the entity
            metadata_endpoints = [
                f"/api/{entity_name}/metadata",
                f"/api/v1/{entity_name}/schema",
                f"/wms/lgfapi/v10/entity/{entity_name}/metadata",
                f"/entities/{entity_name}/schema",
                f"/metadata/{entity_name}",
            ]

            entity_details = None

            for endpoint in metadata_endpoints:
                try:
                    logger.debug("Trying entity metadata endpoint: %s", endpoint)
                    response = self.client.get(endpoint)

                    if response.status_code == 200:
                        metadata = response.json()
                        entity_details = self._parse_entity_metadata(
                            entity_name,
                            metadata,
                        )
                        if entity_details:
                            logger.info(
                                "Retrieved metadata for entity: %s",
                                entity_name,
                            )
                            break

                except Exception as e:
                    logger.debug("Entity metadata endpoint %s failed: %s", endpoint, e)
                    continue

            # If no metadata found, create basic entity
            if not entity_details:
                logger.warning(
                    "No metadata found for %s, creating basic entity",
                    entity_name,
                )
                entity_details = FlextOracleWmsEntity(
                    name=entity_name,
                    description=f"Oracle WMS {entity_name} entity",
                    fields={},
                    endpoint=f"/api/{entity_name}",
                )

            # Cache result
            if use_cache and self.cache_manager:
                cache_result = self.cache_manager.flext_oracle_wms_set_metadata(
                    cache_key,
                    entity_details,
                    ttl=1800,  # Cache for 30 minutes
                )
                if not cache_result:
                    logger.warning("Failed to cache entity details")

            return FlextResult.ok(entity_details)

        except Exception as e:
            logger.exception(
                "Entity detail discovery failed for %s: %s",
                entity_name,
                e,
            )
            return FlextResult.fail(f"Entity detail discovery failed: {e}")

    def _parse_discovery_response(
        self,
        data: object,
        endpoint: str,
    ) -> list[FlextOracleWmsEntity]:
        """Parse discovery response into entity list."""
        entities = []

        try:
            # Handle different response formats
            if isinstance(data, list):
                # Direct list of entity names or objects
                for item in data:
                    entity = self._create_entity_from_item(item, endpoint)
                    if entity:
                        entities.append(entity)

            elif isinstance(data, dict):
                # Check common data keys
                for key in ["data", "entities", "results", "items"]:
                    if key in data and isinstance(data[key], list):
                        for item in data[key]:
                            entity = self._create_entity_from_item(item, endpoint)
                            if entity:
                                entities.append(entity)
                        break

        except Exception as e:
            logger.warning(
                "Failed to parse discovery response from %s: %s",
                endpoint,
                e,
            )

        return entities

    def _create_entity_from_item(
        self,
        item: object,
        endpoint: str,
    ) -> FlextOracleWmsEntity | None:
        """Create entity from discovery response item."""
        try:
            if isinstance(item, str):
                # Simple string entity name
                return FlextOracleWmsEntity(
                    name=item,
                    description=f"Oracle WMS {item} entity",
                    fields={},
                    endpoint=f"/api/{item}",
                )

            if isinstance(item, dict):
                # Structured entity object
                name = (
                    item.get("name")
                    or item.get("entity_name")
                    or item.get("table_name")
                )
                if name:
                    return FlextOracleWmsEntity(
                        name=name,
                        description=item.get(
                            "description",
                            f"Oracle WMS {name} entity",
                        ),
                        fields=item.get("fields", {}),
                        endpoint=item.get("endpoint", f"/api/{name}"),
                    )

        except Exception as e:
            logger.debug("Failed to create entity from item %s: %s", item, e)

        return None

    def _parse_entity_metadata(
        self,
        entity_name: str,
        metadata: dict[str, Any],
    ) -> FlextOracleWmsEntity:
        """Parse entity metadata into FlextOracleWmsEntity."""
        return FlextOracleWmsEntity(
            name=entity_name,
            description=metadata.get("description", f"Oracle WMS {entity_name} entity"),
            fields=metadata.get("fields", {}),
            endpoint=metadata.get("endpoint", f"/api/{entity_name}"),
            primary_key=metadata.get("primary_key"),
            replication_key=metadata.get("replication_key"),
            supports_incremental=metadata.get("supports_incremental", False),
        )

    def _filter_entities(
        self,
        entities: list[FlextOracleWmsEntity],
        include_patterns: list[str] | None,
        exclude_patterns: list[str] | None,
    ) -> list[FlextOracleWmsEntity]:
        """Filter entities based on regex patterns."""
        filtered = entities

        # Apply include patterns
        if include_patterns:
            include_regexes = [re.compile(pattern) for pattern in include_patterns]
            filtered = [
                entity
                for entity in filtered
                if any(regex.search(entity.name) for regex in include_regexes)
            ]

        # Apply exclude patterns
        if exclude_patterns:
            exclude_regexes = [re.compile(pattern) for pattern in exclude_patterns]
            filtered = [
                entity
                for entity in filtered
                if not any(regex.search(entity.name) for regex in exclude_regexes)
            ]

        return filtered

    def _get_fallback_entities(self) -> list[FlextOracleWmsEntity]:
        """Get fallback entities when discovery fails."""
        fallback_entities = []

        for entity_name in FlextOracleWmsEntityTypes.ALL_ENTITIES:
            entity = FlextOracleWmsEntity(
                name=entity_name,
                description=f"Oracle WMS {entity_name} entity (fallback)",
                fields={},
                endpoint=f"/api/{entity_name}",
            )
            fallback_entities.append(entity)

        logger.info("Using %d fallback entities", len(fallback_entities))
        return fallback_entities

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()


def flext_oracle_wms_create_entity_discovery(
    client: httpx.Client,
    cache_manager: FlextOracleWmsCacheManager | None = None,
) -> FlextOracleWmsEntityDiscovery:
    """Create entity discovery system.

    Args:
        client: HTTP client for API requests
        cache_manager: Optional cache manager

    Returns:
        Configured entity discovery instance

    """
    return FlextOracleWmsEntityDiscovery(client, cache_manager)


__all__ = ["FlextOracleWmsEntityDiscovery", "flext_oracle_wms_create_entity_discovery"]
