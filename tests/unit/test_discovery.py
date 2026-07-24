"""Behavioral tests for Oracle WMS discovery outcome constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest
from flext_tests import tm

from tests import c


class TestsFlextOracleWmsDiscovery:
    """Public-contract suite for the discovery outcome tokens.

    ``DISCOVERY_SUCCESS`` / ``DISCOVERY_FAILURE`` are the observable string
    tokens the discovery flow emits to distinguish outcomes. These tests pin
    the published token values and the invariants callers rely on (stable
    string identity and mutual distinctness) without touching internals.
    """

    @pytest.mark.parametrize(
        ("attribute", "expected_token"),
        [
            ("DISCOVERY_SUCCESS", "discovery_success"),
            ("DISCOVERY_FAILURE", "discovery_failure"),
        ],
    )
    def test_discovery_token_exposes_published_string_value(
        self, attribute: str, expected_token: str
    ) -> None:
        """Each discovery outcome token is published with its exact string."""
        token: str = getattr(c.OracleWms, attribute)

        tm.that(token, eq=expected_token)
        tm.that(token, is_=str)

    def test_success_and_failure_tokens_are_distinct(self) -> None:
        """Success and failure outcomes must never collide as the same token."""
        tm.that(c.OracleWms.DISCOVERY_SUCCESS, ne=c.OracleWms.DISCOVERY_FAILURE)

    def test_discovery_tokens_are_stable_across_access(self) -> None:
        """Repeated reads return the identical token (immutable contract)."""
        tm.that(c.OracleWms.DISCOVERY_SUCCESS, eq=c.OracleWms.DISCOVERY_SUCCESS)
        tm.that(c.OracleWms.DISCOVERY_FAILURE, eq=c.OracleWms.DISCOVERY_FAILURE)


__all__: list[str] = ["TestsFlextOracleWmsDiscovery"]
