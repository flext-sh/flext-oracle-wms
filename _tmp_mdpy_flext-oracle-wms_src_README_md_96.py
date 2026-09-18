# from flext-oracle-wms_src/README.md:96
from __future__ import annotations
from flext_oracle_wms import FlextOracleWmsApi, FlextOracleWmsSettings

# Type-safe configuration
settings = FlextOracleWmsSettings(
    base_url="https://your-wms.oraclecloud.com",
    username="your_username",
    password="your_password",
)

# Build the API facade and discover entities (requires a live Oracle WMS)
api = FlextOracleWmsApi.with_settings(settings)
result = api.create_oracle_wms_client(settings)

# Railway-oriented programming with FlextResult
if result.success:
    client = result.value
    print("Client created")
else:
    print(f"Discovery failed: {result.error}")
