# from flext-oracle-wms/src/flext_oracle_wms/README.md:154
from __future__ import annotations
# Query entity data with filtering
result = client.get_entity_data(
    entity_name="item",
    limit=100,
    fields="item_id,item_name,item_desc",
    filters={"status": "active"}
)

if result.success:
    data = result.data
from flext_cli import u
from flext_core import FlextSettings
    u.fetch_logger(__name__).info("Records retrieved", count=len(data.get('results', [])))
