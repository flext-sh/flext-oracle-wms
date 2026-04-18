"""Test utilities for flext-oracle-wms.

Provides TestsFlextOracleWmsUtilities, combining TestsFlextUtilities with
FlextOracleWmsUtilities for test-specific utility definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import override
from urllib.parse import urlparse

from dotenv import load_dotenv
from flext_tests import FlextTestsUtilities

from flext_core import r
from flext_oracle_wms import (
    FlextOracleWmsApi,
    FlextOracleWmsClientSettings,
    FlextOracleWmsSettings,
    FlextOracleWmsUtilities,
)
from tests import TestsFlextOracleWmsTypes, p


class TestsFlextOracleWmsUtilities(FlextTestsUtilities, FlextOracleWmsUtilities):
    """Test utilities combining TestsFlextUtilities with flext-oracle-wms utilities."""

    class OracleWms(FlextOracleWmsUtilities.OracleWms):
        """OracleWms test utilities namespace."""

        class Tests:
            """Oracle WMS-specific test helpers."""

            class ConcreteApi(FlextOracleWmsApi):
                """Concrete test facade for the abstract public API."""

                @override
                def execute(self) -> p.Result[None]:
                    """Execute the no-op test facade."""
                    return r[None].ok(None)

            @staticmethod
            def to_str(
                value: TestsFlextOracleWmsTypes.OptionalContainerValue, default: str
            ) -> str:
                """Normalize a scalar-like value into a string."""
                if value is None:
                    return default
                if isinstance(value, str):
                    return value
                if isinstance(value, (int, float)):
                    return str(value)
                return default

            @staticmethod
            def to_int(
                value: TestsFlextOracleWmsTypes.OptionalContainerValue, default: int
            ) -> int:
                """Normalize a scalar-like value into an integer."""
                if value is None:
                    return default
                if isinstance(value, (int, float)):
                    return int(value)
                if isinstance(value, str):
                    try:
                        return int(value)
                    except ValueError:
                        return default
                return default

            @staticmethod
            def to_bool(
                value: TestsFlextOracleWmsTypes.OptionalContainerValue,
                default: bool,
            ) -> bool:
                """Normalize a scalar-like value into a boolean."""
                if value is None:
                    return default
                return bool(value)

            @classmethod
            def build_client_settings(
                cls,
                env_config: TestsFlextOracleWmsTypes.OracleWms.Tests.EnvConfig,
                api_version: str,
            ) -> FlextOracleWmsClientSettings:
                """Build client settings from normalized test environment data."""
                return FlextOracleWmsClientSettings(
                    base_url=cls.to_str(env_config.get("base_url", ""), ""),
                    username=cls.to_str(env_config.get("username", ""), ""),
                    password=cls.to_str(env_config.get("password", ""), ""),
                    api_version=api_version,
                    auth_method=cls.to_str(
                        env_config.get("auth_method", "BASIC"),
                        "BASIC",
                    ),
                    timeout=cls.to_int(env_config.get("timeout", 30), 30),
                    max_retries=cls.to_int(env_config.get("max_retries", 3), 3),
                    verify_ssl=cls.to_bool(env_config.get("verify_ssl", True), True),
                    enable_logging=cls.to_bool(
                        env_config.get("enable_logging", True),
                        True,
                    ),
                    connection_pool_size=cls.to_int(
                        env_config.get("connection_pool_size", 20),
                        20,
                    ),
                    cache_duration=cls.to_int(
                        env_config.get("cache_duration", 3600),
                        3600,
                    ),
                    project_name=cls.to_str(
                        env_config.get("project_name", "flext-oracle-wms"),
                        "flext-oracle-wms",
                    ),
                    project_version=cls.to_str(
                        env_config.get("project_version", "0.9.0"),
                        "0.9.0",
                    ),
                )

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
                settings: dict[str, str] = {}
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
                    "timeout": cls.to_int(settings.get("ORACLE_WMS_TIMEOUT", "30"), 30),
                    "max_retries": cls.to_int(
                        settings.get("ORACLE_WMS_MAX_RETRIES", "3"),
                        3,
                    ),
                    "verify_ssl": cls.to_bool(
                        settings.get("ORACLE_WMS_VERIFY_SSL", "true").lower() == "true",
                        True,
                    ),
                    "enable_logging": cls.to_bool(
                        settings.get(
                            "ORACLE_WMS_ENABLE_REQUEST_LOGGING",
                            "true",
                        ).lower()
                        == "true",
                        True,
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
                    FlextOracleWmsSettings(
                        base_url=base_url,
                        username=username,
                        password=password,
                        timeout=int(os.getenv("ORACLE_WMS_TIMEOUT", "30")),
                        retry_attempts=int(os.getenv("ORACLE_WMS_MAX_RETRIES", "3")),
                    ),
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
            def sample_entity_data() -> (
                TestsFlextOracleWmsTypes.OptionalContainerValueMapping
            ):
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
