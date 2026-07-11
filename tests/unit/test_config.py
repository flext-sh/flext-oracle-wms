"""Behavioral tests for FlextOracleWmsSettings public contract.

ADR-005: project-scoped scalars live under the nested ``settings.OracleWms.*``
namespace; settings carry raw scalars (range/enum validation lives at the
domain boundary, not in the settings layer).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_oracle_wms import FlextOracleWmsSettings

__all__ = ["TestsFlextOracleWmsConfig"]


class TestsFlextOracleWmsConfig:
    """Behavior contract for FlextOracleWmsSettings."""

    @pytest.mark.unit
    def test_explicit_values_are_exposed_as_public_state(self) -> None:
        """Constructing with explicit values exposes them via public fields."""
        settings = FlextOracleWmsSettings.model_validate({
            "OracleWms": {
                "base_url": "https://wms.oraclecloud.com/test",
                "username": "user",
                "password": "test_password",
                "timeout": 30.0,
                "retry_attempts": 3,
            },
        })
        ns = settings.OracleWms
        assert ns.base_url == "https://wms.oraclecloud.com/test"
        assert ns.username == "user"
        assert ns.password == "test_password"
        assert ns.timeout == pytest.approx(30.0)
        assert ns.retry_attempts == 3

    @pytest.mark.unit
    def test_defaults_define_documented_contract(self) -> None:
        """Default construction yields the documented default configuration."""
        settings = FlextOracleWmsSettings.model_validate({})
        ns = settings.OracleWms
        assert ns.base_url == "http://localhost:8080"
        assert ns.timeout == pytest.approx(30.0)
        assert ns.retry_attempts == 3
        assert ns.username == ""
        assert ns.password == ""
        assert ns.api_version == "LGF_V10"
        assert ns.auth_method == "basic"
        assert ns.verify_ssl is True
        assert ns.enable_logging is False
        assert ns.connection_pool_size == 10
        assert ns.cache_duration == 300

    @pytest.mark.unit
    def test_settings_accept_unvalidated_scalars(self) -> None:
        """Settings carry raw scalars; range checks live at the domain boundary."""
        settings = FlextOracleWmsSettings.model_validate({
            "OracleWms": {"timeout": -1, "retry_attempts": -5},
        })

        assert settings.OracleWms.timeout == -1
        assert settings.OracleWms.retry_attempts == -5

    @pytest.mark.unit
    def test_model_validate_round_trips_public_fields(self) -> None:
        """Public state survives a model_dump/model_validate round trip."""
        original = FlextOracleWmsSettings.model_validate({
            "OracleWms": {
                "base_url": "https://wms.example.com",
                "username": "alice",
                "timeout": 45.0,
                "retry_attempts": 5,
            },
        })
        dumped = original.model_dump()
        assert dumped["OracleWms"]["base_url"] == "https://wms.example.com"
        assert dumped["OracleWms"]["username"] == "alice"
        assert dumped["OracleWms"]["timeout"] == pytest.approx(45.0)
        assert dumped["OracleWms"]["retry_attempts"] == 5

    @pytest.mark.unit
    def test_settings_ignore_unknown_keys(self) -> None:
        """Unknown keys are ignored per the extra=ignore contract."""
        settings = FlextOracleWmsSettings.model_validate({
            "not_a_real_setting": "value",
        })

        assert "not_a_real_setting" not in settings.model_dump()
        assert settings.OracleWms.base_url == "http://localhost:8080"

    @pytest.mark.unit
    def test_default_construction_is_deterministic(self) -> None:
        """Default construction yields stable, equal settings."""
        first = FlextOracleWmsSettings.model_validate({})
        second = FlextOracleWmsSettings.model_validate({})

        assert first.OracleWms.base_url == "http://localhost:8080"
        assert first.model_dump() == second.model_dump()
