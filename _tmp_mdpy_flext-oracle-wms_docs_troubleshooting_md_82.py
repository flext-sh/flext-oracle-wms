# from flext-oracle-wms_docs/troubleshooting.md:82
from __future__ import annotations

error = FlextOracleWmsError("message", field="username")
assert error.field == "username"  # MyPy error: attribute not found
