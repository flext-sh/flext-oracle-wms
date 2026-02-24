"""Unit tests for FlextOracleWmsSettings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextSettings

from flext_oracle_wms import FlextOracleWmsConstants
from flext_oracle_wms.settings import FlextOracleWmsSettings


class TestFlextOracleWmsSettings:
    """Test cases for FlextOracleWmsSettings class."""

    def test_class_inheritance(self) -> None:
        """Test proper inheritance from FlextSettings."""
        assert issubclass(FlextOracleWmsSettings, FlextSettings)

    def test_default_initialization(self) -> None:
        """Test default configuration initialization."""
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
        assert config.enable_ssl_verification is True
        assert config.enable_metrics is False
        assert config.enable_tracing is False
        assert config.enable_audit_logging is False
        assert config.api_version == str(
            FlextOracleWmsConstants.API_CONFIG["version_default"],
        )

    def test_custom_initialization(self) -> None:
        """Test custom configuration initialization."""
        config = FlextOracleWmsSettings(
            base_url="https://custom-wms.example.com",
            timeout=60,
            retry_attempts=5,
            enable_ssl_verification=False,
            enable_metrics=True,
        )

        assert config.base_url == "https://custom-wms.example.com"
        assert config.timeout == 60
        assert config.retry_attempts == 5
        assert config.enable_ssl_verification is False
        assert config.enable_metrics is True

    def test_authentication_fields(self) -> None:
        """Test authentication configuration fields."""
        config = FlextOracleWmsSettings(
            username="test_user",
            password="test_pass",
        )

        assert config.username == "test_user"
        assert config.password == "test_pass"

    def test_enterprise_features(self) -> None:
        """Test enterprise feature configuration."""
        config = FlextOracleWmsSettings(
            enable_metrics=True,
            enable_tracing=True,
            enable_audit_logging=True,
        )

        assert config.enable_metrics is True
        assert config.enable_tracing is True
        assert config.enable_audit_logging is True

    def test_testing_config_factory(self) -> None:
        """Test testing_config classmethod."""
        config = FlextOracleWmsSettings.testing_config()
        assert isinstance(config, FlextOracleWmsSettings)
        assert config.use_mock is True
        assert config.base_url == "https://test-wms.example.com"

    def test_environment_from_url_property(self) -> None:
        """Test environment_from_url property."""
        config = FlextOracleWmsSettings(
            base_url="https://custom.example.com",
        )
        assert isinstance(config.environment_from_url, str)
        assert config.environment_from_url == "unknown"
