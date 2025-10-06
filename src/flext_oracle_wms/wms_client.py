"""FLEXT Oracle WMS Client module.

Provides the main FlextOracleWmsClient class following FLEXT standards with proper inheritance levels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_api import FlextApiClient
from flext_core import FlextResult, FlextTypes

from flext_oracle_wms.config import FlextOracleWmsConfig


class FlextOracleWmsClient:
    """Minimal Oracle WMS client using flext-api for HTTP operations.

    Provides basic Oracle WMS API access with FlextResult error handling.
    """

    def __init__(self, config: FlextOracleWmsConfig | None = None) -> None:
        """Initialize Oracle WMS client.

        Args:
            config: Oracle WMS configuration. Uses default if None.

        """
        self.config = config or FlextOracleWmsConfig()

        # Use unified config fields
        base_url = self.config.base_url
        timeout = self.config.timeout

        self._client = FlextApiClient(
            base_url=base_url,
            timeout=timeout,
        )

    def get(self, path: str, **kwargs: object) -> FlextResult[FlextTypes.Dict]:
        """Make GET request to Oracle WMS API.

        Args:
            path: API endpoint path
            **kwargs: Additional request parameters

        Returns:
            FlextResult containing response data

        """
        try:
            result = self._client.get(path, **kwargs)
            return FlextResult.ok(result)
        except Exception as e:
            return FlextResult.fail(f"GET {path} failed: {e}")

    def post(self, path: str, **kwargs: object) -> FlextResult[FlextTypes.Dict]:
        """Make POST request to Oracle WMS API.

        Args:
            path: API endpoint path
            **kwargs: Additional request parameters

        Returns:
            FlextResult containing response data

        """
        try:
            result = self._client.post(path, **kwargs)
            return FlextResult.ok(result)
        except Exception as e:
            return FlextResult.fail(f"POST {path} failed: {e}")

    def put(self, path: str, **kwargs: object) -> FlextResult[FlextTypes.Dict]:
        """Make PUT request to Oracle WMS API.

        Args:
            path: API endpoint path
            **kwargs: Additional request parameters

        Returns:
            FlextResult containing response data

        """
        try:
            result = self._client.put(path, **kwargs)
            return FlextResult.ok(result)
        except Exception as e:
            return FlextResult.fail(f"PUT {path} failed: {e}")

    def delete(self, path: str, **kwargs: object) -> FlextResult[FlextTypes.Dict]:
        """Make DELETE request to Oracle WMS API.

        Args:
            path: API endpoint path
            **kwargs: Additional request parameters

        Returns:
            FlextResult containing response data

        """
        try:
            result = self._client.delete(path, **kwargs)
            return FlextResult.ok(result)
        except Exception as e:
            return FlextResult.fail(f"DELETE {path} failed: {e}")

    def health_check(self) -> FlextResult[FlextTypes.Dict]:
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

    def discover_entities(self) -> FlextResult[list[FlextTypes.Dict]]:
        """Discover available Oracle WMS entities.

        Returns:
            FlextResult containing list of entities

        """
        try:
            result = self.get("/entities")
            if result.success:
                entities = result.value.get("entities", [])
                return FlextResult.ok(entities)
            return result
        except Exception as e:
            return FlextResult.fail(f"Entity discovery failed: {e}")

    def get_entity_data(
        self,
        entity_name: str,
        limit: int | None = None,
        filters: dict[str, object] | None = None,
    ) -> FlextResult[list[FlextTypes.Dict]]:
        """Get data for a specific Oracle WMS entity.

        Args:
            entity_name: Name of the entity
            limit: Maximum number of records to return
            filters: Optional filters to apply

        Returns:
            FlextResult containing entity data

        """
        try:
            params = {}
            if limit:
                params["limit"] = limit
            if filters:
                params.update(filters)

            result = self.get(f"/entities/{entity_name}", **params)
            if result.success:
                data = result.value.get("data", [])
                return FlextResult.ok(data)
            return result
        except Exception as e:
            return FlextResult.fail(f"Failed to get entity data for {entity_name}: {e}")

    def get_apis_by_category(self, category: str) -> FlextResult[list[FlextTypes.Dict]]:
        """Get Oracle WMS APIs by category.

        Args:
            category: API category name

        Returns:
            FlextResult containing APIs in the category

        """
        try:
            result = self.get(f"/apis/category/{category}")
            if result.success:
                apis = result.value.get("apis", [])
                return FlextResult.ok(apis)
            return result
        except Exception as e:
            return FlextResult.fail(f"Failed to get APIs for category {category}: {e}")

    def call_api(self, api_name: str, **kwargs: object) -> FlextResult[FlextTypes.Dict]:
        """Call a specific Oracle WMS API.

        Args:
            api_name: Name of the API to call
            **kwargs: Additional parameters

        Returns:
            FlextResult containing API response

        """
        try:
            return self.get(f"/api/{api_name}", **kwargs)
        except Exception as e:
            return FlextResult.fail(f"API call failed for {api_name}: {e}")

    def update_oblpn_tracking_number(
        self, oblpn_id: str, tracking_number: str
    ) -> FlextResult[FlextTypes.Dict]:
        """Update OBLPN tracking number.

        Args:
            oblpn_id: OBLPN identifier
            tracking_number: New tracking number

        Returns:
            FlextResult containing update response

        """
        try:
            return self.put(
                f"/oblpn/{oblpn_id}/tracking", json={"tracking_number": tracking_number}
            )
        except Exception as e:
            return FlextResult.fail(f"Failed to update OBLPN tracking: {e}")

    def create_lpn(self, lpn_nbr: str, qty: int) -> FlextResult[FlextTypes.Dict]:
        """Create LPN (License Plate Number).

        Args:
            lpn_nbr: LPN number
            qty: Quantity

        Returns:
            FlextResult containing LPN creation response

        """
        try:
            return self.post("/lpn", json={"lpn_nbr": lpn_nbr, "qty": qty})
        except Exception as e:
            return FlextResult.fail(f"Failed to create LPN: {e}")


__all__ = ["FlextOracleWmsClient"]
