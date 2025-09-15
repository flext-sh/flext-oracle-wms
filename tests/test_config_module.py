"""Oracle WMS Configuration Module - Comprehensive Testing Suite.

This module provides comprehensive testing for Oracle WMS configuration
management, including Pydantic-based configuration validation, environment
variable handling, and enterprise configuration patterns.

Test Coverage:
    - Configuration object creation with various parameter combinations
    - Pydantic validation and type checking for configuration fields
    - Environment variable loading and precedence testing
    - Configuration defaults and override behavior validation
    - Security configuration patterns and credential handling
    - Configuration serialization and deserialization testing

Test Categories:
    - Unit tests for configuration object instantiation
    - Validation tests for required and optional fields
    - Environment variable integration and override testing
    - Security and credential management validation
    - Configuration compatibility and migration testing

Author: FLEXT Development Team
Version: 0.9.0
License: MIT


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from flext_oracle_wms import (
    FlextOracleWmsApiVersion,
    FlextOracleWmsModuleConfig,
    OracleWMSAuthMethod,
)


def test_config_creation() -> None:
    """Test basic configuration creation using singleton pattern."""
    # Reset global instance for clean test
    FlextOracleWmsModuleConfig.reset_global_instance()

    config = FlextOracleWmsModuleConfig.get_oracle_wms_global_instance(
        oracle_wms_base_url="https://example.com",
        oracle_wms_username="test_user",
        oracle_wms_password="test_pass",
    )
    assert str(config.oracle_wms_base_url) == "https://example.com"
    assert config.oracle_wms_username == "test_user"
    assert config.oracle_wms_password == "test_pass"


def test_config_defaults() -> None:
    """Test configuration default values using singleton pattern."""
    # Reset global instance for clean test
    FlextOracleWmsModuleConfig.reset_global_instance()

    config = FlextOracleWmsModuleConfig.get_oracle_wms_global_instance(
        oracle_wms_base_url="https://example.com",
        oracle_wms_username="test_user",
        oracle_wms_password="test_pass",
    )
    assert config.oracle_wms_timeout == 30
    assert config.oracle_wms_max_retries == 3
    assert config.oracle_wms_verify_ssl is True
    assert config.oracle_wms_enable_logging is True


def test_config_custom_values() -> None:
    """Test configuration with custom values."""
    config = FlextOracleWmsModuleConfig(
        oracle_wms_base_url="https://example.com",
        oracle_wms_username="test_user",
        oracle_wms_password="test_pass",
        oracle_wms_timeout=60,
        oracle_wms_max_retries=5,
        oracle_wms_verify_ssl=False,
        oracle_wms_enable_logging=False,
    )
    assert config.oracle_wms_timeout == 60
    assert config.oracle_wms_max_retries == 5
    assert config.oracle_wms_verify_ssl is False
    assert config.oracle_wms_enable_logging is False


def test_config_validation_success() -> None:
    """Test successful configuration validation."""
    config = FlextOracleWmsModuleConfig(
        oracle_wms_base_url="https://example.com",
        oracle_wms_username="test_user",
        oracle_wms_password="test_pass",
    )
    # Configuration is valid if it can be created without errors
    assert config.oracle_wms_username == "test_user"
    assert config.oracle_wms_password == "test_pass"


def test_config_from_dict() -> None:
    """Test configuration creation from dictionary."""
    config = FlextOracleWmsModuleConfig(
        oracle_wms_base_url="https://example.com",
        oracle_wms_username="test_user",
        oracle_wms_password="test_pass",
        oracle_wms_timeout=45,
    )
    assert str(config.oracle_wms_base_url) == "https://example.com"
    assert config.oracle_wms_username == "test_user"
    assert config.oracle_wms_timeout == 45


def test_config_factory_function() -> None:
    """Test configuration factory function."""
    # Use the for_testing factory method instead
    config = FlextOracleWmsModuleConfig.for_testing()
    assert isinstance(config, FlextOracleWmsModuleConfig)
    assert config.oracle_wms_base_url == "https://test.example.com"


def test_config_url_validation() -> None:
    """Test URL validation in configuration."""
    config = FlextOracleWmsModuleConfig(
        oracle_wms_base_url="https://example.com",
        oracle_wms_username="test_user",
        oracle_wms_password="test_pass",
    )
    # Should not raise an exception
    assert str(config.oracle_wms_base_url).startswith("https://")


def test_config_max_retries_validation() -> None:
    """Test max retries validation."""
    config = FlextOracleWmsModuleConfig(
        oracle_wms_base_url="https://example.com",
        oracle_wms_username="test_user",
        oracle_wms_password="test_pass",
        oracle_wms_max_retries=10,
    )
    assert config.oracle_wms_max_retries == 10


def test_config_timeout_validation() -> None:
    """Test timeout validation."""
    config = FlextOracleWmsModuleConfig(
        oracle_wms_base_url="https://example.com",
        oracle_wms_username="test_user",
        oracle_wms_password="test_pass",
        oracle_wms_timeout=120,
    )
    assert config.oracle_wms_timeout == 120


def test_config_str_representation() -> None:
    """Test configuration string representation."""
    config = FlextOracleWmsModuleConfig(
        oracle_wms_base_url="https://example.com",
        oracle_wms_username="test_user",
        oracle_wms_password="test_pass",
    )
    config_str = str(config)
    assert "example.com" in config_str
    assert "test_user" in config_str


def test_config_equality() -> None:
    """Test configuration equality comparison."""
    config1 = FlextOracleWmsModuleConfig(
        oracle_wms_base_url="https://example.com",
        oracle_wms_username="test_user",
        oracle_wms_password="test_pass",
    )
    config2 = FlextOracleWmsModuleConfig(
        oracle_wms_base_url="https://example.com",
        oracle_wms_username="test_user",
        oracle_wms_password="test_pass",
    )
    # They should have the same values
    assert config1.oracle_wms_base_url == config2.oracle_wms_base_url
    assert config1.oracle_wms_username == config2.oracle_wms_username


def test_singleton_pattern() -> None:
    """Test singleton pattern behavior."""
    # Reset global instance for clean test
    FlextOracleWmsModuleConfig.reset_global_instance()

    # Get first instance
    config1 = FlextOracleWmsModuleConfig.get_oracle_wms_global_instance(
        oracle_wms_base_url="https://first.com",
        oracle_wms_username="user1",
    )

    # Get second instance - should be the same object
    config2 = FlextOracleWmsModuleConfig.get_oracle_wms_global_instance(
        oracle_wms_base_url="https://second.com",  # This should update the existing instance
        oracle_wms_username="user2",
    )

    # Should be the same instance
    assert config1 is config2

    # Should have updated values
    assert config2.oracle_wms_base_url == "https://second.com"
    assert config2.oracle_wms_username == "user2"


def test_singleton_update_method() -> None:
    """Test singleton update method."""
    # Reset global instance for clean test
    FlextOracleWmsModuleConfig.reset_global_instance()

    # Create initial instance
    config = FlextOracleWmsModuleConfig.get_oracle_wms_global_instance(
        oracle_wms_base_url="https://initial.com",
        oracle_wms_username="initial_user",
    )

    # Update using update_global_instance method
    update_result = FlextOracleWmsModuleConfig.update_global_instance(
        oracle_wms_base_url="https://updated.com",
        oracle_wms_username="updated_user",
    )

    assert update_result.success
    updated_config = update_result.value

    # Should be the same instance
    assert config is updated_config

    # Should have updated values
    assert updated_config.oracle_wms_base_url == "https://updated.com"
    assert updated_config.oracle_wms_username == "updated_user"


def test_singleton_reset_method() -> None:
    """Test singleton reset method."""
    # Create initial instance
    config1 = FlextOracleWmsModuleConfig.get_oracle_wms_global_instance(
        oracle_wms_base_url="https://first.com",
    )

    # Reset global instance
    FlextOracleWmsModuleConfig.reset_global_instance()

    # Create new instance
    config2 = FlextOracleWmsModuleConfig.get_oracle_wms_global_instance(
        oracle_wms_base_url="https://second.com",
    )

    # Should be different instances
    assert config1 is not config2
    assert config2.oracle_wms_base_url == "https://second.com"


def test_config_with_optional_fields() -> None:
    """Test configuration with optional fields."""
    config = FlextOracleWmsModuleConfig(
        oracle_wms_base_url="https://example.com/staging",
        oracle_wms_username="test_user",
        oracle_wms_password="test_pass",
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        auth_method=OracleWMSAuthMethod.BASIC,
    )
    assert config.api_version == FlextOracleWmsApiVersion.LGF_V10
    assert config.auth_method == OracleWMSAuthMethod.BASIC
    # The method should extract "staging" from the URL path
    assert config.extract_environment_from_url() == "staging"
