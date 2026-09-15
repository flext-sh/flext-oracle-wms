# mypy: warn-unused-ignores=False
"""Behavioral tests for Oracle WMS public enum contracts.

Asserts the enum semantics ``c.OracleWms`` promises to consumers: StrEnum
string-equality semantics and vocabulary completeness. Connection defaults,
environment URLs, and numeric limits are owned by the cross-source agreement
tests in ``test_constants.py``; wire-vocabulary sets here are the immutable
external protocol, not config-owned values.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum

from flext_tests import tm

from tests import c


class TestsFlextOracleWmsSchemaDynamic:
    """Public-contract tests for the Oracle WMS constants namespace."""

    def test_filter_operator_members_are_strenums(self) -> None:
        """Every WmsFilterOperator member is a StrEnum carrying a string value."""
        for operator in c.OracleWms.WmsFilterOperator:
            tm.that(operator, is_=StrEnum)
            tm.that(operator.value, is_=str)

    def test_filter_operator_is_complete(self) -> None:
        """WmsFilterOperator exposes exactly the documented operator set."""
        tm.that(
            {op.value for op in c.OracleWms.WmsFilterOperator},
            eq={"eq", "ne", "gt", "gte", "lt", "lte", "in", "not_in", "contains"},
        )

    def test_auth_method_members_are_strenums(self) -> None:
        """Every OracleWMSAuthMethod member is a StrEnum carrying a string value."""
        for method in c.OracleWms.OracleWMSAuthMethod:
            tm.that(method, is_=StrEnum)
            tm.that(method.value, is_=str)

    def test_auth_method_is_complete(self) -> None:
        """OracleWMSAuthMethod exposes exactly the four supported methods."""
        tm.that(
            {m.value for m in c.OracleWms.OracleWMSAuthMethod},
            eq={"basic", "oauth2", "api_key", "bearer"},
        )


__all__: list[str] = ["TestsFlextOracleWmsSchemaDynamic"]
