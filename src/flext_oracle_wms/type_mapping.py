"""Enterprise Oracle WMS Type Mapping System with flext-core integration.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Centralized type mapping system for Oracle WMS operations using
modern Python 3.13 patterns and Singer SDK compatibility.
"""

from __future__ import annotations

import re
from typing import Any

# Import from flext-core root namespace as required
from flext_core import FlextResult

# Oracle WMS API to Singer Schema Type Mappings
FLEXT_ORACLE_WMS_TYPE_MAPPINGS: dict[str, dict[str, Any]] = {
    # Primary and foreign keys
    "pk": {"type": ["integer", "null"]},
    "fk": {"type": ["integer", "null"]},
    "id": {"type": ["integer", "null"]},
    # String types
    "varchar": {"type": ["string", "null"]},
    "varchar2": {"type": ["string", "null"]},
    "nvarchar": {"type": ["string", "null"]},
    "nvarchar2": {"type": ["string", "null"]},
    "char": {"type": ["string", "null"]},
    "nchar": {"type": ["string", "null"]},
    "text": {"type": ["string", "null"]},
    "clob": {"type": ["string", "null"]},
    "nclob": {"type": ["string", "null"]},
    "string": {"type": ["string", "null"]},
    # Numeric types
    "number": {"type": ["number", "null"]},
    "numeric": {"type": ["number", "null"]},
    "decimal": {"type": ["number", "null"]},
    "float": {"type": ["number", "null"]},
    "double": {"type": ["number", "null"]},
    "real": {"type": ["number", "null"]},
    "binary_float": {"type": ["number", "null"]},
    "binary_double": {"type": ["number", "null"]},
    # Integer types
    "integer": {"type": ["integer", "null"]},
    "int": {"type": ["integer", "null"]},
    "smallint": {"type": ["integer", "null"]},
    "bigint": {"type": ["integer", "null"]},
    # Boolean types
    "boolean": {"type": ["boolean", "null"]},
    "bool": {"type": ["boolean", "null"]},
    # Date/time types
    "date": {"type": ["string", "null"], "format": "date"},
    "datetime": {"type": ["string", "null"], "format": "date-time"},
    "timestamp": {"type": ["string", "null"], "format": "date-time"},
    "timestamp_tz": {"type": ["string", "null"], "format": "date-time"},
    "timestamp_ltz": {"type": ["string", "null"], "format": "date-time"},
    "time": {"type": ["string", "null"], "format": "time"},
    "interval": {"type": ["string", "null"]},
    # Binary types
    "blob": {"type": ["string", "null"], "contentEncoding": "base64"},
    "raw": {"type": ["string", "null"], "contentEncoding": "base64"},
    "long_raw": {"type": ["string", "null"], "contentEncoding": "base64"},
    # JSON and XML types
    "json": {"type": ["object", "null"]},
    "jsonb": {"type": ["object", "null"]},
    "xml": {"type": ["string", "null"], "format": "xml"},
    "xmltype": {"type": ["string", "null"], "format": "xml"},
    # Spatial types
    "geometry": {"type": ["string", "null"]},
    "geography": {"type": ["string", "null"]},
    "sdo_geometry": {"type": ["string", "null"]},
    # Array and collection types
    "array": {"type": ["array", "null"]},
    "varray": {"type": ["array", "null"]},
    "nested_table": {"type": ["array", "null"]},
}

# Oracle WMS specific field patterns
FLEXT_ORACLE_WMS_FIELD_PATTERNS: dict[str, dict[str, Any]] = {
    r".*_id$": {"type": ["integer", "null"], "description": "Entity identifier"},
    r".*_code$": {"type": ["string", "null"], "description": "Entity code"},
    r".*_name$": {"type": ["string", "null"], "description": "Entity name"},
    r".*_desc$": {"type": ["string", "null"], "description": "Entity description"},
    r".*_date$": {
        "type": ["string", "null"],
        "format": "date",
        "description": "Date field",
    },
    r".*_time$": {
        "type": ["string", "null"],
        "format": "time",
        "description": "Time field",
    },
    r".*_timestamp$": {
        "type": ["string", "null"],
        "format": "date-time",
        "description": "Timestamp field",
    },
    r".*_flag$": {"type": ["boolean", "null"], "description": "Boolean flag"},
    r".*_count$": {"type": ["integer", "null"], "description": "Count field"},
    r".*_amount$": {"type": ["number", "null"], "description": "Amount field"},
    r".*_qty$": {"type": ["number", "null"], "description": "Quantity field"},
    r".*_weight$": {"type": ["number", "null"], "description": "Weight field"},
    r".*_volume$": {"type": ["number", "null"], "description": "Volume field"},
}


class FlextOracleWmsTypeMapper:
    """Enterprise Oracle WMS type mapping system with flext-core integration."""

    def __init__(self) -> None:
        """Initialize Oracle WMS type mapper."""
        self._custom_mappings: dict[str, dict[str, Any]] = {}
        self._type_patterns: list[tuple[re.Pattern[str], dict[str, Any]]] = [
            (re.compile(pattern), mapping)
            for pattern, mapping in FLEXT_ORACLE_WMS_FIELD_PATTERNS.items()
        ]

    def flext_oracle_wms_map_oracle_type(
        self,
        oracle_type: str,
    ) -> FlextResult[dict[str, Any]]:
        """Map Oracle WMS type to Singer schema type.

        Args:
            oracle_type: Oracle WMS data type

        Returns:
            FlextResult with Singer schema type definition

        """
        try:
            # Normalize type name
            normalized_type = oracle_type.lower().strip()

            # Check custom mappings first
            if normalized_type in self._custom_mappings:
                return FlextResult.ok(self._custom_mappings[normalized_type])

            # Check built-in mappings
            if normalized_type in FLEXT_ORACLE_WMS_TYPE_MAPPINGS:
                return FlextResult.ok(FLEXT_ORACLE_WMS_TYPE_MAPPINGS[normalized_type])

            # Handle parameterized types (e.g., VARCHAR(255), NUMBER(10,2))
            param_match = re.match(r"^(\w+)\s*\(.*\)$", normalized_type)
            if param_match:
                base_type = param_match.group(1)
                if base_type in FLEXT_ORACLE_WMS_TYPE_MAPPINGS:
                    return FlextResult.ok(FLEXT_ORACLE_WMS_TYPE_MAPPINGS[base_type])

            # Default to string for unknown types
            return FlextResult.ok({"type": ["string", "null"]})

        except Exception as e:
            return FlextResult.fail(f"Type mapping failed: {e}")

    def flext_oracle_wms_map_field_by_name(
        self,
        field_name: str,
    ) -> FlextResult[dict[str, Any]]:
        """Map field by name pattern to Singer schema type.

        Args:
            field_name: Oracle WMS field name

        Returns:
            FlextResult with Singer schema type definition

        """
        try:
            # Check patterns
            for pattern, mapping in self._type_patterns:
                if pattern.match(field_name.lower()):
                    return FlextResult.ok(mapping)

            # Default to string
            return FlextResult.ok({"type": ["string", "null"]})

        except Exception as e:
            return FlextResult.fail(f"Field name mapping failed: {e}")

    def flext_oracle_wms_map_schema_field(
        self,
        field_name: str,
        oracle_type: str | None = None,
        *,
        nullable: bool = True,
    ) -> FlextResult[dict[str, Any]]:
        """Map complete schema field with type and name pattern analysis.

        Args:
            field_name: Oracle WMS field name
            oracle_type: Oracle WMS data type (optional)
            nullable: Whether field is nullable

        Returns:
            FlextResult with complete Singer schema field definition

        """
        try:
            schema_field: dict[str, Any] = {}

            # Start with type mapping if available
            if oracle_type:
                type_result = self.flext_oracle_wms_map_oracle_type(oracle_type)
                if type_result.is_success and type_result.data is not None:
                    schema_field = type_result.data.copy()

            # Enhance with field name pattern if no type or to override
            name_result = self.flext_oracle_wms_map_field_by_name(field_name)
            if name_result.is_success and name_result.data is not None:
                name_mapping = name_result.data
                # Merge, preferring type mapping for core type, name mapping for extras
                if not schema_field:
                    schema_field = name_mapping.copy()
                # Add description and other metadata from name pattern
                elif "description" in name_mapping:
                    schema_field["description"] = name_mapping["description"]

            # Handle nullability
            if (
                not nullable
                and "type" in schema_field
                and (
                    isinstance(schema_field["type"], list)
                    and "null" in schema_field["type"]
                )
            ):
                schema_field["type"] = [t for t in schema_field["type"] if t != "null"]
                if len(schema_field["type"]) == 1:
                    schema_field["type"] = schema_field["type"][0]

            return FlextResult.ok(schema_field)

        except Exception as e:
            return FlextResult.fail(f"Schema field mapping failed: {e}")

    def flext_oracle_wms_add_custom_mapping(
        self,
        oracle_type: str,
        singer_schema: dict[str, Any],
    ) -> FlextResult[bool]:
        """Add custom type mapping.

        Args:
            oracle_type: Oracle WMS type to map
            singer_schema: Singer schema definition

        Returns:
            FlextResult indicating success

        """
        try:
            self._custom_mappings[oracle_type.lower().strip()] = singer_schema
            return FlextResult.ok(data=True)
        except Exception as e:
            return FlextResult.fail(f"Custom mapping addition failed: {e}")

    def flext_oracle_wms_get_supported_types(self) -> list[str]:
        """Get list of supported Oracle WMS types.

        Returns:
            List of supported type names

        """
        return list(FLEXT_ORACLE_WMS_TYPE_MAPPINGS.keys()) + list(
            self._custom_mappings.keys(),
        )


def flext_oracle_wms_create_type_mapper() -> FlextOracleWmsTypeMapper:
    """Create Oracle WMS type mapper.

    Returns:
        Configured Oracle WMS type mapper

    """
    return FlextOracleWmsTypeMapper()


def flext_oracle_wms_map_oracle_to_singer(oracle_type: str) -> dict[str, Any]:
    """Quick utility to map Oracle type to Singer schema.

    Args:
        oracle_type: Oracle WMS data type

    Returns:
        Singer schema type definition

    """
    mapper = flext_oracle_wms_create_type_mapper()
    result = mapper.flext_oracle_wms_map_oracle_type(oracle_type)
    return (
        result.data
        if result.is_success and result.data is not None
        else {"type": ["string", "null"]}
    )


# Additional utility functions inspired by flext-tap-oracle-wms patterns
def flext_oracle_wms_is_timestamp_field(field_name: str) -> bool:
    """Check if field name indicates a timestamp field.

    Args:
        field_name: Name of the field to check

    Returns:
        True if field appears to be a timestamp field

    """
    timestamp_patterns = [
        r".*_ts$",
        r".*_dttm$",
        r".*_date$",
        r".*_time$",
        r"^mod_ts$",
        r"^created_dttm$",
        r"^updated_dttm$",
        r"^last_modified$",
    ]

    field_lower = field_name.lower()
    return any(re.search(pattern, field_lower) for pattern in timestamp_patterns)


def flext_oracle_wms_get_primary_key_schema() -> dict[str, Any]:
    """Get schema definition for primary key fields.

    Returns:
        Singer schema definition for primary keys

    """
    return {"type": ["integer", "null"]}


def flext_oracle_wms_get_replication_key_schema() -> dict[str, Any]:
    """Get schema definition for replication key fields (timestamps).

    Returns:
        Singer schema definition for replication keys

    """
    return {"type": ["string", "null"], "format": "date-time"}


__all__ = [
    "FLEXT_ORACLE_WMS_FIELD_PATTERNS",
    "FLEXT_ORACLE_WMS_TYPE_MAPPINGS",
    "FlextOracleWmsTypeMapper",
    "flext_oracle_wms_create_type_mapper",
    "flext_oracle_wms_get_primary_key_schema",
    "flext_oracle_wms_get_replication_key_schema",
    "flext_oracle_wms_is_timestamp_field",
    "flext_oracle_wms_map_oracle_to_singer",
]
