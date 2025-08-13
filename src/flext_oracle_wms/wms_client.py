"""Oracle WMS Client - Consolidated Client and Authentication.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Consolidated Oracle WMS client implementation combining client.py + authentication.py.
This module provides the primary client interface with integrated authentication support.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import TYPE_CHECKING

from flext_api import FlextApiClient, FlextApiClientConfig
from flext_api.constants import FlextApiConstants
from flext_core import (
    FlextResult,
    FlextValueObject,
    get_logger,
)
from pydantic import Field

from flext_oracle_wms.wms_api import (
    FLEXT_ORACLE_WMS_APIS,
    get_mock_server,
)
from flext_oracle_wms.wms_constants import (
    FlextOracleWmsDefaults,
    OracleWMSAuthMethod,
)
from flext_oracle_wms.wms_exceptions import (
    FlextOracleWmsAuthenticationError,
)

if TYPE_CHECKING:
    from flext_oracle_wms.wms_config import FlextOracleWmsClientConfig
    from flext_oracle_wms.wms_models import (
        FlextOracleWmsApiCategory,
        FlextOracleWmsApiEndpoint,
        TOracleWmsEntityName,
    )

logger = get_logger(__name__)


# =============================================================================
# AUTHENTICATION COMPONENTS
# =============================================================================


class FlextOracleWmsAuthConfig(FlextValueObject):
    """Oracle WMS authentication configuration."""

    auth_type: OracleWMSAuthMethod = Field(
        default=OracleWMSAuthMethod.BASIC,
        description="Authentication method",
    )
    username: str = Field(default="", description="Username for basic auth")
    password: str = Field(default="", description="Password for basic auth")
    token: str = Field(default="", description="Bearer token")
    api_key: str = Field(default="", description="API key")
    timeout: float = Field(
        default=FlextOracleWmsDefaults.DEFAULT_TIMEOUT,
        description="Request timeout in seconds",
    )

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate authentication configuration."""
        if self.auth_type == OracleWMSAuthMethod.BASIC:
            if not self.username or not self.password:
                return FlextResult.fail("Username and password required for basic auth")
        elif self.auth_type == OracleWMSAuthMethod.BEARER:
            if not self.token:
                return FlextResult.fail("Token required for bearer auth")
        elif self.auth_type == OracleWMSAuthMethod.API_KEY and not self.api_key:
            return FlextResult.fail("API key required for API key auth")
        return FlextResult.ok(None)


class FlextOracleWmsAuthenticator:
    """Oracle WMS authenticator using flext-core patterns."""

    def __init__(self, config: FlextOracleWmsAuthConfig) -> None:
        """Initialize authenticator with configuration."""
        self.config = config
        validation_result = self.config.validate_business_rules()
        if not validation_result.success:
            msg: str = (
                f"Invalid authentication configuration: {validation_result.error}"
            )
            raise FlextOracleWmsAuthenticationError(msg)
        logger.debug("Oracle WMS authenticator initialized", auth_type=config.auth_type)

    async def get_auth_headers(self) -> FlextResult[dict[str, str]]:
        """Get authentication headers based on configuration."""
        try:
            headers = {}

            if self.config.auth_type == OracleWMSAuthMethod.BASIC:
                credentials = f"{self.config.username}:{self.config.password}"
                encoded = base64.b64encode(credentials.encode()).decode()
                headers["Authorization"] = f"Basic {encoded}"

            elif self.config.auth_type == OracleWMSAuthMethod.BEARER:
                headers["Authorization"] = f"Bearer {self.config.token}"

            elif self.config.auth_type == OracleWMSAuthMethod.API_KEY:
                headers["X-API-Key"] = self.config.api_key

            headers["Content-Type"] = FlextApiConstants.ContentTypes.JSON
            headers["Accept"] = FlextApiConstants.ContentTypes.JSON

            return FlextResult.ok(headers)

        except (ValueError, TypeError, AttributeError, KeyError) as e:
            return FlextResult.fail(f"Generate auth headers failed: {e}")

    async def validate_credentials(self) -> FlextResult[bool]:
        """Validate credentials."""
        try:
            # Basic validation - actual validation would be against Oracle WMS API
            if self.config.auth_type == OracleWMSAuthMethod.BASIC:
                if not self.config.username or not self.config.password:
                    return FlextResult.fail("Invalid basic auth credentials")
            elif self.config.auth_type == OracleWMSAuthMethod.BEARER:
                if (
                    not self.config.token
                    or len(self.config.token) < FlextOracleWmsDefaults.MIN_TOKEN_LENGTH
                ):
                    return FlextResult.fail("Invalid bearer token")
            elif self.config.auth_type == OracleWMSAuthMethod.API_KEY and (
                not self.config.api_key
                or len(self.config.api_key) < FlextOracleWmsDefaults.MIN_API_KEY_LENGTH
            ):
                return FlextResult.fail("Invalid API key")

            return FlextResult.ok(data=True)

        except (
            ConnectionError,
            TimeoutError,
            OSError,
            TypeError,
            ValueError,
            AttributeError,
        ) as e:
            return FlextResult.fail(f"Validate credentials failed: {e}")


class FlextOracleWmsAuthPlugin:
    """Oracle WMS authentication plugin."""

    def __init__(self, name: str, version: str = "0.9.0") -> None:
        """Initialize authentication plugin."""
        self.name = name
        self.version = version
        self.authenticator: FlextOracleWmsAuthenticator | None = None

    async def initialize(self, context: dict[str, object]) -> FlextResult[None]:
        """Initialize authentication plugin with context."""
        try:
            # Create config from context with proper type extraction
            auth_type = context.get("auth_type", OracleWMSAuthMethod.BASIC)
            username = str(context.get("username", ""))
            password = str(context.get("password", ""))
            token = str(context.get("token", ""))
            api_key = str(context.get("api_key", ""))
            timeout_val = context.get("timeout", FlextOracleWmsDefaults.DEFAULT_TIMEOUT)
            timeout = (
                float(timeout_val)
                if isinstance(timeout_val, (int, float, str))
                else FlextOracleWmsDefaults.DEFAULT_TIMEOUT
            )

            auth_config = FlextOracleWmsAuthConfig(
                auth_type=auth_type
                if isinstance(auth_type, OracleWMSAuthMethod)
                else OracleWMSAuthMethod.BASIC,
                username=username,
                password=password,
                token=token,
                api_key=api_key,
                timeout=timeout,
            )
            self.authenticator = FlextOracleWmsAuthenticator(auth_config)
            return FlextResult.ok(None)
        except (TypeError, ValueError, AttributeError, RuntimeError) as e:
            return FlextResult.fail(f"Auth plugin initialization failed: {e}")


# =============================================================================
# CLIENT COMPONENTS
# =============================================================================


@dataclass
class ApiCallRequest:
    """Parameter Object: Encapsulates API call request data."""

    api_name: str
    kwargs: dict[str, object]

    @property
    def data(self) -> object:
        """Extract data parameter."""
        return self.kwargs.get("data")

    @property
    def params(self) -> object:
        """Extract params parameter."""
        return self.kwargs.get("params")

    @property
    def path_params(self) -> object:
        """Extract path_params parameter."""
        return self.kwargs.get("path_params", {})


@dataclass
class PreparedApiCall:
    """Parameter Object: Encapsulates prepared API call data."""

    method: str
    full_path: str
    data: dict[str, object] | None
    params: dict[str, object] | None


class FlextOracleWmsClient:
    """Oracle WMS Cloud Client - Dynamic & Declarative Implementation.

    Enterprise Oracle WMS Cloud client that dynamically discovers entities via real
    API calls and implements 25+ Oracle WMS Cloud APIs declaratively using flext-api
    patterns.

    Features:
        - Dynamic entity discovery through Oracle WMS Cloud REST API
        - Declarative API implementation with comprehensive endpoint catalog
        - Type-safe configuration management with Pydantic validation
        - Railway-oriented programming with FlextResult error handling
        - Enterprise authentication supporting Basic, Bearer, and API Key methods
        - Intelligent caching with configurable TTL and performance optimization
        - Comprehensive error handling with Oracle WMS-specific categorization

    Architecture:
        Built on FLEXT ecosystem foundations with Clean Architecture principles:
        - Uses FlextApiClient for HTTP communication with connection pooling
        - Implements FlextResult pattern for consistent error handling
        - Integrates with FLEXT observability for monitoring and logging
        - Supports FLEXT dependency injection container patterns
    """

    def __init__(self, config: FlextOracleWmsClientConfig) -> None:
        """Initialize Oracle WMS client with configuration."""
        self.config = config
        self._api_client: FlextApiClient | None = None
        self._authenticator: FlextOracleWmsAuthenticator | None = None

        # Setup authentication
        auth_config = FlextOracleWmsAuthConfig(
            auth_type=OracleWMSAuthMethod.BASIC,
            username=config.username,
            password=config.password,
        )
        self._authenticator = FlextOracleWmsAuthenticator(auth_config)

    async def initialize(self) -> FlextResult[None]:
        """Initialize the Oracle WMS client."""
        try:
            # Setup API client configuration
            api_config = FlextApiClientConfig(
                base_url=self.config.base_url,
                timeout=self.config.timeout,
                max_retries=self.config.max_retries,
                verify_ssl=self.config.verify_ssl,
            )

            # Get authentication headers
            if self._authenticator:
                auth_result = await self._authenticator.get_auth_headers()
                if not auth_result.success:
                    return FlextResult.fail(
                        f"Authentication failed: {auth_result.error}",
                    )
                if auth_result.data:
                    api_config.headers.update(auth_result.data)

            self._api_client = FlextApiClient(api_config)
            logger.info(
                "Oracle WMS client initialized",
                base_url=self.config.base_url,
                environment=self.config.environment,
                verify_ssl=self.config.verify_ssl,
            )
            return FlextResult.ok(None)

        except (
            ConnectionError,
            TimeoutError,
            OSError,
            TypeError,
            ValueError,
            AttributeError,
            RuntimeError,
        ) as e:
            return FlextResult.fail(f"Client initialization failed: {e}")

    # Back-compat: start/stop/health_check helpers expected by tests
    async def start(self) -> FlextResult[None]:
        init = await self.initialize()
        if not init.success:
            return init
        # Ensure underlying HTTP session exists
        if self._api_client:
            await self._api_client.start()
        return FlextResult.ok(None)

    async def stop(self) -> FlextResult[None]:
        try:
            if self._api_client:
                await self._api_client.stop()
            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.fail(f"Stop failed: {e}")

    async def health_check(self) -> FlextResult[dict[str, object]]:
        if not self._api_client:
            return FlextResult.ok(
                {"status": "unhealthy", "error": "Client not initialized"}
            )
        health_data = self._api_client.health_check()
        return FlextResult.ok(dict(health_data))

    async def discover_entities(self) -> FlextResult[list[dict[str, object]]]:  # noqa: PLR0911
        """Discover available Oracle WMS entities."""
        try:
            if not self._api_client:
                return FlextResult.fail("Client not initialized")

            # Use mock server only when explicitly configured
            if getattr(self.config, "use_mock", False):
                mock_server = get_mock_server(self.config.environment)
                mock_result = mock_server.get_mock_response("entity_discovery")
                if mock_result.success and mock_result.data:
                    entities_data = mock_result.data.get("entities", [])
                    return FlextResult.ok(
                        entities_data if isinstance(entities_data, list) else [],
                    )
                return FlextResult.fail(f"Mock discovery failed: {mock_result.error}")

            # Real API discovery
            endpoint = FLEXT_ORACLE_WMS_APIS.get("entity_discovery")
            if not endpoint:
                return FlextResult.fail("Entity discovery endpoint not found")

            full_path = endpoint.get_full_path(self.config.environment)
            resp_result = await self._api_client.get(full_path)

            if not resp_result.success:
                return FlextResult.fail(f"Entity discovery failed: {resp_result.error}")

            api_resp = resp_result.data
            if api_resp is None:
                return FlextResult.fail(
                    "No HTTP response received from entity discovery"
                )

            if hasattr(api_resp, "is_success") and not api_resp.is_success():
                return FlextResult.fail(
                    f"Entity discovery failed: HTTP {getattr(api_resp, 'status_code', 'unknown')}",
                )

            body = api_resp.data if hasattr(api_resp, "data") else None
            if not isinstance(body, dict):
                return FlextResult.fail("Invalid entity discovery response format")

            entities = (
                body.get("entities", [])
                if isinstance(body.get("entities", []), list)
                else []
            )
            return FlextResult.ok(entities)  # type: ignore[arg-type]

        except (
            ConnectionError,
            TimeoutError,
            OSError,
            TypeError,
            ValueError,
            AttributeError,
            RuntimeError,
        ) as e:
            return FlextResult.fail(f"Discover entities failed: {e}")

    async def get_entity_data(  # noqa: PLR0911
        self,
        entity_name: TOracleWmsEntityName,
        params: dict[str, object] | None = None,
    ) -> FlextResult[list[dict[str, object]]]:
        """Get data for a specific Oracle WMS entity."""
        try:
            if not self._api_client:
                return FlextResult.fail("Client not initialized")

            # Use mock server only when explicitly configured
            if getattr(self.config, "use_mock", False):
                mock_server = get_mock_server(self.config.environment)
                mock_result = mock_server.get_mock_response("entity_data", entity_name)
                if mock_result.success and mock_result.data:
                    results_data = mock_result.data.get("results", [])
                    return FlextResult.ok(
                        results_data if isinstance(results_data, list) else [],
                    )
                return FlextResult.fail(f"Mock entity data failed: {mock_result.error}")

            # Real API call
            endpoint = FLEXT_ORACLE_WMS_APIS.get("lgf_entity_extract")
            if not endpoint:
                return FlextResult.fail("Entity extract endpoint not found")

            full_path = endpoint.get_full_path(self.config.environment)
            full_path = full_path.replace("{entity_name}", entity_name)

            resp_result = await self._api_client.get(full_path, params=params or {})

            if not resp_result.success:
                return FlextResult.fail(
                    f"Entity data extraction failed: {resp_result.error}",
                )

            api_resp = resp_result.data
            if api_resp is None:
                return FlextResult.fail(
                    "No HTTP response received from entity data API"
                )

            if hasattr(api_resp, "is_success") and not api_resp.is_success():
                return FlextResult.fail(
                    f"Entity data extraction failed: HTTP {getattr(api_resp, 'status_code', 'unknown')}",
                )

            body = api_resp.data if hasattr(api_resp, "data") else None
            if not isinstance(body, dict):
                return FlextResult.fail("Invalid entity data response format")

            results = (
                body.get("results", [])
                if isinstance(body.get("results", []), list)
                else []
            )
            return FlextResult.ok(results)  # type: ignore[arg-type]

        except (
            ConnectionError,
            TimeoutError,
            OSError,
            TypeError,
            ValueError,
            AttributeError,
            RuntimeError,
        ) as e:
            return FlextResult.fail(f"Get entity data for {entity_name} failed: {e}")

    async def call_api(
        self,
        api_name: str,
        **kwargs: object,
    ) -> FlextResult[dict[str, object]]:
        """Call a specific Oracle WMS API by name."""
        try:
            if not self._api_client:
                return FlextResult.fail("Client not initialized")

            endpoint = FLEXT_ORACLE_WMS_APIS.get(api_name)
            if not endpoint:
                return FlextResult.fail(f"Unknown API endpoint: {api_name}")

            # Prepare API call
            request = ApiCallRequest(api_name=api_name, kwargs=kwargs)
            prepared_call = self._prepare_api_call(endpoint, request)

            # Execute API call
            response = None
            if prepared_call.method.upper() == "GET":
                response = await self._api_client.get(
                    prepared_call.full_path,
                    params=prepared_call.params or {},
                )
            elif prepared_call.method.upper() == "POST":
                # Send JSON when dict provided, otherwise raw data
                json_payload = (
                    prepared_call.data if isinstance(prepared_call.data, dict) else None
                )
                data_payload = (
                    None
                    if json_payload is not None
                    else (
                        str(prepared_call.data)
                        if prepared_call.data is not None
                        else None
                    )
                )
                response = await self._api_client.post(
                    prepared_call.full_path,
                    json_data=json_payload,
                    data=data_payload,
                )
            else:
                return FlextResult.fail(
                    f"Unsupported HTTP method: {prepared_call.method}",
                )

            if not response or not response.success:
                return FlextResult.fail(
                    f"API call failed: {response.error if response else 'No response'}",
                )
            # Validate HTTP status and extract body
            api_resp = response.data
            if api_resp is None:
                return FlextResult.fail("Empty HTTP response")
            if hasattr(api_resp, "is_success") and not api_resp.is_success():
                return FlextResult.fail(
                    f"API call failed: HTTP {getattr(api_resp, 'status_code', 'unknown')}",
                )
            body = api_resp.data if hasattr(api_resp, "data") else None
            data_dict = body if isinstance(body, dict) else {}
            return FlextResult.ok(data_dict)

        except (
            ConnectionError,
            TimeoutError,
            OSError,
            TypeError,
            ValueError,
            AttributeError,
            RuntimeError,
        ) as e:
            return FlextResult.fail(f"Call API {api_name} failed: {e}")

    # Helper methods used by tests (parsing and listing)
    def _parse_entity_discovery_response(self, data: object) -> list[str]:
        if isinstance(data, dict):
            if "entities" in data and isinstance(data["entities"], list):
                return [
                    e if isinstance(e, str) else e.get("name", "")
                    for e in data["entities"]
                ]
            if "results" in data and isinstance(data["results"], list):
                names: list[str] = []
                for item in data["results"]:
                    if isinstance(item, str):
                        names.append(item)
                    elif isinstance(item, dict) and "name" in item:
                        names.append(str(item["name"]))
                return names
            return []
        if isinstance(data, list):
            return [str(x) for x in data]
        return []

    def _filter_valid_entities(self, entities: list[str]) -> list[str]:
        return [
            e for e in entities if isinstance(e, str) and e and not e.startswith("_")
        ]

    def get_available_apis(self) -> dict[str, str]:
        return {name: ep.path for name, ep in FLEXT_ORACLE_WMS_APIS.items()}

    def get_apis_by_category(
        self, category: FlextOracleWmsApiCategory
    ) -> dict[str, str]:
        return {
            name: ep.path
            for name, ep in FLEXT_ORACLE_WMS_APIS.items()
            if ep.category == category
        }

    # Minimal stubs for specialized WMS actions used in tests
    async def ship_oblpn(
        self, *_args: object, **kwargs: object
    ) -> FlextResult[dict[str, object]]:
        return await self.call_api("ship_oblpn", **kwargs)

    async def create_lpn(
        self, *_args: object, **kwargs: object
    ) -> FlextResult[dict[str, object]]:
        return await self.call_api("init_stage_interface", **kwargs)

    def _prepare_api_call(
        self,
        endpoint: FlextOracleWmsApiEndpoint,
        request: ApiCallRequest,
    ) -> PreparedApiCall:
        """Prepare API call with path substitution and parameter handling."""
        full_path = endpoint.get_full_path(self.config.environment)

        # Handle path parameter substitution
        if isinstance(request.path_params, dict):
            for param_name, param_value in request.path_params.items():
                full_path = full_path.replace(f"{{{param_name}}}", str(param_value))

        return PreparedApiCall(
            method=endpoint.method,
            full_path=full_path,
            data=request.data if isinstance(request.data, dict) else None,
            params=request.params if isinstance(request.params, dict) else None,
        )


class FlextOracleWmsClientMock:
    """Mock Oracle WMS client for testing."""

    def __init__(self, config: FlextOracleWmsClientConfig) -> None:
        """Initialize mock client."""
        self.config = config
        self.mock_server = get_mock_server(config.environment)

    async def discover_entities(self) -> FlextResult[list[dict[str, object]]]:
        """Mock entity discovery."""
        mock_result = self.mock_server.get_mock_response("entity_discovery")
        if mock_result.success and mock_result.data:
            entities_data = mock_result.data.get("entities", [])
            return FlextResult.ok(
                entities_data if isinstance(entities_data, list) else [],
            )
        return FlextResult.fail(f"Mock discovery failed: {mock_result.error}")

    async def get_entity_data(
        self,
        entity_name: TOracleWmsEntityName,
        params: dict[str, object] | None = None,
    ) -> FlextResult[list[dict[str, object]]]:
        """Mock entity data retrieval."""
        # Allow simple filtering via params in mock path to exercise parameter usage
        mock_result = self.mock_server.get_mock_response("entity_data", entity_name)
        if mock_result.success and mock_result.data:
            results_data = mock_result.data.get("results", [])
            if isinstance(results_data, list) and isinstance(params, dict):
                # Filter by optional "limit" parameter for demonstration
                limit_val = params.get("limit")
                try:
                    limit = (
                        int(limit_val) if isinstance(limit_val, (int, str)) else None
                    )
                except ValueError:
                    limit = None
                if limit is not None and limit >= 0:
                    results_data = results_data[:limit]
            return FlextResult.ok(
                results_data if isinstance(results_data, list) else [],
            )
        return FlextResult.fail(f"Mock entity data failed: {mock_result.error}")


# =============================================================================
# FACTORY FUNCTIONS
# =============================================================================


def create_oracle_wms_client(
    config: FlextOracleWmsClientConfig,
) -> FlextOracleWmsClient:
    """Create Oracle WMS client instance."""
    return FlextOracleWmsClient(config)


def flext_oracle_wms_create_basic_auth(
    username: str,
    password: str,
) -> FlextOracleWmsAuthConfig:
    """Create basic authentication configuration."""
    return FlextOracleWmsAuthConfig(
        auth_type=OracleWMSAuthMethod.BASIC,
        username=username,
        password=password,
    )


def flext_oracle_wms_create_bearer_auth(token: str) -> FlextOracleWmsAuthConfig:
    """Create bearer token authentication configuration."""
    return FlextOracleWmsAuthConfig(
        auth_type=OracleWMSAuthMethod.BEARER,
        token=token,
    )


def flext_oracle_wms_create_api_key_auth(api_key: str) -> FlextOracleWmsAuthConfig:
    """Create API key authentication configuration."""
    return FlextOracleWmsAuthConfig(
        auth_type=OracleWMSAuthMethod.API_KEY,
        api_key=api_key,
    )


# =============================================================================
# EXPORTS
# =============================================================================

__all__: list[str] = [
    # Authentication
    "FlextOracleWmsAuthConfig",
    "FlextOracleWmsAuthPlugin",
    "FlextOracleWmsAuthenticator",
    # Client
    "FlextOracleWmsClient",
    "FlextOracleWmsClientMock",
    # Factory Functions
    "create_oracle_wms_client",
    "flext_oracle_wms_create_api_key_auth",
    "flext_oracle_wms_create_basic_auth",
    "flext_oracle_wms_create_bearer_auth",
]
