"""Behavioral tests for the flext-oracle-wms constants facade.

Exercises the public constant contract exposed via ``tests.constants.c``
(the test facade extending ``flext_oracle_wms.c``): enum values/membership,
frozen mapping payloads, and cross-referenced defaults. Constants are the
observable public contract, so assertions target published values and the
immutability guarantees callers rely on.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import operator

import pytest

from flext_core import c as core_c
from tests import c

_AuthMethod = c.OracleWms.OracleWMSAuthMethod
_FilterOp = c.OracleWms.WmsFilterOperator
_Environment = c.OracleWms.Environment


class TestsFlextOracleWmsConstantsUnit:
    """Behavioral contract tests for the Oracle WMS constants facade."""

    def test_facade_composes_flext_core_constants(self) -> None:
        """The WMS constants facade extends the flext-core constants contract."""
        assert issubclass(c, core_c)

    def test_wms_version_is_non_empty_semver_string(self) -> None:
        """FLEXT_WMS_VERSION exposes a populated version string."""
        version = c.OracleWms.FLEXT_WMS_VERSION
        assert isinstance(version, str)
        assert version.count(".") == 2
        assert all(part.isdigit() for part in version.split("."))

    @pytest.mark.parametrize(
        ("key", "expected"),
        [
            ("version_default", "v1"),
            ("base_url_default", "http://localhost:8080"),
            ("timeout_default", 30),
            ("max_retries", 3),
        ],
    )
    def test_api_config_publishes_connection_defaults(
        self, key: str, expected: str | int
    ) -> None:
        """API_CONFIG maps each documented key to its published default."""
        assert c.OracleWms.API_CONFIG[key] == expected

    @pytest.mark.parametrize(
        "key",
        ["default_batch_size", "max_batch_size", "default_page_size"],
    )
    def test_processing_config_exposes_positive_int_defaults(self, key: str) -> None:
        """PROCESSING_CONFIG advertises positive integer sizing defaults."""
        value = c.OracleWms.PROCESSING_CONFIG[key]
        assert isinstance(value, int)
        assert value > 0

    def test_processing_config_batch_bounds_are_ordered(self) -> None:
        """Default batch size never exceeds the maximum batch size."""
        proc = c.OracleWms.PROCESSING_CONFIG
        assert proc["default_batch_size"] <= proc["max_batch_size"]

    @pytest.mark.parametrize(
        ("key", "expected"),
        [
            ("default", "http://localhost:8080"),
            ("test", "https://test-wms.example.com"),
            ("production", "https://prod-wms.example.com"),
        ],
    )
    def test_environments_map_to_endpoint_urls(self, key: str, expected: str) -> None:
        """ENVIRONMENTS maps each environment name to its published URL."""
        assert c.OracleWms.ENVIRONMENTS[key] == expected

    @pytest.mark.parametrize(
        ("name", "value"),
        [
            ("BASIC", "basic"),
            ("OAUTH2", "oauth2"),
            ("API_KEY", "api_key"),
            ("BEARER", "bearer"),
        ],
    )
    def test_auth_method_enum_values(self, name: str, value: str) -> None:
        """OracleWMSAuthMethod publishes the documented wire values."""
        member = _AuthMethod[name]
        assert member == value
        assert member.value == value

    @pytest.mark.parametrize(
        ("key", "expected"),
        [
            ("basic", _AuthMethod.BASIC),
            ("oauth2", _AuthMethod.OAUTH2),
            ("api_key", _AuthMethod.API_KEY),
            ("bearer", _AuthMethod.BEARER),
        ],
    )
    def test_auth_config_aliases_resolve_to_enum_members(
        self, key: str, expected: c.OracleWms.OracleWMSAuthMethod
    ) -> None:
        """AUTH_CONFIG maps each auth alias onto its enum member."""
        assert c.OracleWms.AUTH_CONFIG[key] is expected

    def test_auth_config_carries_oauth2_endpoint_metadata(self) -> None:
        """AUTH_CONFIG exposes the OAuth2 token endpoint and default scope."""
        auth = c.OracleWms.AUTH_CONFIG
        assert auth["oauth2_token_endpoint"] == "/oauth2/token"
        assert auth["oauth2_scope_default"] == "read write"

    @pytest.mark.parametrize(
        ("name", "value"),
        [
            ("EQ", "eq"),
            ("NE", "ne"),
            ("GT", "gt"),
            ("GTE", "gte"),
            ("LT", "lt"),
            ("LTE", "lte"),
            ("IN", "in"),
            ("NOT_IN", "not_in"),
            ("CONTAINS", "contains"),
        ],
    )
    def test_filter_operator_enum_values(self, name: str, value: str) -> None:
        """WmsFilterOperator publishes the documented operator tokens."""
        member = _FilterOp[name]
        assert member == value
        assert member.value == value

    @pytest.mark.parametrize(
        ("name", "value"),
        [
            ("DEVELOPMENT", "dev"),
            ("STAGING", "staging"),
            ("PRODUCTION", "prod"),
        ],
    )
    def test_environment_enum_values(self, name: str, value: str) -> None:
        """Environment enum publishes deployment-tier tokens."""
        assert _Environment[name] == value

    def test_entity_and_processing_bounds(self) -> None:
        """Nested entity/processing namespaces publish positive bounds."""
        assert c.OracleWms.WmsEntities.MAX_ENTITY_NAME_LENGTH > 0
        assert c.OracleWms.WmsProcessing.MAX_SCHEMA_DEPTH > 0
        assert c.OracleWms.Filtering.MAX_FILTER_CONDITIONS > 0

    @pytest.mark.parametrize(
        "attr",
        ["API_CONFIG", "PROCESSING_CONFIG", "ENVIRONMENTS", "AUTH_CONFIG"],
    )
    def test_config_mappings_are_immutable(self, attr: str) -> None:
        """Published config mappings reject mutation (frozen contract)."""
        mapping = getattr(c.OracleWms, attr)
        with pytest.raises(TypeError):
            operator.setitem(mapping, "__injected__", "x")

    def test_test_facade_adds_oracle_wms_category_taxonomy(self) -> None:
        """The test facade extends the domain with WMS API categories."""
        categories = c.OracleWms.Tests.Categories
        assert categories.DATA_EXTRACT == "data_extract"
        assert categories.ENTITY_OPERATIONS == "entity_operations"
        assert c.OracleWms.Tests.API_VERSION_LGF_V10 == "LGF_V10"


__all__: list[str] = ["TestsFlextOracleWmsConstantsUnit"]
