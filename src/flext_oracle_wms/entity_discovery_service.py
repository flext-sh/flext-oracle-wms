"""Oracle WMS Entity Discovery Service - Single Responsibility.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Dedicated service for Oracle WMS entity discovery operations.
Follows Single Responsibility Principle - only handles entity discovery.
"""

from __future__ import annotations

from flext_api import FlextApiClient
from flext_core import FlextLogger, FlextResult, FlextTypes

from flext_oracle_wms.wms_api import FLEXT_ORACLE_WMS_APIS, get_mock_server


class OracleWmsEntityDiscoveryService:
    """Dedicated service for Oracle WMS entity discovery operations.

    Single Responsibility: Only handles entity discovery operations.
    """

    def __init__(self, api_client: FlextApiClient, environment: str) -> None:
        """Initialize entity discovery service."""
        self._api_client = api_client
        self._environment = environment
        self._logger = FlextLogger(__name__)

    async def discover_entities(self, *, use_mock: bool = False) -> FlextResult[list[FlextTypes.Core.Dict]]:
        """Discover available Oracle WMS entities."""
        try:
            if use_mock:
                return await self._discover_entities_mock()

            return await self._discover_entities_real()

        except Exception as e:
            error_msg = f"Entity discovery failed: {e}"
            self._logger.exception(error_msg)
            return FlextResult[list[FlextTypes.Core.Dict]].fail(error_msg)

    async def _discover_entities_mock(self) -> FlextResult[list[FlextTypes.Core.Dict]]:
        """Discover entities using mock server."""
        try:
            mock_server = get_mock_server(self._environment)
            mock_result = mock_server.get_mock_response("entity_discovery")

            if not mock_result.success or not mock_result.value:
                return FlextResult[list[FlextTypes.Core.Dict]].fail(
                    f"Mock discovery failed: {mock_result.error}"
                )

            entities_data = mock_result.value.get("entities", [])
            return FlextResult[list[FlextTypes.Core.Dict]].ok(
                entities_data if isinstance(entities_data, list) else []
            )

        except Exception as e:
            return FlextResult[list[FlextTypes.Core.Dict]].fail(f"Mock discovery error: {e}")

    async def _discover_entities_real(self) -> FlextResult[list[FlextTypes.Core.Dict]]:
        """Discover entities using real Oracle WMS API."""
        try:
            endpoint = FLEXT_ORACLE_WMS_APIS.get("entity_discovery")
            if not endpoint:
                return FlextResult[list[FlextTypes.Core.Dict]].fail(
                    "Entity discovery endpoint not configured"
                )

            endpoint_path = f"/{self._environment}{endpoint.path}"
            response = await self._api_client.get(endpoint_path)

            if not response.success or response.value is None:
                return FlextResult[list[FlextTypes.Core.Dict]].fail(
                    response.error or "No response from Oracle WMS"
                )

            api_resp = response.value
            if not api_resp.is_success:
                return FlextResult[list[FlextTypes.Core.Dict]].fail(
                    f"Entity discovery failed: HTTP {api_resp.status_code}"
                )

            body = api_resp.body
            if not isinstance(body, dict):
                return FlextResult[list[FlextTypes.Core.Dict]].fail(
                    "Invalid entity discovery response format"
                )

            entities = body.get("entities", [])
            if not isinstance(entities, list):
                return FlextResult[list[FlextTypes.Core.Dict]].fail(
                    "Entities data is not a list"
                )

            return FlextResult[list[FlextTypes.Core.Dict]].ok(entities)

        except Exception as e:
            return FlextResult[list[FlextTypes.Core.Dict]].fail(f"Real discovery error: {e}")

    @staticmethod
    def get_fallback_entities() -> list[FlextTypes.Core.Dict]:
        """Get fallback entities when API is not available."""
        return [
            {"name": "company", "type": "entity"},
            {"name": "facility", "type": "entity"},
            {"name": "item", "type": "entity"},
        ]
