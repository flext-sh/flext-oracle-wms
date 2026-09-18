# from flext-oracle-wms_docs/development.md:147
from __future__ import annotations


# Current: Custom authentication
class CustomAuth:
    pass  # ❌ VIOLATION


# Required: flext-auth integration
from flext_auth import FlextAuth  # ✅ REQUIRED

_ = FlextAuth  # reference without instantiating the auth facade
