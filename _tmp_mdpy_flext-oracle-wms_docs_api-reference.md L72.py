# from flext-oracle-wms/docs/api-reference.md:72
from __future__ import annotations

result = client.discover_entities()
if result.success:
    entities = result.value
    print(f"Found {len(entities)} entities")
