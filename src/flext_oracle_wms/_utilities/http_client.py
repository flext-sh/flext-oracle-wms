"""Oracle WMS HTTP Client utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import TracebackType
from typing import Self

from flext_api import FlextApiSettings, u
from flext_api._utilities.client import FlextApiClient

from flext_oracle_wms import c, m, p, r, t


class FlextOracleWmsUtilitiesHttpClient:
    """HTTP Client utilities for Oracle WMS -- u.OracleWms.HttpClient.*."""

    class HttpClient:
        """Generic HTTP client using FLEXT delegation with railway-oriented programming."""

        HTTP_BAD_REQUEST_THRESHOLD = 400
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
            self._client: FlextApiClient | None = None

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
        def _normalize_request_body(
            body: t.JsonMapping | None,
        ) -> t.JsonMapping:
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
            self,
            path: str,
            headers: t.StrMapping | None = None,
        ) -> p.Result[t.JsonMapping]:
            """Make DELETE request."""
            try:
                self._ensure_client()
                if self._client is None:
                    return r[t.JsonMapping].fail("Client not initialized")
                request_headers: t.MutableStrMapping = dict(self.default_headers)
                request_headers.update(self._normalize_headers(headers))
                url = f"{self.base_url}/{path.lstrip('/')}"
                request = m.Api.HttpRequest.model_validate({
                    "method": "DELETE",
                    "url": url,
                    "headers": request_headers,
                    "body": {},
                    "query_params": {},
                    "timeout": self.timeout,
                })
                response_result = self._client.request(request)
                if response_result.failure:
                    return r[t.JsonMapping].fail_op(
                        "HTTP request", response_result.error
                    )
                response = response_result.value
                return self._parse_response_body(response.body)
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
                self._ensure_client()
                if self._client is None:
                    return r[t.JsonMapping].fail("Client not initialized")
                request_headers: t.MutableStrMapping = dict(self.default_headers)
                request_headers.update(self._normalize_headers(headers))
                request_body = json_data or data
                url = f"{self.base_url}/{path.lstrip('/')}"
                request = m.Api.HttpRequest.model_validate({
                    "method": "PUT",
                    "url": url,
                    "headers": request_headers,
                    "body": self._normalize_request_body(request_body),
                    "query_params": {},
                    "timeout": self.timeout,
                })
                response_result = self._client.request(request)
                if response_result.failure:
                    return r[t.JsonMapping].fail_op(
                        "HTTP request",
                        response_result.error,
                    )
                response = response_result.value
                if response.status_code >= self.HTTP_BAD_REQUEST_THRESHOLD:
                    return r[t.JsonMapping].fail(
                        f"HTTP {response.status_code}: {response.body!r}",
                    )
                return self._parse_response_body(response.body)
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
                self._client = FlextApiClient(settings=settings)

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
                self._ensure_client()
                if self._client is None:
                    return r[t.JsonMapping].fail("Client not initialized")
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
                response_result = self._client.request(request)
                if response_result.failure:
                    return r[t.JsonMapping].fail(
                        f"HTTP {method} failed: {response_result.error}",
                    )
                response = response_result.value
                if response.status_code >= self.HTTP_BAD_REQUEST_THRESHOLD:
                    return r[t.JsonMapping].fail(
                        f"HTTP {response.status_code}: {response.body!r}",
                    )
                return self._parse_response_body(response.body)
            except c.EXC_VALIDATION_VALUE as exc:
                return r[t.JsonMapping].fail(f"Request validation error: {exc}")
            except OSError as exc:
                return r[t.JsonMapping].fail(f"Request I/O error: {exc}")

        def _parse_response_body(
            self,
            body: t.Api.ResponseBody,
        ) -> p.Result[t.JsonMapping]:
            """Parse response body; propagates parse failure via result."""
            try:
                match body:
                    case dict() as payload:
                        parsed = t.json_mapping_adapter().validate_python(
                            payload,
                        )
                    case str() as raw if raw:
                        parsed = t.json_mapping_adapter().validate_json(
                            raw,
                        )
                    case bytes() as raw_bytes:
                        parsed = t.json_mapping_adapter().validate_json(
                            raw_bytes,
                        )
                    case _:
                        return r[t.JsonMapping].fail(
                            f"Unsupported response body type: {type(body)}"
                        )
                return r[t.JsonMapping].ok(parsed)
            except c.EXC_VALIDATION_VALUE as exc:
                return r[t.JsonMapping].fail(f"Response parse error: {exc}")

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
