"""Unit tests for FlextOracleWmsSettings class.

Tests the configuration module following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextSettings

from flext_oracle_wms.settings import FlextOracleWmsSettings


class TestFlextOracleWmsSettings:
    """Test cases for FlextOracleWmsSettings class."""

    def test_class_inheritance(self) -> None:
        """Test that FlextOracleWmsSettings follows proper inheritance patterns."""
        # FlextOracleWmsSettings should inherit from FlextSettings
        assert issubclass(FlextOracleWmsSettings, FlextSettings)

    def test_default_initialization(self) -> None:
        """Test default configuration initialization."""
        config = FlextOracleWmsSettings()

        # Test default values
        assert config.base_url == "https://wms.oraclecloud.com"
        assert config.timeout == 60
        assert config.retry_attempts == 3
        assert config.enable_ssl_verification is True
        assert config.enable_metrics is False
        assert config.enable_tracing is False
        assert config.enable_audit_logging is False
        assert config.api_version == "v2"

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

    def test_class_methods(self) -> None:
        """Test class method factories."""
        # Test default creation
        config1 = FlextOracleWmsSettings.create_default()
        assert isinstance(config1, FlextOracleWmsSettings)

        # Test development config
        config2 = FlextOracleWmsSettings.create_for_development()
        assert isinstance(config2, FlextOracleWmsSettings)

        # Test testing config
        config3 = FlextOracleWmsSettings.testing_config()
        assert isinstance(config3, FlextOracleWmsSettings)

        # Test global instance
        config4 = FlextOracleWmsSettings.get_oracle_wms_global_instance()
        assert isinstance(config4, FlextOracleWmsSettings)

    def test_environment_extraction(self) -> None:
        """Test environment extraction from URL."""
        # Test production URL
        config_prod = FlextOracleWmsSettings(
            base_url="https://prod-wms.oraclecloud.com"
        )
        assert config_prod.environment_from_url() == "prod"

        # Test test URL
        config_test = FlextOracleWmsSettings(
            base_url="https://test-wms.oraclecloud.com"
        )
        assert config_test.environment_from_url() == "unknown"

        # Test dev URL
        config_dev = FlextOracleWmsSettings(base_url="https://dev-wms.oraclecloud.com")
        assert config_dev.environment_from_url() == "dev"

        # Test staging URL
        config_staging = FlextOracleWmsSettings(
            base_url="https://staging-wms.oraclecloud.com",
        )
        assert config_staging.environment_from_url() == "staging"

        # Test default URL
        config_default = FlextOracleWmsSettings()
        assert config_default.environment_from_url() == "unknown"

    def test_legacy_field_aliases(self) -> None:
        """Test that legacy field aliases still work."""
        config = FlextOracleWmsSettings()

        # Test that both new and legacy field names exist
        assert hasattr(config, "base_url")
        assert hasattr(config, "oracle_wms_base_url")
        assert hasattr(config, "timeout")
        assert hasattr(config, "oracle_wms_timeout")
        assert hasattr(config, "retry_attempts")
        assert hasattr(config, "oracle_wms_max_retries")
        assert hasattr(config, "enable_ssl_verification")
        assert hasattr(config, "oracle_wms_verify_ssl")


__all__ = ["TestFlextOracleWmsSettings"]
