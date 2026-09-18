# from flext-oracle-wms_docs/configuration.md:100
from __future__ import annotations
from flext_oracle_wms import FlextOracleWmsSettings

# Note: This is framework structure, not fully implemented
settings = FlextOracleWmsSettings(
    base_url="https://test.example.com",  # Currently only test URLs
    username="test_user",
    password="test_password",
    timeout=30,
    # Additional configuration options
)
