"""FLEXT Generic HTTP Client - Railway-oriented with Pydantic.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from typing import Self

from flext_api import FlextApiClient, FlextApiModels, FlextApiSettings
from flext_core import FlextLogger, FlextResult, FlextTypes as t
from pydantic import BaseModel, Field

# HTTP status codes
HTTP_BAD_REQUEST_THRESHOLD = 400


class HttpRequest(BaseModel):
    """Generic Pydantic model for HTTP requests."""

    method: str
    url: str
    headers: dict[str, str] = Field(default_factory=dict)
    body: dict[str, t.GeneralValueType] | None = None


class HttpResponse(BaseModel):
    """Generic Pydantic model for HTTP responses."""

    status_code: int
    body: dict[str, t.GeneralValueType] | str = Field(default_factory=dict)


class FlextHttpClient:
    """Generic HTTP client using FLEXT delegation with railway-oriented programming."""

    # Shared logger for all HTTP operations
    logger = FlextLogger(__name__)

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        headers: dict[str, str] | None = None,
        *,
        verify_ssl: bool = True,
    ) -> None:
        """Initialize Oracle WMS HTTP client with FLEXT patterns.

        Args:
        base_url: Base URL for all requests
        timeout: Request timeout in seconds
        headers: Default headers for all requests
        verify_ssl: Whether to verify SSL certificates.

        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.default_headers = headers or {}
        self.verify_ssl = verify_ssl
        self._client: FlextApiClient | None = None

    def __enter__(self) -> Self:
        """Context manager entry."""
        self._ensure_client()
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        """Context manager exit."""
        self.close()

    def _ensure_client(self) -> None:
        """Ensure Oracle WMS HTTP client is initialized using FLEXT delegation."""
        if self._client is None:
            # Create a basic config for the API client
            config = FlextApiSettings(
                base_url=self.base_url,
                timeout=self.timeout,
                headers=self.default_headers,
            )
            self._client = FlextApiClient(config=config)

    def close(self) -> None:
        """Close HTTP client with FLEXT cleanup."""
        if self._client and hasattr(self._client, "close"):
            self._client.close()
        self._client = None

    def get(
        self,
        path: str,
        params: dict[str, str | int | float] | None = None,
        headers: dict[str, str] | None = None,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Make GET request with railway-oriented error handling."""
        return self._execute_request("GET", path, params=params, headers=headers)

    def _execute_request(
        self,
        method: str,
        path: str,
        params: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
        body: dict[str, t.GeneralValueType] | None = None,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Execute HTTP request with FLEXT delegation."""
        try:
            self._ensure_client()
            if self._client is None:
                return FlextResult.fail("Client not initialized")
            # Merge headers using dict union
            request_headers = self.default_headers | (headers or {})
            # Build full URL
            url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url
            if params:
                query = "&".join(f"{k}={v}" for k, v in params.items())
                url = f"{url}?{query}"
            # Create HttpRequest
            request = FlextApiModels.HttpRequest(
                method=method,
                url=url,
                headers=request_headers,
                body=body,
            )
            # Execute via FLEXT API delegation
            response_result = self._client.request(request)
            if response_result.is_failure:
                return FlextResult.fail(
                    f"HTTP {method} failed: {response_result.error}",
                )
            response = response_result.value
            # Check HTTP status
            if response.status_code >= HTTP_BAD_REQUEST_THRESHOLD:
                return FlextResult.fail(f"HTTP {response.status_code}: {response.body}")
            # Parse response body
            return FlextResult.ok(self._parse_response_body(response.body))
        except Exception as e:
            FlextHttpClient.logger.exception(f"HTTP {method} error")
            return FlextResult.fail(f"Request error: {e}")

    def _parse_response_body(self, body: object) -> dict[str, t.GeneralValueType]:
        """Parse response body with modern Python patterns."""
        match body:
            case dict():
                return body
            case str() if body:
                try:
                    return dict(json.loads(body))
                except (ValueError, TypeError):
                    return {"text": body}
            case _:
                return {"data": body} if body else {}

    def post(
        self,
        path: str,
        data: dict[str, t.GeneralValueType] | None = None,
        json_data: dict[str, t.GeneralValueType] | None = None,
        headers: dict[str, str] | None = None,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Make POST request with railway-oriented error handling."""
        body = json_data or data
        return self._execute_request("POST", path, headers=headers, body=body)

    def put(
        self,
        path: str,
        data: dict[str, t.GeneralValueType] | None = None,
        json_data: dict[str, t.GeneralValueType] | None = None,
        headers: dict[str, str] | None = None,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Make PUT request.

        Args:
            path: Request path
            data: Form data
            json_data: JSON data
            headers: Additional headers

        Returns:
            FlextResult containing response data

        """
        try:
            self._ensure_client()
            if self._client is None:
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    "Client not initialized"
                )
            # Prepare headers using flext-api patterns
            request_headers = self.default_headers.copy()
            if headers:
                request_headers.update(headers)
            # Prepare request body
            request_body = json_data or data
            url = f"{self.base_url}/{path.lstrip('/')}"
            # Execute request
            request = FlextApiModels.HttpRequest(
                method="PUT",
                url=url,
                headers=request_headers,
                body=request_body,
            )
            response_result = self._client.request(request)
            if response_result.is_failure:
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    f"HTTP request failed: {response_result.error}",
                )
            response = response_result.value
            if response.status_code >= HTTP_BAD_REQUEST_THRESHOLD:
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    f"HTTP {response.status_code}: {response.body}",
                )
            response_data = self._parse_response_body(response.body)
            return FlextResult[dict[str, t.GeneralValueType]].ok(response_data)
        except Exception as e:
            FlextHttpClient.logger.exception("Unexpected error")
            return FlextResult[dict[str, t.GeneralValueType]].fail(
                f"Unexpected error: {e}"
            )

    def delete(
        self,
        path: str,
        headers: dict[str, str] | None = None,
    ) -> FlextResult[dict[str, t.GeneralValueType]]:
        """Make DELETE request.

        Args:
            path: Request path
            headers: Additional headers

        Returns:
            FlextResult containing response data

        """
        try:
            self._ensure_client()
            if self._client is None:
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    "Client not initialized"
                )
            # Prepare headers using flext-api patterns
            request_headers = self.default_headers.copy()
            if headers:
                request_headers.update(headers)
            url = f"{self.base_url}/{path.lstrip('/')}"
            # Execute request
            request = FlextApiModels.HttpRequest(
                method="DELETE",
                url=url,
                headers=request_headers,
            )
            response_result = self._client.request(request)
            if response_result.is_failure:
                return FlextResult[dict[str, t.GeneralValueType]].fail(
                    f"HTTP request failed: {response_result.error}",
                )
            response = response_result.value
            # Parse JSON response safely
            try:
                if isinstance(response.body, dict):
                    data = response.body
                elif isinstance(response.body, str):
                    data = json.loads(response.body) if response.body else {}
                else:
                    data = {}
            except (ValueError, AttributeError):
                data = {
                    "text": str(response.body) if response.body else "",
                }
            return FlextResult[dict[str, t.GeneralValueType]].ok(data)
        except Exception as e:
            FlextHttpClient.logger.exception(f"DELETE {path} error")
            return FlextResult[dict[str, t.GeneralValueType]].fail(
                f"Request error: {e}"
            )


# Factory function following flext-core patterns
def create_flext_http_client(
    base_url: str,
    timeout: float = 30.0,
    headers: dict[str, str] | None = None,
    *,
    verify_ssl: bool = True,
) -> FlextHttpClient:
    """Create FlextHttpClient instance.

    Args:
        base_url: Base URL for all requests
        timeout: Request timeout in seconds
        headers: Default headers for all requests
        verify_ssl: Whether to verify SSL certificates

    Returns:
        FlextHttpClient instance.

    """
    return FlextHttpClient(
        base_url=base_url,
        timeout=timeout,
        headers=headers,
        verify_ssl=verify_ssl,
    )


__all__ = [
    "FlextHttpClient",
    "create_flext_http_client",
]
