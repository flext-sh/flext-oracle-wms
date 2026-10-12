# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import api, d, h, r, td, tf, tk, tm, x

    from flext_oracle_wms import e
    from tests._factories import (
        _basic_auth_settings,
        _basic_password,
        _basic_token,
        _basic_username,
        _custom_password,
        _oauth_client_id,
        _oauth_client_id_123,
        _oauth_client_id_dashed,
        _oauth_secret,
        _oauth_secret_456,
        _oauth_secret_dashed,
        _secret,
        _short_password,
        _test_pass,
        _wms_password,
        _wms_password_underscore,
        _wms_username,
    )
    from tests.base import TestsFlextOracleWmsServiceBase, s
    from tests.constants import TestsFlextOracleWmsConstants, c
    from tests.models import TestsFlextOracleWmsModels, m
    from tests.protocols import TestsFlextOracleWmsProtocols, p
    from tests.settings import TestsFlextOracleWmsSettings
    from tests.typings import TestsFlextOracleWmsTypes, t
    from tests.utilities import TestsFlextOracleWmsUtilities, u


__all__: tuple[str, ...] = (
    "TestsFlextOracleWmsConstants",
    "TestsFlextOracleWmsModels",
    "TestsFlextOracleWmsProtocols",
    "TestsFlextOracleWmsServiceBase",
    "TestsFlextOracleWmsSettings",
    "TestsFlextOracleWmsTypes",
    "TestsFlextOracleWmsUtilities",
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
    "api",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "TestsFlextOracleWmsConstants": ".constants",
        "TestsFlextOracleWmsModels": ".models",
        "TestsFlextOracleWmsProtocols": ".protocols",
        "TestsFlextOracleWmsServiceBase": ".base",
        "TestsFlextOracleWmsSettings": ".settings",
        "TestsFlextOracleWmsTypes": ".typings",
        "TestsFlextOracleWmsUtilities": ".utilities",
        "_basic_auth_settings": "._factories",
        "_basic_password": "._factories",
        "_basic_token": "._factories",
        "_basic_username": "._factories",
        "_custom_password": "._factories",
        "_oauth_client_id": "._factories",
        "_oauth_client_id_123": "._factories",
        "_oauth_client_id_dashed": "._factories",
        "_oauth_secret": "._factories",
        "_oauth_secret_456": "._factories",
        "_oauth_secret_dashed": "._factories",
        "_secret": "._factories",
        "_short_password": "._factories",
        "_test_pass": "._factories",
        "_wms_password": "._factories",
        "_wms_password_underscore": "._factories",
        "_wms_username": "._factories",
        "api": "flext_tests",
        "c": ".constants",
        "d": "flext_tests",
        "e": "flext_oracle_wms",
        "h": "flext_tests",
        "m": ".models",
        "p": ".protocols",
        "r": "flext_tests",
        "s": ".base",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "x": "flext_tests",
    }),
    public_exports=__all__,
)
