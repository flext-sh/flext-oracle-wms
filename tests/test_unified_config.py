"""Tests for unified Oracle WMS configuration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

import pytest
from pydantic import ValidationError

from flext_oracle_wms import (
    FlextOracleWmsApiVersion,
    FlextOracleWmsConfig,
    OracleWMSAuthMethod,
)


class TestFlextOracleWmsConfig:
    """Test unified Oracle WMS configuration."""

    def test_config_creation_valid(self) -> None:
        """Test config creation with valid parameters."""
        config = FlextOracleWmsConfig(
            oracle_wms_base_url="https://test.wms.oraclecloud.com/test",
            oracle_wms_username="test_user",
            oracle_wms_password="test_password",
            api_version=FlextOracleWmsApiVersion.LGF_V10,
            auth_method=OracleWMSAuthMethod.BASIC,
            oracle_wms_timeout=30,
            oracle_wms_max_retries=3,
            oracle_wms_verify_ssl=True,
            oracle_wms_enable_logging=True,
        )

        assert config.oracle_wms_base_url == "https://test.wms.oraclecloud.com/test"
        assert config.oracle_wms_username == "test_user"
        assert config.oracle_wms_password == "test_password"
        assert config.api_version == FlextOracleWmsApiVersion.LGF_V10
        assert config.auth_method == OracleWMSAuthMethod.BASIC
        assert config.oracle_wms_timeout == 30
        assert config.oracle_wms_max_retries == 3
        assert config.oracle_wms_verify_ssl is True
        assert config.oracle_wms_enable_logging is True

    def test_config_validation_invalid_url(self) -> None:
        """Test config validation with invalid URL."""
        with pytest.raises(ValidationError) as exc_info:
            FlextOracleWmsConfig(
                oracle_wms_base_url="invalid-url-without-protocol",
                oracle_wms_username="test_user",
                oracle_wms_password="test_password",
            )

        assert "Oracle WMS base URL must start with http:// or https://" in str(
            exc_info.value,
        )

    def test_config_validation_invalid_timeout(self) -> None:
        """Test config validation with invalid timeout."""
        with pytest.raises(ValidationError) as exc_info:
            FlextOracleWmsConfig(
                oracle_wms_base_url="https://test.wms.oraclecloud.com/test",
                oracle_wms_username="test_user",
                oracle_wms_password="test_password",
                oracle_wms_timeout=-1,
            )

        assert "Oracle WMS timeout must be greater than 0" in str(exc_info.value)

    def test_config_validation_invalid_retries(self) -> None:
        """Test config validation with invalid retries."""
        with pytest.raises(ValidationError) as exc_info:
            FlextOracleWmsConfig(
                oracle_wms_base_url="https://test.wms.oraclecloud.com/test",
                oracle_wms_username="test_user",
                oracle_wms_password="test_password",
                oracle_wms_max_retries=-1,
            )

        assert "Oracle WMS max retries cannot be negative" in str(exc_info.value)

    def test_business_rules_validation_success(self) -> None:
        """Test business rules validation success."""
        config = FlextOracleWmsConfig(
            oracle_wms_base_url="https://test.wms.oraclecloud.com/test",
            oracle_wms_username="test_user",
            oracle_wms_password="test_password",
        )

        result = config.validate_business_rules()
        assert result.success

    def test_business_rules_validation_failure(self) -> None:
        """Test business rules validation failure."""
        config = FlextOracleWmsConfig(
            oracle_wms_base_url="https://test.wms.oraclecloud.com/test",
            oracle_wms_username="",  # Empty username should fail
            oracle_wms_password="test_password",
            auth_method=OracleWMSAuthMethod.BASIC,
        )

        result = config.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert (
            "Oracle WMS username and password required for basic auth" in result.error
        )

    def test_get_auth_headers_basic(self) -> None:
        """Test getting basic auth headers."""
        config = FlextOracleWmsConfig(
            oracle_wms_base_url="https://test.wms.oraclecloud.com/test",
            oracle_wms_username="test_user",
            oracle_wms_password="test_password",
            auth_method=OracleWMSAuthMethod.BASIC,
        )

        headers = config.get_auth_headers()
        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Basic ")

    def test_build_endpoint_url(self) -> None:
        """Test building endpoint URL."""
        config = FlextOracleWmsConfig(
            oracle_wms_base_url="https://test.wms.oraclecloud.com/test",
            oracle_wms_username="test_user",
            oracle_wms_password="test_password",
        )

        url = config.build_endpoint_url("api/entities")
        assert url == "https://test.wms.oraclecloud.com/test/api/entities"

    def test_build_endpoint_url_with_trailing_slash(self) -> None:
        """Test building endpoint URL with trailing slash in base URL."""
        config = FlextOracleWmsConfig(
            oracle_wms_base_url="https://test.wms.oraclecloud.com/test/",
            oracle_wms_username="test_user",
            oracle_wms_password="test_password",
        )

        url = config.build_endpoint_url("api/entities")
        assert url == "https://test.wms.oraclecloud.com/test/api/entities"
