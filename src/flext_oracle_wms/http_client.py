"""FLEXT Module.

Copyright (c) 2025 FLEXT Team. All rights reserved. SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Self

import httpx
from flext_core import FlextLogger, FlextResult, FlextTypes

logger = FlextLogger(__name__)


class FlextHttpClient:
    """Simple HTTP client using httpx with flext-core patterns."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        headers: dict[str, str] | None = None,
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
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> Self:
        """Async context manager entry."""
        await self._ensure_client()
        return self

    async def __aexit__(
        self, exc_type: object, exc_val: object, exc_tb: object
    ) -> None:
        """Async context manager exit."""
        await self.close()

    async def _ensure_client(self) -> None:
        """Ensure HTTP client is initialized."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                headers=self.default_headers,
                verify=self.verify_ssl,
            )

    async def close(self) -> None:
        """Close HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def get(
        self,
        path: str,
        params: dict[str, str | int | float | bool | None] | None = None,
        headers: dict[str, str] | None = None,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Make GET request.

        Args:
            path: Request path
            params: Query parameters
            headers: Additional headers

        Returns:
            FlextResult containing response data

        """
        try:
            await self._ensure_client()
            if self._client is None:
                return FlextResult[FlextTypes.Core.Dict].fail("Client not initialized")

            request_headers = self.default_headers.copy()
            if headers:
                request_headers.update(headers)

            response = await self._client.get(
                path,
                params=params,
                headers=request_headers,
            )
            response.raise_for_status()

            data = response.json()
            if data is None:
                data = {}
            return FlextResult[FlextTypes.Core.Dict].ok(data)

        except httpx.HTTPStatusError as e:
            logger.exception(f"HTTP error {e.response.status_code}: {e.response.text}")
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"HTTP {e.response.status_code}: {e.response.text}"
            )
        except httpx.RequestError as e:
            logger.exception("Request error")
            return FlextResult[FlextTypes.Core.Dict].fail(f"Request error: {e}")
        except Exception as e:
            logger.exception("Unexpected error")
            return FlextResult[FlextTypes.Core.Dict].fail(f"Unexpected error: {e}")

    async def post(
        self,
        path: str,
        data: dict[str, object] | None = None,
        json_data: dict[str, object] | None = None,
        headers: dict[str, str] | None = None,
    ) -> FlextResult[FlextTypes.Core.Dict]:
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
            await self._ensure_client()
            if self._client is None:
                return FlextResult[FlextTypes.Core.Dict].fail("Client not initialized")

            request_headers = self.default_headers.copy()
            if headers:
                request_headers.update(headers)

            response = await self._client.post(
                path,
                data=data,
                json=json_data,
                headers=request_headers,
            )
            response.raise_for_status()

            data = response.json()
            if data is None:
                data = {}
            return FlextResult[FlextTypes.Core.Dict].ok(data)

        except httpx.HTTPStatusError as e:
            logger.exception(f"HTTP error {e.response.status_code}: {e.response.text}")
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"HTTP {e.response.status_code}: {e.response.text}"
            )
        except httpx.RequestError as e:
            logger.exception("Request error")
            return FlextResult[FlextTypes.Core.Dict].fail(f"Request error: {e}")
        except Exception as e:
            logger.exception("Unexpected error")
            return FlextResult[FlextTypes.Core.Dict].fail(f"Unexpected error: {e}")

    async def put(
        self,
        path: str,
        data: dict[str, object] | None = None,
        json_data: dict[str, object] | None = None,
        headers: dict[str, str] | None = None,
    ) -> FlextResult[FlextTypes.Core.Dict]:
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
            await self._ensure_client()
            if self._client is None:
                return FlextResult[FlextTypes.Core.Dict].fail("Client not initialized")

            request_headers = self.default_headers.copy()
            if headers:
                request_headers.update(headers)

            response = await self._client.put(
                path,
                data=data,
                json=json_data,
                headers=request_headers,
            )
            response.raise_for_status()

            data = response.json()
            if data is None:
                data = {}
            return FlextResult[FlextTypes.Core.Dict].ok(data)

        except httpx.HTTPStatusError as e:
            logger.exception(f"HTTP error {e.response.status_code}: {e.response.text}")
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"HTTP {e.response.status_code}: {e.response.text}"
            )
        except httpx.RequestError as e:
            logger.exception("Request error")
            return FlextResult[FlextTypes.Core.Dict].fail(f"Request error: {e}")
        except Exception as e:
            logger.exception("Unexpected error")
            return FlextResult[FlextTypes.Core.Dict].fail(f"Unexpected error: {e}")

    async def delete(
        self,
        path: str,
        headers: dict[str, str] | None = None,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Make DELETE request.

        Args:
            path: Request path
            headers: Additional headers

        Returns:
            FlextResult containing response data

        """
        try:
            await self._ensure_client()
            if self._client is None:
                return FlextResult[FlextTypes.Core.Dict].fail("Client not initialized")

            request_headers = self.default_headers.copy()
            if headers:
                request_headers.update(headers)

            response = await self._client.delete(
                path,
                headers=request_headers,
            )
            response.raise_for_status()

            data = response.json()
            if data is None:
                data = {}
            return FlextResult[FlextTypes.Core.Dict].ok(data)

        except httpx.HTTPStatusError as e:
            logger.exception(f"HTTP error {e.response.status_code}: {e.response.text}")
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"HTTP {e.response.status_code}: {e.response.text}"
            )
        except httpx.RequestError as e:
            logger.exception("Request error")
            return FlextResult[FlextTypes.Core.Dict].fail(f"Request error: {e}")
        except Exception as e:
            logger.exception("Unexpected error")
            return FlextResult[FlextTypes.Core.Dict].fail(f"Unexpected error: {e}")


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
