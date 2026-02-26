"""Tests for Oracle WMS settings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

import pytest
from flext_oracle_wms import FlextOracleWmsConstants, FlextOracleWmsSettings
from pydantic import ValidationError


class TestFlextOracleWmsSettings:
    """Test Oracle WMS settings configuration."""

    def test_config_creation_defaults(self) -> None:
        """Test config creation with defaults."""
        config = FlextOracleWmsSettings()
        assert config.base_url == str(
            FlextOracleWmsConstants.API_CONFIG["base_url_default"],
        )
        assert config.username is None
        assert config.password is None
        assert config.api_key is None
        assert config.enable_ssl_verification is True
        assert config.use_mock is False

    def test_config_creation_custom(self) -> None:
        """Test config creation with custom values."""
        config = FlextOracleWmsSettings(
            base_url="https://test.wms.oraclecloud.com",
            username="test_user",
            password="test_password",
            api_version="v2",
            timeout=30,
            retry_attempts=5,
            enable_ssl_verification=False,
        )
        assert config.base_url == "https://test.wms.oraclecloud.com"
        assert config.username == "test_user"
        assert config.password == "test_password"
        assert config.api_version == "v2"
        assert config.timeout == 30
        assert config.retry_attempts == 5
        assert config.enable_ssl_verification is False

    def test_config_timeout_bounds(self) -> None:
        """Test timeout validation bounds."""
        with pytest.raises(ValidationError):
            FlextOracleWmsSettings(timeout=0)

        with pytest.raises(ValidationError):
            FlextOracleWmsSettings(timeout=301)

    def test_config_retry_bounds(self) -> None:
        """Test retry_attempts validation bounds."""
        with pytest.raises(ValidationError):
            FlextOracleWmsSettings(retry_attempts=-1)

        with pytest.raises(ValidationError):
            FlextOracleWmsSettings(retry_attempts=11)

    def test_validate_config_success(self) -> None:
        """Test validate_config returns success for valid config."""
        config = FlextOracleWmsSettings(timeout=30, retry_attempts=3)
        result = config.validate_config()
        assert result.is_success

    def test_testing_config_factory(self) -> None:
        """Test testing_config factory method."""
        config = FlextOracleWmsSettings.testing_config()
        assert config.use_mock is True
        assert config.base_url == "https://test-wms.example.com"

    def test_environment_from_url(self) -> None:
        """Test environment extraction from base_url."""
        config = FlextOracleWmsSettings(base_url="https://prod.wms.example.com")
        env = config.environment_from_url
        assert isinstance(env, str)

    def test_environment_from_url_unknown(self) -> None:
        """Test environment extraction returns unknown for unrecognized URL."""
        config = FlextOracleWmsSettings(base_url="https://custom.example.com")
        assert config.environment_from_url == "unknown"

    def test_enterprise_feature_flags(self) -> None:
        """Test enterprise feature flags default to False."""
        config = FlextOracleWmsSettings()
        assert config.enable_metrics is False
        assert config.enable_tracing is False
        assert config.enable_audit_logging is False

    def test_enterprise_feature_flags_enabled(self) -> None:
        """Test enterprise feature flags can be enabled."""
        config = FlextOracleWmsSettings(
            enable_metrics=True,
            enable_tracing=True,
            enable_audit_logging=True,
        )
        assert config.enable_metrics is True
        assert config.enable_tracing is True
        assert config.enable_audit_logging is True
