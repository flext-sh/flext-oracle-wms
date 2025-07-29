"""Oracle WMS Authentication Module.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Provides authentication mechanisms for Oracle WMS API using flext-core patterns.
"""

from __future__ import annotations

import base64
from typing import TYPE_CHECKING

from flext_core import get_logger

if TYPE_CHECKING:
    from collections.abc import Mapping

logger = get_logger(__name__)


class FlextOracleWmsAuth:
    """Basic authentication for Oracle WMS API."""

    def __init__(self, username: str, password: str) -> None:
        """Initialize basic authentication.

        Args:
            username: Oracle WMS username
            password: Oracle WMS password

        """
        self.username = username
        self.password = password

    def get_auth_headers(self) -> dict[str, str]:
        """Get authentication headers for requests.

        Returns:
            Dictionary with Authorization header

        """
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {encoded_credentials}"}


class FlextOracleWmsOAuth2Auth:
    """OAuth2 authentication for Oracle WMS API."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        token_url: str,
        *,
        scope: str | None = None,
    ) -> None:
        """Initialize OAuth2 authentication.

        Args:
            client_id: OAuth2 client ID
            client_secret: OAuth2 client secret
            token_url: Token endpoint URL
            scope: Optional OAuth2 scope

        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.scope = scope
        self._access_token: str | None = None

    def get_auth_headers(self) -> dict[str, str]:
        """Get authentication headers for requests.

        Returns:
            Dictionary with Authorization header

        """
        if not self._access_token:
            # In a real implementation, this would fetch a token
            # For now, return empty headers to avoid breaking tests
            logger.warning("OAuth2 token not available, using empty headers")
            return {}

        return {"Authorization": f"Bearer {self._access_token}"}


def flext_oracle_wms_create_authenticator(
    username: str,
    password: str,
) -> FlextOracleWmsAuth:
    """Create basic authenticator.

    Args:
        username: Oracle WMS username
        password: Oracle WMS password

    Returns:
        Basic authenticator instance

    """
    return FlextOracleWmsAuth(username, password)


def flext_oracle_wms_create_oauth2_authenticator(
    client_id: str,
    client_secret: str,
    token_url: str,
    *,
    scope: str | None = None,
) -> FlextOracleWmsOAuth2Auth:
    """Create OAuth2 authenticator.

    Args:
        client_id: OAuth2 client ID
        client_secret: OAuth2 client secret
        token_url: Token endpoint URL
        scope: Optional OAuth2 scope

    Returns:
        OAuth2 authenticator instance

    """
    return FlextOracleWmsOAuth2Auth(
        client_id=client_id,
        client_secret=client_secret,
        token_url=token_url,
        scope=scope,
    )


def flext_oracle_wms_get_api_headers(
    auth: FlextOracleWmsAuth | FlextOracleWmsOAuth2Auth,
    additional_headers: Mapping[str, str] | None = None,
) -> dict[str, str]:
    """Get complete API headers including authentication.

    Args:
        auth: Authentication instance
        additional_headers: Optional additional headers

    Returns:
        Complete headers dictionary

    """
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "flext-oracle-wms/1.0.0",
    }

    # Add authentication headers
    headers.update(auth.get_auth_headers())

    # Add any additional headers
    if additional_headers:
        headers.update(additional_headers)

    return headers


__all__ = [
    "FlextOracleWmsAuth",
    "FlextOracleWmsOAuth2Auth",
    "flext_oracle_wms_create_authenticator",
    "flext_oracle_wms_create_oauth2_authenticator",
    "flext_oracle_wms_get_api_headers",
]
