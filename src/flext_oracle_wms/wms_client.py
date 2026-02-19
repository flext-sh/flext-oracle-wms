"""FLEXT Oracle WMS Client module.

Provides the main FlextOracleWmsClient class following FLEXT standards with proper inheritance levels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import cast

from flext_api import (
    FlextApiClient,
    FlextApiConstants,
    FlextApiModels,
    FlextApiSettings,
    FlextApiTypes,
)
from flext_core import FlextContainer, FlextResult, FlextTypes as t

from flext_oracle_wms.settings import FlextOracleWmsSettings


class FlextOracleWmsClient:
    """Minimal Oracle WMS client using flext-api for HTTP operations.

    Provides basic Oracle WMS API access with FlextResult error handling.
    Uses singleton pattern for configuration management.
    """

    def __init__(self, config: FlextOracleWmsSettings | None = None) -> None:
        """Initialize Oracle WMS client.

        Args:
        config: Optional configuration. If None, retrieved from global container.

        """
        if config is None:
            container = FlextContainer.get_global()
            config_result = container.get("FlextOracleWmsSettings")
            config_value = config_result.unwrap_or(FlextOracleWmsSettings())
            # Type narrowing - config should be FlextOracleWmsSettings
            if isinstance(config_value, FlextOracleWmsSettings):
                config = config_value
            else:
                config = FlextOracleWmsSettings()

        self.config: FlextOracleWmsSettings = config

        api_config = FlextApiSettings(
            base_url=self.config.base_url,
            timeout=int(self.config.timeout),
        )
        self._client = FlextApiClient(config=api_config)

        # Initialize discovered entities cache
        self._discovered_entities = []

    def get(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Make GET request to Oracle WMS API.

        Args:
        path: API endpoint path
        headers: Optional request headers
        params: Optional query parameters

        Returns:
        FlextResult containing response data

        """
        request = FlextApiModels.HttpRequest(
            method=FlextApiConstants.Api.Method.GET,
            url=path,
            headers=headers or {},
            query_params=params or {},
        )
        result = self._client.request(request)
        if result.is_failure:
            return FlextResult.fail(f"GET {path} failed: {result.error}")
        response = result.value
        if hasattr(response, "body") and isinstance(response.body, dict):
            return FlextResult.ok(cast("dict[str, t.GeneralValueType]", response.body))
        return FlextResult.ok(
            cast(
                "dict[str, t.GeneralValueType]",
                response if isinstance(response, dict) else {},
            )
        )

    def post(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        body: FlextApiTypes.Api.RequestBody | None = None,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Make POST request to Oracle WMS API.

        Args:
        path: API endpoint path
        headers: Optional request headers
        body: Optional request body

        Returns:
        FlextResult containing response data

        """
        request = FlextApiModels.HttpRequest(
            method=FlextApiConstants.Api.Method.POST,
            url=path,
            headers=headers or {},
            body=cast(
                "FlextApiTypes.Api.RequestBody", body if body is not None else {}
            ),
        )
        result = self._client.request(request)
        if result.is_failure:
            return FlextResult.fail(f"POST {path} failed: {result.error}")
        response = result.value
        if hasattr(response, "body") and isinstance(response.body, dict):
            return FlextResult.ok(cast("dict[str, t.GeneralValueType]", response.body))
        return FlextResult.ok(
            cast(
                "dict[str, t.GeneralValueType]",
                response if isinstance(response, dict) else {},
            )
        )

    def put(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        body: FlextApiTypes.Api.RequestBody | None = None,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Make PUT request to Oracle WMS API.

        Args:
        path: API endpoint path
        headers: Optional request headers
        body: Optional request body

        Returns:
        FlextResult containing response data

        """
        request = FlextApiModels.HttpRequest(
            method=FlextApiConstants.Api.Method.PUT,
            url=path,
            headers=headers or {},
            body=cast(
                "FlextApiTypes.Api.RequestBody", body if body is not None else {}
            ),
        )
        result = self._client.request(request)
        if result.is_failure:
            return FlextResult.fail(f"PUT {path} failed: {result.error}")
        response = result.value
        if hasattr(response, "body") and isinstance(response.body, dict):
            return FlextResult.ok(cast("dict[str, t.GeneralValueType]", response.body))
        return FlextResult.ok(
            cast(
                "dict[str, t.GeneralValueType]",
                response if isinstance(response, dict) else {},
            )
        )

    def delete(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Make DELETE request to Oracle WMS API.

        Args:
        path: API endpoint path
        headers: Optional request headers

        Returns:
        FlextResult containing response data

        """
        request = FlextApiModels.HttpRequest(
            method=FlextApiConstants.Api.Method.DELETE,
            url=path,
            headers=headers or {},
        )
        result = self._client.request(request)
        if result.is_failure:
            return FlextResult.fail(f"DELETE {path} failed: {result.error}")
        response = result.value
        if hasattr(response, "body") and isinstance(response.body, dict):
            return FlextResult.ok(cast("dict[str, t.GeneralValueType]", response.body))
        return FlextResult.ok(
            cast(
                "dict[str, t.GeneralValueType]",
                response if isinstance(response, dict) else {},
            )
        )

    def health_check(self) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Check Oracle WMS API health.

        Returns:
        FlextResult containing health status

        """
        return self.get("/health")

    def start(self) -> FlextResult[bool]:
        """Start the Oracle WMS client.

        Returns:
        FlextResult indicating success

        """
        try:
            # Initialize client if needed
            return FlextResult.ok(True)
        except Exception as e:
            return FlextResult.fail(f"Failed to start client: {e}")

    def stop(self) -> FlextResult[bool]:
        """Stop the Oracle WMS client.

        Returns:
        FlextResult indicating success

        """
        try:
            # Cleanup client resources
            return FlextResult.ok(True)
        except Exception as e:
            return FlextResult.fail(f"Failed to stop client: {e}")

    def discover_entities(self) -> FlextResult[list[t.GeneralValueType]]:
        """Discover available Oracle WMS entities.

        Returns:
        FlextResult containing list of entities

        """
        result = self.get("/entities")
        if result.is_failure:
            return FlextResult.fail(result.error)
        data = result.value
        entities = data.get("entities", []) if isinstance(data, dict) else []
        return FlextResult.ok(list(entities) if isinstance(entities, list) else [])

    def get_entity_data(
        self,
        entity_name: str,
        limit: int | None = None,
        filters: dict[str, t.GeneralValueType] | None = None,
    ) -> FlextResult[list[dict[str, t.GeneralValueType]]]:
        """Get data for a specific Oracle WMS entity.

        Args:
        entity_name: Name of the entity
        limit: Maximum number of records to return
        filters: Optional filters to apply

        Returns:
        FlextResult containing entity data

        """
        params: dict[str, str] = {}
        if limit:
            params["limit"] = str(limit)
        if filters:
            params.update({k: str(v) for k, v in filters.items()})

        result = self.get(f"/entities/{entity_name}", params=params)
        if result.is_failure:
            return FlextResult.fail(result.error)
        data = result.value
        entity_data = data.get("data", []) if isinstance(data, dict) else []
        return FlextResult.ok(
            list(entity_data) if isinstance(entity_data, list) else [],
        )

    def get_apis_by_category(
        self,
        category: str,
    ) -> FlextResult[list[dict[str, t.GeneralValueType]]]:
        """Get Oracle WMS APIs by category.

        Args:
        category: API category name

        Returns:
        FlextResult containing APIs in the category

        """
        result = self.get(f"/apis/category/{category}")
        if result.is_failure:
            return FlextResult.fail(result.error)
        data = result.value
        apis = data.get("apis", []) if isinstance(data, dict) else []
        return FlextResult.ok(list(apis) if isinstance(apis, list) else [])

    def call_api(
        self,
        api_name: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Call a specific Oracle WMS API.

        Args:
        api_name: Name of the API to call
        headers: Optional request headers
        params: Optional query parameters

        Returns:
        FlextResult containing API response

        """
        return self.get(f"/api/{api_name}", headers=headers, params=params)

    def update_oblpn_tracking_number(
        self,
        oblpn_id: str,
        tracking_number: str,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Update OBLPN tracking number.

        Args:
        oblpn_id: OBLPN identifier
        tracking_number: New tracking number

        Returns:
        FlextResult containing update response

        """
        return self.put(
            f"/oblpn/{oblpn_id}/tracking",
            body={"tracking_number": tracking_number},
        )

    def create_lpn(
        self, lpn_nbr: str, qty: int
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Create LPN (License Plate Number).

        Args:
        lpn_nbr: LPN number
        qty: Quantity

        Returns:
        FlextResult containing LPN creation response

        """
        return self.post("/lpn", body={"lpn_nbr": lpn_nbr, "qty": qty})


__all__ = ["FlextOracleWmsClient"]
