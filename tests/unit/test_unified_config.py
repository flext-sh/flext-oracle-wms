"""Tests for Oracle WMS settings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

import pytest

from flext_oracle_wms import FlextOracleWmsSettings
from tests import c


class TestFlextOracleWmsSettings:
    """Test Oracle WMS settings configuration."""

    def test_config_creation_defaults(self) -> None:
        """Test settings creation with defaults."""
        settings = FlextOracleWmsSettings()
        assert isinstance(settings.base_url, str)
        assert settings.base_url
        assert settings.timeout >= 1
        assert settings.timeout <= 300

    def test_config_creation_custom(self) -> None:
        """Test settings creation with custom values."""
        settings = FlextOracleWmsSettings(
            base_url="https://test.wms.oraclecloud.com",
            username="test_user",
            password="test_password",
            timeout=30,
            retry_attempts=5,
        )
        assert settings.base_url == "https://test.wms.oraclecloud.com"
        assert settings.username == "test_user"
        assert settings.password == "test_password"
        assert settings.timeout == 30
        assert settings.retry_attempts == 5

    def test_config_timeout_bounds(self) -> None:
        """Test timeout validation bounds."""
        with pytest.raises(c.ValidationError):
            FlextOracleWmsSettings(timeout=0)
        with pytest.raises(c.ValidationError):
            FlextOracleWmsSettings(timeout=301)

    def test_config_retry_bounds(self) -> None:
        """Test retry_attempts validation bounds."""
        with pytest.raises(c.ValidationError):
            FlextOracleWmsSettings(retry_attempts=-1)

    def test_validate_config_success(self) -> None:
        """Test validate_config returns success for valid settings."""
        settings = FlextOracleWmsSettings(timeout=30, retry_attempts=3)
        result = settings.validate_config()
        assert result.success

    def test_testing_config_factory(self) -> None:
        """Test testing_config factory method."""
        settings = FlextOracleWmsSettings.testing_config()
        assert settings.base_url == "https://test-wms.example.com"
        assert settings.username == "test_user"
