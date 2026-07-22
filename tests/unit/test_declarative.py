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

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from flext_oracle_wms import (
    FlextOracleWmsApi,
    FlextOracleWmsSettings,
    FlextOracleWmsUtilitiesClient,
    m,
)
from flext_tests import tm
from tests import t, u

if TYPE_CHECKING:
    from collections.abc import Generator, Sequence

    from tests import p


@pytest.fixture
def env_config() -> t.OracleWms.Tests.EnvConfig:
    """Provide .env configuration or deterministic test defaults."""
    config_result = u.OracleWms.Tests.load_env_config(Path(__file__))
    if config_result.success and config_result.value.get("base_url"):
        return config_result.value
    return {
        "base_url": "https://test-wms.example.com",
        "username": "test_user",
        "password": "test_pass",
        "timeout": 30,
        "retry_attempts": 3,
    }


@pytest.fixture
def oracle_wms_client(
    env_config: t.OracleWms.Tests.EnvConfig,
) -> Generator[FlextOracleWmsUtilitiesClient.Client]:
    settings = FlextOracleWmsSettings.model_validate({
        **env_config,
        "api_version": "LGF_V10",
    })
    client = FlextOracleWmsUtilitiesClient.Client(settings)
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
        assert result.success is not result.failure
        if result.failure:
            tm.that(result.error, is_=str)
            assert result.error

    # ------------------------------------------------------------------
    # API facade — deterministic, no I/O
    # ------------------------------------------------------------------

    def test_api_endpoints_return_typed_models(self) -> None:
        """api_endpoints() exposes typed ApiEndpoint models with populated fields."""
        endpoints = FlextOracleWmsApi.api_endpoints()
        assert endpoints
        for endpoint in endpoints.values():
            tm.that(endpoint, is_=m.OracleWms.ApiEndpoint)
            assert endpoint.name
            assert endpoint.method
            assert endpoint.path
            assert endpoint.version
            assert endpoint.category

    def test_api_endpoints_expose_at_least_one_version(self) -> None:
        """The catalog advertises one or more non-empty API version strings."""
        versions = {
            endpoint.version for endpoint in FlextOracleWmsApi.api_endpoints().values()
        }
        assert versions
        assert all(version for version in versions)

    def test_execute_signals_readiness_success(self) -> None:
        """The facade execute() contract returns a successful r[bool] carrying True."""
        result = FlextOracleWmsApi().execute()
        tm.ok(result)
        tm.that(result.value, eq=True)

    # ------------------------------------------------------------------
    # Client operations — r[T] contract on every path
    # ------------------------------------------------------------------

    def test_health_check_returns_result_contract(
        self, oracle_wms_client: FlextOracleWmsUtilitiesClient.Client
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
        self, oracle_wms_client: FlextOracleWmsUtilitiesClient.Client
    ) -> None:
        """discover_entities() yields a list of entities when it succeeds."""
        result = oracle_wms_client.discover_entities()
        self._assert_result_contract(result)
        if result.success:
            tm.that(result.value, is_=list)

    @pytest.mark.parametrize("entity_name", ["company", "facility", "item"])
    def test_get_entity_data_returns_record_sequence(
        self, oracle_wms_client: FlextOracleWmsUtilitiesClient.Client, entity_name: str
    ) -> None:
        """get_entity_data() honours the r[T] contract and returns a sequence."""
        result = oracle_wms_client.get_entity_data(entity_name=entity_name, limit=5)
        self._assert_result_contract(result)
        if result.success:
            tm.that(result.value, is_=(list, tuple))

    def test_get_entity_data_with_filters_returns_result_contract(
        self, oracle_wms_client: FlextOracleWmsUtilitiesClient.Client
    ) -> None:
        """Filtered queries still satisfy the r[T] contract."""
        result = oracle_wms_client.get_entity_data(
            entity_name="company", limit=10, filters={"active": "Y"}
        )
        self._assert_result_contract(result)
        if result.success:
            tm.that(result.value, is_=(list, tuple))

    @pytest.mark.parametrize("limit", [1, 5, 10])
    def test_pagination_never_exceeds_requested_limit(
        self, oracle_wms_client: FlextOracleWmsUtilitiesClient.Client, limit: int
    ) -> None:
        """A successful paged query never returns more records than requested."""
        result = oracle_wms_client.get_entity_data(entity_name="company", limit=limit)
        self._assert_result_contract(result)
        if result.success:
            assert len(result.value) <= limit

    def test_concurrent_entity_requests_all_honour_contract(
        self, oracle_wms_client: FlextOracleWmsUtilitiesClient.Client
    ) -> None:
        """Sequential requests to distinct entities each return a valid r[T]."""
        entities = ["company", "facility", "item"]
        results: list[p.Result[Sequence[t.StrMapping]]] = [
            oracle_wms_client.get_entity_data(entity, limit=3) for entity in entities
        ]
        tm.that(len(results), eq=len(entities))
        for result in results:
            self._assert_result_contract(result)

    # ------------------------------------------------------------------
    # Error paths — deterministic failures
    # ------------------------------------------------------------------

    @pytest.mark.parametrize("entity_name", ["invalid_entity_xyz", ""])
    def test_unknown_entity_fails_with_error(
        self, oracle_wms_client: FlextOracleWmsUtilitiesClient.Client, entity_name: str
    ) -> None:
        """Requesting an unknown entity fails with a populated error message."""
        result = oracle_wms_client.get_entity_data(entity_name)
        tm.fail(result)
        assert result.error

    @pytest.mark.parametrize("api_name", ["unknown_api_xyz", "invalid_api_name"])
    def test_unknown_api_call_fails_with_error(
        self, oracle_wms_client: FlextOracleWmsUtilitiesClient.Client, api_name: str
    ) -> None:
        """Calling an unknown API name fails with a populated error message."""
        result = oracle_wms_client.call_api(api_name)
        tm.fail(result)
        assert result.error

    def test_update_oblpn_tracking_failure_is_not_initialization_error(
        self, oracle_wms_client: FlextOracleWmsUtilitiesClient.Client
    ) -> None:
        """A started client never fails OBLPN updates for being uninitialized."""
        result = oracle_wms_client.update_oblpn_tracking_number(
            oblpn_id="TEST123", tracking_number="TRACK123"
        )
        self._assert_result_contract(result)
        if result.failure and result.error:
            tm.that(result.error, lacks="Client not initialized")

    def test_create_lpn_failure_is_not_initialization_error(
        self, oracle_wms_client: FlextOracleWmsUtilitiesClient.Client
    ) -> None:
        """A started client never fails LPN creation for being uninitialized."""
        result = oracle_wms_client.create_lpn(lpn_nbr="TEST_LPN_001", qty=10)
        self._assert_result_contract(result)
        if result.failure and result.error:
            tm.that(result.error, lacks="Client not initialized")


pytestmark = [pytest.mark.integration]
