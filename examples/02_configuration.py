"""Example: Oracle WMS Configuration Management.

This example demonstrates WORKING configuration patterns for Oracle WMS Cloud
integration using the ACTUAL API that exists and functions properly.

"""

import contextlib
import os
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from flext_core import FlextLogger
from flext_oracle_wms import (
    FlextOracleWmsClient,
    FlextOracleWmsClientConfig,
)
from flext_oracle_wms.constants import FlextOracleWmsConstants

# Initialize logger
logger = FlextLogger(__name__)


class Environment(StrEnum):
    """Oracle WMS deployment environments."""

    DEVELOPMENT = "dev"
    STAGING = "staging"
    PRODUCTION = "prod"


@dataclass
class WmsEnvironmentConfig:
    """Environment-specific Oracle WMS configuration."""

    name: str
    base_url: str
    timeout: float = FlextOracleWmsConstants.Connection.DEFAULT_TIMEOUT
    max_retries: int = FlextOracleWmsConstants.Connection.DEFAULT_MAX_RETRIES


def get_environment_configs() -> dict[Environment, WmsEnvironmentConfig]:
    """Define environment-specific Oracle WMS configurations."""
    return {
        Environment.DEVELOPMENT: WmsEnvironmentConfig(
            name="Development",
            base_url="https://dev-wms.oraclecloud.com/dev_env",
            timeout=FlextOracleWmsConstants.Connection.DEFAULT_TIMEOUT,
            max_retries=FlextOracleWmsConstants.Connection.DEFAULT_MAX_RETRIES,
        ),
        Environment.STAGING: WmsEnvironmentConfig(
            name="Staging",
            base_url="https://staging-wms.oraclecloud.com/staging_env",
            timeout=FlextOracleWmsConstants.Connection.DEFAULT_TIMEOUT,
            max_retries=FlextOracleWmsConstants.Connection.DEFAULT_MAX_RETRIES,
        ),
        Environment.PRODUCTION: WmsEnvironmentConfig(
            name="Production",
            base_url="https://prod-wms.oraclecloud.com/prod_env",
            timeout=FlextOracleWmsConstants.Connection.DEFAULT_TIMEOUT,
            max_retries=FlextOracleWmsConstants.Connection.DEFAULT_MAX_RETRIES,
        ),
    }


def create_config_from_environment() -> FlextOracleWmsClientConfig:
    """Create Oracle WMS client configuration from environment variables.

    This uses the REAL .env file with working Oracle WMS credentials.

    Returns:
      FlextOracleWmsClientConfig configured from environment

    Raises:
      ValueError: If required environment variables are missing

    """
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    if env_file.exists():
        load_dotenv(env_file)

    # Get required values
    base_url = os.getenv("ORACLE_WMS_BASE_URL")
    username = os.getenv("ORACLE_WMS_USERNAME")
    password = os.getenv("ORACLE_WMS_PASSWORD")
    environment = os.getenv("ORACLE_WMS_ENVIRONMENT")

    if not all([base_url, username, password, environment]):
        missing = [
            name
            for name, value in [
                ("ORACLE_WMS_BASE_URL", base_url),
                ("ORACLE_WMS_USERNAME", username),
                ("ORACLE_WMS_PASSWORD", password),
                ("ORACLE_WMS_ENVIRONMENT", environment),
            ]
            if not value
        ]
        msg = f"Missing required environment variables: {', '.join(missing)}"
        raise ValueError(msg)

    # Method 1: Use global singleton with environment variables
    # The config automatically loads from environment variables
    env_config = FlextOracleWmsClientConfig.get_global_instance()

    # Validate that required fields are set from environment
    if (
        env_config.oracle_wms_username
        and env_config.oracle_wms_password.get_secret_value()
    ):
        return env_config

    # Method 2: Fallback to default configuration
    # if environment variables are not set
    return FlextOracleWmsClientConfig.create_default()


def create_demo_config() -> FlextOracleWmsClientConfig:
    """Create a demo Oracle WMS configuration using singleton pattern.

    Returns:
      FlextOracleWmsClientConfig with demo values

    Note:
      This demonstrates how to use the global singleton with parameter overrides.

    """
    # Use global singleton with demo parameters
    return FlextOracleWmsClientConfig.create_for_environment(
        "demo",
        oracle_wms_base_url="https://demo-wms.oraclecloud.com/demo",
        oracle_wms_username="demo_user",
        oracle_wms_password="demo_password",
        api_version="LGF_V10",
        oracle_wms_timeout=FlextOracleWmsConstants.Connection.DEFAULT_TIMEOUT,
        oracle_wms_max_retries=FlextOracleWmsConstants.Connection.DEFAULT_MAX_RETRIES,
        oracle_wms_verify_ssl=True,
        oracle_wms_enable_logging=True,
    )


def validate_configuration(config: FlextOracleWmsClientConfig) -> dict[str, Any]:
    """Validate Oracle WMS client configuration.

    Args:
      config: Oracle WMS client configuration to validate

    Returns:
      Dictionary containing validation results

    """
    errors: list[str] = []
    warnings: list[str] = []
    config_summary: dict[str, Any] = {}

    # Validate base URL
    if not config.oracle_wms_base_url:
        errors.append("Base URL is required")
    elif not config.oracle_wms_base_url.startswith("https://"):
        warnings.append("Base URL should use HTTPS for security")

    # Validate authentication
    if not config.oracle_wms_username or not config.oracle_wms_password:
        errors.append("Username and password are required")

    # Constants for validation
    min_timeout_seconds = (
        FlextOracleWmsConstants.Connection.DEFAULT_TIMEOUT // 3
    )  # Minimum timeout threshold

    # Validate timeouts and retries
    if config.oracle_wms_timeout <= 0:
        errors.append("Timeout must be positive")
    elif config.oracle_wms_timeout < min_timeout_seconds:
        warnings.append("Timeout less than 10 seconds may cause issues")

    # Constants for validation
    max_retries_warning_threshold = (
        FlextOracleWmsConstants.Connection.DEFAULT_MAX_RETRIES * 3
    )  # High retry count threshold

    if config.oracle_wms_max_retries < 0:
        errors.append("Max retries cannot be negative")
    elif config.oracle_wms_max_retries > max_retries_warning_threshold:
        warnings.append("High retry count may cause delays")

    # Create configuration summary
    config_summary = {
        "base_url": config.oracle_wms_base_url,
        "username": config.oracle_wms_username,
        "api_version": config.api_version,
        "timeout": config.oracle_wms_timeout,
        "max_retries": config.oracle_wms_max_retries,
        "verify_ssl": config.oracle_wms_verify_ssl,
        "enable_logging": config.oracle_wms_enable_logging,
    }

    validation_results: dict[str, Any] = {
        "valid": len(errors) == 0,
        "warnings": warnings,
        "errors": errors,
        "configuration_summary": config_summary,
    }

    return validation_results


def test_configuration(
    config: FlextOracleWmsClientConfig,
) -> dict[str, Any]:
    """Test Oracle WMS configuration by attempting connection.

    Args:
      config: Configuration to test

    Returns:
      Dictionary with test results

    """
    test_results: dict[str, Any] = {
        "connection_success": False,
        "health_check_success": False,
        "error": None,
        "entities_discovered": 0,
    }

    client = FlextOracleWmsClient(config)

    try:
        # Test connection
        client.start()
        test_results["connection_success"] = True

        # Test health check
        health_result = client.health_check()
        if health_result.is_success:
            test_results["health_check_success"] = True

        # Test entity discovery
        entities_result = client.discover_entities()
        if entities_result.is_success and entities_result.value:
            test_results["entities_discovered"] = len(entities_result.value)

    except Exception as e:
        test_results["error"] = str(e)
    finally:
        client.stop()

    return test_results


def demonstrate_configuration_patterns() -> None:
    """Demonstrate working Oracle WMS configuration patterns."""
    # Pattern 1: Environment-driven configuration (REAL)
    try:
        env_config = create_config_from_environment()
        validation = validate_configuration(env_config)

        warnings = validation.get("warnings", [])
        if warnings and isinstance(warnings, list):
            for _warning in warnings:
                pass

        if validation["valid"]:
            pass
        else:
            errors = validation.get("errors", [])
            if errors and isinstance(errors, list):
                for _error in errors:
                    pass

    except ValueError:
        pass

    # Pattern 2: Demo configuration
    try:
        demo_config = create_demo_config()
        validation = validate_configuration(demo_config)

        if validation["warnings"]:
            for _warning in validation["warnings"]:
                pass

    except Exception as e:
        logger.warning(f"Configuration validation failed: {e}")

    # Pattern 3: Environment-specific configurations
    env_configs = get_environment_configs()

    for _config in env_configs.values():
        pass


def main() -> None:
    """Main function demonstrating Oracle WMS configuration patterns."""
    with contextlib.suppress(Exception):
        demonstrate_configuration_patterns()


if __name__ == "__main__":
    main()
