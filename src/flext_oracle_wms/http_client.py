"""FLEXT Oracle WMS HTTP Client module -- backward-compat re-export.

All logic moved to _utilities/http_client.py. Import via u.OracleWms.HttpClient or this shim.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_oracle_wms import FlextOracleWmsUtilitiesHttpClient, t

FlextHttpClient = FlextOracleWmsUtilitiesHttpClient.HttpClient


def create_flext_http_client(
    base_url: str,
    timeout: float = 30.0,
    headers: t.StrMapping | None = None,
    *,
    verify_ssl: bool = True,
) -> FlextHttpClient:
    """Create FlextHttpClient instance -- backward-compat shim."""
    return FlextOracleWmsUtilitiesHttpClient.HttpClient.create(
        base_url=base_url,
        timeout=timeout,
        headers=headers,
        verify_ssl=verify_ssl,
    )


__all__ = ["FlextHttpClient", "create_flext_http_client"]
