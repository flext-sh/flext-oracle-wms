"""Oracle WMS HTTP Client utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from flext_api import FlextApi, FlextApiSettings, u
from flext_oracle_wms import c, m, p, r, t

if TYPE_CHECKING:
    from types import TracebackType


class FlextOracleWmsUtilitiesHttpClient:
    """HTTP Client utilities for Oracle WMS -- u.OracleWms.HttpClient.*."""

    class HttpClient:
        """Generic HTTP client using FLEXT delegation with railway-oriented programming."""

        logger = u.fetch_logger(__name__)

        def __init__(
            self,
            base_url: str,
            timeout: float = 30.0,
            headers: t.StrMapping | None = None,
            *,
            verify_ssl: bool = True,
        ) -> None:
            """Initialize Oracle WMS HTTP client with FLEXT patterns."""
            self.base_url: str = base_url.rstrip("/")
            self.timeout: float = timeout
            self.default_headers = self._normalize_headers(dict(headers or {}))
            self.verify_ssl: bool = verify_ssl
            self._client: FlextApi | None = None

        def __enter__(self) -> Self:
            """Context manager entry."""
            self._ensure_client()
            return self

        def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
        ) -> None:
            """Context manager exit."""
            self.close()

        @staticmethod
        def _normalize_headers(
            headers: t.StrMapping | t.Api.WebHeaders | None,
        ) -> t.StrMapping:
            if headers is None:
                return {}
            normalized: t.MutableStrMapping = {}
            for key, value in headers.items():
                str_value: str
                match value:
                    case str() as s:
                        str_value = s
                    case list() as list_value:
                        str_value = ",".join(item for item in list_value)
                    case _:
                        str_value = str(value)
                normalized[key] = str_value
            return normalized

        @staticmethod
        def _normalize_request_body(body: t.JsonMapping | None) -> t.JsonMapping:
            if body is None:
                empty_body: t.JsonMapping = {}
                return empty_body
            return body

        def close(self) -> None:
            """Close HTTP client with FLEXT cleanup."""
            if self._client is not None:
                close_fn = getattr(self._client, "close", None)
                if callable(close_fn):
                    _ = close_fn()
            self._client = None

        def delete(
            self, path: str, headers: t.StrMapping | None = None
        ) -> p.Result[t.JsonMapping]:
            """Make DELETE request."""
            try:
                return self._execute_request_unchecked(
                    "DELETE", path, headers=headers, body={}
                )
            except c.EXC_VALIDATION_VALUE as exc:
                return r[t.JsonMapping].fail(f"Request validation error: {exc}")
            except OSError as exc:
                return r[t.JsonMapping].fail(f"Request I/O error: {exc}")

        def get(
            self,
            path: str,
            params: t.Api.WebParams | None = None,
            headers: t.StrMapping | None = None,
        ) -> p.Result[t.JsonMapping]:
            """Make GET request with railway-oriented error handling."""
            params_str: t.Api.WebParams | None = params
            return self._execute_request(
                "GET", path, params=params_str, headers=headers
            )

        def post(
            self,
            path: str,
            data: t.JsonMapping | None = None,
            json_data: t.JsonMapping | None = None,
            headers: t.StrMapping | None = None,
        ) -> p.Result[t.JsonMapping]:
            """Make POST request with railway-oriented error handling."""
            body = json_data or data
            return self._execute_request("POST", path, headers=headers, body=body)

        def put(
            self,
            path: str,
            data: t.JsonMapping | None = None,
            json_data: t.JsonMapping | None = None,
            headers: t.StrMapping | None = None,
        ) -> p.Result[t.JsonMapping]:
            """Make PUT request."""
            try:
                return self._execute_request_unchecked(
                    "PUT", path, headers=headers, body=json_data or data
                )
            except c.EXC_VALIDATION_VALUE as exc:
                return r[t.JsonMapping].fail(f"PUT validation error: {exc}")
            except OSError as exc:
                return r[t.JsonMapping].fail(f"PUT I/O error: {exc}")

        def _ensure_client(self) -> None:
            """Ensure Oracle WMS HTTP client is initialized using FLEXT delegation."""
            if self._client is None:
                settings = FlextApiSettings.model_validate({
                    "base_url": self.base_url,
                    "timeout": self.timeout,
                    "headers": dict(self.default_headers),
                    "max_retries": 0,
                    "verify_ssl": self.verify_ssl,
                    "default_headers": dict(self.default_headers),
                    "log_requests": False,
                    "log_responses": False,
                })
                self._client = FlextApi(runtime_settings=settings)

        def _execute_request(
            self,
            method: str,
            path: str,
            params: t.Api.WebParams | None = None,
            headers: t.StrMapping | None = None,
            body: t.JsonMapping | None = None,
        ) -> p.Result[t.JsonMapping]:
            """Execute HTTP request with FLEXT delegation."""
            try:
                return self._execute_request_unchecked(
                    method, path, params=params, headers=headers, body=body
                )
            except c.EXC_VALIDATION_VALUE as exc:
                return r[t.JsonMapping].fail(f"Request validation error: {exc}")
            except OSError as exc:
                return r[t.JsonMapping].fail(f"Request I/O error: {exc}")

        def _execute_request_unchecked(
            self,
            method: str,
            path: str,
            params: t.Api.WebParams | None = None,
            headers: t.StrMapping | None = None,
            body: t.JsonMapping | None = None,
        ) -> p.Result[t.JsonMapping]:
            """Execute a request while allowing validation and I/O exceptions upward."""
            response_result = self._request_response_unchecked(
                method, path, params=params, headers=headers, body=body
            )
            if response_result.failure:
                return r[t.JsonMapping].fail(
                    f"HTTP {method} failed: {response_result.error}"
                )
            response = response_result.value
            if response.status_code >= c.OracleWms.HTTP_BAD_REQUEST_THRESHOLD:
                return r[t.JsonMapping].fail(
                    f"HTTP {response.status_code}: {response.body!r}"
                )
            return self._parse_response_body(response.body)

        def _request_response_unchecked(
            self,
            method: str,
            path: str,
            params: t.Api.WebParams | None = None,
            headers: t.StrMapping | None = None,
            body: t.JsonMapping | None = None,
        ) -> p.Result[p.Api.HttpResponse]:
            """Build and dispatch one FLEXT API request."""
            self._ensure_client()
            if self._client is None:
                return r[p.Api.HttpResponse].fail("Client not initialized")
            request_headers: t.MutableStrMapping = dict(self.default_headers)
            request_headers.update(self._normalize_headers(headers))
            url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url
            if params:
                query = "&".join((f"{k}={v}" for k, v in params.items()))
                url = f"{url}?{query}"
            request = m.Api.HttpRequest.model_validate({
                "method": method,
                "url": url,
                "headers": request_headers,
                "body": self._normalize_request_body(body),
                "query_params": params or {},
                "timeout": self.timeout,
            })
            return self._client.request(request)

        def _parse_response_body(
            self, body: t.Api.ResponseBody
        ) -> p.Result[t.JsonMapping]:
            """Parse response body; propagates parse failure via result."""
            if not isinstance(body, (dict, str, bytes)) or (
                isinstance(body, str) and not body
            ):
                return r[t.JsonMapping].fail(
                    f"Unsupported response body type: {type(body)}"
                )
            try:
                return r[t.JsonMapping].ok(self._parse_response_body_unchecked(body))
            except c.EXC_VALIDATION_VALUE as exc:
                return r[t.JsonMapping].fail(f"Response parse error: {exc}")

        @staticmethod
        def _parse_response_body_unchecked(body: t.Api.ResponseBody) -> t.JsonMapping:
            """Parse a supported response body into a JSON mapping."""
            match body:
                case dict() as payload:
                    return t.json_mapping_adapter().validate_python(payload)
                case str() as raw if raw:
                    return t.json_mapping_adapter().validate_json(raw)
                case bytes() as raw_bytes:
                    return t.json_mapping_adapter().validate_json(raw_bytes)
                case _:
                    msg = f"Unsupported response body type: {type(body)}"
                    raise TypeError(msg)

        @staticmethod
        def create(
            base_url: str,
            timeout: float = 30.0,
            headers: t.StrMapping | None = None,
            *,
            verify_ssl: bool = True,
        ) -> FlextOracleWmsUtilitiesHttpClient.HttpClient:
            """Create HttpClient instance."""
            return FlextOracleWmsUtilitiesHttpClient.HttpClient(
                base_url=base_url,
                timeout=timeout,
                headers=headers,
                verify_ssl=verify_ssl,
            )


__all__: list[str] = ["FlextOracleWmsUtilitiesHttpClient"]
