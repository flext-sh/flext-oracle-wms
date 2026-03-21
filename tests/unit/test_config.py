"""Unit tests for FlextOracleWmsSettings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextSettings
from flext_tests import u

from flext_oracle_wms import FlextOracleWmsConstants
from flext_oracle_wms.settings import FlextOracleWmsSettings


class TestFlextOracleWmsSettings:
    """Test cases for FlextOracleWmsSettings class."""

    def test_class_inheritance(self) -> None:
        """Test proper inheritance from FlextSettings."""
        u.Tests.Matchers.that(
            issubclass(FlextOracleWmsSettings, FlextSettings), eq=True
        )

    def test_default_initialization(self) -> None:
        """Test default configuration initialization."""
        config = FlextOracleWmsSettings()
        u.Tests.Matchers.that(
            config.base_url
            == str(FlextOracleWmsConstants.API_CONFIG["base_url_default"]),
            eq=True,
        )
        u.Tests.Matchers.that(
            config.timeout
            == int(FlextOracleWmsConstants.API_CONFIG["timeout_default"]),
            eq=True,
        )
        u.Tests.Matchers.that(
            config.retry_attempts
            == int(FlextOracleWmsConstants.API_CONFIG["max_retries"]),
            eq=True,
        )
        u.Tests.Matchers.that(config.enable_ssl_verification is True, eq=True)
        u.Tests.Matchers.that(config.enable_metrics is False, eq=True)
        u.Tests.Matchers.that(config.enable_tracing is False, eq=True)
        u.Tests.Matchers.that(config.enable_audit_logging is False, eq=True)
        u.Tests.Matchers.that(
            config.api_version
            == str(FlextOracleWmsConstants.API_CONFIG["version_default"]),
            eq=True,
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
        u.Tests.Matchers.that(
            config.base_url == "https://custom-wms.example.com", eq=True
        )
        u.Tests.Matchers.that(config.timeout == 60, eq=True)
        u.Tests.Matchers.that(config.retry_attempts == 5, eq=True)
        u.Tests.Matchers.that(config.enable_ssl_verification is False, eq=True)
        u.Tests.Matchers.that(config.enable_metrics is True, eq=True)

    def test_authentication_fields(self) -> None:
        """Test authentication configuration fields."""
        config = FlextOracleWmsSettings(username="test_user", password="test_pass")
        u.Tests.Matchers.that(config.username == "test_user", eq=True)
        u.Tests.Matchers.that(config.password == "test_pass", eq=True)

    def test_enterprise_features(self) -> None:
        """Test enterprise feature configuration."""
        config = FlextOracleWmsSettings(
            enable_metrics=True, enable_tracing=True, enable_audit_logging=True
        )
        u.Tests.Matchers.that(config.enable_metrics is True, eq=True)
        u.Tests.Matchers.that(config.enable_tracing is True, eq=True)
        u.Tests.Matchers.that(config.enable_audit_logging is True, eq=True)

    def test_testing_config_factory(self) -> None:
        """Test testing_config classmethod."""
        config = FlextOracleWmsSettings.testing_config()
        u.Tests.Matchers.that(isinstance(config, FlextOracleWmsSettings), eq=True)
        u.Tests.Matchers.that(config.use_mock is True, eq=True)
        u.Tests.Matchers.that(
            config.base_url == "https://test-wms.example.com", eq=True
        )

    def test_environment_from_url_property(self) -> None:
        """Test environment_from_url property."""
        config = FlextOracleWmsSettings(base_url="https://custom.example.com")
        u.Tests.Matchers.that(isinstance(config.environment_from_url, str), eq=True)
        u.Tests.Matchers.that(config.environment_from_url == "unknown", eq=True)
