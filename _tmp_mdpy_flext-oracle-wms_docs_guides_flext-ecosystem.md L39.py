# from flext-oracle-wms/docs/guides/flext-ecosystem.md:39
from __future__ import annotations

# Current: Non-compliant httpx usage
import httpx

client = httpx.Client()

# Required: flext-api integration
from flext_api import FlextApiClient

client = FlextApiClient()
