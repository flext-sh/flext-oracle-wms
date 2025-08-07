"""Oracle WMS Plugin Implementation - Clean Architecture Plugin Implementation.

This module implements the clean plugin architecture for Oracle WMS, providing
proper separation between abstract interfaces and concrete implementations.
Follows the principles established in flext-core interfaces.

Key Components:
    - FlextOracleWmsPlugin: Main implementation of FlextPlugin interface from flext-core
    - FlextOracleWmsDataPlugin: Data-specific plugin implementation extending FlextDataPlugin
    - FlextOracleWmsPluginContext: Context provider for plugin runtime
    - FlextOracleWmsPluginRegistry: Registry implementation for plugin management

Architecture:
    - Implements flext-core interfaces without mixing concrete domain logic
    - Maintains backward compatibility with existing flext-oracle-wms APIs
    - Provides clean separation between abstractions and implementations
    - NO DEPENDENCY on flext-plugin for clean architecture compliance

Example:
    >>> from flext_oracle_wms.plugin_implementation import FlextOracleWmsPlugin
    >>>
    >>> # Create plugin directly using flext-core patterns
    >>> plugin = FlextOracleWmsPlugin(name="oracle-wms", version="0.9.0")
    >>>
    >>> # Initialize and use plugin
    >>> context = FlextOracleWmsPluginContext(
    ...     config={"base_url": "https://wms.oracle.com"}
    ... )
    >>> result = plugin.initialize(context)

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING

from flext_core import FlextResult, get_logger
from flext_core.interfaces import (
    FlextDataPlugin,
    FlextPlugin,
    FlextPluginContext,
)

from flext_oracle_wms.client import FlextOracleWmsClient
from flext_oracle_wms.config import FlextOracleWmsClientConfig

if TYPE_CHECKING:
    from structlog.stdlib import BoundLogger

logger = get_logger(__name__)


# =============================================================================
# ORACLE WMS PLUGIN IMPLEMENTATION - FLEXT-CORE INTERFACE COMPLIANCE
# =============================================================================


class FlextOracleWmsPlugin(FlextPlugin):
    """Oracle WMS plugin implementation using flext-core FlextPlugin interface.

    COMPLIANCE: Pure implementation of FlextPlugin from flext-core, no mixing with flext-plugin.
    NO MIXING: Uses only flext-core interfaces and Oracle WMS client functionality.

    This class provides Oracle WMS-specific functionality while maintaining clean
    architecture boundaries without depending on flext-plugin domain entities.

    Architecture:
        - Implements FlextPlugin interface from flext-core
        - Uses FlextOracleWmsClient for Oracle WMS operations
        - Provides Oracle WMS-specific functionality (discovery, validation)
        - No mixing with flext-plugin domain entities

    Example:
        >>> plugin = FlextOracleWmsPlugin(name="oracle-wms", version="0.9.0")
        >>> config = {"base_url": "https://wms.oracle.com", "username": "user"}
        >>> result = plugin.validate_config(config)

    """

    def __init__(
        self,
        name: str,
        version: str,
        *,
        client_config: FlextOracleWmsClientConfig | None = None,
        client: FlextOracleWmsClient | None = None,
    ) -> None:
        """Initialize Oracle WMS plugin with basic information.

        Args:
            name: Plugin name for identification
            version: Plugin version string
            client_config: Oracle WMS client configuration
            client: Pre-configured Oracle WMS client instance

        """
        self._name = name
        self._version = version
        self._client_config = client_config
        self._client = client
        self._context: FlextOracleWmsPluginContext | None = None
        self._logger = get_logger(f"FlextOracleWmsPlugin.{name}")

    @property
    def name(self) -> str:
        """Get the unique plugin name from abstract interface."""
        return self._name

    @property
    def version(self) -> str:
        """Get the plugin version from abstract interface."""
        return self._version

    @property
    def client(self) -> FlextOracleWmsClient | None:
        """Get the Oracle WMS client instance."""
        return self._client

    def initialize(self, context: FlextPluginContext) -> FlextResult[None]:
        """Initialize plugin with provided context.

        Args:
            context: Plugin context providing logger, config, and services

        Returns:
            FlextResult indicating success or initialization failure

        """
        try:
            # Store context for later use
            self._context = FlextOracleWmsPluginContext.from_plugin_context(context)

            # Initialize client if not provided
            if self._client is None:
                if self._client_config is None:
                    # Try to create config from context
                    config_result = self._create_config_from_context(context)
                    if not config_result.success:
                        return FlextResult.fail(
                            f"Failed to create Oracle WMS config: {config_result.error}",
                        )
                    self._client_config = config_result.data

                # Create client
                try:
                    self._client = FlextOracleWmsClient(self._client_config)
                except Exception as e:
                    return FlextResult.fail(f"Failed to create Oracle WMS client: {e}")

            # Note: Client will be started when first used
            # This allows synchronous initialization as required by interface

            self._logger.info(
                "Oracle WMS plugin initialized successfully", plugin_name=self.name,
            )
            return FlextResult.ok(None)

        except Exception as e:
            self._logger.exception(
                "Oracle WMS plugin initialization failed", plugin_name=self.name,
            )
            return FlextResult.fail(f"Plugin initialization failed: {e}")

    def shutdown(self) -> FlextResult[None]:
        """Shutdown plugin and release resources from abstract interface.

        Returns:
            FlextResult indicating success or shutdown errors

        """
        try:
            # Note: Client cleanup would be handled by the client's destructor
            # or through explicit async shutdown methods if available

            # Clear context
            self._context = None

            self._logger.info(
                "Oracle WMS plugin shutdown successfully", plugin_name=self.name,
            )
            return FlextResult.ok(None)

        except Exception as e:
            self._logger.exception(
                "Oracle WMS plugin shutdown failed", plugin_name=self.name,
            )
            return FlextResult.fail(f"Plugin shutdown failed: {e}")

    def validate_config(self, config: Mapping[str, object]) -> FlextResult[None]:
        """Validate plugin configuration for Oracle WMS.

        Args:
            config: Configuration to validate

        Returns:
            FlextResult indicating validation success or errors

        """
        try:
            # Consolidated validation to reduce return statements
            validation_errors = []

            # Basic validation - config should be a mapping
            if not isinstance(config, Mapping):
                validation_errors.append("Configuration must be a mapping")

            # Oracle WMS-specific validation
            required_fields = ["base_url", "username", "password"]
            missing_fields = [field for field in required_fields if field not in config]
            if missing_fields:
                validation_errors.append(
                    f"Missing required Oracle WMS fields: {missing_fields}",
                )

            # Validate field types
            field_validations = [
                (
                    "base_url",
                    lambda v: isinstance(v, str) and v.strip(),
                    "base_url must be a non-empty string",
                ),
                (
                    "username",
                    lambda v: isinstance(v, str) and v.strip(),
                    "username must be a non-empty string",
                ),
                (
                    "password",
                    lambda v: isinstance(v, str) and v.strip(),
                    "password must be a non-empty string",
                ),
            ]

            for field, validator, error_msg in field_validations:
                if field in config and not validator(config[field]):
                    validation_errors.append(error_msg)

            # Optional field validation
            if "environment" in config and not isinstance(config["environment"], str):
                validation_errors.append("environment must be a string")

            if "timeout" in config:
                timeout = config["timeout"]
                if not isinstance(timeout, (int, float)) or timeout <= 0:
                    validation_errors.append("timeout must be a positive number")

            if validation_errors:
                return FlextResult.fail("; ".join(validation_errors))

            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Config validation failed: {e}")

    def test_connection(self) -> FlextResult[None]:
        """Test connection to Oracle WMS system.

        Returns:
            FlextResult indicating connection success or failure

        """
        try:
            if not self._client:
                return FlextResult.fail("Oracle WMS client not initialized")

            # Note: This is a synchronous interface, so we can't perform async health check
            # This would need to be implemented differently, perhaps with a connection pool
            # or by checking client configuration instead of actual connectivity

            # For now, we'll just validate that the client is properly configured
            if hasattr(self._client, "config") and self._client.config:
                self._logger.info(
                    "Oracle WMS client configuration validated", plugin_name=self.name,
                )
                return FlextResult.ok(None)

            return FlextResult.fail("Oracle WMS client not properly configured")

        except Exception as e:
            self._logger.exception(
                "Oracle WMS connection test error", plugin_name=self.name,
            )
            return FlextResult.fail(f"Connection test failed: {e}")

    async def discover_entities(self) -> FlextResult[list[str]]:
        """Discover available Oracle WMS entities.

        Note: This is an Oracle WMS-specific extension method using async operations.

        Returns:
            FlextResult containing list of discovered entities

        """
        try:
            if not self._client:
                return FlextResult.fail("Oracle WMS client not initialized")

            self._logger.info(
                "Starting Oracle WMS entity discovery", plugin_name=self.name,
            )

            try:
                # Execute discovery
                result = await self._client.discover_entities()

                if result.success:
                    self._logger.info(
                        "Oracle WMS entity discovery successful",
                        plugin_name=self.name,
                        entity_count=len(result.data),
                    )
                    return FlextResult.ok(result.data)

                self._logger.warning(
                    "Oracle WMS entity discovery failed",
                    plugin_name=self.name,
                    error=result.error,
                )
                return FlextResult.fail(f"Entity discovery failed: {result.error}")

            except Exception:
                self._logger.exception(
                    "Oracle WMS discovery exception", plugin_name=self.name,
                )
                raise

        except Exception as e:
            self._logger.exception(
                "Oracle WMS entity discovery error", plugin_name=self.name,
            )
            return FlextResult.fail(f"Entity discovery error: {e}")

    async def get_entity_data(
        self,
        entity_name: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Extract data from Oracle WMS entity.

        Note: This is an Oracle WMS-specific extension method that goes beyond
        the base FlextDataPlugin interface. It's async because it makes network calls.

        Args:
            entity_name: Name of the entity to extract
            limit: Maximum number of records to return
            offset: Offset for pagination

        Returns:
            FlextResult containing extracted data

        """
        try:
            if not self._client:
                return FlextResult.fail("Oracle WMS client not initialized")

            try:
                # Execute extraction
                result = await self._client.get_entity_data(
                    entity_name=entity_name,
                    limit=limit,
                    offset=offset,
                )

                if result.success:
                    self._logger.info(
                        "Oracle WMS data extraction successful",
                        plugin_name=self.name,
                        entity_name=entity_name,
                    )
                    return FlextResult.ok(result.data)

                self._logger.warning(
                    "Oracle WMS data extraction failed",
                    plugin_name=self.name,
                    entity_name=entity_name,
                    error=result.error,
                )
                return FlextResult.fail(f"Data extraction failed: {result.error}")

            except Exception:
                self._logger.exception(
                    "Oracle WMS data extraction exception",
                    plugin_name=self.name,
                    entity_name=entity_name,
                )
                raise

        except Exception as e:
            self._logger.exception(
                "Oracle WMS data extraction error",
                plugin_name=self.name,
                entity_name=entity_name,
            )
            return FlextResult.fail(f"Data extraction error: {e}")

    def _create_config_from_context(
        self,
        context: FlextPluginContext,
    ) -> FlextResult[FlextOracleWmsClientConfig]:
        """Create Oracle WMS client configuration from plugin context.

        Args:
            context: Plugin context containing configuration

        Returns:
            FlextResult containing client configuration

        """
        try:
            config_dict = dict(context.config)

            # Create client configuration
            client_config = FlextOracleWmsClientConfig(
                base_url=config_dict.get("base_url", ""),
                username=config_dict.get("username", ""),
                password=config_dict.get("password", ""),
                environment=config_dict.get("environment", "wms"),
                api_version=config_dict.get("api_version", "v10"),
                timeout=config_dict.get("timeout", 30.0),
                max_retries=config_dict.get("max_retries", 3),
            )

            return FlextResult.ok(client_config)

        except Exception as e:
            return FlextResult.fail(f"Failed to create config from context: {e}")


class FlextOracleWmsDataPlugin(FlextDataPlugin):
    """Oracle WMS data plugin implementation extending FlextDataPlugin interface.

    COMPLIANCE: Extends FlextDataPlugin from flext-core for data operations.
    NO MIXING: Pure implementation without mixing domain logic.

    This class extends the basic plugin with data-specific capabilities like
    configuration validation and connection testing required by data plugins.

    Architecture:
        - Extends FlextDataPlugin interface from flext-core
        - Uses FlextOracleWmsClient for actual data operations
        - Provides Oracle WMS-specific data plugin functionality
        - Clean separation between interface and implementation
    """

    def __init__(
        self,
        name: str,
        version: str,
        *,
        client_config: FlextOracleWmsClientConfig | None = None,
        client: FlextOracleWmsClient | None = None,
    ) -> None:
        """Initialize Oracle WMS data plugin.

        Args:
            name: Plugin name for identification
            version: Plugin version string
            client_config: Oracle WMS client configuration
            client: Pre-configured Oracle WMS client instance

        """
        # Use composition with the basic plugin
        self._basic_plugin = FlextOracleWmsPlugin(
            name=name,
            version=version,
            client_config=client_config,
            client=client,
        )

    @property
    def name(self) -> str:
        """Get plugin name from FlextPlugin interface."""
        return self._basic_plugin.name

    @property
    def version(self) -> str:
        """Get plugin version from FlextPlugin interface."""
        return self._basic_plugin.version

    def initialize(self, context: FlextPluginContext) -> FlextResult[None]:
        """Initialize plugin from FlextPlugin interface."""
        return self._basic_plugin.initialize(context)

    def shutdown(self) -> FlextResult[None]:
        """Shutdown plugin from FlextPlugin interface."""
        return self._basic_plugin.shutdown()

    def validate_config(self, config: Mapping[str, object]) -> FlextResult[None]:
        """Validate plugin configuration from FlextDataPlugin interface."""
        return self._basic_plugin.validate_config(config)

    def test_connection(self) -> FlextResult[None]:
        """Test connection from FlextDataPlugin interface."""
        return self._basic_plugin.test_connection()

    # Oracle WMS-specific methods
    async def discover_entities(self) -> FlextResult[list[str]]:
        """Discover available Oracle WMS entities."""
        return await self._basic_plugin.discover_entities()

    async def get_entity_data(
        self,
        entity_name: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Extract data from Oracle WMS entity."""
        return await self._basic_plugin.get_entity_data(entity_name, limit, offset)

    @property
    def client(self) -> FlextOracleWmsClient | None:
        """Get the Oracle WMS client instance."""
        return self._basic_plugin.client


class FlextOracleWmsPluginContext:
    """Oracle WMS-specific plugin context implementation.

    Provides plugins with access to Oracle WMS-specific services, configuration,
    and logging. Implements the FlextPluginContext protocol.
    """

    def __init__(
        self,
        *,
        logger: BoundLogger,
        config: Mapping[str, object],
        services: dict[str, object] | None = None,
    ) -> None:
        """Initialize Oracle WMS plugin context.

        Args:
            logger: Structured logger for plugin
            config: Plugin configuration
            services: Available services for plugin

        """
        self._logger = logger
        self._config = config
        self._services = services or {}

    @property
    def logger(self) -> BoundLogger:
        """Get logger for plugin."""
        return self._logger

    @property
    def config(self) -> Mapping[str, object]:
        """Get plugin configuration."""
        return self._config

    def get_service(self, service_name: str) -> FlextResult[object]:
        """Get service by name from container.

        Args:
            service_name: Name of service to retrieve

        Returns:
            FlextResult with service instance or not found error

        """
        if service_name in self._services:
            return FlextResult.ok(self._services[service_name])

        return FlextResult.fail(f"Service '{service_name}' not found")

    @classmethod
    def from_plugin_context(
        cls,
        context: FlextPluginContext,
    ) -> FlextOracleWmsPluginContext:
        """Create Oracle WMS context from generic plugin context.

        Args:
            context: Generic plugin context

        Returns:
            Oracle WMS-specific plugin context

        """
        return cls(
            logger=context.logger,
            config=context.config,
        )


class FlextOracleWmsPluginRegistry:
    """Oracle WMS-specific plugin registry implementation.

    COMPLIANCE: Implements FlextPluginRegistry protocol from flext-core.
    NO MIXING: Pure implementation without dependency on external domain entities.

    Simple plugin registry for managing Oracle WMS plugins using only
    in-memory storage with flext-core patterns.
    """

    def __init__(self) -> None:
        """Initialize Oracle WMS plugin registry."""
        self._plugins: dict[str, FlextPlugin] = {}
        self._logger = get_logger(f"{self.__class__.__name__}")

    def register(self, plugin: FlextPlugin) -> FlextResult[None]:
        """Register a plugin.

        Args:
            plugin: Plugin instance to register

        Returns:
            FlextResult indicating registration success or failure

        """
        try:
            if plugin.name in self._plugins:
                return FlextResult.fail(f"Plugin '{plugin.name}' already registered")

            self._plugins[plugin.name] = plugin
            self._logger.info("Plugin registered", plugin_name=plugin.name)
            return FlextResult.ok(None)

        except Exception as e:
            self._logger.exception(
                "Plugin registration failed",
                plugin_name=plugin.name if plugin else "unknown",
            )
            return FlextResult.fail(f"Plugin registration failed: {e}")

    def unregister(self, plugin_name: str) -> FlextResult[None]:
        """Unregister a plugin by name.

        Args:
            plugin_name: Name of plugin to unregister

        Returns:
            FlextResult indicating success or not found error

        """
        try:
            if plugin_name not in self._plugins:
                return FlextResult.fail(f"Plugin '{plugin_name}' not found")

            plugin = self._plugins.pop(plugin_name)

            # Try to shutdown the plugin if it supports it
            try:
                shutdown_result = plugin.shutdown()
                if not shutdown_result.success:
                    self._logger.warning(
                        "Plugin shutdown failed during unregister",
                        plugin_name=plugin_name,
                        error=shutdown_result.error,
                    )
            except Exception as e:
                self._logger.warning(
                    "Plugin shutdown error during unregister",
                    plugin_name=plugin_name,
                    error=str(e),
                )

            self._logger.info("Plugin unregistered", plugin_name=plugin_name)
            return FlextResult.ok(None)

        except Exception as e:
            self._logger.exception(
                "Plugin unregistration failed", plugin_name=plugin_name,
            )
            return FlextResult.fail(f"Plugin unregistration failed: {e}")

    def get_plugin(self, plugin_name: str) -> FlextResult[FlextPlugin]:
        """Get plugin by name.

        Args:
            plugin_name: Name of plugin to retrieve

        Returns:
            FlextResult containing plugin or not found error

        """
        if plugin_name in self._plugins:
            return FlextResult.ok(self._plugins[plugin_name])

        return FlextResult.fail(f"Plugin '{plugin_name}' not found")

    def list_plugins(self) -> list[str]:
        """List all registered plugin names.

        Returns:
            List of registered plugin names

        """
        return list(self._plugins.keys())


# Factory functions for clean instantiation


def create_oracle_wms_data_plugin(
    name: str,
    version: str,
    *,
    _description: str = "",
    client_config: FlextOracleWmsClientConfig | None = None,
) -> FlextResult[FlextOracleWmsDataPlugin]:
    """Create an Oracle WMS data plugin using flext-core patterns.

    Args:
        name: Plugin name
        version: Plugin version
        _description: Plugin description (currently unused)
        client_config: Oracle WMS client configuration

    Returns:
        FlextResult containing the created plugin or error

    """
    try:
        # Create plugin implementation using only flext-core interfaces
        plugin = FlextOracleWmsDataPlugin(
            name=name,
            version=version,
            client_config=client_config,
        )

        return FlextResult.ok(plugin)

    except Exception as e:
        return FlextResult.fail(f"Failed to create Oracle WMS data plugin: {e}")


def create_oracle_wms_plugin_registry() -> FlextResult[FlextOracleWmsPluginRegistry]:
    """Create an Oracle WMS plugin registry using flext-core patterns.

    Returns:
        FlextResult containing the created registry or error

    """
    try:
        # Create registry implementation using only flext-core patterns
        registry = FlextOracleWmsPluginRegistry()

        return FlextResult.ok(registry)

    except Exception as e:
        return FlextResult.fail(f"Failed to create Oracle WMS registry: {e}")
