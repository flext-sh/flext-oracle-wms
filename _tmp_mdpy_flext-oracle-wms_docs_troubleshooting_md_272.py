# from flext-oracle-wms_docs/troubleshooting.md:272
from __future__ import annotations

error = FlextOracleWmsEntityNotFoundError("Entity missing", entity_name="test")
assert error.entity_name == "test"  # Properly handled
