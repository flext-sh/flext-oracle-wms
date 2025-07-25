"""Enterprise Cache Manager for Oracle WMS.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Thread-safe caching system for Oracle WMS operations with TTL support.
"""

from __future__ import annotations

import threading
import time
from typing import Any

from flext_core import get_logger

# Import from flext-core root namespace as required


logger = get_logger(__name__)


class FlextOracleWmsCacheManager:
    """Enterprise thread-safe cache manager for Oracle WMS operations.

    Provides comprehensive caching with TTL, statistics, and cleanup capabilities.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize cache manager with configuration.

        Args:
            config: Cache configuration dictionary

        """
        self.config = config
        self._entity_cache: dict[str, dict[str, Any]] = {}
        self._schema_cache: dict[str, dict[str, Any]] = {}
        self._metadata_cache: dict[str, dict[str, Any]] = {}
        self._cache_lock = threading.RLock()

        # Cache configuration
        self._default_ttl = config.get("cache_ttl_seconds", 3600)  # 1 hour
        self._max_cache_size = config.get("max_cache_entries", 1000)
        self._cleanup_interval = config.get(
            "cleanup_interval_seconds",
            300,
        )  # 5 minutes

        # Cache statistics
        self._stats = {"hits": 0, "misses": 0, "evictions": 0, "expired": 0}

        # Last cleanup time
        self._last_cleanup = time.time()

        logger.info(
            "FlextOracleWms cache manager initialized with TTL=%d seconds",
            self._default_ttl,
        )

    def flext_oracle_wms_get_entity(self, key: str) -> Any | None:
        """Get entity from cache with thread safety.

        Args:
            key: Cache key for entity

        Returns:
            Cached entity data or None

        """
        return self._get_from_cache(self._entity_cache, key, "entity")

    def flext_oracle_wms_set_entity(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> bool:
        """Set entity in cache with TTL.

        Args:
            key: Cache key
            value: Entity data to cache
            ttl: Time-to-live in seconds (uses default if None)

        Returns:
            Success status

        """
        return self._set_in_cache(self._entity_cache, key, value, ttl, "entity")

    def flext_oracle_wms_get_schema(self, key: str) -> Any | None:
        """Get schema from cache with thread safety.

        Args:
            key: Cache key for schema

        Returns:
            Cached schema data or None

        """
        return self._get_from_cache(self._schema_cache, key, "schema")

    def flext_oracle_wms_set_schema(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> bool:
        """Set schema in cache with TTL.

        Args:
            key: Cache key
            value: Schema data to cache
            ttl: Time-to-live in seconds (uses default if None)

        Returns:
            Success status

        """
        return self._set_in_cache(self._schema_cache, key, value, ttl, "schema")

    def flext_oracle_wms_get_metadata(self, key: str) -> Any | None:
        """Get metadata from cache with thread safety.

        Args:
            key: Cache key for metadata

        Returns:
            Cached metadata or None

        """
        return self._get_from_cache(self._metadata_cache, key, "metadata")

    def flext_oracle_wms_set_metadata(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> bool:
        """Set metadata in cache with TTL.

        Args:
            key: Cache key
            value: Metadata to cache
            ttl: Time-to-live in seconds (uses default if None)

        Returns:
            Success status

        """
        return self._set_in_cache(self._metadata_cache, key, value, ttl, "metadata")

    def flext_oracle_wms_clear_all(self) -> bool:
        """Clear all caches with thread safety.

        Returns:
            Success status

        """
        try:
            with self._cache_lock:
                self._entity_cache.clear()
                self._schema_cache.clear()
                self._metadata_cache.clear()
                self._stats = {"hits": 0, "misses": 0, "evictions": 0, "expired": 0}
                logger.info("All FlextOracleWms caches cleared")
                return True
        except Exception as e:
            logger.exception("Failed to clear caches: %s", e)
            return False

    def flext_oracle_wms_get_stats(self) -> dict[str, Any]:
        """Get cache statistics.

        Returns:
            Dictionary with cache statistics

        """
        with self._cache_lock:
            total_requests = self._stats["hits"] + self._stats["misses"]
            hit_rate = (
                (self._stats["hits"] / total_requests * 100)
                if total_requests > 0
                else 0
            )

            return {
                "hit_rate_percent": round(hit_rate, 2),
                "total_hits": self._stats["hits"],
                "total_misses": self._stats["misses"],
                "total_requests": total_requests,
                "evictions": self._stats["evictions"],
                "expired_entries": self._stats["expired"],
                "entity_cache_size": len(self._entity_cache),
                "schema_cache_size": len(self._schema_cache),
                "metadata_cache_size": len(self._metadata_cache),
                "total_cache_size": len(self._entity_cache)
                + len(self._schema_cache)
                + len(self._metadata_cache),
                "max_cache_size": self._max_cache_size,
                "default_ttl_seconds": self._default_ttl,
            }

    def flext_oracle_wms_cleanup_expired(self) -> int:
        """Clean up expired cache entries.

        Returns:
            Number of expired entries removed

        """
        try:
            current_time = time.time()

            # Only cleanup if interval has passed
            if current_time - self._last_cleanup < self._cleanup_interval:
                return 0

            with self._cache_lock:
                expired_count = 0

                # Clean entity cache
                expired_count += self._cleanup_cache(self._entity_cache, current_time)

                # Clean schema cache
                expired_count += self._cleanup_cache(self._schema_cache, current_time)

                # Clean metadata cache
                expired_count += self._cleanup_cache(self._metadata_cache, current_time)

                self._stats["expired"] += expired_count
                self._last_cleanup = current_time

                if expired_count > 0:
                    logger.debug("Cleaned up %d expired cache entries", expired_count)

                return expired_count

        except Exception as e:
            logger.exception("Cache cleanup failed: %s", e)
            return 0

    def _get_from_cache(
        self,
        cache: dict[str, dict[str, Any]],
        key: str,
        cache_type: str,
    ) -> Any | None:
        """Get item from specific cache with TTL check."""
        try:
            # Cleanup expired entries periodically
            self.flext_oracle_wms_cleanup_expired()

            with self._cache_lock:
                if key not in cache:
                    self._stats["misses"] += 1
                    return None

                entry = cache[key]
                current_time = time.time()

                # Check if expired
                if current_time > entry["expires_at"]:
                    del cache[key]
                    self._stats["misses"] += 1
                    self._stats["expired"] += 1
                    logger.debug("Cache entry expired: %s in %s cache", key, cache_type)
                    return None

                # Cache hit
                self._stats["hits"] += 1
                logger.debug("Cache hit: %s in %s cache", key, cache_type)
                return entry["value"]

        except Exception as e:
            logger.exception("Cache get failed for key %s: %s", key, e)
            self._stats["misses"] += 1
            return None

    def _set_in_cache(
        self,
        cache: dict[str, dict[str, Any]],
        key: str,
        value: Any,
        ttl: int | None,
        cache_type: str,
    ) -> bool:
        """Set item in specific cache with TTL."""
        try:
            ttl = ttl or self._default_ttl
            current_time = time.time()
            expires_at = current_time + ttl

            with self._cache_lock:
                # Check cache size limit
                if len(cache) >= self._max_cache_size and key not in cache:
                    # Evict oldest entry
                    oldest_key = min(cache.keys(), key=lambda k: cache[k]["created_at"])
                    del cache[oldest_key]
                    self._stats["evictions"] += 1
                    logger.debug(
                        "Evicted oldest entry: %s from %s cache",
                        oldest_key,
                        cache_type,
                    )

                cache[key] = {
                    "value": value,
                    "created_at": current_time,
                    "expires_at": expires_at,
                    "ttl": ttl,
                }

                logger.debug(
                    "Cached: %s in %s cache (TTL: %d seconds)",
                    key,
                    cache_type,
                    ttl,
                )
                return True

        except Exception as e:
            logger.exception("Cache set failed for key %s: %s", key, e)
            return False

    def _cleanup_cache(
        self,
        cache: dict[str, dict[str, Any]],
        current_time: float,
    ) -> int:
        """Clean expired entries from a specific cache."""
        expired_keys = [
            key for key, entry in cache.items() if current_time > entry["expires_at"]
        ]

        for key in expired_keys:
            del cache[key]

        return len(expired_keys)


def flext_oracle_wms_create_cache_manager(
    config: dict[str, Any],
) -> FlextOracleWmsCacheManager:
    """Factory function to create cache manager.

    Args:
        config: Cache configuration

    Returns:
        Configured cache manager instance

    """
    return FlextOracleWmsCacheManager(config)


__all__ = ["FlextOracleWmsCacheManager", "flext_oracle_wms_create_cache_manager"]
