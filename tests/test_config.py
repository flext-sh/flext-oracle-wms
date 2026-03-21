"""Tests for FlextOracleWmsSettings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_oracle_wms import FlextOracleWmsSettings


@pytest.mark.unit
def test_config_creation_valid() -> None:
    """Test config creation with valid parameters."""
    config = FlextOracleWmsSettings(
        base_url="https://wms.oraclecloud.com/test",
        username="USER_WMS_INTEGRA",
        password="test_password",
        timeout=30,
        retry_attempts=3,
    )
    assert config.base_url == "https://wms.oraclecloud.com/test"
    assert config.username == "USER_WMS_INTEGRA"
    assert config.password == "test_password"
    assert config.timeout == 30
    assert config.retry_attempts == 3


@pytest.mark.unit
def test_config_validate_config_success() -> None:
    """Test validate_config returns success for valid config."""
    config = FlextOracleWmsSettings(timeout=30, retry_attempts=3)
    result = config.validate_config()
    assert result.is_success


@pytest.mark.unit
def test_config_defaults() -> None:
    """Test config default values."""
    config = FlextOracleWmsSettings()
    assert config.base_url == "http://localhost:8080"
    assert config.timeout == pytest.approx(30.0)
    assert config.retry_attempts == 3


@pytest.mark.unit
def test_config_testing_factory() -> None:
    """Test testing_config factory method."""
    config = FlextOracleWmsSettings.testing_config()
    assert config.use_mock is True
    assert config.base_url == "https://test-wms.example.com"


@pytest.mark.unit
def test_config_auth_fields_default_empty() -> None:
    """Test auth fields default to empty string."""
    config = FlextOracleWmsSettings()
    assert config.username == ""
    assert config.password == ""
