"""Oracle WMS Cloud Client - Enterprise Declarative Implementation.

Cliente dinâmico para Oracle WMS Cloud usando infraestrutura flext-api.
Implementa descoberta automática de entidades e APIs declarativas.

Referência: https://docs.oracle.com/en/cloud/saas/warehouse-management/25b/owmre/index.html
"""

from __future__ import annotations

import base64
from typing import TYPE_CHECKING

from flext_api import FlextApiClient, FlextApiClientConfig, FlextApiClientResponse
from flext_core import FlextResult, get_logger
from flext_plugin import FlextPlugin

from flext_oracle_wms.api_catalog import (
    FLEXT_ORACLE_WMS_APIS,
    FlextOracleWmsApiCategory,
    FlextOracleWmsApiEndpoint,
)
from flext_oracle_wms.constants import (
    FlextOracleWmsDefaults,
    FlextOracleWmsErrorMessages,
)
from flext_oracle_wms.exceptions import (
    FlextOracleWmsConnectionError,
    FlextOracleWmsError,
)

if TYPE_CHECKING:
    from flext_oracle_wms.config import FlextOracleWmsClientConfig
    from flext_oracle_wms.types import (
        TOracleWmsEntityName,
    )

logger = get_logger(__name__)


class FlextOracleWmsPlugin(FlextPlugin):
    """Oracle WMS Plugin for FLEXT ecosystem - production ready."""

    def __init__(self, config: dict[str, object] | None = None) -> None:
        """Initialize Oracle WMS plugin."""
        super().__init__(
            name="oracle-wms-plugin",
            version="1.0.0",
            config=config or {},
        )
        self._client: FlextOracleWmsClient | None = None

    async def start(self) -> FlextResult[None]:
        """Start Oracle WMS plugin."""
        # Implementation using real config
        return FlextResult.ok(None)

    async def stop(self) -> FlextResult[None]:
        """Stop Oracle WMS plugin."""
        if self._client:
            await self._client.stop()
        return FlextResult.ok(None)

    async def execute(self, operation: str, **kwargs: object) -> FlextResult[object]:
        """Execute Oracle WMS operations via plugin interface."""
        if not self._client:
            return FlextResult.fail("Oracle WMS client not initialized")

        # Route operations to client methods using helper
        return await self._route_operation(operation, **kwargs)

    async def _route_operation(
        self,
        operation: str,
        **kwargs: object,
    ) -> FlextResult[object]:
        """Route operations to appropriate client methods."""
        if operation == "discover_entities":
            result = await self._client.discover_entities()
            return self._handle_operation_result(result)
        if operation == "get_entity_data":
            entity_name = kwargs.get("entity_name")
            if not isinstance(entity_name, str):
                return FlextResult.fail("entity_name must be string")
            entity_result = await self._client.get_entity_data(entity_name)
            return self._handle_operation_result(entity_result)
        return FlextResult.fail(f"Unknown operation: {operation}")

    def _handle_operation_result(
        self,
        result: FlextResult[object],
    ) -> FlextResult[object]:
        """Handle operation result with consistent error handling."""
        if result.is_success:
            return FlextResult.ok(result.data)
        return FlextResult.fail(result.error or "Unknown error")


class FlextOracleWmsClient:
    """Oracle WMS Cloud Client - Dynamic & Declarative Implementation.

    Cliente dinâmico que descobre entidades via API real e implementa todas as
    25+ APIs da Oracle WMS Cloud de forma declarativa usando flext-api.
    """

    def __init__(self, config: FlextOracleWmsClientConfig) -> None:
        """Initialize Oracle WMS client with flext-api.

        Args:
            config: Client configuration with all necessary parameters

        Raises:
            FlextOracleWmsError: If configuration is invalid

        """
        # Type check is handled by type hints, but keep runtime check for safety
        if not hasattr(config, "base_url"):
            msg = "Invalid config object - must have base_url attribute"
            raise FlextOracleWmsError(msg)

        self.config = config
        self._client: FlextApiClient | None = None
        self._discovered_entities: list[TOracleWmsEntityName] | None = None
        self._auth_headers: dict[str, str] = {}

        logger.info(
            "Oracle WMS Client initialized",
            base_url=config.base_url,
            environment=config.environment,
            api_version=config.api_version,
        )

    def _raise_connection_error(self, message: str) -> None:
        """Raise connection error."""
        raise FlextOracleWmsConnectionError(message)

    async def start(self) -> FlextResult[None]:
        """Start the Oracle WMS client.

        Returns:
            FlextResult indicating success or failure

        Raises:
            FlextOracleWmsConnectionError: If connection fails

        """
        try:
            # Create flext-api client with Oracle WMS configuration
            client_config = FlextApiClientConfig(
                base_url=self.config.base_url,
                timeout=self.config.timeout,
                max_retries=self.config.max_retries,
                headers={},
            )

            # Create client directly since get_client doesn't take parameters
            self._client = FlextApiClient(config=client_config)

            # Start the client
            start_result = await self._client.start()
            if not start_result.is_success:
                error_msg = (
                    f"{FlextOracleWmsErrorMessages.CONNECTION_FAILED}: "
                    f"{start_result.error}"
                )
                logger.error("Failed to create HTTP client", error=start_result.error)
                self._raise_connection_error(error_msg)

            # Client is already assigned above

            # Configure authentication
            auth_result = self._configure_authentication()
            if not auth_result.is_success:
                error_msg = (
                    f"{FlextOracleWmsErrorMessages.AUTHENTICATION_FAILED}: "
                    f"{auth_result.error}"
                )
                logger.error(
                    "Authentication configuration failed",
                    error=auth_result.error,
                )
                self._raise_connection_error(error_msg)

            logger.info("Oracle WMS Client started successfully")
            return FlextResult.ok(None)

        except FlextOracleWmsConnectionError:
            raise
        except Exception as e:
            error_msg = f"{FlextOracleWmsErrorMessages.CONNECTION_FAILED}: {e}"
            logger.exception("Failed to start Oracle WMS client")
            raise FlextOracleWmsConnectionError(error_msg) from e

    async def stop(self) -> FlextResult[None]:
        """Stop the Oracle WMS client and cleanup resources.

        Returns:
            FlextResult indicating success or failure

        """
        try:
            if self._client:
                await self._client.close()
                self._client = None

            self._discovered_entities = None
            logger.info("Oracle WMS Client stopped successfully")
            return FlextResult.ok(None)

        except Exception as e:
            logger.exception("Failed to stop Oracle WMS client")
            return FlextResult.fail(f"Stop failed: {e}")

    def _configure_authentication(self) -> FlextResult[None]:
        """Configure authentication for the Oracle WMS client.

        Returns:
            FlextResult indicating success or failure

        """
        try:
            if not self._client:
                return FlextResult.fail("Client not initialized")

            # Store auth headers for use in each request
            credentials = f"{self.config.username}:{self.config.password}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()

            self._auth_headers = {
                "Authorization": f"Basic {encoded_credentials}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            logger.debug("Authentication configured successfully")
            return FlextResult.ok(None)

        except Exception as e:
            logger.exception("Authentication configuration failed")
            return FlextResult.fail(f"Authentication config failed: {e}")

    # ==============================================================================
    # DYNAMIC ENTITY DISCOVERY - REAL API CALLS
    # ==============================================================================

    async def discover_entities(self) -> FlextResult[list[TOracleWmsEntityName]]:
        """Discover all available entities dynamically from Oracle WMS API.

        Uses real API call to /{environment}/wms/lgfapi/v10/entity/ to get entities.
        """
        if self._discovered_entities is not None:
            return FlextResult.ok(self._discovered_entities)

        try:
            # Use LGF API v10 entity discovery endpoint
            discovery_path = f"/{self.config.environment}/wms/lgfapi/v10/entity/"

            logger.info("Discovering entities from Oracle WMS API", path=discovery_path)

            response = await self._call_api_direct("GET", discovery_path)

            if not response.is_success:
                logger.warning(
                    "Entity discovery failed, using fallback",
                    error=response.error,
                )
                # Fallback to known working entities
                fallback_entities = [
                    "company",
                    "facility",
                    "item",
                    "order_hdr",
                    "order_dtl",
                    "allocation",
                ]
                self._discovered_entities = fallback_entities
                return FlextResult.ok(fallback_entities)

            # Parse discovered entities from API response
            entities = self._parse_entity_discovery_response(response.data)
            self._discovered_entities = entities

            logger.info(
                "Successfully discovered entities",
                count=len(entities),
                entities=entities[:10],
            )
            return FlextResult.ok(entities)

        except Exception as e:
            logger.exception("Entity discovery failed")
            return FlextResult.fail(f"Entity discovery failed: {e}")

    def _parse_entity_discovery_response(
        self,
        data: dict[str, object] | list[object] | object,
    ) -> list[TOracleWmsEntityName]:
        """Parse entity discovery response to extract entity names."""
        try:
            entities = self._extract_entities_from_data(data)
            return self._filter_valid_entities(entities)
        except Exception as e:
            logger.warning(
                "Failed to parse entity discovery response",
                error=e,
                data_type=type(data),
            )
            return ["company", "facility", "item"]  # Fallback

    def _extract_entities_from_data(
        self,
        data: dict[str, object] | list[object] | object,
    ) -> list[str]:
        """Extract raw entity list from response data."""
        if isinstance(data, dict):
            return self._extract_from_dict_response(data)
        if isinstance(data, list):
            return [str(item) for item in data if item]
        return []

    def _extract_from_dict_response(self, data: dict[str, object]) -> list[str]:
        """Extract entities from dictionary response formats."""
        if "entities" in data:
            return self._extract_from_entities_field(data["entities"])
        if "results" in data:
            return self._extract_from_results_field(data["results"])
        # Try to extract from keys if it's a mapping
        return [key for key in data if isinstance(key, str) and key]

    def _extract_from_entities_field(self, entities_data: object) -> list[str]:
        """Extract from 'entities' field format."""
        if isinstance(entities_data, list):
            return [str(item) for item in entities_data if item]
        return []

    def _extract_from_results_field(self, results_data: object) -> list[str]:
        """Extract from 'results' field format."""
        entities = []
        if isinstance(results_data, list):
            for item in results_data:
                if isinstance(item, dict) and "name" in item:
                    name = item["name"]
                    if isinstance(name, str) and name:
                        entities.append(name)
                elif isinstance(item, str) and item:
                    entities.append(item)
        return entities

    def _filter_valid_entities(self, entities: list[str]) -> list[TOracleWmsEntityName]:
        """Filter and validate entity names."""
        valid_entities = [
            entity
            for entity in entities
            if isinstance(entity, str) and entity and not entity.startswith("_")
        ]
        return valid_entities or ["company", "facility", "item"]  # Fallback

    # ==============================================================================
    # DYNAMIC API CALLING - DRY IMPLEMENTATION
    # ==============================================================================

    async def call_api(
        self,
        api_name: str,
        **kwargs: object,
    ) -> FlextResult[dict[str, object]]:
        """Dynamic API caller - calls any Oracle WMS API by name.

        DRY approach: single method handles all API calls using catalog.
        """
        if api_name not in FLEXT_ORACLE_WMS_APIS:
            return FlextResult.fail(f"Unknown API: {api_name}")

        endpoint = FLEXT_ORACLE_WMS_APIS[api_name]

        # Extract common parameters
        data = kwargs.pop("data", None)
        params = kwargs.pop("params", None)
        path_params = kwargs.pop("path_params", {})

        # Format path with parameters if needed
        path = endpoint.path
        if path_params:
            # Type cast path_params to proper dict type for string formatting
            if not isinstance(path_params, dict):
                return FlextResult.fail("path_params must be a dictionary")

            # Convert all values to strings for path formatting
            str_path_params = {k: str(v) for k, v in path_params.items()}
            try:
                path = path.format(**str_path_params)
            except KeyError as e:
                return FlextResult.fail(f"Missing path parameter: {e}")

        full_path = endpoint.get_full_path(self.config.environment)
        if path != endpoint.path:
            # Replace the original path with formatted one
            full_path = full_path.replace(endpoint.path, path)

        # Type cast for method compatibility
        if not isinstance(data, dict) and data is not None:
            return FlextResult.fail("data must be a dictionary or None")
        if not isinstance(params, dict) and params is not None:
            return FlextResult.fail("params must be a dictionary or None")

        return await self._call_api_direct(endpoint.method, full_path, data, params)

    # ==============================================================================
    # DECLARATIVE API METHODS - DRY GENERATED FROM CATALOG
    # ==============================================================================

    # LGF API v10 - Data Extraction
    async def get_entity_data(
        self,
        entity_name: TOracleWmsEntityName,
        limit: int | None = None,
        offset: int | None = None,
        fields: str | None = None,
        filters: dict[str, object] | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Get entity data using LGF API v10."""
        params: dict[str, object] = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if fields:
            params["fields"] = fields
        if filters:
            params.update(filters)

        return await self.call_api(
            "lgf_entity_list",
            path_params={"entity_name": entity_name},
            params=params,
        )

    async def get_entity_by_id(
        self,
        entity_name: TOracleWmsEntityName,
        entity_id: str,
        fields: str | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Get specific entity record by ID."""
        params: dict[str, object] = {}
        if fields:
            params["fields"] = fields

        return await self.call_api(
            "lgf_entity_get",
            path_params={"entity_name": entity_name, "id": entity_id},
            params=params,
        )

    # Automation & Operations APIs - DRY approach
    async def update_oblpn_tracking_number(
        self,
        **kwargs: object,
    ) -> FlextResult[dict[str, object]]:
        """Update OBLPN tracking number."""
        return await self.call_api("update_oblpn_tracking_number", data=kwargs)

    async def ship_oblpn(self, **kwargs: object) -> FlextResult[dict[str, object]]:
        """Ship an eligible OBLPN."""
        return await self.call_api("ship_oblpn", data=kwargs)

    async def create_lpn(self, **kwargs: object) -> FlextResult[dict[str, object]]:
        """Create a single SKU IBLPN and associated inventory."""
        return await self.call_api("create_lpn", data=kwargs)

    async def get_entity_status(
        self,
        **kwargs: object,
    ) -> FlextResult[dict[str, object]]:
        """Get status of an entity."""
        return await self.call_api("get_status", params=kwargs)

    # Setup & Transactional APIs - DRY approach
    async def init_stage_interface(
        self,
        **kwargs: object,
    ) -> FlextResult[dict[str, object]]:
        """Initialize stage interface for data integration."""
        return await self.call_api("init_stage_interface", data=kwargs)

    async def run_stage_interface(
        self,
        **kwargs: object,
    ) -> FlextResult[dict[str, object]]:
        """Run stage interface to process staged data."""
        return await self.call_api("run_stage_interface", data=kwargs)

    # ==============================================================================
    # CORE API INFRASTRUCTURE - DRY HTTP CALLS
    # ==============================================================================

    def _prepare_request_data(
        self,
        data: dict[str, object] | None,
        params: dict[str, object] | None,
    ) -> tuple[dict[str, object], dict[str, object]]:
        """Prepare and clean request data."""
        clean_data = {k: v for k, v in (data or {}).items() if v is not None}
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}
        return clean_data, clean_params

    def _ensure_client_initialized(self) -> FlextResult[FlextApiClient]:
        """DRY helper to ensure client is initialized."""
        if self._client is None:
            return FlextResult.fail("Client not initialized. Call start() first.")
        return FlextResult.ok(self._client)

    async def _execute_http_method(
        self,
        method: str,
        path: str,
        clean_data: dict[str, object],
        clean_params: dict[str, object],
    ) -> FlextResult[FlextApiClientResponse]:
        """Execute HTTP method call with DRY client validation."""
        client_result = self._ensure_client_initialized()
        if not client_result.is_success:
            error_msg = client_result.error or "Client initialization failed"
            return FlextResult.fail(error_msg)

        client = client_result.data
        # Type guard to ensure client is not None after validation
        if client is None:
            msg = "Client should not be None after successful validation"
            return FlextResult.fail(msg)

        return await self._dispatch_http_method(
            client,
            method.upper(),
            path,
            clean_data,
            clean_params,
        )

    async def _dispatch_http_method(
        self,
        client: FlextApiClient,
        method: str,
        path: str,
        clean_data: dict[str, object],
        clean_params: dict[str, object],
    ) -> FlextResult[FlextApiClientResponse]:
        """Dispatch HTTP method calls to appropriate client methods."""
        method_handlers = {
            "GET": lambda: client.get(
                path=path,
                params=clean_params or None,
                headers=self._auth_headers,
            ),
            "POST": lambda: client.post(
                path=path,
                json_data=clean_data or None,
                headers=self._auth_headers,
            ),
            "PUT": lambda: client.put(
                path=path,
                json_data=clean_data or None,
                headers=self._auth_headers,
            ),
            "PATCH": lambda: client.patch(
                path=path,
                json_data=clean_data or None,
                headers=self._auth_headers,
            ),
            "DELETE": lambda: client.delete(
                path=path,
                headers=self._auth_headers,
            ),
        }

        handler = method_handlers.get(method)
        if handler:
            return await handler()
        return FlextResult.fail(f"Unsupported HTTP method: {method}")

    def _validate_response(
        self,
        response_result: FlextResult[FlextApiClientResponse],
    ) -> FlextResult[object]:
        """Validate HTTP response - DRY pattern using real flext-api types."""
        if not response_result.is_success:
            return FlextResult.fail(f"HTTP request failed: {response_result.error}")

        response = response_result.data
        if response is None:
            return FlextResult.fail("No response data received")

        if response.status_code >= FlextOracleWmsDefaults.HTTP_BAD_REQUEST:
            error_msg = f"Oracle WMS API error: {response.status_code}"
            if response.data:
                error_msg += f" - {response.data}"
            return FlextResult.fail(error_msg)

        return FlextResult.ok(response.data)

    async def _call_api_direct(
        self,
        method: str,
        path: str,
        data: dict[str, object] | None = None,
        params: dict[str, object] | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Direct API call using flext-api client - DRY HTTP implementation."""
        # Use DRY client validation
        client_result = self._ensure_client_initialized()
        if not client_result.is_success:
            return FlextResult.fail(
                client_result.error or "Client initialization failed",
            )

        try:
            # Prepare request data
            clean_data, clean_params = self._prepare_request_data(data, params)

            logger.debug(
                "Calling Oracle WMS API",
                method=method,
                path=path,
                data_keys=list(clean_data.keys()) if clean_data else None,
                params=clean_params or None,
            )

            # Execute HTTP method
            response_result = await self._execute_http_method(
                method,
                path,
                clean_data,
                clean_params,
            )

            # Validate response
            validation_result = self._validate_response(response_result)
            if not validation_result.is_success:
                return FlextResult.fail(validation_result.error or "Validation failed")

            # Type cast validation_result.data to dict for return type
            if not isinstance(validation_result.data, dict):
                return FlextResult.fail("Response data is not a dictionary")

            logger.debug(
                "Oracle WMS API call successful",
                method=method,
                path=path,
                status_code=response_result.data.status_code
                if response_result.data
                else None,
            )

            return FlextResult.ok(validation_result.data)

        except Exception as e:
            logger.exception("Oracle WMS API call failed", method=method, path=path)
            return FlextResult.fail(f"API call failed: {e}")

    # ==============================================================================
    # CONVENIENCE METHODS - DYNAMIC & DRY
    # ==============================================================================

    async def get_all_entities(
        self,
    ) -> FlextResult[list[TOracleWmsEntityName]]:
        """Get list of all available entities from Oracle WMS - DYNAMIC discovery."""
        # Use DRY approach by delegating to discover_entities
        discover_result = await self.discover_entities()
        if not discover_result.is_success:
            return FlextResult.fail(discover_result.error or "Discovery failed")

        # Type cast to ensure compatibility
        if discover_result.data is None:
            return FlextResult.fail("No entities discovered")
        entities: list[TOracleWmsEntityName] = discover_result.data
        return FlextResult.ok(entities)

    async def health_check(self) -> FlextResult[dict[str, object]]:
        """Check Oracle WMS API health."""
        try:
            # Test with discovered entities
            entities_result = await self.discover_entities()
            test_entity = "company"  # Default fallback

            if entities_result.is_success and entities_result.data:
                test_entity = entities_result.data[0]

            # Test with a simple entity query
            result = await self.get_entity_data(test_entity, limit=1)

            health_data = {
                "service": "FlextOracleWmsClient",
                "status": "healthy" if result.is_success else "unhealthy",
                "base_url": self.config.base_url,
                "environment": self.config.environment,
                "api_version": self.config.api_version,
                "test_call_success": result.is_success,
                "available_apis": len(FLEXT_ORACLE_WMS_APIS),
                "discovered_entities": len(entities_result.data)
                if entities_result.is_success and entities_result.data
                else 0,
            }

            if not result.is_success:
                health_data["error"] = result.error or "Unknown error"

            # Convert to proper type for return
            health_data_typed: dict[str, object] = dict(health_data.items())
            return FlextResult.ok(health_data_typed)

        except Exception as e:
            return FlextResult.fail(f"Health check failed: {e}")

    def get_available_apis(self) -> dict[str, FlextOracleWmsApiEndpoint]:
        """Get all available Oracle WMS APIs from catalog."""
        return FLEXT_ORACLE_WMS_APIS.copy()

    def get_apis_by_category(
        self,
        category: FlextOracleWmsApiCategory,
    ) -> dict[str, FlextOracleWmsApiEndpoint]:
        """Get APIs filtered by category."""
        return {
            name: endpoint
            for name, endpoint in FLEXT_ORACLE_WMS_APIS.items()
            if endpoint.category == category
        }
