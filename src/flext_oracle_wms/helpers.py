"""Oracle WMS Helper Functions.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Utility functions for Oracle WMS operations using flext-core patterns.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from flext_core import FlextResult, get_logger

from flext_oracle_wms.constants import (
    FlextOracleWmsEntityTypes,
    OracleWMSEntityType,
    OracleWMSFilterOperator,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

logger = get_logger(__name__)


def flext_oracle_wms_validate_connection(
    config: Mapping[str, Any],
) -> FlextResult[bool]:
    """Validate Oracle WMS connection configuration.

    Args:
        config: Configuration dictionary

    Returns:
        FlextResult indicating if configuration is valid

    """
    try:
        required_fields = ["base_url", "username", "password"]

        for field in required_fields:
            if field not in config or not config[field]:
                return FlextResult.fail(f"Missing required field: {field}")

        # Validate URL format
        base_url = str(config["base_url"])
        if not base_url.startswith(("http://", "https://")):
            return FlextResult.fail("base_url must start with http:// or https://")

        return FlextResult.ok(data=True)

    except Exception as e:
        logger.exception("Connection validation failed")
        return FlextResult.fail(f"Validation error: {e}")


def flext_oracle_wms_sanitize_entity_name(entity_name: str) -> FlextResult[str]:
    """Sanitize entity name for safe API usage.

    Args:
        entity_name: Raw entity name

    Returns:
        FlextResult with sanitized entity name

    """
    try:
        # Remove special characters, keep only alphanumeric and underscores
        sanitized = re.sub(r"[^a-zA-Z0-9_]", "", entity_name.strip())

        if not sanitized:
            return FlextResult.fail("Entity name cannot be empty after sanitization")

        # Convert to lowercase for consistency
        sanitized = sanitized.lower()

        return FlextResult.ok(sanitized)

    except Exception as e:
        logger.exception("Entity name sanitization failed")
        return FlextResult.fail(f"Sanitization error: {e}")


def flext_oracle_wms_build_filter_query(
    filters: Mapping[str, Any],
    operator: OracleWMSFilterOperator = "eq",
) -> FlextResult[str]:
    """Build filter query string for Oracle WMS API.

    Args:
        filters: Dictionary of field-value pairs
        operator: Filter operator to use

    Returns:
        FlextResult with query string

    """
    try:
        if not filters:
            return FlextResult.ok("")

        query_parts = []
        for field, value in filters.items():
            # Sanitize field name
            field_result = flext_oracle_wms_sanitize_entity_name(field)
            if not field_result.is_success:
                return FlextResult.fail(f"Invalid field name: {field}")

            sanitized_field = field_result.data

            # Build query part based on operator
            if operator == "eq":
                query_parts.append(f"{sanitized_field}={value}")
            elif operator == "neq":
                query_parts.append(f"{sanitized_field}!={value}")
            elif operator == "gt":
                query_parts.append(f"{sanitized_field}>{value}")
            elif operator == "gte":
                query_parts.append(f"{sanitized_field}>={value}")
            elif operator == "lt":
                query_parts.append(f"{sanitized_field}<{value}")
            elif operator == "lte":
                query_parts.append(f"{sanitized_field}<={value}")
            elif operator == "in":
                if isinstance(value, (list, tuple)):
                    value_str = ",".join(str(v) for v in value)
                    query_parts.append(f"{sanitized_field} IN ({value_str})")
                else:
                    query_parts.append(f"{sanitized_field}={value}")
            else:
                return FlextResult.fail(f"Unsupported operator: {operator}")

        query_string = "&".join(query_parts)
        return FlextResult.ok(query_string)

    except Exception as e:
        logger.exception("Filter query building failed")
        return FlextResult.fail(f"Query building error: {e}")


def flext_oracle_wms_calculate_pagination_info(
    page: int,
    page_size: int,
    total_count: int,
) -> FlextResult[dict[str, Any]]:
    """Calculate pagination information.

    Args:
        page: Current page (1-based)
        page_size: Number of items per page
        total_count: Total number of items

    Returns:
        FlextResult with pagination info

    """
    try:
        if page < 1:
            return FlextResult.fail("Page must be >= 1")

        if page_size < 1:
            return FlextResult.fail("Page size must be >= 1")

        if total_count < 0:
            return FlextResult.fail("Total count must be >= 0")

        if total_count > 0:
            total_pages = (total_count + page_size - 1) // page_size
        else:
            total_pages = 1

        offset = (page - 1) * page_size

        pagination_info = {
            "page": page,
            "page_size": page_size,
            "total_count": total_count,
            "total_pages": total_pages,
            "offset": offset,
            "has_next": page < total_pages,
            "has_previous": page > 1,
            "next_page": page + 1 if page < total_pages else None,
            "previous_page": page - 1 if page > 1 else None,
        }

        return FlextResult.ok(pagination_info)

    except Exception as e:
        logger.exception("Pagination calculation failed")
        return FlextResult.fail(f"Pagination error: {e}")


def flext_oracle_wms_extract_entity_metadata(
    entity_data: Mapping[str, Any],
) -> FlextResult[dict[str, Any]]:
    """Extract metadata from Oracle WMS entity response.

    Args:
        entity_data: Raw entity response data

    Returns:
        FlextResult with extracted metadata

    """
    try:
        metadata = {
            "total_records": 0,
            "page_info": {},
            "schema_info": {},
            "timestamps": {},
        }

        # Extract record count
        if "total" in entity_data:
            metadata["total_records"] = int(entity_data["total"])
        elif "count" in entity_data:
            metadata["total_records"] = int(entity_data["count"])
        elif "data" in entity_data and isinstance(entity_data["data"], list):
            metadata["total_records"] = len(entity_data["data"])

        # Extract pagination info
        if "page" in entity_data:
            metadata["page_info"] = entity_data["page"]

        # Extract schema info if available
        if "schema" in entity_data:
            metadata["schema_info"] = entity_data["schema"]
        elif "fields" in entity_data:
            metadata["schema_info"] = {"fields": entity_data["fields"]}

        # Extract timestamp info
        timestamp_fields = ["created_at", "updated_at", "timestamp", "last_modified"]
        timestamps_dict = metadata["timestamps"]
        for field in timestamp_fields:
            if field in entity_data and isinstance(timestamps_dict, dict):
                timestamps_dict[field] = entity_data[field]

        return FlextResult.ok(metadata)

    except Exception as e:
        logger.exception("Metadata extraction failed")
        return FlextResult.fail(f"Metadata extraction error: {e}")


def flext_oracle_wms_format_wms_record(
    record: Mapping[str, Any],
    entity_type: OracleWMSEntityType,
) -> FlextResult[dict[str, Any]]:
    """Format a record according to Oracle WMS standards.

    Args:
        record: Raw record data
        entity_type: Type of Oracle WMS entity

    Returns:
        FlextResult with formatted record

    """
    try:
        # Validate entity type
        if entity_type not in FlextOracleWmsEntityTypes.ALL_ENTITIES:
            return FlextResult.fail(f"Invalid entity type: {entity_type}")

        formatted_record = dict(record)

        # Add standard Oracle WMS fields if missing
        if "entity_type" not in formatted_record:
            formatted_record["entity_type"] = entity_type

        # Ensure required fields exist (entity-specific logic can be added here)
        if entity_type == "order_hdr":
            required_fields = ["order_id", "status"]
        elif entity_type == "inventory":
            required_fields = ["item_id", "location_id", "quantity"]
        else:
            required_fields = ["id"]  # Default requirement

        for field in required_fields:
            if field not in formatted_record:
                formatted_record[field] = None

        # Standardize field names (convert to lowercase with underscores)
        standardized_record = {}
        for key, value in formatted_record.items():
            # Convert camelCase to snake_case
            snake_case_key = re.sub(r"([A-Z])", r"_\1", key).lower().lstrip("_")
            standardized_record[snake_case_key] = value

        return FlextResult.ok(standardized_record)

    except Exception as e:
        logger.exception("Record formatting failed")
        return FlextResult.fail(f"Formatting error: {e}")


__all__ = [
    "flext_oracle_wms_build_filter_query",
    "flext_oracle_wms_calculate_pagination_info",
    "flext_oracle_wms_extract_entity_metadata",
    "flext_oracle_wms_format_wms_record",
    "flext_oracle_wms_sanitize_entity_name",
    "flext_oracle_wms_validate_connection",
]
