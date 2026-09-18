# from flext-oracle-wms/docs/configuration.md:43
from __future__ import annotations
from flext_oracle_wms import FlextOracleWmsSettings

settings = FlextOracleWmsSettings.model_validate({
    "OracleWms": {
        "base_url": "https://test.example.com",
        "username": "test_user",
        "password": "test_password",
    }
})
print(settings.OracleWms.base_url)  # "https://test.example.com"
print(settings.OracleWms.username)  # "test_user"
print(settings.OracleWms.api_version)  # Current API version
print(settings.OracleWms.timeout)  # Default timeout
