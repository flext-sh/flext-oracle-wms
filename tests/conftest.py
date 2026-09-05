"""Typed fixtures backed by the public Oracle WMS owners.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_oracle_wms import (
    FlextOracleWmsApi,
    FlextOracleWmsSettings,
    config,
    p,
    settings,
    u,
)


@pytest.fixture
def oracle_wms_settings() -> FlextOracleWmsSettings:
    """Return the public runtime settings singleton."""
    return settings


@pytest.fixture
def oracle_wms_config() -> p.OracleWms.Config:
    """Return the validated public business-rule configuration."""
    return config.oracle_wms


@pytest.fixture
def oracle_wms_api(
    oracle_wms_settings: FlextOracleWmsSettings,
) -> FlextOracleWmsApi:
    """Return the real public composition root with injected settings."""
    return FlextOracleWmsApi(settings=oracle_wms_settings)


@pytest.fixture
def oracle_wms_http_client(
    oracle_wms_settings: FlextOracleWmsSettings,
) -> u.OracleWms.HttpClient:
    """Create the public HTTP client from the runtime settings owner."""
    runtime = oracle_wms_settings.OracleWms
    return FlextOracleWmsApi.create_flext_http_client(
        base_url=runtime.base_url,
        timeout=runtime.timeout,
        verify_ssl=runtime.verify_ssl,
    )
