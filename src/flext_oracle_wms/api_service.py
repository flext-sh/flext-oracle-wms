"""Oracle WMS API Service - Single Responsibility.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Dedicated service for Oracle WMS API operations.
Follows Single Responsibility Principle - only handles API calls.
"""

from __future__ import annotations

from typing import override

from flext_core import FlextLogger, FlextResult
from flext_oracle_wms.http_client import FlextHttpClient
from flext_oracle_wms.typings import FlextOracleWmsTypes


class OracleWmsApiService:
    """Dedicated service for Oracle WMS API operations.

    Single Responsibility: Only handles API calls to Oracle WMS.
    """

    @override
    def __init__(self, api_client: FlextHttpClient) -> None:
        """Initialize API service."""
        self._api_client = api_client
        self._logger = FlextLogger(__name__)

    def call_api(
        self,
        endpoint_path: str,
        method: str = "GET",
        data: FlextOracleWmsTypes.Core.Dict | None = None,
    ) -> FlextResult[FlextOracleWmsTypes.Core.Dict]:
        """Make API call to Oracle WMS endpoint."""
        try:
            if method.upper() == "GET":
                response = self._api_client.get(endpoint_path)
            elif method.upper() == "POST":
                response = self._api_client.post(endpoint_path, data=data)
            elif method.upper() == "PUT":
                response = self._api_client.put(endpoint_path, data=data)
            elif method.upper() == "DELETE":
                response = self._api_client.delete(endpoint_path)
            else:
                return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(
                    f"Unsupported HTTP method: {method}",
                )

            if not response.success:
                return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(
                    response.error or "No response from Oracle WMS",
                )

            api_resp = response.value
            # Check if response indicates success (assuming it's a dict with status info)
            if isinstance(api_resp, dict) and api_resp.get("status") != "success":
                return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(
                    f"API call failed: HTTP {api_resp.get('status_code', 'unknown')}",
                )

            body = api_resp
            data_dict: dict[str, object] = body if isinstance(body, dict) else {}
            return FlextResult[FlextOracleWmsTypes.Core.Dict].ok(data_dict)

        except Exception as e:
            error_msg = f"API call failed: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(error_msg)

    def get_entity_data(
        self,
        entity_name: str,
        environment: str,
        filters: FlextOracleWmsTypes.Core.Dict | None = None,
    ) -> FlextResult[
        FlextOracleWmsTypes.Core.Dict | list[FlextOracleWmsTypes.Core.Dict]
    ]:
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

            response = self._api_client.get(endpoint_path)

            if not response.success:
                return FlextResult[
                    FlextOracleWmsTypes.Core.Dict | list[FlextOracleWmsTypes.Core.Dict]
                ].fail(response.error or "No response from Oracle WMS")

            api_resp = response.value
            # Check if response indicates success (assuming it's a dict with status info)
            if isinstance(api_resp, dict) and api_resp.get("status") != "success":
                return FlextResult[
                    FlextOracleWmsTypes.Core.Dict | list[FlextOracleWmsTypes.Core.Dict]
                ].fail(
                    f"Entity data extraction failed: HTTP {api_resp.get('status_code', 'unknown')}",
                )

            body = api_resp
            return FlextResult[
                FlextOracleWmsTypes.Core.Dict | list[FlextOracleWmsTypes.Core.Dict]
            ].ok(
                body,
            )

        except Exception as e:
            error_msg = f"Entity data extraction failed: {e}"
            self._logger.exception(error_msg)
            return FlextResult[
                FlextOracleWmsTypes.Core.Dict | list[FlextOracleWmsTypes.Core.Dict]
            ].fail(
                error_msg,
            )
