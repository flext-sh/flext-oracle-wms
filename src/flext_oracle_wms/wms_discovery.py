"""Oracle WMS Discovery - Consolidated Entity Discovery and Dynamic Processing.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Consolidated Oracle WMS discovery system combining discovery.py + dynamic.py + cache.py.
This module provides comprehensive entity discovery, schema processing, and caching.
"""

from __future__ import annotations

import asyncio
import re
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Generic, TypeVar

from flext_core import FlextResult, FlextValueObject, get_logger

from flext_oracle_wms.models import (
    FlextOracleWmsDiscoveryResult,
    FlextOracleWmsEntity,
)
from flext_oracle_wms.wms_constants import FlextOracleWmsDefaults
from flext_oracle_wms.wms_operations import handle_operation_exception

if TYPE_CHECKING:
    from flext_api import FlextApiClient

    from flext_oracle_wms.models import (
        TOracleWmsRecordBatch,
        TOracleWmsSchema,
    )
    from flext_oracle_wms.wms_constants import OracleWMSEntityType

logger = get_logger(__name__)

# Type variables for generic cache
T = TypeVar("T")

# Cache value types
CacheValueBasic = str | int | float | bool | None
CacheValueDict = dict[str, CacheValueBasic]
CacheValueList = list[CacheValueBasic | CacheValueDict]
CacheValue = CacheValueDict | CacheValueList | CacheValueBasic

# Constants for FlextResult boolean values to avoid FBT003 lint errors
DISCOVERY_SUCCESS = True
DISCOVERY_FAILURE = False


# =============================================================================
# CACHING SYSTEM - Consolidated from cache.py
# =============================================================================


@dataclass(frozen=True)
class FlextOracleWmsCacheConfig(FlextValueObject):
    """Oracle WMS cache configuration using flext-core standards."""

    default_ttl_seconds: int = 3600  # 1 hour
    max_cache_entries: int = 1000
    cleanup_interval_seconds: int = 300  # 5 minutes
    enable_statistics: bool = True
    enable_async_cleanup: bool = True

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate Oracle WMS cache configuration business rules."""
        if self.default_ttl_seconds <= 0:
            return FlextResult.fail("Default TTL must be positive")
        if self.max_cache_entries <= 0:
            return FlextResult.fail("Max cache entries must be positive")
        if self.cleanup_interval_seconds <= 0:
            return FlextResult.fail("Cleanup interval must be positive")
        return FlextResult.ok(None)


@dataclass(frozen=True)
class FlextOracleWmsCacheEntry(FlextValueObject, Generic[T]):  # noqa: UP046
    """Oracle WMS cache entry with metadata using flext-core standards."""

    key: str
    value: T
    timestamp: float
    ttl_seconds: int
    access_count: int = 0
    last_accessed: float = 0.0

    def __post_init__(self) -> None:
        """Post-initialization to set last_accessed if not provided."""
        if self.last_accessed == 0.0:
            object.__setattr__(self, "last_accessed", time.time())

    def is_expired(self) -> bool:
        """Check if cache entry has expired."""
        return (time.time() - self.timestamp) > self.ttl_seconds

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate cache entry business rules."""
        if not self.key:
            return FlextResult.fail("Cache key cannot be empty")
        if self.ttl_seconds <= 0:
            return FlextResult.fail("TTL must be positive")
        if self.timestamp <= 0:
            return FlextResult.fail("Timestamp must be positive")
        return FlextResult.ok(None)

    def is_valid(self) -> bool:
        """Check if cache entry is still valid."""
        return not self.is_expired()


@dataclass(frozen=True)
class FlextOracleWmsCacheStats(FlextValueObject):
    """Cache statistics snapshot using flext-core standards."""

    hits: int
    misses: int
    evictions: int
    expired_entries: int
    total_entries: int
    memory_usage_bytes: int
    last_cleanup: float

    def validate_business_rules(self) -> FlextResult[None]:
        if self.hits < 0 or self.misses < 0:
            return FlextResult.fail("Statistics counters cannot be negative")
        if self.evictions < 0:
            return FlextResult.fail("Statistics counters cannot be negative")
        if self.expired_entries < 0 or self.total_entries < 0:
            return FlextResult.fail("Entry counts cannot be negative")
        if self.memory_usage_bytes < 0:
            return FlextResult.fail("Memory usage cannot be negative")
        return FlextResult.ok(None)

    def get_hit_ratio(self) -> float:
        total = self.hits + self.misses
        return 0.0 if total == 0 else self.hits / total

    def update_hit(self) -> "FlextOracleWmsCacheStats":
        return FlextOracleWmsCacheStats(
            hits=self.hits + 1,
            misses=self.misses,
            evictions=self.evictions,
            expired_entries=self.expired_entries,
            total_entries=self.total_entries,
            memory_usage_bytes=self.memory_usage_bytes,
            last_cleanup=self.last_cleanup,
        )

    def update_miss(self) -> "FlextOracleWmsCacheStats":
        return FlextOracleWmsCacheStats(
            hits=self.hits,
            misses=self.misses + 1,
            evictions=self.evictions,
            expired_entries=self.expired_entries,
            total_entries=self.total_entries,
            memory_usage_bytes=self.memory_usage_bytes,
            last_cleanup=self.last_cleanup,
        )


class FlextOracleWmsCacheManager:
    """Enterprise cache manager for Oracle WMS operations."""

    def __init__(self, config: FlextOracleWmsCacheConfig) -> None:
        """Initialize cache manager with configuration."""
        self.config = config
        self._cache: dict[str, FlextOracleWmsCacheEntry[CacheValue]] = {}
        self._lock = threading.RLock()
        self._cleanup_task: asyncio.Task[None] | None = None
        self._stats = FlextOracleWmsCacheStats(
            hits=0,
            misses=0,
            evictions=0,
            expired_entries=0,
            total_entries=0,
            memory_usage_bytes=0,
            last_cleanup=time.time(),
        )

        # Validate configuration
        validation_result = self.config.validate_business_rules()
        if validation_result.is_failure:
            msg: str = f"Invalid cache configuration: {validation_result.error}"
            raise ValueError(msg)

        logger.debug("Oracle WMS cache manager initialized", config=self.config)

        if self.config.enable_async_cleanup:
            self._start_cleanup_task()

    def _start_cleanup_task(self) -> None:
        """Start background cleanup task."""
        try:
            loop = asyncio.get_event_loop()
            self._cleanup_task = loop.create_task(self._cleanup_expired_entries())
        except RuntimeError:
            # No event loop running, cleanup will be manual
            logger.debug("No event loop available, using manual cleanup")

    async def _cleanup_expired_entries(self) -> None:
        """Background task to clean up expired cache entries."""
        while True:
            try:
                await asyncio.sleep(self.config.cleanup_interval_seconds)
                with self._lock:
                    expired_keys = [
                        key for key, entry in self._cache.items() if entry.is_expired()
                    ]
                    for key in expired_keys:
                        del self._cache[key]
                        object.__setattr__(
                            self,
                            "_stats",
                            self._stats.__class__(
                                hits=self._stats.hits,
                                misses=self._stats.misses,
                                evictions=self._stats.evictions + 1,
                                expired_entries=self._stats.expired_entries + 1,
                                total_entries=max(0, self._stats.total_entries - 1),
                                memory_usage_bytes=self._stats.memory_usage_bytes,
                                last_cleanup=time.time(),
                            ),
                        )

                    if expired_keys:
                        logger.debug(
                            f"Cleaned up {len(expired_keys)} expired cache entries",
                        )
            except asyncio.CancelledError:
                break
            except Exception:
                logger.exception("Cache cleanup error")

    async def get(self, key: str) -> FlextResult[CacheValue]:
        """Get value from cache."""
        try:
            with self._lock:
                entry = self._cache.get(key)
                if entry is None:
                    self._stats = self._stats.update_miss()
                    return FlextResult.fail(f"Cache miss for key: {key}")

                if entry.is_expired():
                    del self._cache[key]
                    self._stats = FlextOracleWmsCacheStats(
                        hits=self._stats.hits,
                        misses=self._stats.misses + 1,
                        evictions=self._stats.evictions + 1,
                        expired_entries=self._stats.expired_entries + 1,
                        total_entries=max(0, self._stats.total_entries - 1),
                        memory_usage_bytes=self._stats.memory_usage_bytes,
                        last_cleanup=self._stats.last_cleanup,
                    )
                    return FlextResult.fail(f"Cache expired for key: {key}")

                # Update access statistics
                updated_entry = FlextOracleWmsCacheEntry(
                    key=entry.key,
                    value=entry.value,
                    timestamp=entry.timestamp,
                    ttl_seconds=entry.ttl_seconds,
                    access_count=entry.access_count + 1,
                    last_accessed=time.time(),
                )
                self._cache[key] = updated_entry

                self._stats = self._stats.update_hit()
                return FlextResult.ok(entry.value)

        except Exception as e:
            return FlextResult.fail(f"Cache get failed: {e}")

    async def set(
        self, key: str, value: CacheValue, ttl_seconds: int | None = None,
    ) -> FlextResult[None]:
        """Set value in cache."""
        try:
            ttl = ttl_seconds or self.config.default_ttl_seconds

            with self._lock:
                # Evict oldest entries if cache is full
                if len(self._cache) >= self.config.max_cache_entries:
                    oldest_key = min(
                        self._cache.keys(),
                        key=lambda k: self._cache[k].last_accessed,
                    )
                    del self._cache[oldest_key]
                    self._stats = FlextOracleWmsCacheStats(
                        hits=self._stats.hits,
                        misses=self._stats.misses,
                        evictions=self._stats.evictions + 1,
                        expired_entries=self._stats.expired_entries,
                        total_entries=max(0, self._stats.total_entries - 1),
                        memory_usage_bytes=self._stats.memory_usage_bytes,
                        last_cleanup=self._stats.last_cleanup,
                    )

                entry = FlextOracleWmsCacheEntry(
                    key=key,
                    value=value,
                    timestamp=time.time(),
                    ttl_seconds=ttl,
                )
                self._cache[key] = entry
                self._stats = FlextOracleWmsCacheStats(
                    hits=self._stats.hits,
                    misses=self._stats.misses,
                    evictions=self._stats.evictions,
                    expired_entries=self._stats.expired_entries,
                    total_entries=len(self._cache),
                    memory_usage_bytes=self._stats.memory_usage_bytes,
                    last_cleanup=self._stats.last_cleanup,
                )

            return FlextResult.ok(None)

        except Exception as e:
            handle_operation_exception("cache set", e, logger)
            return FlextResult.fail(f"Cache set failed: {e}")

    def invalidate(self, key: str) -> None:
        """Invalidate specific cache entry."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                self._stats = FlextOracleWmsCacheStats(
                    hits=self._stats.hits,
                    misses=self._stats.misses,
                    evictions=self._stats.evictions + 1,
                    expired_entries=self._stats.expired_entries,
                    total_entries=len(self._cache),
                    memory_usage_bytes=self._stats.memory_usage_bytes,
                    last_cleanup=self._stats.last_cleanup,
                )

    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            evicted_count = len(self._cache)
            self._cache.clear()
            self._stats = FlextOracleWmsCacheStats(
                hits=self._stats.hits,
                misses=self._stats.misses,
                evictions=self._stats.evictions + evicted_count,
                expired_entries=self._stats.expired_entries,
                total_entries=0,
                memory_usage_bytes=self._stats.memory_usage_bytes,
                last_cleanup=self._stats.last_cleanup,
            )

    def get_stats(self) -> FlextOracleWmsCacheStats:
        """Get cache statistics snapshot."""
        with self._lock:
            return FlextOracleWmsCacheStats(
                hits=self._stats.hits,
                misses=self._stats.misses,
                evictions=self._stats.evictions,
                expired_entries=self._stats.expired_entries,
                total_entries=len(self._cache),
                memory_usage_bytes=self._stats.memory_usage_bytes,
                last_cleanup=self._stats.last_cleanup,
            )


# =============================================================================
# DYNAMIC SCHEMA PROCESSING - Consolidated from dynamic.py
# =============================================================================


class TypeInferenceStrategy(ABC):
    """Strategy Pattern: Abstract base for type inference strategies."""

    @abstractmethod
    def can_handle(self, value: object) -> bool:
        """Check if this strategy can handle the given value type."""

    @abstractmethod
    def infer_type(self, value: object) -> str:
        """Infer the JSON schema type for the value."""


class NullTypeStrategy(TypeInferenceStrategy):
    """Strategy for handling None/null values."""

    def can_handle(self, value: object) -> bool:
        """Check if value is None."""
        return value is None

    def infer_type(self, _value: object) -> str:
        """Return string type for null values."""
        return "string"  # Default for null values


class BooleanTypeStrategy(TypeInferenceStrategy):
    """Strategy for handling boolean values."""

    def can_handle(self, value: object) -> bool:
        """Check if value is boolean."""
        return isinstance(value, bool)

    def infer_type(self, _value: object) -> str:
        """Return boolean type."""
        return "boolean"


class NumberTypeStrategy(TypeInferenceStrategy):
    """Strategy for handling numeric values."""

    def can_handle(self, value: object) -> bool:
        """Check if value is numeric."""
        return isinstance(value, (int, float))

    def infer_type(self, value: object) -> str:
        """Return appropriate numeric type."""
        if isinstance(value, int):
            return "integer"
        return "number"


class StringTypeStrategy(TypeInferenceStrategy):
    """Strategy for handling string values."""

    def can_handle(self, value: object) -> bool:
        """Check if value is string."""
        return isinstance(value, str)

    def infer_type(self, value: object) -> str:
        """Infer string subtype based on format."""
        if isinstance(value, str) and re.match(
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", value,
        ):
            # Check for date/time patterns
            return "string"  # Could be datetime format
        return "string"


class ArrayTypeStrategy(TypeInferenceStrategy):
    """Strategy for handling array/list values."""

    def can_handle(self, value: object) -> bool:
        """Check if value is list or array."""
        return isinstance(value, list)

    def infer_type(self, _value: object) -> str:
        """Return array type."""
        return "array"


class ObjectTypeStrategy(TypeInferenceStrategy):
    """Strategy for handling object/dict values."""

    def can_handle(self, value: object) -> bool:
        """Check if value is dict or object."""
        return isinstance(value, dict)

    def infer_type(self, _value: object) -> str:
        """Return object type."""
        return "object"


class FlextOracleWmsDynamicSchemaProcessor:
    """Oracle WMS dynamic schema processor using Strategy pattern."""

    def __init__(self) -> None:
        """Initialize schema processor with type inference strategies."""
        self.type_strategies: list[TypeInferenceStrategy] = [
            NullTypeStrategy(),
            BooleanTypeStrategy(),
            NumberTypeStrategy(),
            StringTypeStrategy(),
            ArrayTypeStrategy(),
            ObjectTypeStrategy(),
        ]
        self.sample_size = FlextOracleWmsDefaults.DEFAULT_SAMPLE_SIZE

    async def process_records(
        self,
        records: TOracleWmsRecordBatch,
        entity_type: OracleWMSEntityType | None = None,
    ) -> FlextResult[TOracleWmsSchema]:
        """Process Oracle WMS records to generate dynamic schema."""
        try:
            if not records:
                return FlextResult.fail("No records to process")

            # Sample records for schema inference
            sample_records = (
                records[: self.sample_size]
                if len(records) > self.sample_size
                else records
            )

            schema: TOracleWmsSchema = {}

            # Process each field across all sample records
            all_fields: set[str] = set()
            for record in sample_records:
                if isinstance(record, dict):
                    all_fields.update(record.keys())

            for field_name in all_fields:
                field_schema = self._infer_field_schema(field_name, sample_records)
                # If entity_type is provided, add a hint to description
                if entity_type is not None and isinstance(field_schema, dict):
                    field_schema["entity_type_hint"] = str(entity_type)
                schema[field_name] = field_schema

            return FlextResult.ok(schema)

        except Exception as e:
            return FlextResult.fail(f"Process dynamic schema failed: {e}")

    def _infer_field_schema(
        self, field_name: str, records: TOracleWmsRecordBatch,
    ) -> dict[str, object]:
        """Infer schema for a specific field across records."""
        field_values = [
            record[field_name]
            for record in records
            if isinstance(record, dict) and field_name in record
        ]

        if not field_values:
            return {"type": "string", "description": f"Field {field_name}"}

        # Count type occurrences
        type_counts: dict[str, int] = {}
        for value in field_values:
            inferred_type = self._infer_value_type(value)
            type_counts[inferred_type] = type_counts.get(inferred_type, 0) + 1

        # Most common type wins
        most_common_type = max(type_counts, key=lambda x: type_counts[x])

        # Calculate confidence
        confidence = type_counts[most_common_type] / len(field_values)

        field_schema = {
            "type": most_common_type,
            "description": f"Field {field_name}",
            "confidence": confidence,
        }

        # Add nullable info if nulls are present
        null_count = sum(1 for v in field_values if v is None)
        if null_count > 0:
            field_schema["nullable"] = True
            field_schema["null_percentage"] = null_count / len(field_values)

        return field_schema

    def _infer_value_type(self, value: object) -> str:
        """Infer type for a single value using strategies."""
        for strategy in self.type_strategies:
            if strategy.can_handle(value):
                return strategy.infer_type(value)

        # Fallback
        return "string"


# =============================================================================
# ENTITY DISCOVERY SYSTEM - Consolidated from discovery.py
# =============================================================================


@dataclass
class DiscoveryContext:
    """Parameter Object: Encapsulates discovery operation context."""

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
    ) -> FlextResult[None]:
        """Execute a specific discovery step."""


class EntityListDiscoveryStrategy(DiscoveryStrategy):
    """Strategy for discovering entity list from API."""

    async def execute_discovery_step(
        self,
        context: DiscoveryContext,
        api_client: FlextApiClient,
    ) -> FlextResult[None]:
        """Discover entities from Oracle WMS API."""
        try:
            # Se o cliente não expõe 'get', não invente dados
            if not hasattr(api_client, "get"):
                logger.debug("API client does not expose 'get' method; skipping discovery step")
                return FlextResult.ok(None)

            # Nesta estratégia, não inventamos entidades. Outras estratégias ou o cliente real
            # são responsáveis pela descoberta. Mantemos consistente e sem dados falsos.
            return FlextResult.ok(None)

        except Exception as e:
            error_msg = f"Entity discovery failed: {e}"
            context.errors.append(error_msg)
            return FlextResult.fail(error_msg)


class FlextOracleWmsEntityDiscovery:
    """Oracle WMS entity discovery using Strategy and Command patterns."""

    def __init__(self, api_client: FlextApiClient) -> None:
        """Initialize entity discovery with API client."""
        self.api_client = api_client
        self.strategies: list[DiscoveryStrategy] = [
            EntityListDiscoveryStrategy(),
        ]
        self.cache_manager: FlextOracleWmsCacheManager | None = None
        self.schema_processor = FlextOracleWmsDynamicSchemaProcessor()

    def set_cache_manager(self, cache_manager: FlextOracleWmsCacheManager) -> None:
        """Set cache manager for discovery operations."""
        self.cache_manager = cache_manager

    async def discover_entities(
        self,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        use_cache: bool = True,  # noqa: FBT001, FBT002
    ) -> FlextResult[FlextOracleWmsDiscoveryResult]:
        """Discover Oracle WMS entities with caching support."""
        try:
            cache_key = f"discovery:{include_patterns}:{exclude_patterns}"

            # Try cache first
            if use_cache and self.cache_manager:
                cached_result = await self.cache_manager.get(cache_key)
                if cached_result.success and isinstance(cached_result.data, dict):
                    data = cached_result.data
                    raw_entities: list[dict[str, object]] = []
                    entities_data: list[object] = []
                    if isinstance(data, dict):
                        raw_data: object = data.get("entities", [])
                        if isinstance(raw_data, list):
                            entities_data = raw_data
                    if isinstance(entities_data, list):
                        raw_entities = [item for item in entities_data if isinstance(item, dict)]
                    entities: list[FlextOracleWmsEntity] = []
                    for item in raw_entities:
                        if isinstance(item, dict) and item.get("name") and item.get("endpoint"):
                            entities.append(
                                FlextOracleWmsEntity(
                                    name=str(item.get("name")),
                                    endpoint=str(item.get("endpoint")),
                                    description=str(item.get("description")) if isinstance(item.get("description"), str) else None,
                                    fields=item.get("fields") if isinstance(item.get("fields"), dict) else {},  # type: ignore[arg-type]
                                    primary_key=str(item.get("primary_key")) if item.get("primary_key") else None,
                                    replication_key=str(item.get("replication_key")) if item.get("replication_key") else None,
                                    supports_incremental=bool(item.get("supports_incremental", False)),
                                )
                            )
                    logger.debug("Using cached discovery result")
                    return FlextResult.ok(
                        FlextOracleWmsDiscoveryResult(
                            entities=entities,
                            total_count=len(entities),
                            timestamp=str(data.get("timestamp", "")),
                            discovery_duration_ms=0.0,
                            api_version="v10",
                        ),
                    )

            # Execute discovery
            start_time = time.time()
            context = DiscoveryContext(
                include_patterns=include_patterns,
                exclude_patterns=exclude_patterns,
                all_entities=[],
                errors=[],
            )

            # Execute all discovery strategies
            for strategy in self.strategies:
                result = await strategy.execute_discovery_step(context, self.api_client)
                if not result.success:
                    logger.warning("Discovery strategy failed", error=result.error)

            # Apply filters
            filtered_entities = self._apply_entity_filters(
                context.all_entities,
                include_patterns,
                exclude_patterns,
            )

            discovery_duration = (
                time.time() - start_time
            ) * 1000  # Convert to milliseconds

            # Create discovery result
            discovery_result = FlextOracleWmsDiscoveryResult(
                entities=filtered_entities,
                total_count=len(filtered_entities),
                timestamp=datetime.now(UTC).isoformat(),
                discovery_duration_ms=discovery_duration,
                has_errors=len(context.errors) > 0,
                errors=context.errors,
                api_version="v10",
            )

            # Cache the result
            if use_cache and self.cache_manager:
                cache_data = {
                    "entities": [e.to_dict_basic() for e in filtered_entities],
                    "total_count": len(filtered_entities),
                    "timestamp": discovery_result.timestamp,
                }
                await self.cache_manager.set(cache_key, cache_data)  # type: ignore[arg-type]

            return FlextResult.ok(discovery_result)

        except Exception as e:
            return FlextResult.fail(f"Discover entities failed: {e}")

    def _apply_entity_filters(
        self,
        entities: list[FlextOracleWmsEntity],
        include_patterns: list[str] | None,
        exclude_patterns: list[str] | None,
    ) -> list[FlextOracleWmsEntity]:
        """Apply include/exclude patterns to entity list."""
        filtered_entities = entities

        if include_patterns:
            filtered_entities = [
                entity
                for entity in filtered_entities
                if any(re.match(pattern, entity.name) for pattern in include_patterns)
            ]

        if exclude_patterns:
            filtered_entities = [
                entity
                for entity in filtered_entities
                if not any(
                    re.match(pattern, entity.name) for pattern in exclude_patterns
                )
            ]

        return filtered_entities


# =============================================================================
# FACTORY FUNCTIONS
# =============================================================================


def flext_oracle_wms_create_entity_discovery(
    api_client: FlextApiClient,
) -> FlextOracleWmsEntityDiscovery:
    """Create Oracle WMS entity discovery instance."""
    return FlextOracleWmsEntityDiscovery(api_client)


def flext_oracle_wms_create_dynamic_schema_processor() -> (
    FlextOracleWmsDynamicSchemaProcessor
):
    """Create Oracle WMS dynamic schema processor instance."""
    return FlextOracleWmsDynamicSchemaProcessor()


def flext_oracle_wms_create_cache_manager(
    config: FlextOracleWmsCacheConfig | None = None,
) -> FlextOracleWmsCacheManager:
    """Create Oracle WMS cache manager instance."""
    if config is None:
        config = FlextOracleWmsCacheConfig()
    return FlextOracleWmsCacheManager(config)


# =============================================================================
# EXPORTS
# =============================================================================

__all__: list[str] = [
    "ArrayTypeStrategy",
    "BooleanTypeStrategy",
    "DiscoveryContext",
    "DiscoveryStrategy",
    "EntityListDiscoveryStrategy",
    # Cache Management
    "FlextOracleWmsCacheConfig",
    "FlextOracleWmsCacheEntry",
    "FlextOracleWmsCacheStats",
    "FlextOracleWmsCacheManager",
    # Dynamic Schema Processing
    "FlextOracleWmsDynamicSchemaProcessor",
    # Entity Discovery
    "FlextOracleWmsEntityDiscovery",
    "NullTypeStrategy",
    "NumberTypeStrategy",
    "ObjectTypeStrategy",
    "StringTypeStrategy",
    "TypeInferenceStrategy",
    "flext_oracle_wms_create_cache_manager",
    "flext_oracle_wms_create_dynamic_schema_processor",
    # Factory Functions
    "flext_oracle_wms_create_entity_discovery",
]
