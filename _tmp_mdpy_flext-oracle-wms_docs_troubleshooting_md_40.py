# from flext-oracle-wms_docs/troubleshooting.md:40
from __future__ import annotations

# Expected behavior with current implementation
settings = FlextOracleWmsModuleSettings.for_testing()
client = FlextOracleWmsClient(settings)
result = client.test_connection()  # Expected to fail
