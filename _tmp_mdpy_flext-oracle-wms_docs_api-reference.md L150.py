# from flext-oracle-wms/docs/api-reference.md:150
from __future__ import annotations

result = client.some_operation()
if result.success:
    data = result.value  # Type-safe access
else:
    error = result.error  # Error message
