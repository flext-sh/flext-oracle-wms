"""Enterprise Cache Manager for Oracle WMS.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Thread-safe caching system for Oracle WMS operations using flext-core patterns.
"""

from __future__ import annotations

import asyncio
import contextlib
import threading
import time
from dataclasses import dataclass
from typing import TypeVar

from flext_core import FlextResult, FlextValueObject, get_logger

from flext_oracle_wms.constants import FlextOracleWmsDefaults
from flext_oracle_wms.helpers import handle_operation_exception

logger = get_logger(__name__)

# Type variables for generic cache
T = TypeVar("T")

# Cache value types - using specific types from Oracle WMS instead of Any
CacheValueBasic = str | int | float | bool | None
CacheValueDict = dict[str, CacheValueBasic]
CacheValueList = list[CacheValueBasic | CacheValueDict]
CacheValue = CacheValueDict | CacheValueList | CacheValueBasic


@dataclass(frozen=True)
class FlextOracleWmsCacheConfig(FlextValueObject):
    """Oracle WMS cache configuration using flext-core standards."""

    default_ttl_seconds: int = 3600  # 1 hour
    max_cache_entries: int = 1000
    cleanup_interval_seconds: int = 300  # 5 minutes
    enable_statistics: bool = True
    enable_async_cleanup: bool = True

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate Oracle WMS cache configuration domain rules."""
        if self.default_ttl_seconds <= 0:
            return FlextResult.fail("Default TTL must be positive")
        if self.max_cache_entries <= 0:
            return FlextResult.fail("Max cache entries must be positive")
        if self.cleanup_interval_seconds <= 0:
            return FlextResult.fail("Cleanup interval must be positive")
        return FlextResult.ok(None)


@dataclass(frozen=True)
class FlextOracleWmsCacheEntry[T](FlextValueObject):
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

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate Oracle WMS cache entry domain rules."""
        if not self.key:
            return FlextResult.fail("Cache key cannot be empty")
        if self.ttl_seconds <= 0:
            return FlextResult.fail("TTL must be positive")
        if self.timestamp <= 0:
            return FlextResult.fail("Timestamp must be positive")
        if self.access_count < 0:
            return FlextResult.fail("Access count cannot be negative")
        return FlextResult.ok(None)

    def is_expired(self) -> bool:
        """Check if cache entry is expired."""
        return time.time() > (self.timestamp + self.ttl_seconds)

    def update_access(self) -> FlextOracleWmsCacheEntry[T]:
        """Update access statistics and return new entry."""
        return FlextOracleWmsCacheEntry(
            key=self.key,
            value=self.value,
            timestamp=self.timestamp,
            ttl_seconds=self.ttl_seconds,
            access_count=self.access_count + 1,
            last_accessed=time.time(),
        )


@dataclass(frozen=True)
class FlextOracleWmsCacheStats(FlextValueObject):
    """Oracle WMS cache statistics using flext-core standards."""

    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expired_entries: int = 0
    total_entries: int = 0
    memory_usage_bytes: int = 0
    last_cleanup: float = 0.0

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate Oracle WMS cache statistics domain rules."""
        if self.hits < 0 or self.misses < 0 or self.evictions < 0:
            return FlextResult.fail("Statistics counters cannot be negative")
        if self.expired_entries < 0 or self.total_entries < 0:
            return FlextResult.fail("Entry counts cannot be negative")
        if self.memory_usage_bytes < 0:
            return FlextResult.fail("Memory usage cannot be negative")
        return FlextResult.ok(None)

    def get_hit_ratio(self) -> float:
        """Calculate cache hit ratio."""
        total_requests = self.hits + self.misses
        return self.hits / total_requests if total_requests > 0 else 0.0

    def update_hit(self) -> FlextOracleWmsCacheStats:
        """Update hit statistics and return new stats."""
        return FlextOracleWmsCacheStats(
            hits=self.hits + 1,
            misses=self.misses,
            evictions=self.evictions,
            expired_entries=self.expired_entries,
            total_entries=self.total_entries,
            memory_usage_bytes=self.memory_usage_bytes,
            last_cleanup=self.last_cleanup,
        )

    def update_miss(self) -> FlextOracleWmsCacheStats:
        """Update miss statistics and return new stats."""
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
    """Enterprise thread-safe cache manager for Oracle WMS using flext-core patterns.

    Provides comprehensive caching with TTL, statistics, and cleanup capabilities.
    """

    def __init__(self, config: FlextOracleWmsCacheConfig) -> None:
        """Initialize cache manager with configuration.

        Args:
            config: Cache configuration

        """
        self.config = config
        self._entity_cache: dict[str, FlextOracleWmsCacheEntry[object]] = {}
        self._schema_cache: dict[str, FlextOracleWmsCacheEntry[object]] = {}
        self._metadata_cache: dict[str, FlextOracleWmsCacheEntry[object]] = {}
        self._cache_lock = threading.RLock()

        # Statistics
        self._stats = FlextOracleWmsCacheStats(last_cleanup=time.time())

        # Cleanup task
        self._cleanup_task: asyncio.Task[None] | None = None
        self._shutdown_event = asyncio.Event()

        logger.info(
            "Oracle WMS cache manager initialized",
            ttl_seconds=config.default_ttl_seconds,
            max_entries=config.max_cache_entries,
        )

    async def start(self) -> FlextResult[None]:
        """Start the cache manager and cleanup task."""
        try:
            if self.config.enable_async_cleanup:
                self._cleanup_task = asyncio.create_task(self._cleanup_loop())

            logger.info("Oracle WMS cache manager started")
            return FlextResult.ok(None)
        except Exception as e:
            handle_operation_exception(e, "start cache manager")
            # Never reached due to handle_operation_exception always raising
            return FlextResult.fail(f"Start cache manager failed: {e}")

    async def stop(self) -> FlextResult[None]:
        """Stop the cache manager and cleanup task."""
        try:
            self._shutdown_event.set()

            if self._cleanup_task:
                self._cleanup_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await self._cleanup_task

            # Clear all caches
            await self.clear_all()

            logger.info("Oracle WMS cache manager stopped")
            return FlextResult.ok(None)
        except Exception as e:
            handle_operation_exception(e, "stop cache manager")
            # Never reached due to handle_operation_exception always raising
            return FlextResult.fail(f"Stop cache manager failed: {e}")

    async def get_entity(self, key: str) -> FlextResult[object | None]:
        """Get entity from cache with thread safety.

        Args:
            key: Cache key for entity

        Returns:
            FlextResult containing cached entity data or None

        """
        return await self._get_from_cache(self._entity_cache, key, "entity")

    async def set_entity(
        self,
        key: str,
        value: CacheValue,
        ttl_seconds: int | None = None,
    ) -> FlextResult[bool]:
        """Set entity in cache with thread safety.

        Args:
            key: Cache key for entity
            value: Entity data to cache
            ttl_seconds: Optional TTL override

        Returns:
            FlextResult indicating success

        """
        return await self._set_in_cache(
            self._entity_cache,
            key,
            value,
            ttl_seconds,
            "entity",
        )

    async def get_schema(self, key: str) -> FlextResult[object | None]:
        """Get schema from cache."""
        return await self._get_from_cache(self._schema_cache, key, "schema")

    async def set_schema(
        self,
        key: str,
        value: CacheValue,
        ttl_seconds: int | None = None,
    ) -> FlextResult[bool]:
        """Set schema in cache."""
        return await self._set_in_cache(
            self._schema_cache,
            key,
            value,
            ttl_seconds,
            "schema",
        )

    async def get_metadata(self, key: str) -> FlextResult[object | None]:
        """Get metadata from cache."""
        return await self._get_from_cache(self._metadata_cache, key, "metadata")

    async def set_metadata(
        self,
        key: str,
        value: CacheValue,
        ttl_seconds: int | None = None,
    ) -> FlextResult[bool]:
        """Set metadata in cache."""
        return await self._set_in_cache(
            self._metadata_cache,
            key,
            value,
            ttl_seconds,
            "metadata",
        )

    async def invalidate_key(self, key: str) -> FlextResult[bool]:
        """Invalidate a specific key from all caches.

        Args:
            key: Cache key to invalidate

        Returns:
            FlextResult indicating if any key was removed

        """
        try:
            removed = False

            with self._cache_lock:
                # Remove from all cache types
                for cache in [
                    self._entity_cache,
                    self._schema_cache,
                    self._metadata_cache,
                ]:
                    if key in cache:
                        del cache[key]
                        removed = True

                if removed:
                    self._stats = FlextOracleWmsCacheStats(
                        hits=self._stats.hits,
                        misses=self._stats.misses,
                        evictions=self._stats.evictions + 1,
                        expired_entries=self._stats.expired_entries,
                        total_entries=self._stats.total_entries - 1,
                        memory_usage_bytes=self._stats.memory_usage_bytes,
                        last_cleanup=self._stats.last_cleanup,
                    )

            logger.debug("Cache key invalidated", key=key, removed=removed)
            return FlextResult.ok(removed)

        except Exception as e:
            logger.exception("Failed to invalidate cache key", key=key)
            return FlextResult.fail(f"Cache invalidation failed: {e}")

    async def clear_all(self) -> FlextResult[None]:
        """Clear all caches."""
        try:
            with self._cache_lock:
                self._entity_cache.clear()
                self._schema_cache.clear()
                self._metadata_cache.clear()

                self._stats = FlextOracleWmsCacheStats(last_cleanup=time.time())

            logger.info("All caches cleared")
            return FlextResult.ok(None)

        except Exception as e:
            logger.exception("Failed to clear caches")
            return FlextResult.fail(f"Cache clear failed: {e}")

    async def get_statistics(self) -> FlextResult[FlextOracleWmsCacheStats]:
        """Get cache statistics.

        Returns:
            FlextResult containing cache statistics

        """
        try:
            with self._cache_lock:
                # Update total entries count
                total_entries = (
                    len(self._entity_cache)
                    + len(self._schema_cache)
                    + len(self._metadata_cache)
                )

                current_stats = FlextOracleWmsCacheStats(
                    hits=self._stats.hits,
                    misses=self._stats.misses,
                    evictions=self._stats.evictions,
                    expired_entries=self._stats.expired_entries,
                    total_entries=total_entries,
                    memory_usage_bytes=self._stats.memory_usage_bytes,
                    last_cleanup=self._stats.last_cleanup,
                )

            return FlextResult.ok(current_stats)

        except Exception as e:
            logger.exception("Failed to get cache statistics")
            return FlextResult.fail(f"Statistics retrieval failed: {e}")

    async def _get_from_cache(
        self,
        cache: dict[str, FlextOracleWmsCacheEntry[object]],
        key: str,
        cache_type: str,
    ) -> FlextResult[object | None]:
        """Get value from specific cache with thread safety."""
        try:
            with self._cache_lock:
                if key not in cache:
                    self._stats = self._stats.update_miss()
                    logger.debug("Cache miss", key=key, cache_type=cache_type)
                    return FlextResult.ok(None)

                entry = cache[key]

                # Check if expired
                if entry.is_expired():
                    del cache[key]
                    self._stats = FlextOracleWmsCacheStats(
                        hits=self._stats.hits,
                        misses=self._stats.misses + 1,
                        evictions=self._stats.evictions,
                        expired_entries=self._stats.expired_entries + 1,
                        total_entries=self._stats.total_entries - 1,
                        memory_usage_bytes=self._stats.memory_usage_bytes,
                        last_cleanup=self._stats.last_cleanup,
                    )
                    logger.debug("Cache entry expired", key=key, cache_type=cache_type)
                    return FlextResult.ok(None)

                # Update access statistics
                cache[key] = entry.update_access()
                self._stats = self._stats.update_hit()

                logger.debug("Cache hit", key=key, cache_type=cache_type)
                return FlextResult.ok(entry.value)

        except Exception as e:
            logger.exception("Failed to get from cache", key=key, cache_type=cache_type)
            return FlextResult.fail(f"Cache get failed: {e}")

    async def _set_in_cache(
        self,
        cache: dict[str, FlextOracleWmsCacheEntry[object]],
        key: str,
        value: CacheValue,
        ttl_seconds: int | None,
        cache_type: str,
    ) -> FlextResult[bool]:
        """Set value in specific cache with thread safety."""
        try:
            ttl = ttl_seconds or self.config.default_ttl_seconds

            with self._cache_lock:
                # Check if we need to evict entries
                if len(cache) >= self.config.max_cache_entries:
                    await self._evict_oldest_entry(cache)

                # Create cache entry with proper typing
                entry = FlextOracleWmsCacheEntry[object](
                    key=key,
                    value=value,
                    timestamp=time.time(),
                    ttl_seconds=ttl,
                )

                cache[key] = entry

                # Update statistics
                self._stats = FlextOracleWmsCacheStats(
                    hits=self._stats.hits,
                    misses=self._stats.misses,
                    evictions=self._stats.evictions,
                    expired_entries=self._stats.expired_entries,
                    total_entries=self._stats.total_entries + 1,
                    memory_usage_bytes=self._stats.memory_usage_bytes,
                    last_cleanup=self._stats.last_cleanup,
                )

            logger.debug("Cache entry set", key=key, cache_type=cache_type, ttl=ttl)
            return FlextResult.ok(data=True)

        except Exception as e:
            logger.exception(
                "Failed to set cache entry",
                key=key,
                cache_type=cache_type,
            )
            return FlextResult.fail(f"Cache set failed: {e}")

    async def _evict_oldest_entry(
        self,
        cache: dict[str, FlextOracleWmsCacheEntry[object]],
    ) -> None:
        """Evict the oldest entry from cache."""
        if not cache:
            return

        # Find oldest entry by timestamp
        oldest_key = min(cache.keys(), key=lambda k: cache[k].timestamp)
        del cache[oldest_key]

        self._stats = FlextOracleWmsCacheStats(
            hits=self._stats.hits,
            misses=self._stats.misses,
            evictions=self._stats.evictions + 1,
            expired_entries=self._stats.expired_entries,
            total_entries=self._stats.total_entries - 1,
            memory_usage_bytes=self._stats.memory_usage_bytes,
            last_cleanup=self._stats.last_cleanup,
        )

        logger.debug("Cache entry evicted", key=oldest_key)

    async def _cleanup_loop(self) -> None:
        """Background cleanup loop for expired entries."""
        logger.info("Cache cleanup loop started")

        while not self._shutdown_event.is_set():
            try:
                await asyncio.sleep(self.config.cleanup_interval_seconds)
                await self._cleanup_expired_entries()
            except asyncio.CancelledError:
                break
            except Exception:
                logger.exception("Cache cleanup error")
                await asyncio.sleep(60)  # Wait before retrying

    async def _cleanup_expired_entries(self) -> None:
        """Clean up expired entries from all caches."""
        try:
            expired_count = 0
            current_time = time.time()

            with self._cache_lock:
                for cache in [
                    self._entity_cache,
                    self._schema_cache,
                    self._metadata_cache,
                ]:
                    expired_keys = [
                        key
                        for key, entry in cache.items()
                        if current_time > (entry.timestamp + entry.ttl_seconds)
                    ]

                    for key in expired_keys:
                        del cache[key]
                        expired_count += 1

                # Update statistics
                self._stats = FlextOracleWmsCacheStats(
                    hits=self._stats.hits,
                    misses=self._stats.misses,
                    evictions=self._stats.evictions,
                    expired_entries=self._stats.expired_entries + expired_count,
                    total_entries=self._stats.total_entries - expired_count,
                    memory_usage_bytes=self._stats.memory_usage_bytes,
                    last_cleanup=current_time,
                )

            if expired_count > 0:
                logger.info("Cache cleanup completed", expired_entries=expired_count)

        except Exception:
            logger.exception("Failed to cleanup expired cache entries")


# Factory function for easy usage
def flext_oracle_wms_create_cache_manager(
    entity_ttl: int = FlextOracleWmsDefaults.DEFAULT_CACHE_TTL,
    schema_ttl: int = FlextOracleWmsDefaults.DEFAULT_CACHE_TTL,
    metadata_ttl: int = FlextOracleWmsDefaults.DEFAULT_CACHE_TTL,
    max_size: int = FlextOracleWmsDefaults.MAX_CACHE_SIZE,
) -> FlextOracleWmsCacheManager:
    """Create cache manager.

    Args:
        entity_ttl: Entity cache TTL in seconds
        schema_ttl: Schema cache TTL in seconds
        metadata_ttl: Metadata cache TTL in seconds
        max_size: Maximum cache size

    Returns:
        Configured cache manager

    """
    config = FlextOracleWmsCacheConfig(
        default_ttl_seconds=min(entity_ttl, schema_ttl, metadata_ttl),
        max_cache_entries=max_size,
    )
    return FlextOracleWmsCacheManager(config)
