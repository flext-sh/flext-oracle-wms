"""FLEXT Oracle WMS Client module.

Provides the main FlextOracleWmsClient class following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence

from flext_api import (
    FlextApiClient,
    FlextApiConstants,
    FlextApiModels,
    FlextApiSettings,
    FlextApiTypes,
)
from flext_core import FlextContainer, e, r
from pydantic import BaseModel, ValidationError

from flext_oracle_wms.models import FlextOracleWmsModels as m
from flext_oracle_wms.settings import FlextOracleWmsSettings
from flext_oracle_wms.typings import FlextOracleWmsTypes as t
from flext_oracle_wms.utilities import FlextOracleWmsUtilities as u

HTTP_BAD_REQUEST_THRESHOLD = 400


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
                        config_result.value,
                    )
            except (ValueError, e.BaseError):
                pass
        if resolved_config is None:
            resolved_config = FlextOracleWmsSettings.testing_config()
        self.config: FlextOracleWmsSettings = resolved_config
        api_config = FlextApiSettings.model_validate({
            "base_url": self.config.base_url,
            "timeout": int(self.config.timeout),
        })
        self._client: FlextApiClient = FlextApiClient(config=api_config)
        self._discovered_entities: t.StrSequence = []

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
        headers: t.StrMapping | None = None,
        params: FlextApiTypes.Api.WebParams | None = None,
    ) -> r[FlextApiModels.Api.HttpResponse]:
        """Call a specific Oracle WMS API."""
        return self.get(f"/api/{api_name}", headers=headers, params=params)

    def create_lpn(self, lpn_nbr: str, qty: int) -> r[FlextApiModels.Api.HttpResponse]:
        """Create LPN (License Plate Number)."""
        payload: FlextApiTypes.Api.RequestBody = {"lpn_nbr": lpn_nbr, "qty": qty}
        return self.post("/lpn", body=payload)

    def delete(
        self,
        path: str,
        *,
        headers: t.StrMapping | None = None,
    ) -> r[FlextApiModels.Api.HttpResponse]:
        """Make DELETE request to Oracle WMS API."""
        return self._request(FlextApiConstants.Api.Method.DELETE, path, headers=headers)

    def discover_entities(self) -> r[t.StrSequence]:
        """Discover available Oracle WMS entities."""
        result = self.get("/entities")
        if result.is_failure:
            return r[t.StrSequence].fail(result.error)
        payload_result = self._decode_response_model(
            result.value.body,
            m.OracleWms.EntitiesResponse,
        )
        if payload_result.is_failure:
            return r[t.StrSequence].fail(payload_result.error)
        self._discovered_entities = payload_result.value.entities
        return r[t.StrSequence].ok(payload_result.value.entities)

    def get(
        self,
        path: str,
        *,
        headers: t.StrMapping | None = None,
        params: FlextApiTypes.Api.WebParams | None = None,
    ) -> r[FlextApiModels.Api.HttpResponse]:
        """Make GET request to Oracle WMS API."""
        return self._request(
            FlextApiConstants.Api.Method.GET,
            path,
            headers=headers,
            params=params,
        )

    def get_apis_by_category(self, category: str) -> r[Sequence[t.StrMapping]]:
        """Get Oracle WMS APIs by category."""
        result = self.get(f"/apis/category/{category}")
        if result.is_failure:
            return r[Sequence[t.StrMapping]].fail(result.error)
        payload_result = self._decode_response_model(
            result.value.body,
            m.OracleWms.ApiCategoryResponse,
        )
        if payload_result.is_failure:
            return r[Sequence[t.StrMapping]].fail(payload_result.error)
        return r[Sequence[t.StrMapping]].ok(payload_result.value.apis)

    def get_entity_data(
        self,
        entity_name: str,
        limit: int | None = None,
        filters: t.ConfigurationMapping | None = None,
    ) -> r[Sequence[t.StrMapping]]:
        """Get data for a specific Oracle WMS entity."""
        params_dict: dict[str, str] = {}
        if limit is not None:
            params_dict["limit"] = str(limit)
        if filters:
            params_dict |= {key: str(value) for key, value in filters.items()}
        params: FlextApiTypes.Api.WebParams = params_dict
        result = self.get(f"/entities/{entity_name}", params=params)
        if result.is_failure:
            return r[Sequence[t.StrMapping]].fail(result.error)
        payload_result = self._decode_response_model(
            result.value.body,
            m.OracleWms.EntityDataResponse,
        )
        if payload_result.is_failure:
            return r[Sequence[t.StrMapping]].fail(payload_result.error)
        return r[Sequence[t.StrMapping]].ok(payload_result.value.data)

    def health_check(self) -> r[FlextApiModels.Api.HttpResponse]:
        """Check Oracle WMS API health."""
        return self.get("/health")

    def post(
        self,
        path: str,
        *,
        headers: t.StrMapping | None = None,
        body: FlextApiTypes.Api.RequestBody | None = None,
    ) -> r[FlextApiModels.Api.HttpResponse]:
        """Make POST request to Oracle WMS API."""
        return self._request(
            FlextApiConstants.Api.Method.POST,
            path,
            headers=headers,
            body=body,
        )

    def put(
        self,
        path: str,
        *,
        headers: t.StrMapping | None = None,
        body: FlextApiTypes.Api.RequestBody | None = None,
    ) -> r[FlextApiModels.Api.HttpResponse]:
        """Make PUT request to Oracle WMS API."""
        return self._request(
            FlextApiConstants.Api.Method.PUT,
            path,
            headers=headers,
            body=body,
        )

    def start(self) -> r[bool]:
        """Start the Oracle WMS client."""
        return r[bool].ok(True)

    def stop(self) -> r[bool]:
        """Stop the Oracle WMS client."""
        return r[bool].ok(True)

    def update_oblpn_tracking_number(
        self,
        oblpn_id: str,
        tracking_number: str,
    ) -> r[FlextApiModels.Api.HttpResponse]:
        """Update OBLPN tracking number."""
        payload: FlextApiTypes.Api.RequestBody = {"tracking_number": tracking_number}
        return self.put(f"/oblpn/{oblpn_id}/tracking", body=payload)

    def _request(
        self,
        method: str,
        path: str,
        *,
        headers: t.StrMapping | None = None,
        params: FlextApiTypes.Api.WebParams | None = None,
        body: FlextApiTypes.Api.RequestBody | None = None,
    ) -> r[FlextApiModels.Api.HttpResponse]:
        request = FlextApiModels.Api.HttpRequest(
            method=method,
            url=path,
            timeout=self.config.timeout,
            headers=dict(headers) if headers is not None else {},
            query_params=params or {},
            body=body or {},
        )
        result = self._client.request(request)
        if result.is_failure:
            return r[FlextApiModels.Api.HttpResponse].fail(
                f"{method} {path} failed: {result.error}",
            )
        response = result.value
        if response.status_code >= HTTP_BAD_REQUEST_THRESHOLD:
            return r[FlextApiModels.Api.HttpResponse].fail(
                f"{method} {path} returned HTTP {response.status_code}",
            )
        return r[FlextApiModels.Api.HttpResponse].ok(response)


__all__ = ["FlextOracleWmsClient"]
