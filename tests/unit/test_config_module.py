"""Oracle WMS Configuration Module tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Callable

import pytest
from pydantic import ValidationError

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
        settings = FlextOracleWmsSettings()

        assert settings.base_url == "http://localhost:8080"
        assert settings.timeout == pytest.approx(30.0)
        assert settings.username == ""
        assert settings.password == ""
        assert settings.retry_attempts == 3
        assert settings.api_version == "LGF_V10"
        assert settings.auth_method == "basic"
        assert settings.verify_ssl is True
        assert settings.enable_logging is False
        assert settings.connection_pool_size == 10
        assert settings.cache_duration == 300

    def test_custom_values_are_retained(self) -> None:
        """Explicit field values are preserved on the constructed instance."""
        settings = FlextOracleWmsSettings(
            base_url="https://example.com",
            username="test_user",
            password="test_password",
        )

        assert settings.base_url == "https://example.com"
        assert settings.username == "test_user"
        assert settings.password == "test_password"

    def test_model_dump_round_trips_public_state(self) -> None:
        """model_dump() reflects the constructed public field state."""
        settings = FlextOracleWmsSettings(base_url="https://wms.example.com")
        dumped = settings.model_dump()

        assert dumped["base_url"] == "https://wms.example.com"
        rebuilt = FlextOracleWmsSettings.model_validate(dumped)
        assert rebuilt.base_url == settings.base_url
        assert rebuilt.timeout == settings.timeout

    @pytest.mark.parametrize(
        ("label", "build"),
        [
            ("empty_base_url", lambda: FlextOracleWmsSettings(base_url="")),
            ("timeout_below_min", lambda: FlextOracleWmsSettings(timeout=0.5)),
            ("timeout_above_max", lambda: FlextOracleWmsSettings(timeout=301.0)),
            ("negative_retries", lambda: FlextOracleWmsSettings(retry_attempts=-1)),
            ("zero_pool_size", lambda: FlextOracleWmsSettings(connection_pool_size=0)),
            ("negative_cache", lambda: FlextOracleWmsSettings(cache_duration=-1)),
        ],
    )
    def test_field_constraints_reject_invalid_values(
        self, label: str, build: Callable[[], FlextOracleWmsSettings]
    ) -> None:
        """Out-of-range field values raise a pydantic ValidationError."""
        assert label
        with pytest.raises(ValidationError):
            build()

    def test_validate_config_succeeds_for_valid_settings(self) -> None:
        """validate_config() returns a successful result carrying True."""
        settings = FlextOracleWmsSettings(timeout=30.0, retry_attempts=3)
        result = settings.validate_config()

        assert result.success
        assert result.value is True
        assert result.unwrap() is True

    def test_validate_config_result_supports_map_combinator(self) -> None:
        """The success result chains through map without losing its value."""
        settings = FlextOracleWmsSettings()
        mapped = settings.validate_config().map(lambda ok: "ok" if ok else "no")

        assert mapped.success
        assert mapped.value == "ok"

    def test_testing_factory_builds_deterministic_settings(self) -> None:
        """testing_config() yields the documented deterministic fixture."""
        settings = FlextOracleWmsSettings.testing_config()

        assert isinstance(settings, FlextOracleWmsSettings)
        assert settings.base_url == "https://test-wms.example.com"
        assert settings.username == "test_user"
        assert settings.password == "test_password"
        assert settings.timeout == pytest.approx(30.0)

    def test_singleton_returns_same_instance(self) -> None:
        """Repeated construction returns the same singleton instance."""
        first = FlextOracleWmsSettings()
        second = FlextOracleWmsSettings()

        assert first is second

    def test_reset_for_testing_creates_fresh_instance(self) -> None:
        """reset_for_testing() breaks the singleton so a new instance is built."""
        first = FlextOracleWmsSettings()
        FlextOracleWmsSettings.reset_for_testing()
        second = FlextOracleWmsSettings()

        assert first is not second
