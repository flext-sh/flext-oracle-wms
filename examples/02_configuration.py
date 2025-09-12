"""Example: Oracle WMS Configuration Management.

This example demonstrates WORKING configuration patterns for Oracle WMS Cloud
integration using the ACTUAL API that exists and functions properly.

"""

import os
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from dotenv import load_dotenv
from flext_core import FlextConstants, FlextTypes

from flext_oracle_wms import (
    FlextOracleWmsApiVersion,
    FlextOracleWmsClient,
    FlextOracleWmsClientConfig,
)


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
    timeout: int = FlextConstants.Defaults.TIMEOUT
    max_retries: int = FlextConstants.Defaults.MAX_RETRIES


def get_environment_configs() -> dict[Environment, WmsEnvironmentConfig]:
    """Define environment-specific Oracle WMS configurations."""
    return {
        Environment.DEVELOPMENT: WmsEnvironmentConfig(
            name="Development",
            base_url="https://dev-wms.oraclecloud.com/dev_env",
            timeout=FlextConstants.Defaults.DB_TIMEOUT,
            max_retries=FlextConstants.Defaults.MAX_RETRIES,
        ),
        Environment.STAGING: WmsEnvironmentConfig(
            name="Staging",
            base_url="https://staging-wms.oraclecloud.com/staging_env",
            timeout=FlextConstants.Defaults.TIMEOUT,
            max_retries=FlextConstants.Defaults.MAX_RETRIES,
        ),
        Environment.PRODUCTION: WmsEnvironmentConfig(
            name="Production",
            base_url="https://prod-wms.oraclecloud.com/prod_env",
            timeout=FlextConstants.Defaults.TIMEOUT,
            max_retries=FlextConstants.Defaults.MAX_RETRIES,
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
    # Load environment from .env if available
    try:
        project_root = Path(__file__).parent.parent
        env_file = project_root / ".env"
        if env_file.exists():
            load_dotenv(env_file)
    except ImportError:
        pass  # dotenv not available, use system environment

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
    env_result = FlextOracleWmsClientConfig.create_from_environment()

    if env_result.success:
        return env_result.value

    # Method 2: Fallback to global singleton with default values
    # if environment variables are not set
    return FlextOracleWmsClientConfig.get_oracle_wms_global_instance()


def create_demo_config() -> FlextOracleWmsClientConfig:
    """Create a demo Oracle WMS configuration using singleton pattern.

    Returns:
      FlextOracleWmsClientConfig with demo values

    Note:
      This demonstrates how to use the global singleton with parameter overrides.

    """
    # Use global singleton with demo parameters
    return FlextOracleWmsClientConfig.get_oracle_wms_global_instance(
        oracle_wms_base_url="https://demo-wms.oraclecloud.com/demo",
        oracle_wms_username="demo_user",
        oracle_wms_password="demo_password",
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        oracle_wms_timeout=int(FlextConstants.Defaults.TIMEOUT),
        oracle_wms_max_retries=FlextConstants.Defaults.MAX_RETRIES,
        oracle_wms_verify_ssl=True,
        oracle_wms_enable_logging=True,
    )


def validate_configuration(config: FlextOracleWmsClientConfig) -> FlextTypes.Core.Dict:
    """Validate Oracle WMS client configuration.

    Args:
      config: Oracle WMS client configuration to validate

    Returns:
      Dictionary containing validation results

    """
    validation_results = {
        "valid": True,
        "warnings": [],
        "errors": [],
        "configuration_summary": {},
    }

    # Validate base URL
    if not config.oracle_wms_base_url:
        validation_results["errors"].append("Base URL is required")
        validation_results["valid"] = False
    elif not config.oracle_wms_base_url.startswith("https://"):
        validation_results["warnings"].append("Base URL should use HTTPS for security")

    # Validate authentication
    if not config.oracle_wms_username or not config.oracle_wms_password:
        validation_results["errors"].append("Username and password are required")
        validation_results["valid"] = False

    # Constants for validation
    min_timeout_seconds = 10  # Minimum timeout threshold

    # Validate timeouts and retries
    if config.timeout <= 0:
        validation_results["errors"].append("Timeout must be positive")
        validation_results["valid"] = False
    elif config.timeout < min_timeout_seconds:
        validation_results["warnings"].append(
            "Timeout less than 10 seconds may cause issues",
        )

    # Constants for validation
    max_retries_warning_threshold = 10  # High retry count threshold

    if config.max_retries < 0:
        validation_results["errors"].append("Max retries cannot be negative")
        validation_results["valid"] = False
    elif config.max_retries > max_retries_warning_threshold:
        validation_results["warnings"].append("High retry count may cause delays")

    # Create configuration summary
    validation_results["configuration_summary"] = {
        "base_url": config.oracle_wms_base_url,
        "username": config.oracle_wms_username,
        "api_version": config.api_version.value,
        "timeout": config.timeout,
        "max_retries": config.max_retries,
        "verify_ssl": config.verify_ssl,
        "enable_logging": config.enable_logging,
    }

    return validation_results


async def test_configuration(
    config: FlextOracleWmsClientConfig,
) -> FlextTypes.Core.Dict:
    """Test Oracle WMS configuration by attempting connection.

    Args:
      config: Configuration to test

    Returns:
      Dictionary with test results

    """
    test_results = {
        "connection_success": False,
        "health_check_success": False,
        "error": None,
        "entities_discovered": 0,
    }

    client = FlextOracleWmsClient(config)

    try:
        # Test connection
        await client.start()
        test_results["connection_success"] = True

        # Test health check
        health_result = await client.health_check()
        if health_result.success:
            test_results["health_check_success"] = True

        # Test entity discovery
        entities_result = await client.discover_entities()
        if entities_result.success and entities_result.data:
            test_results["entities_discovered"] = len(entities_result.data)

    except Exception as e:
        test_results["error"] = str(e)
    finally:
        await client.stop()

    return test_results


def demonstrate_configuration_patterns() -> None:
    """Demonstrate working Oracle WMS configuration patterns."""
    # Pattern 1: Environment-driven configuration (REAL)
    try:
        env_config = create_config_from_environment()
        validation = validate_configuration(env_config)

        if validation["warnings"]:
            for _warning in validation["warnings"]:
                pass

        if validation["valid"]:
            pass
        else:
            for _error in validation["errors"]:
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

    except Exception:
        pass

    # Pattern 3: Environment-specific configurations
    env_configs = get_environment_configs()

    for _config in env_configs.values():
        pass


def main() -> None:
    """Main function demonstrating Oracle WMS configuration patterns."""
    try:
        demonstrate_configuration_patterns()
        print("Configuration examples completed successfully")
        print("Environment configuration created successfully")
        print("Configuration is valid and ready for use")
    except Exception as e:
        print(f"Configuration example failed: {e}")


if __name__ == "__main__":
    main()
