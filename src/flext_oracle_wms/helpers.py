"""FlextOracleWms helpers with flext_ prefix following SOLID/KISS/DRY.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Enterprise-grade helper functions for Oracle WMS operations with
proper prefixing and flext-core integration.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

# Import from flext-core root namespace as required
from flext_core import FlextResult

if TYPE_CHECKING:
    from flext_oracle_wms.typedefs import (
        FlextOracleWmsConnectionInfo,
        FlextOracleWmsEntityInfo,
        WMSFilterCondition,
        WMSRecord,
    )


def flext_oracle_wms_validate_connection(
    connection_info: FlextOracleWmsConnectionInfo,
) -> FlextResult[bool]:
    """Validate Oracle WMS connection information.

    Args:
        connection_info: WMS connection configuration

    Returns:
        FlextResult with validation status

    """
    try:
        # Validate required fields
        if not connection_info.get("base_url"):
            return FlextResult.fail("Missing base_url in connection info")

        if not connection_info.get("username"):
            return FlextResult.fail("Missing username in connection info")

        if not connection_info.get("password"):
            return FlextResult.fail("Missing password in connection info")

        # Validate URL format
        base_url = connection_info["base_url"]
        if not (base_url.startswith(("http://", "https://"))):
            return FlextResult.fail("Invalid base_url format")

        return FlextResult.ok(True)

    except Exception as e:
        return FlextResult.fail(f"Connection validation error: {e}")


def flext_oracle_wms_sanitize_entity_name(entity_name: str) -> FlextResult[str]:
    """Sanitize Oracle WMS entity name for safe usage.

    Args:
        entity_name: Raw entity name

    Returns:
        FlextResult with sanitized entity name

    """
    try:
        if not entity_name:
            return FlextResult.fail("Entity name cannot be empty")

        # Convert to lowercase and replace invalid characters
        sanitized = entity_name.lower().replace(" ", "_").replace("-", "_")

        # Remove non-alphanumeric characters except underscores
        sanitized = "".join(c for c in sanitized if c.isalnum() or c == "_")

        if not sanitized:
            return FlextResult.fail("Entity name contains no valid characters")

        return FlextResult.ok(sanitized)

    except Exception as e:
        return FlextResult.fail(f"Entity name sanitization error: {e}")


def flext_oracle_wms_build_filter_query(
    filters: list[WMSFilterCondition],
) -> FlextResult[dict[str, Any]]:
    """Build Oracle WMS API filter query from conditions.

    Args:
        filters: List of filter conditions

    Returns:
        FlextResult with built query parameters

    """
    try:
        if not filters:
            return FlextResult.ok({})

        query_params = {}

        for i, filter_condition in enumerate(filters):
            field = filter_condition.get("field")
            operator = filter_condition.get("operator")
            value = filter_condition.get("value")

            if not all([field, operator, value is not None]):
                return FlextResult.fail(f"Invalid filter condition at index {i}")

            # Build query parameter based on operator
            if operator == "eq":
                query_params[field] = value
            elif operator == "neq":
                query_params[f"{field}__neq"] = value
            elif operator == "gt":
                query_params[f"{field}__gt"] = value
            elif operator == "gte":
                query_params[f"{field}__gte"] = value
            elif operator == "lt":
                query_params[f"{field}__lt"] = value
            elif operator == "lte":
                query_params[f"{field}__lte"] = value
            elif operator == "in":
                query_params[f"{field}__in"] = value
            elif operator == "nin":
                query_params[f"{field}__nin"] = value
            elif operator == "like":
                query_params[f"{field}__like"] = value
            else:
                return FlextResult.fail(f"Unsupported operator: {operator}")

        # Cast to proper dict type
        result_params: dict[str, Any] = {str(k): v for k, v in query_params.items()}
        return FlextResult.ok(result_params)

    except Exception as e:
        return FlextResult.fail(f"Filter query build error: {e}")


def flext_oracle_wms_extract_entity_metadata(
    entity_info: FlextOracleWmsEntityInfo,
) -> FlextResult[dict[str, Any]]:
    """Extract metadata from Oracle WMS entity information.

    Args:
        entity_info: Entity information from WMS API

    Returns:
        FlextResult with extracted metadata

    """
    try:
        # Extract field types summary
        fields = entity_info.get("fields", {})

        metadata = {
            "name": entity_info.get("name", "unknown"),
            "description": entity_info.get("description", ""),
            "endpoint": entity_info.get("endpoint", ""),
            "primary_key": entity_info.get("primary_key"),
            "replication_key": entity_info.get("replication_key"),
            "supports_incremental": entity_info.get("supports_incremental", False),
            "field_count": len(fields) if isinstance(fields, dict) else 0,
        }
        field_types: dict[str, int] = {}
        if isinstance(fields, dict):
            for field_info in fields.values():
                if isinstance(field_info, dict):
                    field_type = field_info.get("type", "unknown")
                    field_types[field_type] = field_types.get(field_type, 0) + 1

        metadata["field_types_summary"] = field_types

        return FlextResult.ok(metadata)

    except Exception as e:
        return FlextResult.fail(f"Entity metadata extraction error: {e}")


def flext_oracle_wms_format_wms_record(
    record: WMSRecord,
    entity_name: str,
) -> FlextResult[dict[str, Any]]:
    """Format Oracle WMS record for consistent processing.

    Args:
        record: Raw WMS record data (guaranteed to be dict by type annotation)
        entity_name: Entity name for context

    Returns:
        FlextResult with formatted record

    """
    try:
        # WMSRecord is typed as dict[str, Any], so no need for isinstance check
        formatted_record = {
            "entity": entity_name,
            "data": record.copy(),
            "extracted_at": None,  # Will be set by extraction process
            "flattened": False,
            "checksum": None,  # Will be calculated if needed
        }

        # Extract ID if available (common patterns)
        id_fields = ["id", "ID", "Id", f"{entity_name}_id", "primary_key"]
        for id_field in id_fields:
            if id_field in record:
                formatted_record["id"] = str(record[id_field])
                break

        return FlextResult.ok(formatted_record)

    except Exception as e:
        return FlextResult.fail(f"Record formatting error: {e}")


def flext_oracle_wms_calculate_pagination_info(
    current_page: int,
    page_size: int,
    total_records: int,
) -> FlextResult[dict[str, Any]]:
    """Calculate Oracle WMS pagination information.

    Args:
        current_page: Current page number (0-based)
        page_size: Records per page
        total_records: Total number of records

    Returns:
        FlextResult with pagination information

    """
    try:
        if page_size <= 0:
            return FlextResult.fail("Page size must be positive")

        if current_page < 0:
            return FlextResult.fail("Current page must be non-negative")

        total_pages = (total_records + page_size - 1) // page_size
        has_next = current_page < total_pages - 1
        has_previous = current_page > 0

        pagination_info = {
            "current_page": current_page,
            "page_size": page_size,
            "total_records": total_records,
            "total_pages": total_pages,
            "has_next": has_next,
            "has_previous": has_previous,
            "start_index": current_page * page_size,
            "end_index": min((current_page + 1) * page_size, total_records),
        }

        return FlextResult.ok(pagination_info)

    except Exception as e:
        return FlextResult.fail(f"Pagination calculation error: {e}")


# Export all helpers with flext_ prefix
__all__ = [
    "flext_oracle_wms_build_filter_query",
    "flext_oracle_wms_calculate_pagination_info",
    "flext_oracle_wms_extract_entity_metadata",
    "flext_oracle_wms_format_wms_record",
    "flext_oracle_wms_sanitize_entity_name",
    "flext_oracle_wms_validate_connection",
]
