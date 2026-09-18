# from flext-oracle-wms/src/README.md:121
from __future__ import annotations
import os

from flext_oracle_wms import FlextOracleWmsSettings

# Environment-driven configuration with validation
settings = FlextOracleWmsSettings.model_validate({
    "OracleWms": {
        "base_url": os.getenv("FLEXT_ORACLE_WMS_BASE_URL", "https://test.example.com"),
        "username": os.getenv("FLEXT_ORACLE_WMS_USERNAME", "test_user"),
        "password": os.getenv("FLEXT_ORACLE_WMS_PASSWORD", "test_password"),
        "auth_method": "basic",
        "timeout": 30,
        "retry_attempts": 3,
    }
})
print(settings.OracleWms.base_url)
