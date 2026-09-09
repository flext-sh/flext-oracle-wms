"""Behavioral tests for FlextOracleWmsSettings public contract.

ADR-005: project-scoped scalars live under the nested ``settings.OracleWms.*``
namespace; settings carry raw scalars (range/enum validation lives at the
domain boundary, not in the settings layer).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_tests import tm

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
            }
        })
        ns = settings.OracleWms
        tm.that(ns.base_url, eq="https://wms.oraclecloud.com/test")
        tm.that(ns.username, eq="user")
        tm.that(ns.password, eq="test_password")
        tm.that(ns.timeout, eq=pytest.approx(30.0))
        tm.that(ns.retry_attempts, eq=3)

    @pytest.mark.unit
    def test_defaults_define_documented_contract(self) -> None:
        """Default construction yields the documented default configuration."""
        settings = FlextOracleWmsSettings.model_validate({})
        ns = settings.OracleWms
        tm.that(ns.base_url, eq="http://localhost:8080")
        tm.that(ns.timeout, eq=pytest.approx(30.0))
        tm.that(ns.retry_attempts, eq=3)
        tm.that(ns.username, eq="")
        tm.that(ns.password, eq="")
        tm.that(ns.api_version, eq="LGF_V10")
        tm.that(ns.auth_method, eq="basic")
        tm.that(ns.verify_ssl, eq=True)
        tm.that(ns.enable_logging, eq=False)
        tm.that(ns.connection_pool_size, eq=10)
        tm.that(ns.cache_duration, eq=300)

    @pytest.mark.unit
    def test_settings_accept_unvalidated_scalars(self) -> None:
        """Settings carry raw scalars; range checks live at the domain boundary."""
        settings = FlextOracleWmsSettings.model_validate({
            "OracleWms": {"timeout": -1, "retry_attempts": -5}
        })

        tm.that(settings.OracleWms.timeout, eq=-1)
        tm.that(settings.OracleWms.retry_attempts, eq=-5)

    @pytest.mark.unit
    def test_model_validate_round_trips_public_fields(self) -> None:
        """Public state survives a model_dump/model_validate round trip."""
        original = FlextOracleWmsSettings.model_validate({
            "OracleWms": {
                "base_url": "https://wms.example.com",
                "username": "alice",
                "timeout": 45.0,
                "retry_attempts": 5,
            }
        })
        dumped = original.model_dump()
        tm.that(dumped["OracleWms"]["base_url"], eq="https://wms.example.com")
        tm.that(dumped["OracleWms"]["username"], eq="alice")
        tm.that(dumped["OracleWms"]["timeout"], eq=pytest.approx(45.0))
        tm.that(dumped["OracleWms"]["retry_attempts"], eq=5)

    @pytest.mark.unit
    def test_settings_ignore_unknown_keys(self) -> None:
        """Unknown keys are ignored per the extra=ignore contract."""
        settings = FlextOracleWmsSettings.model_validate({
            "not_a_real_setting": "value"
        })

        tm.that(settings.model_dump(), lacks="not_a_real_setting")
        tm.that(settings.OracleWms.base_url, eq="http://localhost:8080")

    @pytest.mark.unit
    def test_default_construction_is_deterministic(self) -> None:
        """Default construction yields stable, equal settings."""
        first = FlextOracleWmsSettings.model_validate({})
        second = FlextOracleWmsSettings.model_validate({})

        tm.that(first.OracleWms.base_url, eq="http://localhost:8080")
        tm.that(first.model_dump(), eq=second.model_dump())
