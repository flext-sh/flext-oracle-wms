# from flext-oracle-wms_docs/troubleshooting.md:91
from __future__ import annotations

# Exception classes have been updated with proper type annotations
error = FlextOracleWmsError("message", field="username")
assert error.field == "username"  # Now works with MyPy
