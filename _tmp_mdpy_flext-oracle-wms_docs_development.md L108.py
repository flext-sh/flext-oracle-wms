# from flext-oracle-wms/docs/development.md:108
from __future__ import annotations

# Current: Non-compliant httpx usage
import httpx  # ❌ VIOLATION

client = httpx.Client()

# Required: flext-api integration
from flext_api import FlextApiClient  # ✅ REQUIRED

client = FlextApiClient()
