"""Behavioral tests for Oracle WMS settings public contract.

ADR-005: project-scoped scalars live under the nested ``settings.OracleWms.*``
namespace; settings carry raw scalars (range/enum validation lives at the
domain boundary, not in the settings layer).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_oracle_wms import FlextOracleWmsSettings

__all__ = ["TestsFlextOracleWmsUnifiedConfig"]


class TestsFlextOracleWmsUnifiedConfig:
    """Public-contract behavior of FlextOracleWmsSettings."""

    def test_defaults_satisfy_declared_field_contract(self) -> None:
        """Default construction yields a usable, contract-valid config."""
        settings = FlextOracleWmsSettings.model_validate({})
        ns = settings.OracleWms

        tm.that(ns.base_url, eq="http://localhost:8080")
        tm.that(ns.timeout, eq=pytest.approx(30.0))
        tm.that(ns.retry_attempts, eq=3)
        tm.that(ns.api_version, eq="LGF_V10")
        tm.that(ns.auth_method, eq="basic")
        tm.that(ns.verify_ssl, eq=True)
        tm.that(ns.enable_logging, eq=False)
        tm.that(ns.connection_pool_size, eq=10)
        tm.that(ns.cache_duration, eq=300)

    def test_custom_values_are_preserved_on_public_fields(self) -> None:
        """Explicit values round-trip through the public field API."""
        settings = FlextOracleWmsSettings.model_validate({
            "OracleWms": {
                "base_url": "https://test.wms.oraclecloud.com",
                "username": "test_user",
                "password": "test_password",
                "timeout": 45.0,
                "retry_attempts": 5,
            }
        })
        ns = settings.OracleWms

        tm.that(ns.base_url, eq="https://test.wms.oraclecloud.com")
        tm.that(ns.username, eq="test_user")
        tm.that(ns.password, eq="test_password")
        tm.that(ns.timeout, eq=pytest.approx(45.0))
        tm.that(ns.retry_attempts, eq=5)

    def test_model_dump_exposes_full_public_state(self) -> None:
        """model_dump reflects the exact public field state."""
        settings = FlextOracleWmsSettings.model_validate({
            "OracleWms": {"base_url": "https://wms.example.com"}
        })
        dumped = settings.model_dump()

        tm.that(dumped["OracleWms"]["base_url"], eq="https://wms.example.com")
        tm.that(dumped["OracleWms"]["timeout"], eq=pytest.approx(30.0))
        tm.that(dumped["OracleWms"]["retry_attempts"], eq=3)

    @pytest.mark.parametrize("timeout", [1.0, 30.0, 150.0, 300.0])
    def test_timeout_scalars_are_carried_raw(self, timeout: float) -> None:
        """Timeout scalars are stored verbatim (no range checks at this layer)."""
        settings = FlextOracleWmsSettings.model_validate({
            "OracleWms": {"timeout": timeout}
        })
        tm.that(settings.OracleWms.timeout, eq=timeout)

    @pytest.mark.parametrize("timeout", [0.0, 0.5, 300.5, 1000.0])
    def test_out_of_range_timeouts_are_accepted_raw(self, timeout: float) -> None:
        """Out-of-range timeouts are accepted (ADR-005: raw scalars in settings)."""
        settings = FlextOracleWmsSettings.model_validate({
            "OracleWms": {"timeout": timeout}
        })
        tm.that(settings.OracleWms.timeout, eq=timeout)

    @pytest.mark.parametrize("retry_attempts", [0, 1, 5, 100])
    def test_non_negative_retry_attempts_are_accepted(
        self, retry_attempts: int
    ) -> None:
        """retry_attempts >= 0 are accepted."""
        settings = FlextOracleWmsSettings.model_validate({
            "OracleWms": {"retry_attempts": retry_attempts}
        })
        tm.that(settings.OracleWms.retry_attempts, eq=retry_attempts)

    @pytest.mark.parametrize("retry_attempts", [-1, -10])
    def test_negative_retry_attempts_are_carried_raw(self, retry_attempts: int) -> None:
        """Negative retry_attempts are stored raw (no range checks at this layer)."""
        settings = FlextOracleWmsSettings.model_validate({
            "OracleWms": {"retry_attempts": retry_attempts}
        })
        tm.that(settings.OracleWms.retry_attempts, eq=retry_attempts)

    def test_empty_base_url_is_carried_raw(self) -> None:
        """An empty base_url is stored raw (no min_length at the settings layer)."""
        settings = FlextOracleWmsSettings.model_validate({
            "OracleWms": {"base_url": ""}
        })
        tm.that(settings.OracleWms.base_url, eq="")

    @pytest.mark.parametrize("pool_size", [0, -1])
    def test_non_positive_connection_pool_size_is_carried_raw(
        self, pool_size: int
    ) -> None:
        """connection_pool_size scalars are stored raw."""
        settings = FlextOracleWmsSettings.model_validate({
            "OracleWms": {"connection_pool_size": pool_size}
        })
        tm.that(settings.OracleWms.connection_pool_size, eq=pool_size)

    def test_negative_cache_duration_is_carried_raw(self) -> None:
        """cache_duration scalars are stored raw."""
        settings = FlextOracleWmsSettings.model_validate({
            "OracleWms": {"cache_duration": -1}
        })
        tm.that(settings.OracleWms.cache_duration, eq=-1)

    def test_model_validate_is_idempotent(self) -> None:
        """Repeated default constructions yield equal public state."""
        first = FlextOracleWmsSettings.model_validate({}).model_dump()
        second = FlextOracleWmsSettings.model_validate({}).model_dump()

        tm.that(first, eq=second)
