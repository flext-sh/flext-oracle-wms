"""FLEXT Oracle WMS Client module.

Provides the main FlextOracleWmsClient class following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated

from flext_api import (
    FlextApiClient,
    FlextApiConstants,
    FlextApiModels,
    FlextApiSettings,
    FlextApiTypes,
)
from flext_core import FlextContainer, FlextExceptions, r, t, u
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from flext_oracle_wms.settings import FlextOracleWmsSettings

HTTP_BAD_REQUEST_THRESHOLD = 400


class EntitiesResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    entities: Annotated[list[str], Field(default_factory=list)]


class ApiCategoryResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    apis: Annotated[list[dict[str, str]], Field(default_factory=list)]


class EntityDataResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    data: Annotated[list[dict[str, str]], Field(default_factory=list)]


class FlextOracleWmsClient:
    """Oracle WMS client with strict request/response typing."""

    def __init__(self, config: FlextOracleWmsSettings | None = None) -> None:
        """Initialize client with strict settings resolution."""
        resolved_config = config
        if resolved_config is None:
            try:
                container = FlextContainer.get_global()
                config_result = container.get("FlextOracleWmsSettings")
                if config_result.is_success:
                    resolved_config = FlextOracleWmsSettings.model_validate(
                        config_result.value
                    )
            except (ValueError, FlextExceptions.BaseError):
                pass
        if resolved_config is None:
            resolved_config = FlextOracleWmsSettings.testing_config()
        self.config: FlextOracleWmsSettings = resolved_config
        api_config = FlextApiSettings.model_validate({
            "base_url": self.config.base_url,
            "timeout": int(self.config.timeout),
        })
        self._client: FlextApiClient = FlextApiClient(config=api_config)
        self._discovered_entities: list[str] = []

    @staticmethod
    def _decode_response_model[T: BaseModel](
        payload: FlextApiTypes.Api.ResponseBody | t.ContainerValue,
        model_type: type[T],
    ) -> r[T]:
        if isinstance(payload, dict):
            return u.try_(
                lambda: model_type.model_validate(payload),
                catch=ValidationError,
            ).map_error(lambda exc: f"Invalid response payload: {exc}")
        if isinstance(payload, str):
            return u.try_(
                lambda: model_type.model_validate_json(payload),
                catch=ValidationError,
            ).map_error(lambda exc: f"Invalid JSON payload: {exc}")
        if isinstance(payload, bytes):
            return u.try_(
                lambda: model_type.model_validate_json(payload),
                catch=ValidationError,
            ).map_error(lambda exc: f"Invalid JSON payload: {exc}")
        if payload is None:
            return r[T].fail("Empty response payload")
        return r[T].fail("Unsupported response type")

    def call_api(
        self,
        api_name: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: FlextApiTypes.Api.WebParams | None = None,
    ) -> r[FlextApiModels.HttpResponse]:
        """Call a specific Oracle WMS API."""
        return self.get(f"/api/{api_name}", headers=headers, params=params)

    def create_lpn(self, lpn_nbr: str, qty: int) -> r[FlextApiModels.HttpResponse]:
        """Create LPN (License Plate Number)."""
        payload: FlextApiTypes.Api.RequestBody = {"lpn_nbr": lpn_nbr, "qty": qty}
        return self.post("/lpn", body=payload)

    def delete(
        self, path: str, *, headers: Mapping[str, str] | None = None
    ) -> r[FlextApiModels.HttpResponse]:
        """Make DELETE request to Oracle WMS API."""
        return self._request(FlextApiConstants.Api.Method.DELETE, path, headers=headers)

    def discover_entities(self) -> r[list[str]]:
        """Discover available Oracle WMS entities."""
        result = self.get("/entities")
        if result.is_failure:
            return r[list[str]].fail(result.error)
        payload_result = self._decode_response_model(
            result.value.body, EntitiesResponse
        )
        if payload_result.is_failure:
            return r[list[str]].fail(payload_result.error)
        self._discovered_entities = payload_result.value.entities
        return r[list[str]].ok(payload_result.value.entities)

    def get(
        self,
        path: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: FlextApiTypes.Api.WebParams | None = None,
    ) -> r[FlextApiModels.HttpResponse]:
        """Make GET request to Oracle WMS API."""
        return self._request(
            FlextApiConstants.Api.Method.GET, path, headers=headers, params=params
        )

    def get_apis_by_category(self, category: str) -> r[list[dict[str, str]]]:
        """Get Oracle WMS APIs by category."""
        result = self.get(f"/apis/category/{category}")
        if result.is_failure:
            return r[list[dict[str, str]]].fail(result.error)
        payload_result = self._decode_response_model(
            result.value.body, ApiCategoryResponse
        )
        if payload_result.is_failure:
            return r[list[dict[str, str]]].fail(payload_result.error)
        return r[list[dict[str, str]]].ok(payload_result.value.apis)

    def get_entity_data(
        self,
        entity_name: str,
        limit: int | None = None,
        filters: Mapping[str, t.Scalar] | None = None,
    ) -> r[list[dict[str, str]]]:
        """Get data for a specific Oracle WMS entity."""
        params: FlextApiTypes.Api.WebParams = {}
        if limit is not None:
            params["limit"] = str(limit)
        if filters:
            params |= {key: str(value) for key, value in filters.items()}
        result = self.get(f"/entities/{entity_name}", params=params)
        if result.is_failure:
            return r[list[dict[str, str]]].fail(result.error)
        payload_result = self._decode_response_model(
            result.value.body, EntityDataResponse
        )
        if payload_result.is_failure:
            return r[list[dict[str, str]]].fail(payload_result.error)
        return r[list[dict[str, str]]].ok(payload_result.value.data)

    def health_check(self) -> r[FlextApiModels.HttpResponse]:
        """Check Oracle WMS API health."""
        return self.get("/health")

    def post(
        self,
        path: str,
        *,
        headers: Mapping[str, str] | None = None,
        body: FlextApiTypes.Api.RequestBody | None = None,
    ) -> r[FlextApiModels.HttpResponse]:
        """Make POST request to Oracle WMS API."""
        return self._request(
            FlextApiConstants.Api.Method.POST, path, headers=headers, body=body
        )

    def put(
        self,
        path: str,
        *,
        headers: Mapping[str, str] | None = None,
        body: FlextApiTypes.Api.RequestBody | None = None,
    ) -> r[FlextApiModels.HttpResponse]:
        """Make PUT request to Oracle WMS API."""
        return self._request(
            FlextApiConstants.Api.Method.PUT, path, headers=headers, body=body
        )

    def start(self) -> r[bool]:
        """Start the Oracle WMS client."""
        return r[bool].ok(True)

    def stop(self) -> r[bool]:
        """Stop the Oracle WMS client."""
        return r[bool].ok(True)

    def update_oblpn_tracking_number(
        self, oblpn_id: str, tracking_number: str
    ) -> r[FlextApiModels.HttpResponse]:
        """Update OBLPN tracking number."""
        payload: FlextApiTypes.Api.RequestBody = {"tracking_number": tracking_number}
        return self.put(f"/oblpn/{oblpn_id}/tracking", body=payload)

    def _request(
        self,
        method: str,
        path: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: FlextApiTypes.Api.WebParams | None = None,
        body: FlextApiTypes.Api.RequestBody | None = None,
    ) -> r[FlextApiModels.HttpResponse]:
        request = FlextApiModels.HttpRequest(
            method=method,
            url=path,
            timeout=self.config.timeout,
            headers=dict(headers) if headers is not None else {},
            query_params=params or {},
            body=body or {},
        )
        result = self._client.request(request)
        if result.is_failure:
            return r[FlextApiModels.HttpResponse].fail(
                f"{method} {path} failed: {result.error}"
            )
        response = result.value
        if response.status_code >= HTTP_BAD_REQUEST_THRESHOLD:
            return r[FlextApiModels.HttpResponse].fail(
                f"{method} {path} returned HTTP {response.status_code}"
            )
        return r[FlextApiModels.HttpResponse].ok(response)


__all__ = ["FlextOracleWmsClient"]
