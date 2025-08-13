"""Backward-compatibility helpers shim.

Re-exports helper utilities from the consolidated operations module so
legacy imports `flext_oracle_wms.helpers` continue to function.
"""

from __future__ import annotations

from .wms_operations import (
    flext_oracle_wms_build_entity_url,
    flext_oracle_wms_chunk_records,
    flext_oracle_wms_extract_environment_from_url,
    flext_oracle_wms_extract_pagination_info,
    flext_oracle_wms_format_timestamp,
    flext_oracle_wms_normalize_url,
    flext_oracle_wms_validate_api_response,
    flext_oracle_wms_validate_entity_name,
    handle_operation_exception,
    validate_dict_parameter,
    validate_records_list,
    validate_string_parameter,
)

__all__ = [
    "flext_oracle_wms_build_entity_url",
    "flext_oracle_wms_chunk_records",
    "flext_oracle_wms_extract_environment_from_url",
    "flext_oracle_wms_extract_pagination_info",
    "flext_oracle_wms_format_timestamp",
    "flext_oracle_wms_normalize_url",
    "flext_oracle_wms_validate_api_response",
    "flext_oracle_wms_validate_entity_name",
    "handle_operation_exception",
    "validate_dict_parameter",
    "validate_records_list",
    "validate_string_parameter",
]
