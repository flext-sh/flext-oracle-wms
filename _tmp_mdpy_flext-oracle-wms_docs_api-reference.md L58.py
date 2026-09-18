# from flext-oracle-wms/docs/api-reference.md:58
from __future__ import annotations

result = client.test_connection()
if result.success:
    print("Connection structure verified")
else:
    print(f"Connection failed: {result.error}")
