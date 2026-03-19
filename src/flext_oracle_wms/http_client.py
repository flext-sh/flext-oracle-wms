"""FLEXT Generic HTTP Client - Railway-oriented with Pydantic.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping
from types import TracebackType
from typing import Self

from flext_api import FlextApiClient, FlextApiModels, FlextApiSettings, FlextApiTypes
from flext_core import FlextLogger, r
from pydantic import TypeAdapter, ValidationError

from flext_oracle_wms import t
from flext_oracle_wms.typings import HttpJsonObject

HTTP_BAD_REQUEST_THRESHOLD = 400


class FlextHttpClient:
    """Generic HTTP client using FLEXT delegation with railway-oriented programming."""

    logger = FlextLogger(__name__)

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        headers: Mapping[str, str] | None = None,
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
        headers: Mapping[str, str] | FlextApiTypes.Api.WebHeaders | None,
    ) -> Mapping[str, str]:
        if headers is None:
            return {}
        normalized: MutableMapping[str, str] = {}
        for key, value in headers.items():
            match value:
                case str() as str_value:
                    normalized[str(key)] = str_value
                case list() as list_value:
                    normalized[str(key)] = ",".join(str(item) for item in list_value)
                case _:
                    normalized[str(key)] = str(value)
        return normalized

    @staticmethod
    def _normalize_request_body(
        body: HttpJsonObject | None,
    ) -> HttpJsonObject:
        if body is None:
            return {}
        return body

    def close(self) -> None:
        """Close HTTP client with FLEXT cleanup."""
        if self._client is not None:
            close_fn = getattr(self._client, "close", None)
            if callable(close_fn):
                _ = close_fn()
        self._client = None

    def delete(
        self, path: str, headers: Mapping[str, str] | None = None
    ) -> r[HttpJsonObject]:
        """Make DELETE request."""
        try:
            self._ensure_client()
            if self._client is None:
                return r[HttpJsonObject].fail("Client not initialized")
            request_headers = dict(self.default_headers)
            request_headers.update(self._normalize_headers(headers))
            url = f"{self.base_url}/{path.lstrip('/')}"
            request = FlextApiModels.HttpRequest(
                method="DELETE",
                url=url,
                headers=request_headers,
                body={},
                query_params={},
                timeout=self.timeout,
            )
            response_result = self._client.request(request)
            if response_result.is_failure:
                return r[HttpJsonObject].fail(
                    f"HTTP request failed: {response_result.error}"
                )
            response = response_result.value
            return r[HttpJsonObject].ok(self._parse_response_body(response.body))
        except Exception as exc:
            FlextHttpClient.logger.exception(f"DELETE {path} error")
            return r[HttpJsonObject].fail(f"Request error: {exc}")

    def get(
        self,
        path: str,
        params: FlextApiTypes.Api.WebParams | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> r[HttpJsonObject]:
        """Make GET request with railway-oriented error handling."""
        params_str: FlextApiTypes.Api.WebParams | None = (
            {str(k): str(v) for k, v in params.items()} if params else None
        )
        return self._execute_request("GET", path, params=params_str, headers=headers)

    def post(
        self,
        path: str,
        data: HttpJsonObject | None = None,
        json_data: HttpJsonObject | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> r[HttpJsonObject]:
        """Make POST request with railway-oriented error handling."""
        body = json_data or data
        return self._execute_request("POST", path, headers=headers, body=body)

    def put(
        self,
        path: str,
        data: HttpJsonObject | None = None,
        json_data: HttpJsonObject | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> r[HttpJsonObject]:
        """Make PUT request."""
        try:
            self._ensure_client()
            if self._client is None:
                return r[HttpJsonObject].fail("Client not initialized")
            request_headers = dict(self.default_headers)
            request_headers.update(self._normalize_headers(headers))
            request_body = json_data or data
            url = f"{self.base_url}/{path.lstrip('/')}"
            request = FlextApiModels.HttpRequest(
                method="PUT",
                url=url,
                headers=request_headers,
                body=self._normalize_request_body(request_body),
                query_params={},
                timeout=self.timeout,
            )
            response_result = self._client.request(request)
            if response_result.is_failure:
                return r[HttpJsonObject].fail(
                    f"HTTP request failed: {response_result.error}"
                )
            response = response_result.value
            if response.status_code >= HTTP_BAD_REQUEST_THRESHOLD:
                return r[HttpJsonObject].fail(
                    f"HTTP {response.status_code}: {response.body!r}"
                )
            return r[HttpJsonObject].ok(self._parse_response_body(response.body))
        except Exception as exc:
            FlextHttpClient.logger.exception("Unexpected error")
            return r[HttpJsonObject].fail(f"Unexpected error: {exc}")

    def _ensure_client(self) -> None:
        """Ensure Oracle WMS HTTP client is initialized using FLEXT delegation."""
        if self._client is None:
            config = FlextApiSettings(
                base_url=self.base_url,
                timeout=self.timeout,
                headers=dict(self.default_headers),
                max_retries=0,
                verify_ssl=self.verify_ssl,
                default_headers=dict(self.default_headers),
                log_requests=False,
                log_responses=False,
            )
            self._client = FlextApiClient(config=config)

    def _execute_request(
        self,
        method: str,
        path: str,
        params: FlextApiTypes.Api.WebParams | None = None,
        headers: Mapping[str, str] | None = None,
        body: HttpJsonObject | None = None,
    ) -> r[HttpJsonObject]:
        """Execute HTTP request with FLEXT delegation."""
        try:
            self._ensure_client()
            if self._client is None:
                return r[HttpJsonObject].fail("Client not initialized")
            request_headers = dict(self.default_headers)
            request_headers.update(self._normalize_headers(headers))
            url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url
            if params:
                query = "&".join((f"{k}={v}" for k, v in params.items()))
                url = f"{url}?{query}"
            request = FlextApiModels.HttpRequest(
                method=method,
                url=url,
                headers=request_headers,
                body=self._normalize_request_body(body),
                query_params=params or {},
                timeout=self.timeout,
            )
            response_result = self._client.request(request)
            if response_result.is_failure:
                return r[HttpJsonObject].fail(
                    f"HTTP {method} failed: {response_result.error}"
                )
            response = response_result.value
            if response.status_code >= HTTP_BAD_REQUEST_THRESHOLD:
                return r[HttpJsonObject].fail(
                    f"HTTP {response.status_code}: {response.body!r}"
                )
            return r[HttpJsonObject].ok(self._parse_response_body(response.body))
        except Exception as exc:
            FlextHttpClient.logger.exception(f"HTTP {method} error")
            return r[HttpJsonObject].fail(f"Request error: {exc}")

    def _parse_response_body(
        self, body: FlextApiTypes.Api.ResponseBody
    ) -> HttpJsonObject:
        """Parse response body using strict model validation."""
        match body:
            case dict() as payload:
                try:
                    return TypeAdapter(dict[str, t.ContainerValue]).validate_python(
                        payload
                    )
                except ValidationError:
                    return {"text": str(payload)}
            case str() as raw if raw:
                try:
                    return TypeAdapter(dict[str, t.ContainerValue]).validate_json(raw)
                except (ValidationError, ValueError):
                    return {"text": raw}
            case bytes() as raw_bytes:
                try:
                    return TypeAdapter(dict[str, t.ContainerValue]).validate_json(
                        raw_bytes
                    )
                except (ValidationError, ValueError):
                    return {"text": raw_bytes.decode("utf-8", errors="ignore")}
            case _:
                return {}


def create_flext_http_client(
    base_url: str,
    timeout: float = 30.0,
    headers: Mapping[str, str] | None = None,
    *,
    verify_ssl: bool = True,
) -> FlextHttpClient:
    """Create FlextHttpClient instance."""
    return FlextHttpClient(
        base_url=base_url, timeout=timeout, headers=headers, verify_ssl=verify_ssl
    )


__all__ = ["FlextHttpClient", "create_flext_http_client"]
