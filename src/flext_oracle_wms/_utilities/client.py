"""Oracle WMS Client utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_api import FlextApi, FlextApiSettings, u

from flext_oracle_wms import FlextOracleWmsSettings, c, m, p, r, t
from flext_oracle_wms._utilities.auth import FlextOracleWmsUtilitiesAuth


class FlextOracleWmsUtilitiesClient:
    """Client utilities for Oracle WMS -- u.OracleWms.Client.*."""

    class Client:
        """Oracle WMS client with strict request/response typing."""

        HTTP_BAD_REQUEST_THRESHOLD = 400

        @classmethod
        def from_auth_settings(
            cls,
            auth_settings: m.OracleWms.AuthSettings,
        ) -> p.Result[FlextOracleWmsUtilitiesClient.Client]:
            """Create a concrete client by merging auth settings with runtime WMS settings."""
            validation_result = auth_settings.validate_business_rules()
            if validation_result.failure:
                return r[FlextOracleWmsUtilitiesClient.Client].fail(
                    validation_result.error or "Invalid Oracle WMS auth settings"
                )
            basic_method = str(c.OracleWms.OracleWMSAuthMethod.BASIC)
            if auth_settings.normalized_method != basic_method:
                return r[FlextOracleWmsUtilitiesClient.Client].fail(
                    "Oracle WMS runtime client currently supports BASIC auth only"
                )
            base_settings = FlextOracleWmsSettings.fetch_global()
            resolved_settings = FlextOracleWmsSettings.model_validate({
                "base_url": base_settings.base_url,
                "timeout": base_settings.timeout,
                "username": auth_settings.username or base_settings.username,
                "password": auth_settings.password or base_settings.password,
                "auth_method": auth_settings.normalized_method,
            })
            return r[FlextOracleWmsUtilitiesClient.Client].ok(cls(resolved_settings))

        def __init__(self, settings: FlextOracleWmsSettings | None = None) -> None:
            """Initialize client with strict settings resolution."""
            resolved_config = (
                settings
                if settings is not None
                else FlextOracleWmsSettings.fetch_global()
            )
            self.settings: FlextOracleWmsSettings = resolved_config
            default_headers = self._build_default_headers(self.settings)
            self._api_config = FlextApiSettings.model_validate({
                "base_url": self.settings.base_url,
                "timeout": int(self.settings.timeout),
                "headers": default_headers,
                "default_headers": default_headers,
            })
            self._client: FlextApi | None = self._create_api_client()
            self._discovered_entities: t.StrSequence = []
            self._started = False

        @staticmethod
        def _build_default_headers(settings: FlextOracleWmsSettings) -> t.StrMapping:
            """Build default request headers from Oracle WMS auth settings."""
            if not settings.username and not settings.password:
                return {}
            resolved_method = (
                str(
                    getattr(
                        settings,
                        "auth_method",
                        c.OracleWms.OracleWMSAuthMethod.BASIC,
                    )
                )
                .strip()
                .lower()
            )
            auth_settings = m.OracleWms.AuthSettings(
                method=resolved_method,
                username=settings.username or None,
                password=settings.password or None,
                oauth2_client_id=getattr(settings, "oauth2_client_id", None),
                oauth2_client_secret=getattr(settings, "oauth2_client_secret", None),
            )
            authenticator = FlextOracleWmsUtilitiesAuth.Authenticator(auth_settings)
            auth_headers = authenticator.get_auth_headers()
            if auth_headers.failure:
                error_message = auth_headers.error or "Invalid Oracle WMS credentials"
                raise ValueError(error_message)
            return auth_headers.value

        def _create_api_client(self) -> FlextApi:
            """Create a configured API client for Oracle WMS requests."""
            return FlextApi(settings=self._api_config)

        @staticmethod
        def _decode_response_model[T: m.BaseModel](
            payload: t.Api.ResponseBody | t.JsonValue,
            model_type: type[T],
        ) -> p.Result[T]:
            if isinstance(payload, dict):
                return u.try_(
                    lambda: model_type.model_validate(payload),
                    catch=c.ValidationError,
                ).map_error(lambda exc: f"Invalid response payload: {exc}")
            if isinstance(payload, str):
                return u.try_(
                    lambda: model_type.model_validate_json(payload),
                    catch=c.ValidationError,
                ).map_error(lambda exc: f"Invalid JSON payload: {exc}")
            if isinstance(payload, bytes):
                return u.try_(
                    lambda: model_type.model_validate_json(payload),
                    catch=c.ValidationError,
                ).map_error(lambda exc: f"Invalid JSON payload: {exc}")
            if payload is None:
                return r[T].fail("Empty response payload")
            return r[T].fail("Unsupported response type")

        def call_api(
            self,
            api_name: str,
            *,
            headers: t.StrMapping | None = None,
            params: t.Api.WebParams | None = None,
        ) -> p.Result[m.Api.HttpResponse]:
            """Call a specific Oracle WMS API."""
            return self.get(f"/api/{api_name}", headers=headers, params=params)

        def create_lpn(self, lpn_nbr: str, qty: int) -> p.Result[m.Api.HttpResponse]:
            """Create LPN (License Plate Number)."""
            payload: t.Api.RequestBody = {"lpn_nbr": lpn_nbr, "qty": qty}
            return self.post("/lpn", body=payload)

        def delete(
            self,
            path: str,
            *,
            headers: t.StrMapping | None = None,
        ) -> p.Result[m.Api.HttpResponse]:
            """Make DELETE request to Oracle WMS API."""
            return self._request(c.Api.Method.DELETE, path, headers=headers)

        def discover_entities(self) -> p.Result[t.StrSequence]:
            """Discover available Oracle WMS entities."""
            result = self.get("/entities")
            if result.failure:
                return r[t.StrSequence].fail(result.error)
            payload_result = self._decode_response_model(
                result.value.body,
                m.OracleWms.EntitiesResponse,
            )
            if payload_result.failure:
                return r[t.StrSequence].fail(payload_result.error)
            self._discovered_entities = payload_result.value.entities
            return r[t.StrSequence].ok(payload_result.value.entities)

        def get(
            self,
            path: str,
            *,
            headers: t.StrMapping | None = None,
            params: t.Api.WebParams | None = None,
        ) -> p.Result[m.Api.HttpResponse]:
            """Make GET request to Oracle WMS API."""
            return self._request(
                c.Api.Method.GET,
                path,
                headers=headers,
                params=params,
            )

        def get_apis_by_category(
            self, category: str
        ) -> p.Result[t.SequenceOf[t.StrMapping]]:
            """Get Oracle WMS APIs by category."""
            result = self.get(f"/apis/category/{category}")
            if result.failure:
                return r[t.SequenceOf[t.StrMapping]].fail(result.error)
            payload_result = self._decode_response_model(
                result.value.body,
                m.OracleWms.ApiCategoryResponse,
            )
            if payload_result.failure:
                return r[t.SequenceOf[t.StrMapping]].fail(payload_result.error)
            return r[t.SequenceOf[t.StrMapping]].ok(payload_result.value.apis)

        def get_entity_data(
            self,
            entity_name: str,
            limit: int | None = None,
            filters: t.ConfigurationMapping | None = None,
        ) -> p.Result[t.SequenceOf[t.StrMapping]]:
            """Get data for a specific Oracle WMS entity."""
            params_dict: dict[str, str] = {}
            if limit is not None:
                params_dict["limit"] = str(limit)
            if filters:
                params_dict |= {key: str(value) for key, value in filters.items()}
            params: t.Api.WebParams = params_dict
            result = self.get(f"/entities/{entity_name}", params=params)
            if result.failure:
                return r[t.SequenceOf[t.StrMapping]].fail(result.error)
            payload_result = self._decode_response_model(
                result.value.body,
                m.OracleWms.EntityDataResponse,
            )
            if payload_result.failure:
                return r[t.SequenceOf[t.StrMapping]].fail(payload_result.error)
            return r[t.SequenceOf[t.StrMapping]].ok(payload_result.value.data)

        def health_check(self) -> p.Result[m.Api.HttpResponse]:
            """Check Oracle WMS API health."""
            return self.get("/health")

        def post(
            self,
            path: str,
            *,
            headers: t.StrMapping | None = None,
            body: t.Api.RequestBody | None = None,
        ) -> p.Result[m.Api.HttpResponse]:
            """Make POST request to Oracle WMS API."""
            return self._request(
                c.Api.Method.POST,
                path,
                headers=headers,
                body=body,
            )

        def put(
            self,
            path: str,
            *,
            headers: t.StrMapping | None = None,
            body: t.Api.RequestBody | None = None,
        ) -> p.Result[m.Api.HttpResponse]:
            """Make PUT request to Oracle WMS API."""
            return self._request(
                c.Api.Method.PUT,
                path,
                headers=headers,
                body=body,
            )

        def start(self) -> p.Result[bool]:
            """Start the Oracle WMS client after validating runtime settings."""
            if self._client is None:
                self._client = self._create_api_client()
            self._started = True
            return r[bool].ok(True)

        def stop(self) -> p.Result[bool]:
            """Stop the Oracle WMS client and release the delegated API client."""
            if self._client is not None:
                close_fn = getattr(self._client, "close", None)
                if callable(close_fn):
                    _ = close_fn()
                self._client = None
            self._started = False
            return r[bool].ok(True)

        def update_oblpn_tracking_number(
            self,
            oblpn_id: str,
            tracking_number: str,
        ) -> p.Result[m.Api.HttpResponse]:
            """Update OBLPN tracking number."""
            payload: t.Api.RequestBody = {"tracking_number": tracking_number}
            return self.put(f"/oblpn/{oblpn_id}/tracking", body=payload)

        def _request(
            self,
            method: str,
            path: str,
            *,
            headers: t.StrMapping | None = None,
            params: t.Api.WebParams | None = None,
            body: t.Api.RequestBody | None = None,
        ) -> p.Result[m.Api.HttpResponse]:
            if self._client is None:
                self._client = self._create_api_client()
            request_headers: t.MutableStrMapping = {}
            if headers is not None:
                request_headers.update(headers)
            request = m.Api.HttpRequest.model_validate({
                "method": method,
                "url": path,
                "timeout": self.settings.timeout,
                "headers": request_headers,
                "query_params": params or {},
                "body": body or {},
            })
            result = self._client.request(request)
            if result.failure:
                return r[m.Api.HttpResponse].fail(
                    f"{method} {path} failed: {result.error}",
                )
            response = result.value
            if response.status_code >= self.HTTP_BAD_REQUEST_THRESHOLD:
                return r[m.Api.HttpResponse].fail(
                    f"{method} {path} returned HTTP {response.status_code}",
                )
            return r[m.Api.HttpResponse].ok(response)


__all__: list[str] = ["FlextOracleWmsUtilitiesClient"]
