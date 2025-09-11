"""Unit tests for FlextOracleWmsClientConfig - BASED ON WORKING CODE.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import pytest
from pydantic import ValidationError

from flext_oracle_wms import FlextOracleWmsApiVersion, FlextOracleWmsClientConfig


@pytest.mark.unit
def test_config_creation_valid() -> None:
    """Test config creation with valid parameters - EXACTLY like working example."""
    config = FlextOracleWmsClientConfig(
        base_url="https://ta29.wms.ocs.oraclecloud.com/raizen_test",
        username="USER_WMS_INTEGRA",
        password="test_password",
        environment="development",
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        timeout=30.0,
        max_retries=3,
        verify_ssl=True,
        enable_logging=True,
    )

    assert config.base_url == "https://ta29.wms.ocs.oraclecloud.com/raizen_test"
    assert config.username == "USER_WMS_INTEGRA"
    assert config.password == "test_password"
    assert config.environment == "test"
    assert config.api_version == FlextOracleWmsApiVersion.LGF_V10
    assert config.timeout == 30.0
    assert config.max_retries == 3
    assert config.verify_ssl is True
    assert config.enable_logging is True


@pytest.mark.unit
def test_config_validation_success() -> None:
    """Test config domain validation - BASED ON WORKING PATTERN."""
    config = FlextOracleWmsClientConfig(
        base_url="https://test.wms.oraclecloud.com/test",
        username="test_user",
        password="test_password",
        environment="development",
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        timeout=30.0,
        max_retries=3,
        verify_ssl=True,
        enable_logging=True,
    )

    # This should not raise an exception
    result = config.validate_business_rules()
    assert result.success


@pytest.mark.unit
def test_config_validation_invalid_url() -> None:
    """Test config validation with invalid URL."""
    config = FlextOracleWmsClientConfig(
        base_url="invalid-url-without-protocol",
        username="test_user",
        password="test_password",
        environment="development",
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        timeout=30.0,
        max_retries=3,
        verify_ssl=True,
        enable_logging=True,
    )

    result = config.validate_business_rules()
    assert result.is_failure
    assert "http://" in result.error or "https://" in result.error


@pytest.mark.unit
def test_config_validation_empty_username() -> None:
    """Test config validation with empty username."""
    config = FlextOracleWmsClientConfig(
        base_url="https://test.wms.oraclecloud.com/test",
        username="",
        password="test_password",
        environment="development",
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        timeout=30.0,
        max_retries=3,
        verify_ssl=True,
        enable_logging=True,
    )

    result = config.validate_business_rules()
    assert result.is_failure
    assert "username" in result.error.lower()


@pytest.mark.unit
def test_config_validation_empty_password() -> None:
    """Test config validation with empty password."""
    config = FlextOracleWmsClientConfig(
        base_url="https://test.wms.oraclecloud.com/test",
        username="test_user",
        password="",
        environment="development",
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        timeout=30.0,
        max_retries=3,
        verify_ssl=True,
        enable_logging=True,
    )

    result = config.validate_business_rules()
    assert result.is_failure
    assert "password" in result.error.lower()


@pytest.mark.unit
def test_config_validation_invalid_timeout() -> None:
    """Test config validation with invalid timeout."""
    with pytest.raises(ValidationError) as exc_info:
        FlextOracleWmsClientConfig(
            base_url="https://test.wms.oraclecloud.com/test",
            username="test_user",
            password="test_password",
            environment="development",
            api_version=FlextOracleWmsApiVersion.LGF_V10,
            timeout=-1,  # Invalid negative timeout
            max_retries=3,
            verify_ssl=True,
            enable_logging=True,
        )

    # Check that the error mentions invalid input
    assert (
        "Invalid input" in str(exc_info.value)
        or "timeout" in str(exc_info.value).lower()
    )


@pytest.mark.unit
def test_config_validation_invalid_retries() -> None:
    """Test config validation with invalid retries."""
    config = FlextOracleWmsClientConfig(
        base_url="https://test.wms.oraclecloud.com/test",
        username="test_user",
        password="test_password",
        environment="development",
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        timeout=30.0,
        max_retries=-1,  # Invalid negative retries
        verify_ssl=True,
        enable_logging=True,
    )

    result = config.validate_business_rules()
    assert result.is_failure
    assert "retries" in result.error.lower()
