"""Oracle WMS API Service - Single Responsibility.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Dedicated service for Oracle WMS API operations.
Follows Single Responsibility Principle - only handles API calls.
"""

from __future__ import annotations

from flext_api import FlextApiClient
from flext_core import FlextLogger, FlextResult, FlextTypes


class OracleWmsApiService:
    """Dedicated service for Oracle WMS API operations.

    Single Responsibility: Only handles API calls to Oracle WMS.
    """

    def __init__(self, api_client: FlextApiClient) -> None:
        """Initialize API service."""
        self._api_client = api_client
        self._logger = FlextLogger(__name__)

    async def call_api(
        self,
        endpoint_path: str,
        method: str = "GET",
        data: FlextTypes.Core.Dict | None = None,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Make API call to Oracle WMS endpoint."""
        try:
            if method.upper() == "GET":
                response = await self._api_client.get(endpoint_path)
            elif method.upper() == "POST":
                response = await self._api_client.post(endpoint_path, data=data)
            elif method.upper() == "PUT":
                response = await self._api_client.put(endpoint_path, data=data)
            elif method.upper() == "DELETE":
                response = await self._api_client.delete(endpoint_path)
            else:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"Unsupported HTTP method: {method}"
                )

            if not response.success or response.value is None:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    response.error or "No response from Oracle WMS"
                )

            api_resp = response.value
            if not api_resp.is_success:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    f"API call failed: HTTP {api_resp.status_code}"
                )

            body = api_resp.body
            data_dict = body if isinstance(body, dict) else {}
            return FlextResult[FlextTypes.Core.Dict].ok(data_dict)

        except Exception as e:
            error_msg = f"API call failed: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)

    async def get_entity_data(
        self,
        entity_name: str,
        environment: str,
        filters: FlextTypes.Core.Dict | None = None,
    ) -> FlextResult[FlextTypes.Core.Dict | list[FlextTypes.Core.Dict]]:
        """Get data for a specific entity."""
        try:
            endpoint_path = f"/{environment}/wms/lgfapi/v10/entity/{entity_name}/"

            if filters:
                # Add filters as query parameters
                params = {}
                for key, value in filters.items():
                    if isinstance(value, (str, int, float, bool)):
                        params[key] = str(value)
                endpoint_path += "?" + "&".join(f"{k}={v}" for k, v in params.items())

            response = await self._api_client.get(endpoint_path)

            if not response.success or response.value is None:
                return FlextResult[FlextTypes.Core.Dict | list[FlextTypes.Core.Dict]].fail(
                    response.error or "No response from Oracle WMS"
                )

            api_resp = response.value
            if not api_resp.is_success:
                return FlextResult[FlextTypes.Core.Dict | list[FlextTypes.Core.Dict]].fail(
                    f"Entity data extraction failed: HTTP {api_resp.status_code}"
                )

            body = api_resp.body
            if isinstance(body, dict):
                return FlextResult[FlextTypes.Core.Dict | list[FlextTypes.Core.Dict]].ok(body)
            if isinstance(body, list):
                # Cast to expected type - Oracle WMS returns list of dicts
                typed_body: list[FlextTypes.Core.Dict] = [item for item in body if isinstance(item, dict)]
                return FlextResult[FlextTypes.Core.Dict | list[FlextTypes.Core.Dict]].ok(typed_body)
            return FlextResult[FlextTypes.Core.Dict | list[FlextTypes.Core.Dict]].fail(
                "Invalid response body format"
            )

        except Exception as e:
            error_msg = f"Entity data extraction failed: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict | list[FlextTypes.Core.Dict]].fail(error_msg)
