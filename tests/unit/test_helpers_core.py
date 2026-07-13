"""Behavioral unit tests for Oracle WMS test utilities.

Exercises the observable public contract of ``TestsFlextOracleWmsUtilities``
(the ``u`` facade): environment/config loading, client-settings construction,
canonical sample data, and the concrete API facade — all through the public
API only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from flext_tests import tm

from flext_core import u as core_u
from tests import u

if TYPE_CHECKING:
    from pathlib import Path

__all__ = ["TestsFlextOracleWmsHelpersCore"]

_TESTS = u.OracleWms.Tests


@pytest.mark.unit
class TestsFlextOracleWmsHelpersCore:
    """Contract tests for the Oracle WMS test-utilities facade."""

    def test_utilities_facade_specializes_flext_core_utilities(self) -> None:
        # Consumers rely on core converter helpers being available on ``u``.
        assert issubclass(u, core_u)

    @pytest.mark.parametrize(
        ("raw", "expected"),
        [(123, "123"), ("abc", "abc"), (True, "True")],
    )
    def test_to_str_coerces_values_to_string(
        self,
        raw: str | int | bool,
        expected: str,
    ) -> None:
        tm.that(u.to_str(raw, default=""), eq=expected)

    @pytest.mark.parametrize(
        ("raw", "expected"),
        [("5", 5), (7, 7), ("not-a-number", 0)],
    )
    def test_to_int_coerces_or_falls_back_to_default(
        self,
        raw: str | int,
        expected: int,
    ) -> None:
        tm.that(u.to_int(raw, default=0), eq=expected)

    @pytest.mark.parametrize(
        ("raw", "expected"),
        [("true", True), (True, True), (False, False)],
    )
    def test_to_bool_coerces_values(
        self,
        raw: str | bool,
        *,
        expected: bool,
    ) -> None:
        assert u.to_bool(raw, default=False) is expected

    def test_sample_entities_returns_canonical_entity_list(self) -> None:
        tm.that(
            _TESTS.sample_entities(),
            eq=[
                "action_code",
                "company",
                "facility",
                "item",
                "order_hdr",
                "order_dtl",
            ],
        )

    def test_sample_entity_data_exposes_paged_result_envelope(self) -> None:
        data = _TESTS.sample_entity_data()

        tm.that(data, none=False)
        tm.that(data["result_count"], eq=4)
        tm.that(data["page_count"], eq=1)
        tm.that(data["next_page"], none=True)

        results = data["results"]
        tm.that(results, is_=list)
        tm.that(len(results), eq=2)
        first = results[0]
        tm.that(first, is_=dict)
        tm.that(first["code"], eq="TEST_CODE")

    def test_build_client_settings_maps_env_config_to_settings_fields(self) -> None:
        settings = _TESTS.build_client_settings(
            {
                "base_url": "https://wms.example/prod",
                "username": "svc_user",
                "password": "secret",
                "auth_method": "BASIC",
                "timeout": "45",
                "retry_attempts": "2",
                "verify_ssl": "true",
                "enable_logging": "true",
                "connection_pool_size": "10",
                "cache_duration": "100",
            },
            "LGF_V10",
        )

        tm.that(settings.OracleWms.base_url, eq="https://wms.example/prod")
        tm.that(settings.OracleWms.username, eq="svc_user")
        tm.that(settings.OracleWms.api_version, eq="LGF_V10")
        tm.that(settings.OracleWms.timeout, eq=45)
        tm.that(settings.OracleWms.retry_attempts, eq=2)

    def test_build_client_settings_applies_defaults_for_missing_keys(self) -> None:
        settings = _TESTS.build_client_settings({"base_url": "https://x"}, "LGF_V10")

        tm.that(settings.OracleWms.base_url, eq="https://x")
        tm.that(settings.OracleWms.timeout, eq=30)
        tm.that(settings.OracleWms.retry_attempts, eq=3)

    def test_find_env_file_locates_nearest_env(self, tmp_path: Path) -> None:
        (tmp_path / ".env").write_text("ORACLE_WMS_BASE_URL=https://h\n")
        nested = tmp_path / "a" / "b"
        nested.mkdir(parents=True)

        tm.that(_TESTS.find_env_file(nested / "file.py"), eq=tmp_path / ".env")

    def test_find_env_file_returns_none_when_absent(self, tmp_path: Path) -> None:
        nested = tmp_path / "x" / "y"
        nested.mkdir(parents=True)

        tm.that(_TESTS.find_env_file(nested / "z.py"), none=True)

    def test_load_env_config_parses_env_and_ignores_comments(
        self,
        tmp_path: Path,
    ) -> None:
        (tmp_path / ".env").write_text(
            "ORACLE_WMS_BASE_URL=https://h/production\n"
            "ORACLE_WMS_USERNAME=u1\n"
            "# a comment line\n"
            "ORACLE_WMS_TIMEOUT=50\n",
        )
        start = tmp_path / "a"
        start.mkdir()

        result = _TESTS.load_env_config(start / "file.py")

        tm.ok(result)
        config = result.unwrap()
        tm.that(config["base_url"], eq="https://h/production")
        tm.that(config["username"], eq="u1")
        tm.that(config["timeout"], eq=50)
        tm.that(config["api_version"], eq="LGF_V10")

    def test_load_env_config_fails_when_no_env_present(self, tmp_path: Path) -> None:
        nested = tmp_path / "x" / "y"
        nested.mkdir(parents=True)

        result = _TESTS.load_env_config(nested / "z.py")

        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error, has="No .env file found")

    @pytest.mark.parametrize(
        ("url_tail", "expected_env"),
        [
            ("prod", "production"),
            ("production", "production"),
            ("staging", "staging"),
            ("testing", "test"),
            ("local", "local"),
            ("anything-else", "development"),
        ],
    )
    def test_load_env_config_resolves_environment_from_base_url(
        self,
        tmp_path: Path,
        url_tail: str,
        expected_env: str,
    ) -> None:
        (tmp_path / ".env").write_text(
            f"ORACLE_WMS_BASE_URL=https://host/{url_tail}\n",
        )
        start = tmp_path / "a"
        start.mkdir()

        result = _TESTS.load_env_config(start / "file.py")

        tm.ok(result)
        tm.that(result.unwrap()["environment"], eq=expected_env)

    def test_load_test_env_reports_presence_of_env_file(self, tmp_path: Path) -> None:
        tm.that(_TESTS.load_test_env(tmp_path), eq=False)

        (tmp_path / ".env").write_text("ORACLE_WMS_BASE_URL=https://h\n")
        tm.that(_TESTS.load_test_env(tmp_path), eq=True)

    def test_create_real_settings_fails_without_credentials(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        for var in (
            "ORACLE_WMS_BASE_URL",
            "FLEXT_ORACLE_WMS_BASE_URL",
            "ORACLE_WMS_USERNAME",
            "FLEXT_ORACLE_WMS_USERNAME",
            "ORACLE_WMS_PASSWORD",
            "FLEXT_ORACLE_WMS_PASSWORD",
        ):
            monkeypatch.delenv(var, raising=False)

        result = _TESTS.create_real_settings()

        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error, has="credentials not available")

    def test_create_real_settings_builds_settings_from_environment(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setenv("ORACLE_WMS_BASE_URL", "https://wms.example/prod")
        monkeypatch.setenv("ORACLE_WMS_USERNAME", "svc_user")
        monkeypatch.setenv("ORACLE_WMS_PASSWORD", "secret")
        monkeypatch.setenv("ORACLE_WMS_TIMEOUT", "42")
        monkeypatch.setenv("ORACLE_WMS_MAX_RETRIES", "4")

        result = _TESTS.create_real_settings()

        tm.ok(result)
        settings = result.unwrap()
        tm.that(settings.OracleWms.base_url, eq="https://wms.example/prod")
        tm.that(settings.OracleWms.username, eq="svc_user")
        tm.that(settings.OracleWms.timeout, eq=42)
        tm.that(settings.OracleWms.retry_attempts, eq=4)

    def test_concrete_api_execute_returns_successful_result(self) -> None:
        result = _TESTS.ConcreteApi().execute()

        tm.ok(result)
        tm.that(result.unwrap(), eq=True)
