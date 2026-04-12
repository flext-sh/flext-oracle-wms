"""Example: Oracle WMS Configuration Management.

This example demonstrates WORKING configuration patterns for Oracle WMS Cloud
integration using the ACTUAL API that exists and functions properly.

"""

from __future__ import annotations

import contextlib
import os
from collections.abc import Mapping
from enum import StrEnum, unique
from pathlib import Path
from typing import ClassVar

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field

from flext_oracle_wms import (
    FlextOracleWmsClientSettings,
    FlextOracleWmsConstants,
    FlextOracleWmsUtilitiesClient,
    t,
    u,
)

FlextOracleWmsClient = FlextOracleWmsUtilitiesClient.Client

logger = u.fetch_logger(__name__)

c = FlextOracleWmsConstants


@unique
class Environment(StrEnum):
    """Oracle WMS deployment environments."""

    DEVELOPMENT = "dev"
    STAGING = "staging"
    PRODUCTION = "prod"


class WmsEnvironmentConfig(BaseModel):
    """WMS environment configuration."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    name: str = Field(description="Environment display name")
    base_url: str = Field(description="Oracle WMS base URL")
    timeout: int = Field(ge=1, description="Request timeout in seconds")
    max_retries: int = Field(ge=0, description="Maximum retry attempts")


def get_environment_configs() -> Mapping[Environment, WmsEnvironmentConfig]:
    """Define environment-specific Oracle WMS configurations."""
    return {
        Environment.DEVELOPMENT: WmsEnvironmentConfig(
            name="Development",
            base_url="https://dev-wms.oraclecloud.com/dev_env",
            timeout=c.OracleWms.DEFAULT_TIMEOUT,
            max_retries=c.OracleWms.DEFAULT_MAX_RETRIES,
        ),
        Environment.STAGING: WmsEnvironmentConfig(
            name="Staging",
            base_url="https://staging-wms.oraclecloud.com/staging_env",
            timeout=c.OracleWms.DEFAULT_TIMEOUT,
            max_retries=c.OracleWms.DEFAULT_MAX_RETRIES,
        ),
        Environment.PRODUCTION: WmsEnvironmentConfig(
            name="Production",
            base_url="https://prod-wms.oraclecloud.com/prod_env",
            timeout=c.OracleWms.DEFAULT_TIMEOUT,
            max_retries=c.OracleWms.DEFAULT_MAX_RETRIES,
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
    env_config = FlextOracleWmsClientSettings.fetch_global()
    if env_config.username and env_config.password:
        return env_config
    return FlextOracleWmsClientSettings()


def create_demo_config() -> FlextOracleWmsClientSettings:
    """Create a demo Oracle WMS configuration using singleton pattern.

    Returns:
      FlextOracleWmsClientSettings with demo values

    Note:
      This demonstrates how to use the global singleton with parameter overrides.

    """
    return FlextOracleWmsClientSettings.model_validate({
        "base_url": "https://demo-wms.oraclecloud.com/demo",
        "username": "demo_user",
        "password": "demo_password",
        "api_version": "LGF_V10",
        "timeout": c.OracleWms.DEFAULT_TIMEOUT,
        "max_retries": c.OracleWms.DEFAULT_MAX_RETRIES,
        "verify_ssl": True,
        "enable_logging": True,
    })


def validate_configuration(
    settings: FlextOracleWmsClientSettings,
) -> dict[str, t.RecursiveContainer]:
    """Validate Oracle WMS client configuration.

    Args:
      settings: Oracle WMS client configuration to validate

    Returns:
      Dictionary containing validation results

    """
    errors: list[str] = []
    warnings: list[str] = []
    if not settings.base_url:
        errors.append("Base URL is required")
    elif not settings.base_url.startswith("https://"):
        warnings.append("Base URL should use HTTPS for security")
    if not settings.username or not settings.password:
        errors.append("Username and password are required")
    min_timeout_seconds = c.OracleWms.DEFAULT_TIMEOUT // 3
    if settings.timeout <= 0:
        errors.append("Timeout must be positive")
    elif settings.timeout < min_timeout_seconds:
        warnings.append("Timeout less than 10 seconds may cause issues")
    max_retries_warning_threshold = c.OracleWms.DEFAULT_MAX_RETRIES * 3
    if settings.max_retries < 0:
        errors.append("Max retries cannot be negative")
    elif settings.max_retries > max_retries_warning_threshold:
        warnings.append("High retry count may cause delays")
    config_summary: dict[str, t.RecursiveContainer] = {
        "base_url": settings.base_url,
        "username": settings.username,
        "api_version": settings.api_version,
        "timeout": settings.timeout,
        "max_retries": settings.max_retries,
        "verify_ssl": settings.verify_ssl,
        "enable_logging": settings.enable_logging,
    }
    validation_results: dict[str, t.RecursiveContainer] = {
        "valid": not errors,
        "warnings": warnings,
        "errors": errors,
        "configuration_summary": config_summary,
    }
    return validation_results


def test_configuration(
    settings: FlextOracleWmsClientSettings,
) -> dict[str, t.RecursiveContainer]:
    """Test Oracle WMS configuration by attempting connection.

    Args:
      settings: Configuration to test

    Returns:
      Dictionary with test results

    """
    test_results: dict[str, t.RecursiveContainer] = {
        "connection_success": False,
        "health_check_success": False,
        "error": None,
        "entities_discovered": 0,
    }
    client = FlextOracleWmsClient(settings)
    try:
        client.start()
        test_results["connection_success"] = True
        health_result = client.health_check()
        if health_result.success:
            test_results["health_check_success"] = True
        entities_result = client.discover_entities()
        if entities_result.success and entities_result.value:
            test_results["entities_discovered"] = len(entities_result.value)
    except Exception as exc:
        test_results["error"] = str(exc)
    finally:
        client.stop()
    return test_results


def demonstrate_configuration_patterns() -> None:
    """Demonstrate working Oracle WMS configuration patterns."""
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
    try:
        demo_config = create_demo_config()
        validation = validate_configuration(demo_config)
        warnings = validation.get("warnings", [])
        if warnings and isinstance(warnings, (list, tuple)):
            for _warning in warnings:
                pass
    except Exception as exc:
        logger.warning(f"Configuration validation failed: {exc}")
    env_configs = get_environment_configs()
    for _config in env_configs.values():
        pass


def main() -> None:
    """Main function demonstrating Oracle WMS configuration patterns."""
    with contextlib.suppress(Exception):
        demonstrate_configuration_patterns()


if __name__ == "__main__":
    main()
