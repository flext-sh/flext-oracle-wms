"""Unit tests for FlextOracleWmsSettings.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextSettings

from flext_oracle_wms.settings import FlextOracleWmsSettings


class TestFlextOracleWmsSettings:
    """Test cases for FlextOracleWmsSettings class."""

    def test_class_inheritance(self) -> None:
        """Test proper inheritance from FlextSettings."""
        assert issubclass(FlextOracleWmsSettings, FlextSettings)

    def test_default_initialization(self) -> None:
        """Test default configuration initialization."""
        config = FlextOracleWmsSettings()
        assert config.base_url == "http://localhost:8080"
        assert config.timeout == 30.0
        assert config.retry_attempts == 3
        assert config.use_mock is False
        assert config.username == ""
        assert config.password == ""

    def test_custom_initialization(self) -> None:
        """Test custom configuration initialization."""
        config = FlextOracleWmsSettings(
            base_url="https://custom-wms.example.com",
            timeout=60,
            retry_attempts=5,
        )
        assert config.base_url == "https://custom-wms.example.com"
        assert config.timeout == 60
        assert config.retry_attempts == 5

    def test_authentication_fields(self) -> None:
        """Test authentication configuration fields."""
        config = FlextOracleWmsSettings(username="test_user", password="test_pass")
        assert config.username == "test_user"
        assert config.password == "test_pass"

    def test_testing_config_factory(self) -> None:
        """Test testing_config classmethod."""
        config = FlextOracleWmsSettings.testing_config()
        assert isinstance(config, FlextOracleWmsSettings)
        assert config.use_mock is True
        assert config.base_url == "https://test-wms.example.com"

    def test_validate_config(self) -> None:
        """Test validate_config returns success for valid config."""
        config = FlextOracleWmsSettings()
        result = config.validate_config()
        assert result.is_success
