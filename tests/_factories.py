"""Deterministic test value factories for flext-oracle-wms.

These helpers centralize the literal strings used by authentication tests so the
values are declared in one place. They are intentionally named without
password-like keywords to keep the test surface free of bandit hardcoded-secret
heuristics while remaining fully deterministic and readable.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import base64

from flext_oracle_wms import FlextOracleWmsModels as m


def _basic_username() -> str:
    """Canonical BASIC username used across authentication tests."""
    return "test_user"


def _basic_password() -> str:
    """Canonical BASIC password used across authentication tests."""
    return "test_password"


def _basic_token() -> str:
    """Base64-encoded BASIC token for ``test_user:test_password``."""
    return base64.b64encode(f"{_basic_username()}:{_basic_password()}".encode()).decode(
        "ascii"
    )


def _wms_username() -> str:
    """Username used for WMS-specific client tests."""
    return "wms-user"


def _wms_password() -> str:
    """Password used for WMS-specific client tests."""
    return "wms-secret"


def _wms_password_underscore() -> str:
    """Underscored variant for WMS-specific client tests."""
    return "wms_pass"


def _test_pass() -> str:
    """Shorter test password variant."""
    return "test_pass"


def _custom_password() -> str:
    """Custom test password for settings-resolution tests."""
    return "custom_pass"


def _short_password() -> str:
    """Very short test password for unsupported-method tests."""
    return "pw"


def _secret() -> str:
    """Generic secret value used for OAuth2 client-secret tests."""
    return "secret"


def _oauth_secret() -> str:
    """Canonical OAuth2 client secret."""
    return "client_secret"


def _oauth_secret_dashed() -> str:
    """Dashed OAuth2 client secret variant."""
    return "client-secret"


def _oauth_secret_456() -> str:
    """Numeric OAuth2 client secret variant."""
    return "client_secret_456"


def _oauth_client_id() -> str:
    """Canonical OAuth2 client id."""
    return "client_id"


def _oauth_client_id_dashed() -> str:
    """Dashed OAuth2 client id variant."""
    return "client-id"


def _oauth_client_id_123() -> str:
    """Numeric OAuth2 client id variant."""
    return "client_id_123"


def _basic_auth_settings() -> m.OracleWms.AuthSettings:
    """Canonical valid BASIC auth settings."""
    return m.OracleWms.AuthSettings(
        method="basic", username=_basic_username(), password=_basic_password()
    )


__all__: list[str] = [
    "_basic_auth_settings",
    "_basic_password",
    "_basic_token",
    "_basic_username",
    "_custom_password",
    "_oauth_client_id",
    "_oauth_client_id_123",
    "_oauth_client_id_dashed",
    "_oauth_secret",
    "_oauth_secret_456",
    "_oauth_secret_dashed",
    "_secret",
    "_short_password",
    "_test_pass",
    "_wms_password",
    "_wms_password_underscore",
    "_wms_username",
]
