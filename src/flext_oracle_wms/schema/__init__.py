"""Oracle WMS Schema Package - Dynamic schema processing capabilities.

This package provides dynamic schema discovery and processing capabilities
for Oracle WMS integrations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_oracle_wms.schema.dynamic import (
    # Core schema classes
    FlextOracleWmsDynamicSchemaProcessor,
    FlextOracleWmsEntityProcessingResult,
    # Result types
    FlextOracleWmsSchemaDiscoveryResult,
    # Factory functions
    flext_oracle_wms_create_dynamic_schema_processor,
    # Convenience functions
    flext_oracle_wms_discover_entity_schemas,
    flext_oracle_wms_process_entity_with_schema,
)

__all__ = [
    "FlextOracleWmsDynamicSchemaProcessor",
    "FlextOracleWmsEntityProcessingResult",
    "FlextOracleWmsSchemaDiscoveryResult",
    "flext_oracle_wms_create_dynamic_schema_processor",
    "flext_oracle_wms_discover_entity_schemas",
    "flext_oracle_wms_process_entity_with_schema",
]
