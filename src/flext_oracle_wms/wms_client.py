"""FLEXT Oracle WMS Client module.

Provides the main FlextOracleWmsClient class following FLEXT standards with proper inheritance levels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextContainer, FlextResult

from flext_oracle_wms.config import FlextOracleWmsConfig


class FlextOracleWmsClient:
    """Minimal Oracle WMS client using flext-api for HTTP operations.

    Provides basic Oracle WMS API access with FlextResult error handling.
    Uses singleton pattern for configuration management.
    """

    def __init__(self, config: FlextOracleWmsConfig | None = None) -> None:
        """Initialize Oracle WMS client.

        Args:
            config: Optional configuration. If None, retrieved from global container.

        """
        if config is None:
            container = FlextContainer.get_global()
            config_result = container.get("FlextOracleWmsConfig")
            config = config_result.unwrap_or(FlextOracleWmsConfig())

        self.config: FlextOracleWmsConfig = config

        self._client = FlextApiClient(
            base_url=self.config.base_url,
            timeout=int(self.config.timeout),
        )

        # Initialize discovered entities cache
        self._discovered_entities = []

    def get(self, path: str, **kwargs: object) -> FlextResult[dict[str, object]]:
        """Make GET request to Oracle WMS API.

        Args:
            path: API endpoint path
            **kwargs: Additional request parameters

        Returns:
            FlextResult containing response data

        """
        request = FlextApiModels.HttpRequest(
            method="GET",
            url=path,
            headers=kwargs.get("headers", {}),
            params=kwargs.get("params", {}),
        )
        result = self._client.request(request)
        if result.is_failure:
            return FlextResult.fail(f"GET {path} failed: {result.error}")
        response = result.unwrap()
        if hasattr(response, "body") and isinstance(response.body, dict):
            return FlextResult.ok(response.body)
        return FlextResult.ok(response if isinstance(response, dict) else {})

    def post(self, path: str, **kwargs: object) -> FlextResult[dict[str, object]]:
        """Make POST request to Oracle WMS API.

        Args:
            path: API endpoint path
            **kwargs: Additional request parameters

        Returns:
            FlextResult containing response data

        """
        request = FlextApiModels.HttpRequest(
            method="POST",
            url=path,
            headers=kwargs.get("headers", {}),
            body=kwargs.get("body"),
        )
        result = self._client.request(request)
        if result.is_failure:
            return FlextResult.fail(f"POST {path} failed: {result.error}")
        response = result.unwrap()
        if hasattr(response, "body") and isinstance(response.body, dict):
            return FlextResult.ok(response.body)
        return FlextResult.ok(response if isinstance(response, dict) else {})

    def put(self, path: str, **kwargs: object) -> FlextResult[dict[str, object]]:
        """Make PUT request to Oracle WMS API.

        Args:
            path: API endpoint path
            **kwargs: Additional request parameters

        Returns:
            FlextResult containing response data

        """
        request = FlextApiModels.HttpRequest(
            method="PUT",
            url=path,
            headers=kwargs.get("headers", {}),
            body=kwargs.get("body"),
        )
        result = self._client.request(request)
        if result.is_failure:
            return FlextResult.fail(f"PUT {path} failed: {result.error}")
        response = result.unwrap()
        if hasattr(response, "body") and isinstance(response.body, dict):
            return FlextResult.ok(response.body)
        return FlextResult.ok(response if isinstance(response, dict) else {})

    def delete(self, path: str, **kwargs: object) -> FlextResult[dict[str, object]]:
        """Make DELETE request to Oracle WMS API.

        Args:
            path: API endpoint path
            **kwargs: Additional request parameters

        Returns:
            FlextResult containing response data

        """
        request = FlextApiModels.HttpRequest(
            method="DELETE",
            url=path,
            headers=kwargs.get("headers", {}),
        )
        result = self._client.request(request)
        if result.is_failure:
            return FlextResult.fail(f"DELETE {path} failed: {result.error}")
        response = result.unwrap()
        if hasattr(response, "body") and isinstance(response.body, dict):
            return FlextResult.ok(response.body)
        return FlextResult.ok(response if isinstance(response, dict) else {})

    def health_check(self) -> FlextResult[dict[str, object]]:
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

    def discover_entities(self) -> FlextResult[list[object]]:
        """Discover available Oracle WMS entities.

        Returns:
            FlextResult containing list of entities

        """
        result = self.get("/entities")
        if result.is_failure:
            return FlextResult.fail(result.error)
        data = result.unwrap()
        entities = data.get("entities", []) if isinstance(data, dict) else []
        return FlextResult.ok(list(entities) if isinstance(entities, list) else [])

    def get_entity_data(
        self,
        entity_name: str,
        limit: int | None = None,
        filters: dict[str, object] | None = None,
    ) -> FlextResult[list[dict[str, object]]]:
        """Get data for a specific Oracle WMS entity.

        Args:
            entity_name: Name of the entity
            limit: Maximum number of records to return
            filters: Optional filters to apply

        Returns:
            FlextResult containing entity data

        """
        params: dict[str, object] = {}
        if limit:
            params["limit"] = limit
        if filters:
            params.update(filters)

        result = self.get(f"/entities/{entity_name}", **params)
        if result.is_failure:
            return FlextResult.fail(result.error)
        data = result.unwrap()
        entity_data = data.get("data", []) if isinstance(data, dict) else []
        return FlextResult.ok(
            list(entity_data) if isinstance(entity_data, list) else []
        )

    def get_apis_by_category(
        self, category: str
    ) -> FlextResult[list[dict[str, object]]]:
        """Get Oracle WMS APIs by category.

        Args:
            category: API category name

        Returns:
            FlextResult containing APIs in the category

        """
        result = self.get(f"/apis/category/{category}")
        if result.is_failure:
            return FlextResult.fail(result.error)
        data = result.unwrap()
        apis = data.get("apis", []) if isinstance(data, dict) else []
        return FlextResult.ok(list(apis) if isinstance(apis, list) else [])

    def call_api(
        self, api_name: str, **kwargs: object
    ) -> FlextResult[dict[str, object]]:
        """Call a specific Oracle WMS API.

        Args:
            api_name: Name of the API to call
            **kwargs: Additional parameters

        Returns:
            FlextResult containing API response

        """
        return self.get(f"/api/{api_name}", **kwargs)

    def update_oblpn_tracking_number(
        self, oblpn_id: str, tracking_number: str
    ) -> FlextResult[dict[str, object]]:
        """Update OBLPN tracking number.

        Args:
            oblpn_id: OBLPN identifier
            tracking_number: New tracking number

        Returns:
            FlextResult containing update response

        """
        return self.put(
            f"/oblpn/{oblpn_id}/tracking", body={"tracking_number": tracking_number}
        )

    def create_lpn(self, lpn_nbr: str, qty: int) -> FlextResult[dict[str, object]]:
        """Create LPN (License Plate Number).

        Args:
            lpn_nbr: LPN number
            qty: Quantity

        Returns:
            FlextResult containing LPN creation response

        """
        return self.post("/lpn", body={"lpn_nbr": lpn_nbr, "qty": qty})


__all__ = ["FlextOracleWmsClient"]
