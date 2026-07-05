"""Behavioral tests for FlextOracleWmsSettings public contract.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_oracle_wms import FlextOracleWmsSettings
from tests.constants import c

__all__ = ["TestsFlextOracleWmsConfig"]


class TestsFlextOracleWmsConfig:
    """Behavior contract for FlextOracleWmsSettings."""

    @pytest.mark.unit
    def test_explicit_values_are_exposed_as_public_state(self) -> None:
        """Constructing with explicit values exposes them via public fields."""
        settings = FlextOracleWmsSettings(
            base_url="https://wms.oraclecloud.com/test",
            username="user",
            password="test_password",
            timeout=30.0,
            retry_attempts=3,
        )
        assert settings.base_url == "https://wms.oraclecloud.com/test"
        assert settings.username == "user"
        assert settings.password == "test_password"
        assert settings.timeout == pytest.approx(30.0)
        assert settings.retry_attempts == 3

    @pytest.mark.unit
    def test_defaults_define_documented_contract(self) -> None:
        """Default construction yields the documented default configuration."""
        settings = FlextOracleWmsSettings()
        assert settings.base_url == "http://localhost:8080"
        assert settings.timeout == pytest.approx(30.0)
        assert settings.retry_attempts == 3
        assert settings.username == ""
        assert settings.password == ""
        assert settings.api_version == "LGF_V10"
        assert settings.auth_method == "basic"
        assert settings.verify_ssl is True
        assert settings.enable_logging is False
        assert settings.connection_pool_size == 10
        assert settings.cache_duration == 300

    @pytest.mark.unit
    def test_validate_config_reports_success_for_valid_settings(self) -> None:
        """validate_config returns a successful result carrying True."""
        settings = FlextOracleWmsSettings(timeout=30.0, retry_attempts=3)
        result = settings.validate_config()
        assert result.success
        assert result.unwrap() is True

    @pytest.mark.unit
    def test_validate_config_is_idempotent(self) -> None:
        """Repeated validation of the same settings yields the same outcome."""
        settings = FlextOracleWmsSettings()
        first = settings.validate_config()
        second = settings.validate_config()
        assert first.success is second.success
        assert first.unwrap() == second.unwrap()

    @pytest.mark.unit
    def test_testing_factory_builds_deterministic_settings(self) -> None:
        """testing_config produces fixed, valid credentials and endpoint."""
        settings = FlextOracleWmsSettings.testing_config()
        assert settings.base_url == "https://test-wms.example.com"
        assert settings.username == "test_user"
        assert settings.password == "test_password"
        assert settings.validate_config().success

    @pytest.mark.unit
    def test_model_dump_round_trips_public_fields(self) -> None:
        """Public state survives a model_dump/model_validate round trip."""
        original = FlextOracleWmsSettings(
            base_url="https://wms.example.com",
            username="alice",
            timeout=45.0,
            retry_attempts=5,
        )
        dumped = original.model_dump()
        assert dumped["base_url"] == "https://wms.example.com"
        assert dumped["username"] == "alice"
        assert dumped["timeout"] == pytest.approx(45.0)
        assert dumped["retry_attempts"] == 5

    @pytest.mark.unit
    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("base_url", ""),
            ("timeout", 0.0),
            ("timeout", 0.5),
            ("timeout", 301.0),
            ("retry_attempts", -1),
            ("connection_pool_size", 0),
            ("cache_duration", -1),
        ],
    )
    def test_out_of_range_values_are_rejected(
        self, field: str, value: str | float
    ) -> None:
        """Field constraints reject values outside their documented range."""
        with pytest.raises(c.ValidationError):
            FlextOracleWmsSettings.model_validate({field: value})

    @pytest.mark.unit
    @pytest.mark.parametrize("timeout", [1.0, 30.0, 150.0, 300.0])
    def test_boundary_timeouts_are_accepted(self, timeout: float) -> None:
        """Timeouts on and within the inclusive bounds are accepted."""
        settings = FlextOracleWmsSettings(timeout=timeout)
        assert settings.timeout == pytest.approx(timeout)
