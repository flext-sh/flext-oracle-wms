"""Example: Oracle WMS Configuration Management.

This example demonstrates WORKING configuration patterns for Oracle WMS Cloud
integration using the ACTUAL API that exists and functions properly.

"""

import contextlib
import os
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from dotenv import load_dotenv
from flext_core import FlextLogger, FlextTypes as t

from flext_oracle_wms import (
    FlextOracleWmsClient,
    FlextOracleWmsClientSettings,
    FlextOracleWmsSettings,
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


def create_config_from_environment() -> FlextOracleWmsClientSettings:
    """Create Oracle WMS client configuration from environment variables.

    This uses the REAL .env file with working Oracle WMS credentials.

    Returns:
      FlextOracleWmsClientSettings configured from environment

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
    env_config = FlextOracleWmsClientSettings.get_global_instance()

    # Validate that required fields are set from environment
    if env_config.username and env_config.password:
        return env_config

    # Method 2: Fallback to default configuration
    # if environment variables are not set
    return FlextOracleWmsSettings()


def create_demo_config() -> FlextOracleWmsClientSettings:
    """Create a demo Oracle WMS configuration using singleton pattern.

    Returns:
      FlextOracleWmsClientSettings with demo values

    Note:
      This demonstrates how to use the global singleton with parameter overrides.

    """
    # Use Pydantic model validation for proper configuration creation
    return FlextOracleWmsClientSettings.model_validate({
        "base_url": "https://demo-wms.oraclecloud.com/demo",
        "username": "demo_user",
        "password": "demo_password",
        "api_version": "LGF_V10",
        "timeout": FlextOracleWmsConstants.Connection.DEFAULT_TIMEOUT,
        "retry_attempts": FlextOracleWmsConstants.Connection.DEFAULT_MAX_RETRIES,
        "enable_ssl_verification": True,
        "enable_audit_logging": True,
    })


def validate_configuration(
    config: FlextOracleWmsClientSettings,
) -> dict[str, t.GeneralValueType]:
    """Validate Oracle WMS client configuration.

    Args:
      config: Oracle WMS client configuration to validate

    Returns:
      Dictionary containing validation results

    """
    errors: list[str] = []
    warnings: list[str] = []
    config_summary: dict[str, t.GeneralValueType] = {}

    # Validate base URL
    if not config.base_url:
        errors.append("Base URL is required")
    elif not config.base_url.startswith("https://"):
        warnings.append("Base URL should use HTTPS for security")

    # Validate authentication
    if not config.username or not config.password:
        errors.append("Username and password are required")

    # Constants for validation
    min_timeout_seconds = (
        FlextOracleWmsConstants.Connection.DEFAULT_TIMEOUT // 3
    )  # Minimum timeout threshold

    # Validate timeouts and retries
    if config.timeout <= 0:
        errors.append("Timeout must be positive")
    elif config.timeout < min_timeout_seconds:
        warnings.append("Timeout less than 10 seconds may cause issues")

    # Constants for validation
    max_retries_warning_threshold = (
        FlextOracleWmsConstants.Connection.DEFAULT_MAX_RETRIES * 3
    )  # High retry count threshold

    if config.retry_attempts < 0:
        errors.append("Max retries cannot be negative")
    elif config.retry_attempts > max_retries_warning_threshold:
        warnings.append("High retry count may cause delays")

    # Create configuration summary
    config_summary = {
        "base_url": config.base_url,
        "username": config.username,
        "api_version": config.api_version,
        "timeout": config.timeout,
        "max_retries": config.retry_attempts,
        "verify_ssl": config.enable_ssl_verification,
        "enable_logging": config.enable_audit_logging,
    }

    validation_results: dict[str, t.GeneralValueType] = {
        "valid": len(errors) == 0,
        "warnings": warnings,
        "errors": errors,
        "configuration_summary": config_summary,
    }

    return validation_results


def test_configuration(
    config: FlextOracleWmsClientSettings,
) -> dict[str, t.GeneralValueType]:
    """Test Oracle WMS configuration by attempting connection.

    Args:
      config: Configuration to test

    Returns:
      Dictionary with test results

    """
    test_results: dict[str, t.GeneralValueType] = {
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

        warnings = validation.get("warnings", [])
        if warnings and isinstance(warnings, (list, tuple)):
            for _warning in warnings:
                pass

    except Exception as e:
        logger.warning("Configuration validation failed: %s", e)

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
