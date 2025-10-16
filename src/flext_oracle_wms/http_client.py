"""FLEXT Module.

Copyright (c) 2025 FLEXT Team. All rights reserved. SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from typing import Self, override

from flext_api import FlextApiClient
from flext_core import FlextLogger, FlextResult, FlextTypes

from flext_oracle_wms.typings import FlextOracleWmsTypes

# HTTP Status Code Constants
HTTP_BAD_REQUEST = 400


class FlextHttpClient:
    """HTTP client using flext-api foundation with flext-core patterns."""

    # Shared logger for all HTTP client operations
    logger = FlextLogger(__name__)

    @override
    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        headers: FlextTypes.StringDict | None = None,
        *,
        verify_ssl: bool = True,
    ) -> None:
        """Initialize HTTP client.

        Args:
            base_url: Base URL for all requests
            timeout: Request timeout in seconds
            headers: Default headers for all requests
            verify_ssl: Whether to verify SSL certificates

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

    def __exit__(
        self,
        exc_type: object,
        exc_val: object,
        exc_tb: object,
    ) -> None:
        """Context manager exit."""
        self.close()

    def _ensure_client(self) -> None:
        """Ensure HTTP client is initialized."""
        if self._client is None:
            # Use flext-api foundation instead of direct httpx
            self._client = FlextApiClient(
                base_url=self.base_url,
                timeout=int(self.timeout),
                default_headers=self.default_headers,
                verify_ssl=self.verify_ssl,
            )

    def close(self) -> None:
        """Close HTTP client."""
        if self._client is not None:
            # FlextApiClient handles cleanup internally
            self._client.close() if hasattr(self._client, "close") else None
            self._client = None

    def get(
        self,
        path: str,
        params: dict[str, str | int | float] | None = None,
        headers: FlextTypes.StringDict | None = None,
    ) -> FlextResult[FlextOracleWmsTypes.Core.Dict]:
        """Make GET request.

        Args:
            path: Request path
            params: Query parameters
            headers: Additional headers

        Returns:
            FlextResult containing response data

        """
        try:
            self._ensure_client()
            if self._client is None:
                return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(
                    "Client not initialized"
                )

            # Prepare headers using flext-api patterns
            request_headers = self.default_headers.copy()
            if headers:
                request_headers.update(headers)

            # Use flext-api client for HTTP requests
            response_result = self._client.request(
                "GET",
                path,
                headers=request_headers,
                params=params,
            )

            if response_result.is_failure:
                return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(
                    f"HTTP request failed: {response_result.error}",
                )

            response = response_result.unwrap()

            if response.status_code >= HTTP_BAD_REQUEST:
                return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(
                    f"HTTP {response.status_code}: {response.body}",
                )

            # Parse JSON response safely
            try:
                if isinstance(response.body, dict):
                    data = response.body
                elif isinstance(response.body, str):
                    data: FlextTypes.Dict = (
                        json.loads(response.body) if response.body else {}
                    )
                else:
                    data = {}
            except (ValueError, AttributeError):
                data: FlextTypes.Dict = {
                    "text": str(response.body) if response.body else ""
                }

            return FlextResult[FlextOracleWmsTypes.Core.Dict].ok(data)

        except Exception as e:
            FlextHttpClient.logger.exception("HTTP request error")
            return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(
                f"Request error: {e}"
            )

    def post(
        self,
        path: str,
        data: FlextTypes.Dict | None = None,
        json_data: FlextTypes.Dict | None = None,
        headers: FlextTypes.StringDict | None = None,
    ) -> FlextResult[FlextOracleWmsTypes.Core.Dict]:
        """Make POST request.

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
                return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(
                    "Client not initialized"
                )

            # Prepare headers using flext-api patterns
            request_headers = self.default_headers.copy()
            if headers:
                request_headers.update(headers)

            # Use flext-api client for HTTP requests
            # Prepare request body
            request_body = None
            if json_data:
                request_body = json_data
            elif data:
                request_body = data

            response_result = self._client.request(
                "POST",
                path,
                headers=request_headers,
                body=request_body,
            )

            if response_result.is_failure:
                return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(
                    f"HTTP request failed: {response_result.error}",
                )

            response = response_result.unwrap()

            if response.status_code >= HTTP_BAD_REQUEST:
                return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(
                    f"HTTP {response.status_code}: {response.body}",
                )

            # Parse JSON response safely
            try:
                if isinstance(response.body, dict):
                    response_data = response.body
                elif isinstance(response.body, str):
                    response_data: FlextTypes.Dict = (
                        json.loads(response.body) if response.body else {}
                    )
                else:
                    response_data = {}
            except (ValueError, AttributeError):
                response_data: FlextTypes.Dict = {
                    "text": str(response.body) if response.body else ""
                }

            return FlextResult[FlextOracleWmsTypes.Core.Dict].ok(response_data)

        except Exception as e:
            FlextHttpClient.logger.exception("HTTP POST request error")
            return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(
                f"Request error: {e}"
            )

    def put(
        self,
        path: str,
        data: FlextTypes.Dict | None = None,
        json_data: FlextTypes.Dict | None = None,
        headers: FlextTypes.StringDict | None = None,
    ) -> FlextResult[FlextOracleWmsTypes.Core.Dict]:
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
                return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(
                    "Client not initialized"
                )

            # Prepare headers using flext-api patterns
            request_headers = self.default_headers.copy()
            if headers:
                request_headers.update(headers)

            # Use flext-api client for HTTP requests
            # Prepare request body
            request_body = None
            if json_data:
                request_body = json_data
            elif data:
                request_body = data

            response_result = self._client.request(
                "PUT",
                path,
                headers=request_headers,
                body=request_body,
            )

            if response_result.is_failure:
                return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(
                    f"HTTP request failed: {response_result.error}",
                )

            response = response_result.unwrap()

            if response.status_code >= HTTP_BAD_REQUEST:
                return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(
                    f"HTTP {response.status_code}: {response.body}",
                )

            # Parse JSON response safely
            try:
                if isinstance(response.body, dict):
                    response_data = response.body
                elif isinstance(response.body, str):
                    response_data: FlextTypes.Dict = (
                        json.loads(response.body) if response.body else {}
                    )
                else:
                    response_data = {}
            except (ValueError, AttributeError):
                response_data: FlextTypes.Dict = {
                    "text": str(response.body) if response.body else ""
                }

            return FlextResult[FlextOracleWmsTypes.Core.Dict].ok(response_data)

        except Exception as e:
            FlextHttpClient.logger.exception("Unexpected error")
            return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(
                f"Unexpected error: {e}"
            )

    def delete(
        self,
        path: str,
        headers: FlextTypes.StringDict | None = None,
    ) -> FlextResult[FlextOracleWmsTypes.Core.Dict]:
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
                return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(
                    "Client not initialized"
                )

            request_headers = self.default_headers.copy()
            if headers:
                request_headers.update(headers)

            response_result: FlextResult[object] = self._client.delete(
                path, headers=request_headers
            )

            if response_result.is_failure:
                return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(
                    f"HTTP request failed: {response_result.error}",
                )

            response = response_result.unwrap()

            if response.status_code >= HTTP_BAD_REQUEST:
                return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(
                    f"HTTP {response.status_code}: {response.body}",
                )

            # Parse JSON response safely
            try:
                if isinstance(response.body, dict):
                    data = response.body
                elif isinstance(response.body, str):
                    data: FlextTypes.Dict = (
                        json.loads(response.body) if response.body else {}
                    )
                else:
                    data = {}
            except (ValueError, AttributeError):
                data: FlextTypes.Dict = {
                    "text": str(response.body) if response.body else ""
                }

            return FlextResult[FlextOracleWmsTypes.Core.Dict].ok(data)

        except Exception as e:
            FlextHttpClient.logger.exception("Unexpected error")
            return FlextResult[FlextOracleWmsTypes.Core.Dict].fail(
                f"Unexpected error: {e}"
            )


# Factory function following flext-core patterns
def create_flext_http_client(
    base_url: str,
    timeout: float = 30.0,
    headers: FlextTypes.StringDict | None = None,
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
        FlextHttpClient instance

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
