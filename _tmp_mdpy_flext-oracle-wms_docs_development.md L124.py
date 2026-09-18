# from flext-oracle-wms/docs/development.md:124
from __future__ import annotations

from flext_core import s


# Current: Multiple classes per module (71 classes total)
class WmsClient:
    pass


class WmsHelper:
    pass  # ❌ VIOLATION


# Required: Single unified class per module
class FlextOracleWmsClient(s):
    class _ClientHelper:  # ✅ NESTED HELPER
        pass
