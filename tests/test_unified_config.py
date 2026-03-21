"""Tests for Oracle WMS settings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from flext_oracle_wms import FlextOracleWmsSettings


class TestFlextOracleWmsSettings:
    """Test Oracle WMS settings configuration."""

    def test_config_creation_defaults(self) -> None:
        """Test config creation with defaults."""
        config = FlextOracleWmsSettings()
        assert config.base_url == "http://localhost:8080"
        assert config.username == ""
        assert config.password == ""
        assert config.use_mock is False

    def test_config_creation_custom(self) -> None:
        """Test config creation with custom values."""
        config = FlextOracleWmsSettings(
            base_url="https://test.wms.oraclecloud.com",
            username="test_user",
            password="test_password",
            timeout=30,
            retry_attempts=5,
        )
        assert config.base_url == "https://test.wms.oraclecloud.com"
        assert config.username == "test_user"
        assert config.password == "test_password"
        assert config.timeout == 30
        assert config.retry_attempts == 5

    def test_config_timeout_bounds(self) -> None:
        """Test timeout validation bounds."""
        with pytest.raises(ValidationError):
            FlextOracleWmsSettings(timeout=0)
        with pytest.raises(ValidationError):
            FlextOracleWmsSettings(timeout=301)

    def test_config_retry_bounds(self) -> None:
        """Test retry_attempts validation bounds."""
        with pytest.raises(ValidationError):
            FlextOracleWmsSettings(retry_attempts=-1)

    def test_validate_config_success(self) -> None:
        """Test validate_config returns success for valid config."""
        config = FlextOracleWmsSettings(timeout=30, retry_attempts=3)
        result = config.validate_config()
        assert result.is_success

    def test_testing_config_factory(self) -> None:
        """Test testing_config factory method."""
        config = FlextOracleWmsSettings.testing_config()
        assert config.use_mock is True
        assert config.base_url == "https://test-wms.example.com"
