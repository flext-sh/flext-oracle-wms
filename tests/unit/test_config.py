"""Tests for FlextOracleWmsSettings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_oracle_wms import FlextOracleWmsSettings


@pytest.mark.unit
def test_config_creation_valid() -> None:
    """Test settings creation with valid parameters."""
    settings = FlextOracleWmsSettings(
        base_url="https://wms.oraclecloud.com/test",
        username="user",
        password="test_password",
        timeout=30,
        retry_attempts=3,
    )
    assert settings.base_url == "https://wms.oraclecloud.com/test"
    assert settings.username == "user"
    assert settings.password == "test_password"
    assert settings.timeout == 30
    assert settings.retry_attempts == 3


@pytest.mark.unit
def test_config_validate_config_success() -> None:
    """Test validate_config returns success for valid settings."""
    settings = FlextOracleWmsSettings(timeout=30, retry_attempts=3)
    result = settings.validate_config()
    assert result.success


@pytest.mark.unit
def test_config_defaults() -> None:
    """Test settings default values."""
    settings = FlextOracleWmsSettings()
    assert settings.base_url == "http://localhost:8080"
    assert abs(settings.timeout - 30.0) < 1e-9
    assert settings.retry_attempts == 3


@pytest.mark.unit
def test_config_testing_factory() -> None:
    """Test testing_config factory method."""
    settings = FlextOracleWmsSettings.testing_config()
    assert settings.base_url == "https://test-wms.example.com"
    assert settings.username == "test_user"


@pytest.mark.unit
def test_config_auth_fields_default_empty() -> None:
    """Test auth fields default to empty string."""
    settings = FlextOracleWmsSettings()
    assert settings.username == ""
    assert settings.password == ""
