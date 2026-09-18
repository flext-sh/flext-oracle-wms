# from flext-oracle-wms_docs/troubleshooting.md:263
from __future__ import annotations

error = FlextOracleWmsConnectionError("failed", retry_count=3)
assert error.retry_count == 3  # Now works after exception class updates
