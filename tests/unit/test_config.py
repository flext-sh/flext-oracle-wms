"""Unit tests for FlextOracleWmsConfig class.

Tests the configuration module following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextConfig

from flext_oracle_wms.config import FlextOracleWmsConfig


class TestFlextOracleWmsConfig:
    """Test cases for FlextOracleWmsConfig class."""

    def test_class_inheritance(self) -> None:
        """Test that FlextOracleWmsConfig follows proper inheritance patterns."""
        # FlextOracleWmsConfig should inherit from FlextConfig
        assert issubclass(FlextOracleWmsConfig, FlextConfig)

    def test_default_initialization(self) -> None:
        """Test default configuration initialization."""
        config = FlextOracleWmsConfig()

        # Test default values
        assert config.base_url == "https://wms.oraclecloud.com"
        assert config.timeout == 30
        assert config.retry_attempts == 3
        assert config.enable_ssl_verification is True
        assert config.enable_metrics is False
        assert config.enable_tracing is False
        assert config.enable_audit_logging is False
        assert config.api_version == "v2"

    def test_custom_initialization(self) -> None:
        """Test custom configuration initialization."""
        config = FlextOracleWmsConfig(
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
        config = FlextOracleWmsConfig(
            username="test_user",
            password="test_pass",
        )

        assert config.username == "test_user"
        assert config.password == "test_pass"

    def test_enterprise_features(self) -> None:
        """Test enterprise feature configuration."""
        config = FlextOracleWmsConfig(
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
        config1 = FlextOracleWmsConfig.create_default()
        assert isinstance(config1, FlextOracleWmsConfig)

        # Test development config
        config2 = FlextOracleWmsConfig.create_for_development()
        assert isinstance(config2, FlextOracleWmsConfig)

        # Test testing config
        config3 = FlextOracleWmsConfig.for_testing()
        assert isinstance(config3, FlextOracleWmsConfig)

        # Test global instance
        config4 = FlextOracleWmsConfig.get_oracle_wms_global_instance()
        assert isinstance(config4, FlextOracleWmsConfig)

    def test_environment_extraction(self) -> None:
        """Test environment extraction from URL."""
        # Test production URL
        config_prod = FlextOracleWmsConfig(base_url="https://prod-wms.oraclecloud.com")
        assert config_prod.extract_environment_from_url() == "production"

        # Test test URL
        config_test = FlextOracleWmsConfig(base_url="https://test-wms.oraclecloud.com")
        assert config_test.extract_environment_from_url() == "test"

        # Test demo URL
        config_demo = FlextOracleWmsConfig(base_url="https://demo-wms.oraclecloud.com")
        assert config_demo.extract_environment_from_url() == "demo"

        # Test default URL
        config_default = FlextOracleWmsConfig()
        assert config_default.extract_environment_from_url() == "default"

    def test_legacy_field_aliases(self) -> None:
        """Test that legacy field aliases still work."""
        config = FlextOracleWmsConfig()

        # Test that both new and legacy field names exist
        assert hasattr(config, "base_url")
        assert hasattr(config, "oracle_wms_base_url")
        assert hasattr(config, "timeout")
        assert hasattr(config, "oracle_wms_timeout")
        assert hasattr(config, "retry_attempts")
        assert hasattr(config, "oracle_wms_max_retries")
        assert hasattr(config, "enable_ssl_verification")
        assert hasattr(config, "oracle_wms_verify_ssl")


__all__ = ["TestFlextOracleWmsConfig"]
