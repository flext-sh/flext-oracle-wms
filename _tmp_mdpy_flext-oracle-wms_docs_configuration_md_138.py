# from flext-oracle-wms_docs/configuration.md:138
from __future__ import annotations
from flext_oracle_wms import FlextOracleWmsSettings

# Configuration validation is implemented
settings = FlextOracleWmsSettings(
    base_url="https://test.example.com", username="test_user", password="test_password"
)
# Pydantic automatically validates configuration structure
