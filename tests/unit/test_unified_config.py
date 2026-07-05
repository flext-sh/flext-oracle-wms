"""Behavioral tests for Oracle WMS settings public contract.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

import pytest

from flext_oracle_wms import FlextOracleWmsSettings
from tests.constants import c

__all__ = ["TestsFlextOracleWmsUnifiedConfig"]


class TestsFlextOracleWmsUnifiedConfig:
    """Public-contract behavior of FlextOracleWmsSettings."""

    def test_defaults_satisfy_declared_field_contract(self) -> None:
        """Default construction yields a usable, contract-valid config."""
        settings = FlextOracleWmsSettings()

        assert settings.base_url == "http://localhost:8080"
        assert settings.timeout == pytest.approx(30.0)
        assert settings.retry_attempts == 3
        assert settings.api_version == "LGF_V10"
        assert settings.auth_method == "basic"
        assert settings.verify_ssl is True
        assert settings.enable_logging is False
        assert settings.connection_pool_size == 10
        assert settings.cache_duration == 300

    def test_custom_values_are_preserved_on_public_fields(self) -> None:
        """Explicit values round-trip through the public field API."""
        settings = FlextOracleWmsSettings(
            base_url="https://test.wms.oraclecloud.com",
            username="test_user",
            password="test_password",
            timeout=45.0,
            retry_attempts=5,
        )

        assert settings.base_url == "https://test.wms.oraclecloud.com"
        assert settings.username == "test_user"
        assert settings.password == "test_password"
        assert settings.timeout == pytest.approx(45.0)
        assert settings.retry_attempts == 5

    def test_model_dump_exposes_full_public_state(self) -> None:
        """model_dump reflects the exact public field state."""
        settings = FlextOracleWmsSettings(base_url="https://wms.example.com")
        dumped = settings.model_dump()

        assert dumped["base_url"] == "https://wms.example.com"
        assert dumped["timeout"] == pytest.approx(30.0)
        assert dumped["retry_attempts"] == 3

    @pytest.mark.parametrize("timeout", [1.0, 30.0, 150.0, 300.0])
    def test_timeout_within_bounds_is_accepted(self, timeout: float) -> None:
        """Timeouts on the inclusive [1, 300] range are accepted."""
        settings = FlextOracleWmsSettings(timeout=timeout)
        assert settings.timeout == timeout

    @pytest.mark.parametrize("timeout", [0.0, 0.5, 300.5, 1000.0])
    def test_timeout_outside_bounds_is_rejected(self, timeout: float) -> None:
        """Out-of-range timeouts raise a validation error."""
        with pytest.raises(c.ValidationError):
            FlextOracleWmsSettings(timeout=timeout)

    @pytest.mark.parametrize("retry_attempts", [0, 1, 5, 100])
    def test_non_negative_retry_attempts_are_accepted(
        self, retry_attempts: int
    ) -> None:
        """retry_attempts >= 0 are accepted."""
        settings = FlextOracleWmsSettings(retry_attempts=retry_attempts)
        assert settings.retry_attempts == retry_attempts

    @pytest.mark.parametrize("retry_attempts", [-1, -10])
    def test_negative_retry_attempts_are_rejected(self, retry_attempts: int) -> None:
        """Negative retry_attempts raise a validation error."""
        with pytest.raises(c.ValidationError):
            FlextOracleWmsSettings(retry_attempts=retry_attempts)

    def test_empty_base_url_is_rejected(self) -> None:
        """base_url must be non-empty (min_length=1)."""
        with pytest.raises(c.ValidationError):
            FlextOracleWmsSettings(base_url="")

    @pytest.mark.parametrize("pool_size", [0, -1])
    def test_non_positive_connection_pool_size_is_rejected(
        self, pool_size: int
    ) -> None:
        """connection_pool_size must be >= 1."""
        with pytest.raises(c.ValidationError):
            FlextOracleWmsSettings(connection_pool_size=pool_size)

    def test_negative_cache_duration_is_rejected(self) -> None:
        """cache_duration must be >= 0."""
        with pytest.raises(c.ValidationError):
            FlextOracleWmsSettings(cache_duration=-1)

    def test_validate_config_returns_success_result_for_valid_settings(self) -> None:
        """validate_config yields a successful result carrying True."""
        settings = FlextOracleWmsSettings(timeout=30.0, retry_attempts=3)

        result = settings.validate_config()

        assert result.success
        assert result.unwrap() is True

    def test_validate_config_result_supports_combinator_chaining(self) -> None:
        """The returned r[bool] composes via the FlextResult DSL."""
        settings = FlextOracleWmsSettings()

        mapped = settings.validate_config().map(lambda ok: "valid" if ok else "invalid")

        assert mapped.success
        assert mapped.unwrap() == "valid"

    def test_testing_config_builds_deterministic_fixture(self) -> None:
        """testing_config returns a fixed, known-good settings instance."""
        settings = FlextOracleWmsSettings.testing_config()

        assert settings.base_url == "https://test-wms.example.com"
        assert settings.username == "test_user"
        assert settings.password == "test_password"
        assert settings.timeout == pytest.approx(30.0)
        assert settings.validate_config().success

    def test_testing_config_is_idempotent(self) -> None:
        """Repeated testing_config calls yield equal public state."""
        first = FlextOracleWmsSettings.testing_config().model_dump()
        second = FlextOracleWmsSettings.testing_config().model_dump()

        assert first == second
