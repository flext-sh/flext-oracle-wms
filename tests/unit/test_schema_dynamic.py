"""Behavioral tests for Oracle WMS public constants and enum contracts.

Asserts the observable public contract exposed via ``c.OracleWms`` — enum
member values, enum completeness, StrEnum string-equality semantics, mapping
immutability, and the exact numeric limits promised to consumers. No private
attributes, no internal collaborators, no implementation details.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum

import pytest

from tests.constants import c

_WMS = c.OracleWms


class TestsFlextOracleWmsSchemaDynamic:
    """Public-contract tests for the Oracle WMS constants namespace."""

    def test_version_is_nonempty_string(self) -> None:
        """FLEXT_WMS_VERSION is exposed as a concrete non-empty version string."""
        assert _WMS.FLEXT_WMS_VERSION == "1.0.0"

    @pytest.mark.parametrize(
        ("key", "expected"),
        [
            ("version_default", "v1"),
            ("base_url_default", "http://localhost:8080"),
            ("timeout_default", 30),
            ("max_retries", 3),
        ],
    )
    def test_api_config_exposes_expected_values(
        self, key: str, expected: str | int
    ) -> None:
        """API_CONFIG maps each documented key to its promised default value."""
        assert _WMS.API_CONFIG[key] == expected

    def test_api_config_is_immutable(self) -> None:
        """API_CONFIG is a read-only mapping; consumers cannot mutate it."""
        with pytest.raises(TypeError):
            _WMS.API_CONFIG["version_default"] = "v2"  # type: ignore[index]  # Why: proving read-only contract

    @pytest.mark.parametrize(
        "key",
        ["default_batch_size", "max_batch_size", "default_page_size"],
    )
    def test_processing_config_keys_are_positive_ints(self, key: str) -> None:
        """PROCESSING_CONFIG exposes positive integer sizing defaults."""
        value = _WMS.PROCESSING_CONFIG[key]
        assert isinstance(value, int)
        assert value > 0

    @pytest.mark.parametrize(
        ("env", "expected_url"),
        [
            ("default", "http://localhost:8080"),
            ("test", "https://test-wms.example.com"),
            ("production", "https://prod-wms.example.com"),
        ],
    )
    def test_environments_map_to_expected_urls(
        self, env: str, expected_url: str
    ) -> None:
        """ENVIRONMENTS resolves each named environment to its endpoint URL."""
        assert _WMS.ENVIRONMENTS[env] == expected_url

    @pytest.mark.parametrize(
        ("member", "value"),
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
    def test_filter_operator_member_values(self, member: str, value: str) -> None:
        """WmsFilterOperator members carry their documented string values."""
        operator = _WMS.WmsFilterOperator[member]
        assert operator == value
        assert isinstance(operator, StrEnum)

    def test_filter_operator_is_complete(self) -> None:
        """WmsFilterOperator exposes exactly the documented operator set."""
        assert {op.value for op in _WMS.WmsFilterOperator} == {
            "eq",
            "ne",
            "gt",
            "gte",
            "lt",
            "lte",
            "in",
            "not_in",
            "contains",
        }

    @pytest.mark.parametrize(
        ("member", "value"),
        [
            ("BASIC", "basic"),
            ("OAUTH2", "oauth2"),
            ("API_KEY", "api_key"),
            ("BEARER", "bearer"),
        ],
    )
    def test_auth_method_member_values(self, member: str, value: str) -> None:
        """OracleWMSAuthMethod members carry their documented string values."""
        method = _WMS.OracleWMSAuthMethod[member]
        assert method == value
        assert isinstance(method, StrEnum)

    def test_auth_method_is_complete(self) -> None:
        """OracleWMSAuthMethod exposes exactly the four supported methods."""
        assert {m.value for m in _WMS.OracleWMSAuthMethod} == {
            "basic",
            "oauth2",
            "api_key",
            "bearer",
        }

    def test_filtering_max_conditions_limit(self) -> None:
        """Filtering caps filter conditions at the documented maximum."""
        assert _WMS.Filtering.MAX_FILTER_CONDITIONS == 50

    def test_entity_name_length_limit(self) -> None:
        """WmsEntities bounds entity names to the documented maximum length."""
        assert _WMS.WmsEntities.MAX_ENTITY_NAME_LENGTH == 100

    def test_processing_schema_depth_limit(self) -> None:
        """WmsProcessing bounds schema nesting to the documented maximum depth."""
        assert _WMS.WmsProcessing.MAX_SCHEMA_DEPTH == 10


__all__: list[str] = ["TestsFlextOracleWmsSchemaDynamic"]
