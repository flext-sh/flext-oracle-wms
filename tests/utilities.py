"""Test utilities for flext-oracle-wms.

Provides TestsFlextOracleWmsUtilities, combining TestsFlextUtilities with
FlextOracleWmsUtilities for test-specific utility definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, override
from urllib.parse import urlparse

from dotenv import load_dotenv
from flext_tests import FlextTestsUtilities, r

from flext_oracle_wms import (
    FlextOracleWmsApi,
    FlextOracleWmsSettings,
    FlextOracleWmsUtilities as u,
)
from tests import TestsFlextOracleWmsTypes, p, t

if TYPE_CHECKING:
    from pathlib import Path


class TestsFlextOracleWmsUtilities(FlextTestsUtilities, u):
    """Test utilities combining TestsFlextUtilities with flext-oracle-wms utilities."""

    class OracleWms(u.OracleWms):
        """OracleWms test utilities namespace."""

        class Tests:
            """Oracle WMS-specific test helpers."""

            class ConcreteApi(FlextOracleWmsApi):
                """Concrete test facade for the abstract public API."""

                @override
                def execute(self) -> p.Result[bool]:
                    """Execute the no-op test facade."""
                    return r[bool].ok(True)

            @classmethod
            def build_client_settings(
                cls,
                env_config: TestsFlextOracleWmsTypes.OracleWms.Tests.EnvConfig,
                api_version: str,
            ) -> FlextOracleWmsSettings:
                """Build client settings from normalized test environment data."""
                # NOTE (multi-agent): ADR-005 — project scalars live under the
                # nested ``OracleWms`` namespace; build via model_validate with
                # the namespaced payload, never flat constructor kwargs.
                return FlextOracleWmsSettings.model_validate({
                    "OracleWms": {
                        "base_url": u.to_str(
                            env_config.get("base_url", ""),
                            default="",
                        ),
                        "username": u.to_str(
                            env_config.get("username", ""), default=""
                        ),
                        "password": u.to_str(
                            env_config.get("password", ""), default=""
                        ),
                        "api_version": api_version,
                        "auth_method": u.to_str(
                            env_config.get("auth_method", "BASIC"),
                            default="BASIC",
                        ),
                        "timeout": u.to_int(env_config.get("timeout", 30), default=30),
                        "retry_attempts": u.to_int(
                            env_config.get("retry_attempts", 3),
                            default=3,
                        ),
                        "verify_ssl": u.to_bool(
                            env_config.get("verify_ssl", True),
                            default=True,
                        ),
                        "enable_logging": u.to_bool(
                            env_config.get("enable_logging", True),
                            default=True,
                        ),
                        "connection_pool_size": u.to_int(
                            env_config.get("connection_pool_size", 20),
                            default=20,
                        ),
                        "cache_duration": u.to_int(
                            env_config.get("cache_duration", 3600),
                            default=3600,
                        ),
                    },
                })

            @staticmethod
            def find_env_file(start_path: Path) -> Path | None:
                """Find the closest `.env` file in the test project hierarchy."""
                current_dir = start_path.parent
                for _ in range(4):
                    env_path = current_dir / ".env"
                    if env_path.exists():
                        return env_path
                    current_dir = current_dir.parent
                project_root = start_path.parent.parent
                env_path = project_root / ".env"
                if env_path.exists():
                    return env_path
                return None

            @staticmethod
            def _resolve_environment_name(base_url: str) -> str:
                """Derive the environment name from the configured base URL."""
                if not base_url:
                    return "development"
                parsed = urlparse(base_url)
                path_parts = parsed.path.strip("/").split("/")
                if not path_parts or not path_parts[-1]:
                    return "development"
                env_name = path_parts[-1].lower()
                if env_name in {"prod", "production"}:
                    return "production"
                if env_name in {"stage", "staging"}:
                    return "staging"
                if env_name in {"test", "testing", "company_unknow"}:
                    return "test"
                if env_name == "local":
                    return "local"
                return "development"

            @classmethod
            def load_env_config(
                cls,
                start_path: Path,
            ) -> p.Result[TestsFlextOracleWmsTypes.OracleWms.Tests.EnvConfig]:
                """Load declarative integration settings from the nearest `.env` file."""
                env_path = cls.find_env_file(start_path)
                if env_path is None:
                    return r[TestsFlextOracleWmsTypes.OracleWms.Tests.EnvConfig].fail(
                        "No .env file found for Oracle WMS integration tests",
                    )
                settings: t.MutableStrMapping = {}
                try:
                    with env_path.open(encoding="utf-8") as file_handle:
                        for raw_line in file_handle:
                            line = raw_line.strip()
                            if line and not line.startswith("#") and "=" in line:
                                key, value = line.split("=", 1)
                                settings[key.strip()] = value.strip()
                except (OSError, ValueError, TypeError) as exc:
                    return r[TestsFlextOracleWmsTypes.OracleWms.Tests.EnvConfig].fail(
                        f"Failed to load .env settings: {exc}",
                    )
                base_url = settings.get("ORACLE_WMS_BASE_URL", "")
                return r[TestsFlextOracleWmsTypes.OracleWms.Tests.EnvConfig].ok({
                    "base_url": base_url,
                    "username": settings.get("ORACLE_WMS_USERNAME"),
                    "password": settings.get("ORACLE_WMS_PASSWORD"),
                    "environment": cls._resolve_environment_name(base_url),
                    "api_version": "LGF_V10",
                    "timeout": u.to_int(
                        settings.get("ORACLE_WMS_TIMEOUT", "30"),
                        default=30,
                    ),
                    "max_retries": u.to_int(
                        settings.get("ORACLE_WMS_MAX_RETRIES", "3"),
                        default=3,
                    ),
                    "verify_ssl": u.to_bool(
                        settings.get("ORACLE_WMS_VERIFY_SSL", "true").lower() == "true",
                        default=True,
                    ),
                    "enable_logging": u.to_bool(
                        settings.get(
                            "ORACLE_WMS_ENABLE_REQUEST_LOGGING",
                            "true",
                        ).lower()
                        == "true",
                        default=True,
                    ),
                })

            @staticmethod
            def load_test_env(project_root: Path) -> bool:
                """Load the project `.env` into process environment when present."""
                env_file = project_root / ".env"
                if env_file.exists():
                    load_dotenv(env_file)
                    return True
                return False

            @staticmethod
            def create_real_settings() -> p.Result[FlextOracleWmsSettings]:
                """Create runtime settings from process environment variables."""
                base_url = os.getenv("ORACLE_WMS_BASE_URL") or os.getenv(
                    "FLEXT_ORACLE_WMS_BASE_URL",
                )
                username = os.getenv("ORACLE_WMS_USERNAME") or os.getenv(
                    "FLEXT_ORACLE_WMS_USERNAME",
                )
                password = os.getenv("ORACLE_WMS_PASSWORD") or os.getenv(
                    "FLEXT_ORACLE_WMS_PASSWORD",
                )
                if not base_url or not username or not password:
                    return r[FlextOracleWmsSettings].fail(
                        "Real Oracle WMS credentials not available in .env",
                    )
                return r[FlextOracleWmsSettings].ok(
                    FlextOracleWmsSettings.model_validate({
                        "OracleWms": {
                            "base_url": base_url,
                            "username": username,
                            "password": password,
                            "timeout": int(os.getenv("ORACLE_WMS_TIMEOUT", "30")),
                            "retry_attempts": int(
                                os.getenv("ORACLE_WMS_MAX_RETRIES", "3"),
                            ),
                        },
                    }),
                )

            @staticmethod
            def sample_entities() -> TestsFlextOracleWmsTypes.StrSequence:
                """Return the canonical sample entity list for tests."""
                return [
                    "action_code",
                    "company",
                    "facility",
                    "item",
                    "order_hdr",
                    "order_dtl",
                ]

            @staticmethod
            def sample_entity_data() -> TestsFlextOracleWmsTypes.JsonMapping | None:
                """Return canonical sample entity payload data for tests."""
                return {
                    "result_count": 4,
                    "page_count": 1,
                    "page_nbr": 1,
                    "next_page": None,
                    "previous_page": None,
                    "results": [
                        {"id": 1, "code": "TEST_CODE", "description": "Test Record"},
                        {
                            "id": 2,
                            "code": "TEST_CODE_2",
                            "description": "Test Record 2",
                        },
                    ],
                }


u = TestsFlextOracleWmsUtilities
__all__: list[str] = ["TestsFlextOracleWmsUtilities", "u"]
