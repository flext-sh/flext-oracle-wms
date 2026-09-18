# from flext-oracle-wms_docs/getting-started.md:59
from __future__ import annotations
from flext_oracle_wms import FlextOracleWmsApi, FlextOracleWmsSettings

# Using test configuration (not real Oracle WMS)
settings = FlextOracleWmsSettings.model_validate({
    "OracleWms": {
        "base_url": "https://test.example.com",
        "username": "test_user",
        "password": "test_password",
    }
})
print(f"Test Base URL: {settings.OracleWms.base_url}")

# Build the API facade from the settings
api = FlextOracleWmsApi(settings=settings)

# execute() returns a FlextResult — inspect .success / .value
result = api.execute()
print(f"Execute success: {result.success}")
