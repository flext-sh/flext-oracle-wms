"""Enterprise Oracle WMS Authentication with flext-core integration.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Comprehensive authentication system for Oracle WMS API operations
using modern Python 3.13 patterns and flext-core standards.
"""

from __future__ import annotations

import base64
import secrets
import urllib.parse
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Self

import httpx

# Import from flext-core root namespace as required
from flext_core import FlextResult, get_logger

if TYPE_CHECKING:
    from collections.abc import Generator
    from typing import TypedDict

    class OAuthTokenResponse(TypedDict):
        """OAuth token response structure."""

        access_token: str
        token_type: str
        expires_in: int
        refresh_token: str
        scope: str


logger = get_logger(__name__)


class FlextOracleWmsAuth(httpx.Auth):
    """Enterprise Oracle WMS authentication handler with flext-core integration."""

    def __init__(
        self,
        username: str,
        password: str,
        auth_method: str = "basic",
    ) -> None:
        """Initialize Oracle WMS authentication.

        Args:
            username: Oracle WMS username
            password: Oracle WMS password
            auth_method: Authentication method (basic, token, etc.)

        """
        self.username = username
        self.password = password
        self.auth_method = auth_method
        self._token_cache: str | None = None
        logger.debug(f"Initialized FlextOracleWms authentication for user: {username}")

    def auth_flow(
        self,
        request: httpx.Request,
    ) -> Generator[httpx.Request, httpx.Response]:
        """Apply Oracle WMS authentication to request.

        Args:
            request: HTTP request to authenticate

        Yields:
            Authenticated HTTP request

        """
        if self.auth_method == "basic":
            request.headers["Authorization"] = f"Basic {self._get_basic_auth()}"
        elif self.auth_method == "token" and self._token_cache:
            request.headers["Authorization"] = f"Bearer {self._token_cache}"

        yield request

    def _get_basic_auth(self) -> str:
        """Generate basic authentication string.

        Returns:
            Base64 encoded credentials

        """
        credentials = f"{self.username}:{self.password}"
        return base64.b64encode(credentials.encode()).decode()

    def flext_oracle_wms_validate_credentials(self) -> FlextResult[bool]:
        """Validate Oracle WMS credentials.

        Returns:
            FlextResult indicating credential validity

        """
        try:
            if not self.username or not self.password:
                return FlextResult.fail("Username and password are required")

            if len(self.username) < 1 or len(self.password) < 1:
                return FlextResult.fail("Username and password cannot be empty")

            logger.debug("Oracle WMS credentials validated successfully")
            return FlextResult.ok(True)
        except Exception as e:
            logger.exception("Credential validation failed: %s", e)
            return FlextResult.fail(f"Credential validation error: {e}")

    def flext_oracle_wms_test_connection(self, base_url: str) -> FlextResult[bool]:
        """Test Oracle WMS connection with current credentials.

        Args:
            base_url: Oracle WMS base URL

        Returns:
            FlextResult indicating connection success

        """
        try:
            with httpx.Client(auth=self) as client:
                # Test with a lightweight endpoint
                response = client.get(f"{base_url}/health", timeout=10.0)

                if response.status_code == 200:
                    logger.info("Oracle WMS connection test successful")
                    return FlextResult.ok(True)
                if response.status_code == 401:
                    return FlextResult.fail(
                        "Authentication failed - invalid credentials",
                    )
                if response.status_code == 403:
                    return FlextResult.fail(
                        "Access forbidden - insufficient permissions",
                    )
                return FlextResult.fail(
                    f"Connection test failed: HTTP {response.status_code}",
                )

        except httpx.TimeoutException:
            return FlextResult.fail("Connection test timeout")
        except httpx.ConnectError:
            return FlextResult.fail("Connection failed - server unreachable")
        except Exception as e:
            logger.exception("Connection test error: %s", e)
            return FlextResult.fail(f"Connection test error: {e}")

    def __enter__(self) -> Self:
        """Context manager entry."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Context manager exit."""
        # Cleanup any cached tokens or resources
        self._token_cache = None


class FlextOracleWmsOAuth2Auth(httpx.Auth):
    """Enterprise Oracle WMS OAuth2 authentication handler."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        authorization_url: str,
        token_url: str,
        redirect_uri: str = "http://localhost:8080/callback",
        scope: str = "read write",
    ) -> None:
        """Initialize OAuth2 authentication for Oracle WMS.

        Args:
            client_id: OAuth2 client ID
            client_secret: OAuth2 client secret
            authorization_url: OAuth2 authorization endpoint
            token_url: OAuth2 token endpoint
            redirect_uri: OAuth2 redirect URI
            scope: OAuth2 scope

        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_url = authorization_url
        self.token_url = token_url
        self.redirect_uri = redirect_uri
        self.scope = scope

        # Token storage
        self._access_token: str | None = None
        self._refresh_token: str | None = None
        self._token_expires_at: datetime | None = None

        logger.debug("Initialized OAuth2 authentication for Oracle WMS")

    def auth_flow(
        self,
        request: httpx.Request,
    ) -> Generator[httpx.Request, httpx.Response]:
        """Apply OAuth2 authentication to request.

        Args:
            request: HTTP request to authenticate

        Yields:
            Authenticated HTTP request

        """
        # Check if we have a valid access token
        if not self._is_token_valid():
            # Try to refresh token if we have refresh_token
            if self._refresh_token:
                refresh_result = self._refresh_access_token()
                if not refresh_result.success:
                    logger.error(
                        "Failed to refresh OAuth2 token: %s",
                        refresh_result.error,
                    )
                    # Could implement re-authorization flow here
            else:
                logger.warning("No valid OAuth2 token available, request may fail")

        # Add access token if available
        if self._access_token:
            request.headers["Authorization"] = f"Bearer {self._access_token}"

        yield request

    def get_authorization_url(self) -> FlextResult[str]:
        """Generate OAuth2 authorization URL.

        Returns:
            FlextResult with authorization URL

        """
        try:
            state = secrets.token_urlsafe(32)

            params = {
                "response_type": "code",
                "client_id": self.client_id,
                "redirect_uri": self.redirect_uri,
                "scope": self.scope,
                "state": state,
            }

            query_string = urllib.parse.urlencode(params)
            auth_url = f"{self.authorization_url}?{query_string}"

            # Store state for validation
            # (in real implementation, this should be persisted)
            self._oauth_state = state

            logger.info("Generated OAuth2 authorization URL")
            return FlextResult.ok(auth_url)

        except Exception as e:
            return FlextResult.fail(f"Failed to generate authorization URL: {e}")

    def exchange_code_for_token(
        self,
        authorization_code: str,
        state: str | None = None,
    ) -> FlextResult[bool]:
        """Exchange authorization code for access token.

        Args:
            authorization_code: Authorization code from OAuth2 callback
            state: State parameter for security validation

        Returns:
            FlextResult indicating success

        """
        try:
            # Validate state if provided
            if state and hasattr(self, "_oauth_state") and state != self._oauth_state:
                return FlextResult.fail(
                    "Invalid state parameter - possible CSRF attack",
                )

            # Prepare token request
            data = {
                "grant_type": "authorization_code",
                "code": authorization_code,
                "redirect_uri": self.redirect_uri,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }

            # Make token request
            with httpx.Client() as client:
                response = client.post(
                    self.token_url,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=30.0,
                )

                if response.status_code != 200:
                    return FlextResult.fail(
                        f"Token exchange failed: HTTP {response.status_code}",
                    )

                token_data = response.json()
                return self._store_token_data(token_data)

        except Exception as e:
            logger.exception("Token exchange failed: %s", e)
            return FlextResult.fail(f"Token exchange error: {e}")

    def _store_token_data(self, token_data: dict[str, Any]) -> FlextResult[bool]:
        """Store OAuth2 token data.

        Args:
            token_data: Token response from OAuth2 server

        Returns:
            FlextResult indicating success

        """
        try:
            if "access_token" not in token_data:
                return FlextResult.fail("No access_token in response")

            self._access_token = token_data["access_token"]
            self._refresh_token = token_data.get("refresh_token")

            # Calculate expiration time
            expires_in = token_data.get("expires_in", 3600)  # Default to 1 hour
            self._token_expires_at = datetime.now() + timedelta(seconds=expires_in)

            logger.info("OAuth2 tokens stored successfully")
            return FlextResult.ok(True)

        except Exception as e:
            return FlextResult.fail(f"Failed to store token data: {e}")

    def _is_token_valid(self) -> bool:
        """Check if current access token is valid.

        Returns:
            True if token is valid and not expired

        """
        if not self._access_token or not self._token_expires_at:
            return False

        # Check if token is expired (with 5 minute buffer)
        return datetime.now() < (self._token_expires_at - timedelta(minutes=5))

    def _refresh_access_token(self) -> FlextResult[bool]:
        """Refresh access token using refresh token.

        Returns:
            FlextResult indicating success

        """
        try:
            if not self._refresh_token:
                return FlextResult.fail("No refresh token available")

            data = {
                "grant_type": "refresh_token",
                "refresh_token": self._refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }

            with httpx.Client() as client:
                response = client.post(
                    self.token_url,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=30.0,
                )

                if response.status_code != 200:
                    return FlextResult.fail(
                        f"Token refresh failed: HTTP {response.status_code}",
                    )

                token_data = response.json()
                return self._store_token_data(token_data)

        except Exception as e:
            logger.exception("Token refresh failed: %s", e)
            return FlextResult.fail(f"Token refresh error: {e}")

    def clear_tokens(self) -> None:
        """Clear stored OAuth2 tokens."""
        self._access_token = None
        self._refresh_token = None
        self._token_expires_at = None
        logger.info("OAuth2 tokens cleared")

    def __enter__(self) -> Self:
        """Context manager entry."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Context manager exit."""
        # Optionally clear tokens on exit


def flext_oracle_wms_create_authenticator(
    username: str,
    password: str,
    auth_method: str = "basic",
) -> FlextOracleWmsAuth:
    """Factory function to create Oracle WMS authenticator.

    Args:
        username: Oracle WMS username
        password: Oracle WMS password
        auth_method: Authentication method

    Returns:
        Configured Oracle WMS authenticator

    """
    return FlextOracleWmsAuth(
        username=username,
        password=password,
        auth_method=auth_method,
    )


def flext_oracle_wms_create_oauth2_authenticator(
    client_id: str,
    client_secret: str,
    authorization_url: str,
    token_url: str,
    redirect_uri: str = "http://localhost:8080/callback",
    scope: str = "read write",
) -> FlextOracleWmsOAuth2Auth:
    """Factory function to create Oracle WMS OAuth2 authenticator.

    Args:
        client_id: OAuth2 client ID
        client_secret: OAuth2 client secret
        authorization_url: OAuth2 authorization endpoint
        token_url: OAuth2 token endpoint
        redirect_uri: OAuth2 redirect URI
        scope: OAuth2 scope

    Returns:
        Configured Oracle WMS OAuth2 authenticator

    """
    return FlextOracleWmsOAuth2Auth(
        client_id=client_id,
        client_secret=client_secret,
        authorization_url=authorization_url,
        token_url=token_url,
        redirect_uri=redirect_uri,
        scope=scope,
    )


def flext_oracle_wms_get_api_headers(
    config: dict[str, Any] | None = None,
) -> dict[str, str]:
    """Get standard Oracle WMS API headers.

    Args:
        config: Optional configuration dictionary with additional headers

    Returns:
        Dictionary of HTTP headers for Oracle WMS API requests

    """
    headers: dict[str, str] = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "flext-oracle-wms/1.0",
        "Cache-Control": "no-cache",
    }

    # Add any additional headers from config
    if config and "headers" in config:
        for key, value in config["headers"].items():
            headers[str(key)] = str(value)

    return headers


__all__ = [
    "FlextOracleWmsAuth",
    "FlextOracleWmsOAuth2Auth",
    "flext_oracle_wms_create_authenticator",
    "flext_oracle_wms_create_oauth2_authenticator",
    "flext_oracle_wms_get_api_headers",
]
