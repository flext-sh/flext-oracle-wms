# from flext-oracle-wms_docs/api-reference.md:37
from __future__ import annotations
from flext_oracle_wms import FlextOracleWmsApi, FlextOracleWmsSettings

# Initialize the API facade
settings = FlextOracleWmsSettings.model_validate({
    "OracleWms": {
        "base_url": "https://test.example.com",
        "username": "test_user",
        "password": "test_password",
    }
})
api = FlextOracleWmsApi(settings=settings)
