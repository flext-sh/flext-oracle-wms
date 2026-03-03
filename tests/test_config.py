"""Tests for FlextOracleWmsSettings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

import pytest

from flext_oracle_wms import FlextOracleWmsConstants, FlextOracleWmsSettings


@pytest.mark.unit
def test_config_creation_valid() -> None:
    """Test config creation with valid parameters."""
    config = FlextOracleWmsSettings(
        base_url="https://wms.oraclecloud.com/test",
        username="USER_WMS_INTEGRA",
        password="test_password",
        api_version="v1",
        timeout=30,
        retry_attempts=3,
        enable_ssl_verification=True,
    )
    assert config.base_url == "https://wms.oraclecloud.com/test"
    assert config.username == "USER_WMS_INTEGRA"
    assert config.password == "test_password"
    assert config.api_version == "v1"
    assert config.timeout == 30
    assert config.retry_attempts == 3
    assert config.enable_ssl_verification is True


@pytest.mark.unit
def test_config_validate_config_success() -> None:
    """Test validate_config returns success for valid config."""
    config = FlextOracleWmsSettings(timeout=30, retry_attempts=3)
    result = config.validate_config()
    assert result.is_success


@pytest.mark.unit
def test_config_defaults_from_constants() -> None:
    """Test config defaults come from API_CONFIG constants."""
    config = FlextOracleWmsSettings()
    assert config.base_url == str(
        FlextOracleWmsConstants.API_CONFIG["base_url_default"],
    )
    assert config.timeout == int(
        FlextOracleWmsConstants.API_CONFIG["timeout_default"],
    )
    assert config.retry_attempts == int(
        FlextOracleWmsConstants.API_CONFIG["max_retries"],
    )


@pytest.mark.unit
def test_config_testing_factory() -> None:
    """Test testing_config factory method."""
    config = FlextOracleWmsSettings.testing_config()
    assert config.use_mock is True
    assert config.base_url == "https://test-wms.example.com"


@pytest.mark.unit
def test_config_optional_auth_fields() -> None:
    """Test optional auth fields default to None."""
    config = FlextOracleWmsSettings()
    assert config.username is None
    assert config.password is None
    assert config.api_key is None


@pytest.mark.unit
def test_config_environment_from_url() -> None:
    """Test environment_from_url property."""
    config = FlextOracleWmsSettings(base_url="https://custom.example.com")
    assert isinstance(config.environment_from_url, str)


@pytest.mark.unit
def test_config_enterprise_features() -> None:
    """Test enterprise feature flags."""
    config = FlextOracleWmsSettings(
        enable_metrics=True,
        enable_tracing=True,
        enable_audit_logging=True,
    )
    assert config.enable_metrics is True
    assert config.enable_tracing is True
    assert config.enable_audit_logging is True
