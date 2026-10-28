"""Behavioral tests for the Oracle WMS declarative client and API facade.

Asserts observable public contracts only:
- ``FlextOracleWmsApi.api_endpoints()`` returns typed endpoint models.
- ``FlextOracleWmsApi.execute()`` honours its ``s[bool]`` readiness contract.
- Every client operation returns an ``r[T]`` value (never raises) that satisfies
  the success-XOR-failure invariant, with a non-empty error message on failure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from flext_oracle_wms import FlextOracleWmsApi, FlextOracleWmsSettings, m
from tests import t, tm, u

if TYPE_CHECKING:
    from collections.abc import Generator

from tests import p


@pytest.fixture
def env_config() -> t.OracleWms.Tests.EnvConfig:
    """Provide .env configuration or deterministic test defaults.

    Returns:
        The resulting ``t.OracleWms.Tests.EnvConfig``.

    """
    config_result = u.OracleWms.Tests.load_env_config(Path(__file__))
    if config_result.success and config_result.value.get("base_url"):
        return config_result.value
    return {
        "base_url": "https://test-wms.example.com",
        "username": "test_user",
        "password": "p" + "6" * 12,
        "timeout": 30,
        "retry_attempts": 3,
    }


@pytest.fixture
def oracle_wms_client(
    env_config: t.OracleWms.Tests.EnvConfig,
) -> Generator[u.OracleWms.Client]:
    """Provide ``oracle_wms_client``.

    Yields:
        Each ``u.OracleWms.Client``.

    """
    settings = FlextOracleWmsSettings.model_validate({
        **env_config,
        "api_version": "LGF_V10",
    })
    client = u.OracleWms.Client(settings)
    start_result = client.start()
    if not start_result.success:
        pytest.fail(f"Failed to start Oracle WMS client: {start_result.error}")
    yield client
    client.stop()


class TestsFlextOracleWmsDeclarative:
    """Behavioral contract for the declarative Oracle WMS surface."""

    @staticmethod
    def _assert_result_contract[T](result: p.Result[T]) -> None:
        """Assert the universal ``r[T]`` invariant: exactly one of success/failure.

        On failure the error must be a non-empty, human-readable string so that
        callers can surface it. This is the fail-loud guarantee: operations
        return a typed result instead of raising or hiding failures.
        """
        tm.that(result.success is not result.failure, truth=True)
        if result.failure:
            tm.that(result.error, is_=str)
            tm.that(result.error, truth=True)

    # ------------------------------------------------------------------
    # API facade — deterministic, no I/O
    # ------------------------------------------------------------------

    @staticmethod
    def test_api_endpoints_return_typed_models() -> None:
        """api_endpoints() exposes typed ApiEndpoint models with populated fields."""
        endpoints = FlextOracleWmsApi.api_endpoints()
        tm.that(endpoints, truth=True)
        for endpoint in endpoints.values():
            tm.that(endpoint, is_=m.OracleWms.ApiEndpoint)
            tm.that(endpoint.name, truth=True)
            tm.that(endpoint.method, truth=True)
            tm.that(endpoint.path, truth=True)
            tm.that(endpoint.version, truth=True)
            tm.that(endpoint.category, truth=True)

    @staticmethod
    def test_api_endpoints_expose_at_least_one_version() -> None:
        """The catalog advertises one or more non-empty API version strings."""
        versions = {
            endpoint.version for endpoint in FlextOracleWmsApi.api_endpoints().values()
        }
        tm.that(versions, truth=True)
        tm.that(all(version for version in versions), truth=True)

    @staticmethod
    def test_execute_signals_readiness_success() -> None:
        """The facade execute() contract returns a successful r[bool] carrying True."""
        result = FlextOracleWmsApi().execute()
        tm.ok(result)
        tm.ok(result.value)

    # ------------------------------------------------------------------
    # Client operations — r[T] contract on every path
    # ------------------------------------------------------------------

    def test_health_check_returns_result_contract(
        self,
        oracle_wms_client: u.OracleWms.Client,
    ) -> None:
        """health_check() returns a well-formed r[T]; on success reports service."""
        result = oracle_wms_client.health_check()
        self._assert_result_contract(result)
        if result.success:
            body = result.value.body
            payload = body if isinstance(body, dict) else dict[str, t.JsonValue]()
            tm.that(payload.get("service"), eq="FlextOracleWmsClient")
            tm.that({"healthy", "unhealthy"}, has=payload.get("status"))

    def test_discover_entities_returns_sequence_on_success(
        self,
        oracle_wms_client: u.OracleWms.Client,
    ) -> None:
        """discover_entities() yields a list of entities when it succeeds."""
        result = oracle_wms_client.discover_entities()
        self._assert_result_contract(result)
        if result.success:
            tm.that(result.value, is_=list)

    @pytest.mark.parametrize("entity_name", ["company", "facility", "item"])
    def test_fetch_entity_data_returns_record_sequence(
        self,
        oracle_wms_client: u.OracleWms.Client,
        entity_name: str,
    ) -> None:
        """fetch_entity_data() honours the r[T] contract and returns a sequence."""
        result = oracle_wms_client.fetch_entity_data(entity_name=entity_name, limit=5)
        self._assert_result_contract(result)
        if result.success:
            tm.that(result.value, is_=(list, tuple))

    def test_fetch_entity_data_with_filters_returns_result_contract(
        self,
        oracle_wms_client: u.OracleWms.Client,
    ) -> None:
        """Filtered queries still satisfy the r[T] contract."""
        result = oracle_wms_client.fetch_entity_data(
            entity_name="company",
            limit=10,
            filters={"active": "Y"},
        )
        self._assert_result_contract(result)
        if result.success:
            tm.that(result.value, is_=(list, tuple))

    @pytest.mark.parametrize("limit", [1, 5, 10])
    def test_pagination_never_exceeds_requested_limit(
        self,
        oracle_wms_client: u.OracleWms.Client,
        limit: int,
    ) -> None:
        """A successful paged query never returns more records than requested."""
        result = oracle_wms_client.fetch_entity_data(entity_name="company", limit=limit)
        self._assert_result_contract(result)
        if result.success:
            tm.that(len(result.value) <= limit, truth=True)

    def test_concurrent_entity_requests_all_honour_contract(
        self,
        oracle_wms_client: u.OracleWms.Client,
    ) -> None:
        """Sequential requests to distinct entities each return a valid r[T]."""
        entities = ["company", "facility", "item"]
        results: list[p.Result[Sequence[Mapping[str, str]]]] = [
            oracle_wms_client.fetch_entity_data(entity, limit=3) for entity in entities
        ]
        tm.that(len(results), eq=len(entities))
        for result in results:
            self._assert_result_contract(result)

    # ------------------------------------------------------------------
    # Error paths — deterministic failures
    # ------------------------------------------------------------------

    @staticmethod
    @pytest.mark.parametrize("entity_name", ["invalid_entity_xyz", ""])
    def test_unknown_entity_fails_with_error(
        oracle_wms_client: u.OracleWms.Client,
        entity_name: str,
    ) -> None:
        """Requesting an unknown entity fails with a populated error message."""
        result = oracle_wms_client.fetch_entity_data(entity_name)
        tm.fail(result)
        tm.that(result.error, truth=True)

    @staticmethod
    @pytest.mark.parametrize("api_name", ["unknown_api_xyz", "invalid_api_name"])
    def test_unknown_api_call_fails_with_error(
        oracle_wms_client: u.OracleWms.Client,
        api_name: str,
    ) -> None:
        """Calling an unknown API name fails with a populated error message."""
        result = oracle_wms_client.call_api(api_name)
        tm.fail(result)
        tm.that(result.error, truth=True)

    def test_update_oblpn_tracking_failure_is_not_initialization_error(
        self,
        oracle_wms_client: u.OracleWms.Client,
    ) -> None:
        """A started client never fails OBLPN updates for being uninitialized."""
        result = oracle_wms_client.update_oblpn_tracking_number(
            oblpn_id="TEST123",
            tracking_number="TRACK123",
        )
        self._assert_result_contract(result)
        if result.failure and result.error:
            tm.that(result.error, lacks="Client not initialized")

    def test_create_lpn_failure_is_not_initialization_error(
        self,
        oracle_wms_client: u.OracleWms.Client,
    ) -> None:
        """A started client never fails LPN creation for being uninitialized."""
        result = oracle_wms_client.create_lpn(lpn_nbr="TEST_LPN_001", qty=10)
        self._assert_result_contract(result)
        if result.failure and result.error:
            tm.that(result.error, lacks="Client not initialized")


pytestmark = [pytest.mark.integration]
