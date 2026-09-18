# from flext-oracle-wms/src/flext_oracle_wms/README.md:124
from __future__ import annotations
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsClientSettings

# Create configuration
settings = FlextOracleWmsClientSettings(
    base_url="https://your-wms.oraclecloud.com",
    username="your_username",
    password="your_password",
    environment="production",
)

# Initialize client
client = FlextOracleWmsClient(settings)
client.start()

# Discover entities
result = client.discover_entities()
from flext_cli import u
from flext_core import FlextSettings

if result.success:
    logger = u.fetch_logger(__name__)
    logger.info("Discovered WMS entities", count=len(result.data))
    for entity in result.data:
        logger.info("Entity", name=str(entity))
