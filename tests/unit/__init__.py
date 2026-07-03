# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_oracle_wms.tests.unit.complete_mock_pipeline import (
        CompleteMockPipeline as CompleteMockPipeline,
    )
    from flext_oracle_wms.tests.unit.oracle_wms_complete_discovery import (
        OracleWmsCompleteDiscovery as OracleWmsCompleteDiscovery,
    )
    from flext_oracle_wms.tests.unit.oracle_wms_focused_discovery import (
        FocusedOracleWmsDiscovery as FocusedOracleWmsDiscovery,
    )
    from flext_oracle_wms.tests.unit.oracle_wms_optimized_discovery import (
        OptimizedOracleWmsDiscovery as OptimizedOracleWmsDiscovery,
    )
    from flext_oracle_wms.tests.unit.test_authentication import (
        TestsFlextOracleWmsAuthentication as TestsFlextOracleWmsAuthentication,
    )
    from flext_oracle_wms.tests.unit.test_authentication_core import (
        TestsFlextOracleWmsAuthenticationCore as TestsFlextOracleWmsAuthenticationCore,
    )
    from flext_oracle_wms.tests.unit.test_client import (
        TestsFlextOracleWmsClient as TestsFlextOracleWmsClient,
    )
    from flext_oracle_wms.tests.unit.test_client_class import (
        TestsFlextOracleWmsClientClass as TestsFlextOracleWmsClientClass,
    )
    from flext_oracle_wms.tests.unit.test_client_core import (
        TestsFlextOracleWmsClientCore as TestsFlextOracleWmsClientCore,
    )
    from flext_oracle_wms.tests.unit.test_config import (
        TestsFlextOracleWmsConfig as TestsFlextOracleWmsConfig,
    )
    from flext_oracle_wms.tests.unit.test_config_module import (
        TestsFlextOracleWmsConfigModule as TestsFlextOracleWmsConfigModule,
    )
    from flext_oracle_wms.tests.unit.test_connection import (
        TestsFlextOracleWmsConnection as TestsFlextOracleWmsConnection,
    )
    from flext_oracle_wms.tests.unit.test_declarative import (
        TestsFlextOracleWmsDeclarative as TestsFlextOracleWmsDeclarative,
    )
    from flext_oracle_wms.tests.unit.test_discovery import (
        TestsFlextOracleWmsDiscovery as TestsFlextOracleWmsDiscovery,
    )
    from flext_oracle_wms.tests.unit.test_filtering import (
        TestsFlextOracleWmsFiltering as TestsFlextOracleWmsFiltering,
    )
    from flext_oracle_wms.tests.unit.test_helpers import (
        TestsFlextOracleWmsHelpers as TestsFlextOracleWmsHelpers,
    )
    from flext_oracle_wms.tests.unit.test_helpers_core import (
        TestsFlextOracleWmsHelpersCore as TestsFlextOracleWmsHelpersCore,
    )
    from flext_oracle_wms.tests.unit.test_models import (
        TestsFlextOracleWmsModelsUnit as TestsFlextOracleWmsModelsUnit,
    )
    from flext_oracle_wms.tests.unit.test_schema_dynamic import (
        TestsFlextOracleWmsSchemaDynamic as TestsFlextOracleWmsSchemaDynamic,
    )
    from flext_oracle_wms.tests.unit.test_singer_flattening import (
        TestsFlextOracleWmsSingerFlattening as TestsFlextOracleWmsSingerFlattening,
    )
    from flext_oracle_wms.tests.unit.test_unified_config import (
        TestsFlextOracleWmsUnifiedConfig as TestsFlextOracleWmsUnifiedConfig,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".complete_mock_pipeline": ("CompleteMockPipeline",),
        ".oracle_wms_complete_discovery": ("OracleWmsCompleteDiscovery",),
        ".oracle_wms_focused_discovery": ("FocusedOracleWmsDiscovery",),
        ".oracle_wms_optimized_discovery": ("OptimizedOracleWmsDiscovery",),
        ".sitecustomize": ("sitecustomize",),
        ".test_api": ("test_api",),
        ".test_authentication": ("TestsFlextOracleWmsAuthentication",),
        ".test_authentication_core": ("TestsFlextOracleWmsAuthenticationCore",),
        ".test_client": ("TestsFlextOracleWmsClient",),
        ".test_client_class": ("TestsFlextOracleWmsClientClass",),
        ".test_client_core": ("TestsFlextOracleWmsClientCore",),
        ".test_config": ("TestsFlextOracleWmsConfig",),
        ".test_config_module": ("TestsFlextOracleWmsConfigModule",),
        ".test_connection": ("TestsFlextOracleWmsConnection",),
        ".test_constants": ("test_constants",),
        ".test_declarative": ("TestsFlextOracleWmsDeclarative",),
        ".test_discovery": ("TestsFlextOracleWmsDiscovery",),
        ".test_filtering": ("TestsFlextOracleWmsFiltering",),
        ".test_helpers": ("TestsFlextOracleWmsHelpers",),
        ".test_helpers_core": ("TestsFlextOracleWmsHelpersCore",),
        ".test_models": ("TestsFlextOracleWmsModelsUnit",),
        ".test_schema_dynamic": ("TestsFlextOracleWmsSchemaDynamic",),
        ".test_singer_flattening": ("TestsFlextOracleWmsSingerFlattening",),
        ".test_unified_config": ("TestsFlextOracleWmsUnifiedConfig",),
        ".test_wms_api": ("test_wms_api",),
        ".test_wms_client": ("test_wms_client",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
