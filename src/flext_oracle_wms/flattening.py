"""Oracle WMS Data Flattening using flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Simplified data flattening for Oracle WMS nested structures.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import FlextResult, get_logger

if TYPE_CHECKING:
    from flext_oracle_wms.types import TOracleWmsRecord, TOracleWmsRecordBatch

logger = get_logger(__name__)


class FlextOracleWmsDataFlattener:
    """Simplified data flattener for Oracle WMS using flext-core patterns."""

    def __init__(
        self,
        separator: str = "_",
        max_depth: int = 5,
        *,
        preserve_lists: bool = True,
    ) -> None:
        """Initialize data flattener.

        Args:
            separator: Separator for nested field names
            max_depth: Maximum nesting depth to flatten
            preserve_lists: Whether to preserve list structures

        """
        self.separator = separator
        self.max_depth = max_depth
        self.preserve_lists = preserve_lists
        logger.info(
            "Data flattener initialized",
            separator=separator,
            max_depth=max_depth,
            preserve_lists=preserve_lists,
        )

    async def flatten_records(
        self,
        records: TOracleWmsRecordBatch,
        entity_name: str | None = None,
    ) -> FlextResult[TOracleWmsRecordBatch]:
        """Flatten nested records.

        Args:
            records: Records to flatten
            entity_name: Optional entity name for logging

        Returns:
            FlextResult with flattened records

        """
        try:
            flattened_records = []

            for record in records:
                if isinstance(record, dict):
                    flattened_record = self._flatten_record(record)
                    flattened_records.append(flattened_record)
                else:
                    # Skip non-dict records
                    flattened_records.append(record)

            logger.info(
                "Records flattened successfully",
                entity_name=entity_name,
                record_count=len(flattened_records),
            )

            return FlextResult.ok(flattened_records)

        except Exception as e:
            logger.exception("Record flattening failed", entity_name=entity_name)
            return FlextResult.fail(f"Record flattening failed: {e}")

    async def unflatten_records(
        self,
        records: TOracleWmsRecordBatch,
        entity_name: str | None = None,
    ) -> FlextResult[TOracleWmsRecordBatch]:
        """Unflatten records back to nested structure.

        Args:
            records: Flattened records to unflatten
            entity_name: Optional entity name for logging

        Returns:
            FlextResult with unflattened records

        """
        try:
            unflattened_records = []

            for record in records:
                if isinstance(record, dict):
                    unflattened_record = self._unflatten_record(record)
                    unflattened_records.append(unflattened_record)
                else:
                    # Skip non-dict records
                    unflattened_records.append(record)

            logger.info(
                "Records unflattened successfully",
                entity_name=entity_name,
                record_count=len(unflattened_records),
            )

            return FlextResult.ok(unflattened_records)

        except Exception as e:
            logger.exception("Record unflattening failed", entity_name=entity_name)
            return FlextResult.fail(f"Record unflattening failed: {e}")

    def _flatten_record(
        self, record: TOracleWmsRecord, prefix: str = "", depth: int = 0
    ) -> TOracleWmsRecord:
        """Flatten a single record recursively."""
        if depth > self.max_depth:
            # Stop recursion at max depth
            return {"__deep_object__": str(record)}

        flattened = {}

        for key, value in record.items():
            new_key = f"{prefix}{self.separator}{key}" if prefix else key

            if isinstance(value, dict) and depth < self.max_depth:
                # Recursively flatten nested dictionaries
                nested_flattened = self._flatten_record(value, new_key, depth + 1)
                flattened.update(nested_flattened)
            elif isinstance(value, list) and not self.preserve_lists:
                # Flatten lists if not preserving them
                flattened.update(self._flatten_list(value, new_key, depth))
            else:
                # Keep the value as is
                flattened[new_key] = value

        return flattened

    def _flatten_list(self, lst: list[Any], prefix: str, depth: int) -> dict[str, Any]:
        """Flatten a list into indexed keys."""
        flattened = {}

        for i, item in enumerate(lst):
            new_key = f"{prefix}{self.separator}{i}"

            if isinstance(item, dict) and depth < self.max_depth:
                # Recursively flatten nested dictionaries in list
                nested_flattened = self._flatten_record(item, new_key, depth + 1)
                flattened.update(nested_flattened)
            else:
                flattened[new_key] = item

        return flattened

    def _unflatten_record(self, record: TOracleWmsRecord) -> TOracleWmsRecord:
        """Unflatten a single record by expanding dot-notation keys."""
        unflattened: dict[str, Any] = {}

        for key, value in record.items():
            self._set_nested_value(unflattened, key, value)

        return unflattened

    def _set_nested_value(self, target: dict[str, Any], key: str, value: Any) -> None:
        """Set a nested value in the target dictionary using dot notation.

        Simplified version to avoid complex type issues with dict/list union.
        """
        if "." not in key:
            target[key] = value
            return

        # For complex nested structures with mixed dict/list, we'll use a simpler approach
        # that just creates nested dicts and converts the final key appropriately
        parts = key.split(".")
        current: dict[str, Any] = target

        # Navigate through all parts except the last one, creating dicts
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            if not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]

        # Set the final value
        final_part = parts[-1]
        current[final_part] = value

    async def get_flattening_stats(
        self,
        records: TOracleWmsRecordBatch,
    ) -> FlextResult[dict[str, Any]]:
        """Get statistics about data structure complexity.

        Args:
            records: Records to analyze

        Returns:
            FlextResult with flattening statistics

        """
        try:
            stats: dict[str, int | float] = {
                "total_records": len(records),
                "nested_records": 0,
                "max_depth": 0,
                "total_fields": 0,
                "nested_fields": 0,
                "list_fields": 0,
            }

            for record in records:
                if isinstance(record, dict):
                    record_stats = self._analyze_record_structure(record)
                    stats["nested_records"] += 1 if record_stats["depth"] > 1 else 0
                    stats["max_depth"] = max(stats["max_depth"], record_stats["depth"])
                    stats["total_fields"] += record_stats["total_fields"]
                    stats["nested_fields"] += record_stats["nested_fields"]
                    stats["list_fields"] += record_stats["list_fields"]

            # Calculate averages (explicitly handling float results)
            if stats["total_records"] > 0:
                avg_fields = stats["total_fields"] / stats["total_records"]
                nested_percentage = (stats["nested_records"] / stats["total_records"]) * 100

                # Update stats with proper types
                stats["avg_fields_per_record"] = avg_fields
                stats["nested_percentage"] = nested_percentage
            else:
                stats["avg_fields_per_record"] = 0.0
                stats["nested_percentage"] = 0.0

            logger.info("Flattening statistics calculated", **stats)

            return FlextResult.ok(stats)

        except Exception as e:
            logger.exception("Failed to calculate flattening statistics")
            return FlextResult.fail(f"Statistics calculation failed: {e}")

    def _analyze_record_structure(
        self, record: TOracleWmsRecord, depth: int = 1
    ) -> dict[str, int]:
        """Analyze the structure of a single record."""
        stats = {
            "depth": depth,
            "total_fields": 0,
            "nested_fields": 0,
            "list_fields": 0,
        }

        for value in record.values():
            stats["total_fields"] += 1

            if isinstance(value, dict):
                stats["nested_fields"] += 1
                # Recursively analyze nested structure
                nested_stats = self._analyze_record_structure(value, depth + 1)
                stats["depth"] = max(stats["depth"], nested_stats["depth"])
                stats["total_fields"] += nested_stats["total_fields"]
                stats["nested_fields"] += nested_stats["nested_fields"]
                stats["list_fields"] += nested_stats["list_fields"]
            elif isinstance(value, list):
                stats["list_fields"] += 1
                # Analyze list items
                for item in value:
                    if isinstance(item, dict):
                        nested_stats = self._analyze_record_structure(item, depth + 1)
                        stats["depth"] = max(stats["depth"], nested_stats["depth"])
                        stats["total_fields"] += nested_stats["total_fields"]
                        stats["nested_fields"] += nested_stats["nested_fields"]
                        stats["list_fields"] += nested_stats["list_fields"]

        return stats


# Factory function for easy usage
def flext_oracle_wms_create_data_flattener(
    separator: str = "_",
    max_depth: int = 5,
    *,
    preserve_lists: bool = True,
) -> FlextOracleWmsDataFlattener:
    """Create data flattener.

    Args:
        separator: Separator for nested field names
        max_depth: Maximum nesting depth
        preserve_lists: Whether to preserve list structures

    Returns:
        Configured data flattener

    """
    return FlextOracleWmsDataFlattener(
        separator=separator, max_depth=max_depth, preserve_lists=preserve_lists
    )
