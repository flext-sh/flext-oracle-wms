"""Oracle WMS Configuration Module tests.

ADR-005: project-scoped scalars live under the nested ``settings.OracleWms.*``
namespace; settings carry raw scalars (range/enum validation lives at the
domain boundary, not in the settings layer).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_oracle_wms import FlextOracleWmsSettings

__all__ = ["TestsFlextOracleWmsConfigModule"]


class TestsFlextOracleWmsConfigModule:
    """Behavior contract for FlextOracleWmsSettings public API."""

    @pytest.fixture
    def _isolated_singleton(self) -> None:
        """Guarantee each test starts from a fresh settings singleton."""
        FlextOracleWmsSettings.reset_for_testing()

    def test_defaults_expose_documented_values(self) -> None:
        """A default instance exposes the documented default field values."""
        settings = FlextOracleWmsSettings.model_validate({})
        ns = settings.OracleWms

        assert ns.base_url == "http://localhost:8080"
        assert ns.timeout == pytest.approx(30.0)
        assert ns.username == ""
        assert ns.password == ""
        assert ns.retry_attempts == 3
        assert ns.api_version == "LGF_V10"
        assert ns.auth_method == "basic"
        assert ns.verify_ssl is True
        assert ns.enable_logging is False
        assert ns.connection_pool_size == 10
        assert ns.cache_duration == 300

    def test_custom_values_are_retained(self) -> None:
        """Explicit field values are preserved on the constructed instance."""
        settings = FlextOracleWmsSettings.model_validate({
            "OracleWms": {
                "base_url": "https://example.com",
                "username": "test_user",
                "password": "test_password",
            },
        })

        assert settings.OracleWms.base_url == "https://example.com"
        assert settings.OracleWms.username == "test_user"
        assert settings.OracleWms.password == "test_password"

    def test_model_dump_round_trips_public_state(self) -> None:
        """model_dump() reflects the constructed public field state."""
        settings = FlextOracleWmsSettings.model_validate({
            "OracleWms": {"base_url": "https://wms.example.com"},
        })
        dumped = settings.model_dump()

        assert dumped["OracleWms"]["base_url"] == "https://wms.example.com"
        rebuilt = FlextOracleWmsSettings.model_validate(dumped)
        assert rebuilt.OracleWms.base_url == settings.OracleWms.base_url
        assert rebuilt.OracleWms.timeout == settings.OracleWms.timeout

    def test_out_of_range_scalars_are_carried_raw(self) -> None:
        """Out-of-range scalars are stored as-is (ADR-005: no range checks here)."""
        settings = FlextOracleWmsSettings.model_validate({
            "OracleWms": {
                "base_url": "",
                "timeout": 0.5,
                "retry_attempts": -1,
                "connection_pool_size": 0,
                "cache_duration": -1,
            },
        })
        ns = settings.OracleWms

        assert ns.base_url == ""
        assert ns.timeout == pytest.approx(0.5)
        assert ns.retry_attempts == -1
        assert ns.connection_pool_size == 0
        assert ns.cache_duration == -1

    def test_singleton_returns_same_instance(self) -> None:
        """Repeated fetch_global calls return the same singleton instance."""
        first = FlextOracleWmsSettings.fetch_global()
        second = FlextOracleWmsSettings.fetch_global()

        assert first is second

    def test_reset_for_testing_creates_fresh_instance(self) -> None:
        """reset_for_testing() breaks the singleton so a new instance is built."""
        first = FlextOracleWmsSettings.fetch_global()
        FlextOracleWmsSettings.reset_for_testing()
        second = FlextOracleWmsSettings.fetch_global()

        assert first is not second

    def test_clone_overrides_isolated_copy_without_mutating_singleton(self) -> None:
        """clone() returns an isolated re-validated copy; the singleton is intact."""
        base = FlextOracleWmsSettings.fetch_global()
        cloned = base.clone(OracleWms={"base_url": "https://clone.example.com"})

        assert cloned is not base
        assert cloned.OracleWms.base_url == "https://clone.example.com"
        assert base.OracleWms.base_url == "http://localhost:8080"
