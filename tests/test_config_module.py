"""Oracle WMS Configuration Module - Standardized Testing Suite.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_oracle_wms import FlextOracleWmsConfig


def test_config_creation() -> None:
    """Test basic configuration creation using enhanced singleton pattern."""
    # Reset global instance for clean test
    FlextOracleWmsConfig.reset_global_instance()

    config = FlextOracleWmsConfig.get_global_instance()
    assert isinstance(config, FlextOracleWmsConfig)
    assert config.oracle_wms_base_url is not None
    assert config.oracle_wms_username is not None


def test_config_singleton_behavior() -> None:
    """Test enhanced singleton pattern implementation."""
    # Reset global instance for clean test
    FlextOracleWmsConfig.reset_global_instance()

    config1 = FlextOracleWmsConfig.get_global_instance()
    config2 = FlextOracleWmsConfig.get_global_instance()
    assert config1 is config2


def test_config_custom_values() -> None:
    """Test configuration with custom values."""
    config = FlextOracleWmsConfig(
        oracle_wms_base_url="https://example.com",
        oracle_wms_username="test_user",
        oracle_wms_password="test_password",
    )
    assert str(config.oracle_wms_base_url) == "https://example.com"
    assert config.oracle_wms_username == "test_user"
    assert config.oracle_wms_password.get_secret_value() == "test_password"


def test_config_validation() -> None:
    """Test successful configuration validation."""
    config = FlextOracleWmsConfig(
        oracle_wms_base_url="https://example.com",
        oracle_wms_username="test_user",
        oracle_wms_password="test_password",
    )
    result = config.validate_business_rules()
    assert result.is_success


def test_config_factory_methods() -> None:
    """Test configuration factory methods."""
    # Test for_testing factory method
    config = FlextOracleWmsConfig.create_testing_config()
    assert isinstance(config, FlextOracleWmsConfig)
    assert config.oracle_wms_base_url == "https://test.example.com"


def test_config_environment_specific() -> None:
    """Test environment-specific configuration creation."""
    dev_config = FlextOracleWmsConfig.create_for_development()
    prod_config = FlextOracleWmsConfig.create_for_production()

    assert dev_config.oracle_wms_timeout == 10
    assert prod_config.oracle_wms_timeout == 60
    assert dev_config.oracle_wms_use_mock is True
    assert prod_config.oracle_wms_use_mock is False


def test_config_reset_functionality() -> None:
    """Test singleton reset functionality."""
    # Create initial instance
    config1 = FlextOracleWmsConfig.get_global_instance()

    # Reset global instance
    FlextOracleWmsConfig.reset_global_instance()
    config2 = FlextOracleWmsConfig.get_global_instance()

    # Should be different instances after reset
    assert config1 is not config2
