# from flext-oracle-wms/examples/README.md:78
from __future__ import annotations
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsClientSettings

# Configure Oracle WMS connection
settings = FlextOracleWmsClientSettings(
    base_url="https://your-wms-instance.oraclecloud.com",
    username="your_username",
    password="your_password",
)

# Initialize client
client = FlextOracleWmsClient(settings)

# Discover available entities
result = client.discover_entities()
if result.success:
    print(f"Found {len(result.data)} WMS entities")
    for entity in result.data:
        print(f"- {entity.name}: {entity.description}")
