"""Example: Oracle WMS Configuration Management.

This example demonstrates WORKING configuration patterns for Oracle WMS Cloud
integration using the ACTUAL API that exists and functions properly.

REFACTORED: Only includes patterns that work with the real FlextOracleWmsClientConfig.

Requirements:
    - Real Oracle WMS credentials in .env file
    - Understanding of working FlextOracleWmsClientConfig parameters

Environment Variables (from .env):
    - ORACLE_WMS_BASE_URL: Oracle WMS Cloud base URL
    - ORACLE_WMS_USERNAME: Authentication username
    - ORACLE_WMS_PASSWORD: Authentication password
    - ORACLE_WMS_ENVIRONMENT: Environment name
    - ORACLE_WMS_TIMEOUT: Request timeout in seconds
    - ORACLE_WMS_MAX_RETRIES: Maximum retry attempts

Usage:
    python examples/configuration.py
"""

import os
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

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
    timeout: int = 30
    max_retries: int = 3


def get_environment_configs() -> dict[Environment, WmsEnvironmentConfig]:
    """Define environment-specific Oracle WMS configurations."""
    return {
        Environment.DEVELOPMENT: WmsEnvironmentConfig(
            name="Development",
            base_url="https://dev-wms.oraclecloud.com/dev_env",
            timeout=60,
            max_retries=1,
        ),
        Environment.STAGING: WmsEnvironmentConfig(
            name="Staging",
            base_url="https://staging-wms.oraclecloud.com/staging_env",
            timeout=45,
            max_retries=2,
        ),
        Environment.PRODUCTION: WmsEnvironmentConfig(
            name="Production",
            base_url="https://prod-wms.oraclecloud.com/prod_env",
            timeout=30,
            max_retries=3,
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

    return FlextOracleWmsClientConfig(
        base_url=base_url,
        username=username,
        password=password,
        environment=environment,
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        timeout=float(os.getenv("ORACLE_WMS_TIMEOUT", "30")),
        max_retries=int(os.getenv("ORACLE_WMS_MAX_RETRIES", "3")),
        verify_ssl=os.getenv("ORACLE_WMS_VERIFY_SSL", "true").lower() == "true",
        enable_logging=True,
    )


def create_demo_config() -> FlextOracleWmsClientConfig:
    """Create a demo Oracle WMS configuration for testing.

    Returns:
      FlextOracleWmsClientConfig with demo values

    Note:
      This is for demonstration only. Use real credentials from .env in practice.

    """
    return FlextOracleWmsClientConfig(
        base_url="https://demo-wms.oraclecloud.com/demo",
        username="demo_user",
        password="demo_password",  # noqa: S106 - Demo password argument for configuration example
        environment="demo",
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        timeout=30.0,
        max_retries=3,
        verify_ssl=True,
        enable_logging=True,
    )


def validate_configuration(config: FlextOracleWmsClientConfig) -> dict[str, Any]:
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
    if not config.base_url:
        validation_results["errors"].append("Base URL is required")
        validation_results["valid"] = False
    elif not config.base_url.startswith("https://"):
        validation_results["warnings"].append("Base URL should use HTTPS for security")

    # Validate authentication
    if not config.username or not config.password:
        validation_results["errors"].append("Username and password are required")
        validation_results["valid"] = False

    # Constants for validation
    min_timeout_seconds = 10

    # Validate timeouts and retries
    if config.timeout <= 0:
        validation_results["errors"].append("Timeout must be positive")
        validation_results["valid"] = False
    elif config.timeout < min_timeout_seconds:
        validation_results["warnings"].append(
            "Timeout less than 10 seconds may cause issues",
        )

    # Constants for validation
    max_retries_warning_threshold = 5

    if config.max_retries < 0:
        validation_results["errors"].append("Max retries cannot be negative")
        validation_results["valid"] = False
    elif config.max_retries > max_retries_warning_threshold:
        validation_results["warnings"].append("High retry count may cause delays")

    # Create configuration summary
    validation_results["configuration_summary"] = {
        "base_url": config.base_url,
        "username": config.username,
        "environment": config.environment,
        "api_version": config.api_version.value,
        "timeout": config.timeout,
        "max_retries": config.max_retries,
        "verify_ssl": config.verify_ssl,
        "enable_logging": config.enable_logging,
    }

    return validation_results


async def test_configuration(config: FlextOracleWmsClientConfig) -> dict[str, Any]:
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
    print("🔧 Oracle WMS Configuration Management Examples")
    print("=" * 60)

    # Pattern 1: Environment-driven configuration (REAL)
    print("\n📋 Pattern 1: Environment-driven Configuration")
    print("-" * 45)
    try:
        env_config = create_config_from_environment()
        validation = validate_configuration(env_config)

        print("✅ Environment configuration created successfully")
        print(f"   Base URL: {env_config.base_url}")
        print(f"   Username: {env_config.username}")
        print(f"   Environment: {env_config.environment}")
        print(f"   API Version: {env_config.api_version.value}")
        print(f"   Timeout: {env_config.timeout}s")

        if validation["warnings"]:
            print("⚠️  Configuration warnings:")
            for warning in validation["warnings"]:
                print(f"   - {warning}")

        if validation["valid"]:
            print("✅ Configuration is valid and ready for use")
        else:
            print("❌ Configuration has errors:")
            for error in validation["errors"]:
                print(f"   - {error}")

    except ValueError as e:
        print(f"❌ Configuration example failed: {e}")
        print("   Check your environment setup and try again")

    # Pattern 2: Demo configuration
    print("\n📋 Pattern 2: Demo Configuration")
    print("-" * 45)
    try:
        demo_config = create_demo_config()
        validation = validate_configuration(demo_config)

        print("✅ Demo configuration created successfully")
        print(f"   Base URL: {demo_config.base_url}")
        print(f"   Configuration valid: {validation['valid']}")

        if validation["warnings"]:
            print("⚠️  Configuration warnings:")
            for warning in validation["warnings"]:
                print(f"   - {warning}")

    except Exception as e:
        print(f"❌ Demo configuration failed: {e}")

    # Pattern 3: Environment-specific configurations
    print("\n📋 Pattern 3: Environment-specific Templates")
    print("-" * 45)
    env_configs = get_environment_configs()

    for config in env_configs.values():
        print(f"🌍 {config.name} Environment:")
        print(f"   Base URL: {config.base_url}")
        print(f"   Timeout: {config.timeout}s")
        print(f"   Max Retries: {config.max_retries}")
        print()


def main() -> None:
    """Main function demonstrating Oracle WMS configuration patterns."""
    print("🚀 FLEXT Oracle WMS - Configuration Examples")
    print("=" * 60)

    try:
        demonstrate_configuration_patterns()

        print("\n✅ Configuration examples completed successfully!")
        print("\n💡 Next steps:")
        print("   - Ensure your .env file has valid Oracle WMS credentials")
        print("   - Test with basic_usage.py for real Oracle WMS connection")
        print("   - Explore entity discovery and data retrieval examples")

    except Exception as e:
        print(f"❌ Configuration example failed: {e}")
        print("   Check your environment setup and try again")


if __name__ == "__main__":
    main()
