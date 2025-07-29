"""Oracle WMS Client Library - Essential API.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

__version__ = "2.0.0"

# Core client - the main thing users need
# Cache manager - useful for performance
from flext_oracle_wms.cache import FlextOracleWmsCacheManager
from flext_oracle_wms.client import FlextOracleWmsClient

# Configuration - essential for setup
from flext_oracle_wms.config import FlextOracleWmsModuleConfig

# Constants - useful for configuration
from flext_oracle_wms.constants import (
    FlextOracleWmsDefaults,
    FlextOracleWmsEntityTypes,
)

# ESSENTIAL FUNCTIONALITIES
# Discovery - for entity discovery
from flext_oracle_wms.discovery import (
    FlextOracleWmsEntityDiscovery,
    flext_oracle_wms_create_entity_discovery,
)

# Dynamic schema processing - essential for schema discovery
# from flext_oracle_wms.dynamic import (
#     FlextOracleWmsDynamicSchemaProcessor,
#     FlextOracleWmsEntityProcessingResult,
#     FlextOracleWmsSchemaDiscoveryResult,
#     flext_oracle_wms_create_dynamic_schema_processor,
#     flext_oracle_wms_discover_entity_schemas,
#     flext_oracle_wms_process_entity_with_schema,
# )
# Exceptions - for error handling
from flext_oracle_wms.exceptions import (
    FlextOracleWmsApiError,
    FlextOracleWmsAuthenticationError,
    FlextOracleWmsError,
)

# Flattening - essential for Singer SDK compliance
from flext_oracle_wms.flattening import (
    FlatteningResult,
    FlextOracleWmsDeflattener,
    FlextOracleWmsDeflatteningResult,
    FlextOracleWmsFlattener,
    flext_oracle_wms_create_deflattener,
    flext_oracle_wms_create_flattener,
    flext_oracle_wms_deflattened_wms_record,
    flext_oracle_wms_flatten_wms_record,
)

# Models - for type safety
from flext_oracle_wms.models import (
    FlextOracleWmsEntity,
    FlextOracleWmsResponse,
)

# Types - for advanced usage
from flext_oracle_wms.types import (
    OracleWMSConfiguration,
    OracleWMSConnectionConfiguration,
)

# Clean public API - essential functionality
__all__ = [
    "FlatteningResult",
    "FlextOracleWmsApiError",
    "FlextOracleWmsAuthenticationError",
    # Cache
    "FlextOracleWmsCacheManager",
    # Main client
    "FlextOracleWmsClient",
    "FlextOracleWmsDefaults",
    "FlextOracleWmsDeflattener",
    "FlextOracleWmsDeflatteningResult",
    # Dynamic schema processing
    # "FlextOracleWmsDynamicSchemaProcessor",
    # "FlextOracleWmsEntityProcessingResult",
    # "FlextOracleWmsSchemaDiscoveryResult",
    # "flext_oracle_wms_create_dynamic_schema_processor",
    # "flext_oracle_wms_discover_entity_schemas",
    # "flext_oracle_wms_process_entity_with_schema",
    # Models
    "FlextOracleWmsEntity",
    # Discovery
    "FlextOracleWmsEntityDiscovery",
    # Constants
    "FlextOracleWmsEntityTypes",
    # Exceptions
    "FlextOracleWmsError",
    # Flattening
    "FlextOracleWmsFlattener",
    # Configuration
    "FlextOracleWmsModuleConfig",
    "FlextOracleWmsResponse",
    # "FlextOracleWmsSchemaDiscoveryResult",
    "OracleWMSConfiguration",
    "OracleWMSConnectionConfiguration",
    "flext_oracle_wms_create_deflattener",
    "flext_oracle_wms_create_entity_discovery",
    # "flext_oracle_wms_create_dynamic_schema_processor",
    "flext_oracle_wms_create_entity_discovery",
    "flext_oracle_wms_create_flattener",
    "flext_oracle_wms_deflattened_wms_record",
    # "flext_oracle_wms_discover_entity_schemas",
    "flext_oracle_wms_flatten_wms_record",
    # "flext_oracle_wms_process_entity_with_schema",
]
