# from flext-oracle-wms_docs/troubleshooting.md:105
from __future__ import annotations
from flext_oracle_wms import FlextOracleWmsModuleSettings, FlextOracleWmsApiVersion

settings = FlextOracleWmsModuleSettings(
    api_version=FlextOracleWmsApiVersion.V1,  # Use enum, not string
    oracle_wms_timeout=30,  # Use int, not float
)
