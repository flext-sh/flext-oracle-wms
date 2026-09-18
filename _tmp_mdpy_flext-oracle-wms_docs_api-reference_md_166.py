# from flext-oracle-wms_docs/api-reference.md:166
from __future__ import annotations
from flext_oracle_wms import m

entity = m.OracleWms.Entity(
    name="inventory_item",
    endpoint="/entity/inventory_item",
    description="Inventory item entity",
    # Additional metadata
)
