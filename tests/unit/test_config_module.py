"""Oracle WMS Configuration Module tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_oracle_wms import FlextOracleWmsSettings


def test_config_creation() -> None:
    """Test basic configuration creation."""
    settings = FlextOracleWmsSettings()
    assert isinstance(settings, FlextOracleWmsSettings)
    assert settings.base_url is not None


def test_config_singleton_behavior() -> None:
    """Test singleton pattern: same class returns same instance."""
    config1 = FlextOracleWmsSettings()
    config2 = FlextOracleWmsSettings()
    assert config1 is config2


def test_config_custom_values() -> None:
    """Test configuration with custom values."""
    settings = FlextOracleWmsSettings(
        base_url="https://example.com",
        username="test_user",
        password="test_password",
    )
    assert settings.base_url == "https://example.com"
    assert settings.username == "test_user"
    assert settings.password == "test_password"


def test_config_validation() -> None:
    """Test validate_config returns success for valid settings."""
    settings = FlextOracleWmsSettings(timeout=30, retry_attempts=3)
    result = settings.validate_config()
    assert result.success


def test_config_testing_factory() -> None:
    """Test testing_config factory method."""
    settings = FlextOracleWmsSettings.testing_config()
    assert isinstance(settings, FlextOracleWmsSettings)
    assert settings.base_url == "https://test-wms.example.com"
    assert settings.username == "test_user"


def test_config_reset_functionality() -> None:
    """Test singleton reset creates fresh instance."""
    config1 = FlextOracleWmsSettings()
    FlextOracleWmsSettings._reset_instance()
    config2 = FlextOracleWmsSettings()
    assert config1 is not config2
