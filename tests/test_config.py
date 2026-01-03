"""Unit tests for FlextOracleWmsClientSettings - BASED ON WORKING CODE.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

import pytest
from pydantic import ValidationError

from flext_oracle_wms import FlextOracleWmsApiVersion, FlextOracleWmsClientSettings


@pytest.mark.unit
def test_config_creation_valid() -> None:
    """Test config creation with valid parameters - EXACTLY like working example."""
    config = FlextOracleWmsClientSettings(
        oracle_wms_base_url="https://invalid.wms.ocs.oraclecloud.com/company_unknow",
        oracle_wms_username="USER_WMS_INTEGRA",
        oracle_wms_password="test_password",
        environment="development",
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        oracle_wms_timeout=30,
        oracle_wms_max_retries=3,
        oracle_wms_verify_ssl=True,
        oracle_wms_enable_logging=True,
    )

    assert (
        config.oracle_wms_base_url
        == "https://invalid.wms.ocs.oraclecloud.com/company_unknow"
    )
    assert config.oracle_wms_username == "USER_WMS_INTEGRA"
    assert config.oracle_wms_password == "test_password"
    assert config.api_version == FlextOracleWmsApiVersion.LGF_V10
    assert config.oracle_wms_timeout == 30.0
    assert config.oracle_wms_max_retries == 3
    assert config.oracle_wms_verify_ssl is True
    assert config.oracle_wms_enable_logging is True


@pytest.mark.unit
def test_config_validation_success() -> None:
    """Test config domain validation - BASED ON WORKING PATTERN."""
    config = FlextOracleWmsClientSettings(
        oracle_wms_base_url="https://test.wms.oraclecloud.com/test",
        oracle_wms_username="test_user",
        oracle_wms_password="test_password",
        environment="development",
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        oracle_wms_timeout=30,
        oracle_wms_max_retries=3,
        oracle_wms_verify_ssl=True,
        oracle_wms_enable_logging=True,
    )

    # This should not raise an exception
    result = config.validate_business_rules()
    assert result.is_success


@pytest.mark.unit
def test_config_validation_invalid_url() -> None:
    """Test config validation with invalid URL."""
    # The constructor should raise a validation error for invalid URL
    with pytest.raises(ValidationError) as exc_info:
        FlextOracleWmsClientSettings(
            oracle_wms_base_url="invalid-url-without-protocol",
            oracle_wms_username="test_user",
            oracle_wms_password="test_password",
            api_version=FlextOracleWmsApiVersion.LGF_V10,
            oracle_wms_timeout=30,
            oracle_wms_max_retries=3,
            oracle_wms_verify_ssl=True,
            oracle_wms_enable_logging=True,
        )

    assert "Oracle WMS base URL must start with http:// or https://" in str(
        exc_info.value,
    )


@pytest.mark.unit
def test_config_validation_empty_username() -> None:
    """Test config validation with empty username."""
    config = FlextOracleWmsClientSettings(
        oracle_wms_base_url="https://test.wms.oraclecloud.com/test",
        oracle_wms_username="",
        oracle_wms_password="test_password",
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        oracle_wms_timeout=30,
        oracle_wms_max_retries=3,
        oracle_wms_verify_ssl=True,
        oracle_wms_enable_logging=True,
    )

    result = config.validate_business_rules()
    assert result.is_failure
    assert result.error is not None
    assert result.error is not None and "username" in result.error.lower()


@pytest.mark.unit
def test_config_validation_empty_password() -> None:
    """Test config validation with empty password."""
    config = FlextOracleWmsClientSettings(
        oracle_wms_base_url="https://test.wms.oraclecloud.com/test",
        oracle_wms_username="test_user",
        oracle_wms_password="",
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        oracle_wms_timeout=30,
        oracle_wms_max_retries=3,
        oracle_wms_verify_ssl=True,
        oracle_wms_enable_logging=True,
    )

    result = config.validate_business_rules()
    assert result.is_failure
    assert result.error is not None
    assert result.error is not None and "password" in result.error.lower()


@pytest.mark.unit
def test_config_validation_invalid_timeout() -> None:
    """Test config validation with invalid timeout."""
    with pytest.raises(ValidationError) as exc_info:
        FlextOracleWmsClientSettings(
            oracle_wms_base_url="https://test.wms.oraclecloud.com/test",
            oracle_wms_username="test_user",
            oracle_wms_password="test_password",
            environment="development",
            api_version=FlextOracleWmsApiVersion.LGF_V10,
            oracle_wms_timeout=-1,  # Invalid negative timeout
            oracle_wms_max_retries=3,
            oracle_wms_verify_ssl=True,
            oracle_wms_enable_logging=True,
        )

    # Check that the error mentions invalid input
    assert (
        "Invalid input" in str(exc_info.value)
        or "timeout" in str(exc_info.value).lower()
    )


@pytest.mark.unit
def test_config_validation_invalid_retries() -> None:
    """Test config validation with invalid retries."""
    with pytest.raises(ValidationError) as exc_info:
        FlextOracleWmsClientSettings(
            oracle_wms_base_url="https://test.wms.oraclecloud.com/test",
            oracle_wms_username="test_user",
            oracle_wms_password="test_password",
            api_version=FlextOracleWmsApiVersion.LGF_V10,
            oracle_wms_timeout=30,
            oracle_wms_max_retries=-1,  # Invalid negative retries
            oracle_wms_verify_ssl=True,
            oracle_wms_enable_logging=True,
        )

    assert "Oracle WMS max retries cannot be negative" in str(exc_info.value)
