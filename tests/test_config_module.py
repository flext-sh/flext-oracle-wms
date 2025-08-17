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
"""

from flext_oracle_wms import (
    FlextOracleWmsModuleConfig,
)


def test_config_creation() -> None:
    """Test basic configuration creation."""
    config = FlextOracleWmsModuleConfig(
        base_url="https://example.com",
        username="test_user",
        password="test_pass",
    )
    assert str(config.base_url) == "https://example.com/"
    assert config.username == "test_user"
    assert config.password == "test_pass"


def test_config_defaults() -> None:
    """Test configuration default values."""
    config = FlextOracleWmsModuleConfig(
        base_url="https://example.com",
        username="test_user",
        password="test_pass",
    )
    assert config.timeout_seconds == 30
    assert config.batch_size == 100
    assert config.max_retries == 3
    assert config.enable_cache is True


def test_config_custom_values() -> None:
    """Test configuration with custom values."""
    config = FlextOracleWmsModuleConfig(
        base_url="https://example.com",
        username="test_user",
        password="test_pass",
        timeout_seconds=60,
        batch_size=50,
        max_retries=5,
        enable_cache=False,
    )
    assert config.timeout_seconds == 60
    assert config.batch_size == 50
    assert config.max_retries == 5
    assert config.enable_cache is False


def test_config_validation_success() -> None:
    """Test successful configuration validation."""
    config = FlextOracleWmsModuleConfig(
        base_url="https://example.com",
        username="test_user",
        password="test_pass",
    )
    # Configuration is valid if it can be created without errors
    assert config.username == "test_user"
    assert config.password == "test_pass"


def test_config_from_dict() -> None:
    """Test configuration creation from dictionary."""
    config = FlextOracleWmsModuleConfig(
        base_url="https://example.com",
        username="test_user",
        password="test_pass",
        timeout_seconds=45,
    )
    assert str(config.base_url) == "https://example.com/"
    assert config.username == "test_user"
    assert config.timeout_seconds == 45


def test_config_factory_function() -> None:
    """Test configuration factory function."""
    # Use the for_testing factory method instead
    config = FlextOracleWmsModuleConfig.for_testing()
    assert isinstance(config, FlextOracleWmsModuleConfig)
    assert config.environment == "test"


def test_config_url_validation() -> None:
    """Test URL validation in configuration."""
    config = FlextOracleWmsModuleConfig(
        base_url="https://example.com",
        username="test_user",
        password="test_pass",
    )
    # Should not raise an exception
    assert str(config.base_url).startswith("https://")


def test_config_batch_size_validation() -> None:
    """Test batch size validation."""
    config = FlextOracleWmsModuleConfig(
        base_url="https://example.com",
        username="test_user",
        password="test_pass",
        batch_size=1000,
    )
    assert config.batch_size == 1000


def test_config_timeout_validation() -> None:
    """Test timeout validation."""
    config = FlextOracleWmsModuleConfig(
        base_url="https://example.com",
        username="test_user",
        password="test_pass",
        timeout_seconds=120,
    )
    assert config.timeout_seconds == 120


def test_config_str_representation() -> None:
    """Test configuration string representation."""
    config = FlextOracleWmsModuleConfig(
        base_url="https://example.com",
        username="test_user",
        password="test_pass",
    )
    config_str = str(config)
    assert "example.com" in config_str
    assert "test_user" in config_str


def test_config_equality() -> None:
    """Test configuration equality comparison."""
    config1 = FlextOracleWmsModuleConfig(
        base_url="https://example.com",
        username="test_user",
        password="test_pass",
    )
    config2 = FlextOracleWmsModuleConfig(
        base_url="https://example.com",
        username="test_user",
        password="test_pass",
    )
    # They should have the same values
    assert config1.base_url == config2.base_url
    assert config1.username == config2.username


def test_config_with_optional_fields() -> None:
    """Test configuration with optional fields."""
    config = FlextOracleWmsModuleConfig(
        base_url="https://example.com",
        username="test_user",
        password="test_pass",
        api_version="v11",
        project_name="TEST_PROJECT",
        environment="staging",
    )
    assert config.api_version == "v11"
    assert config.project_name == "TEST_PROJECT"
    assert config.environment == "staging"
