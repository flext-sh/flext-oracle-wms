# from flext-oracle-wms/docs/development.md:166
from __future__ import annotations

from flext_core import p, r


def operation() -> p.Result[str]:
    try:
        # Operation logic
        result = "ok"
        return r.ok(result)
    except Exception as e:
        return r.fail(f"Operation failed: {e}")
