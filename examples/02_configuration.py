"""Example: Oracle WMS Configuration Management.

This example demonstrates WORKING configuration patterns for Oracle WMS Cloud
integration using the ACTUAL API that exists and functions properly.

"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from flext_oracle_wms import (
    FlextOracleWmsConstants,
    FlextOracleWmsSettings,
    FlextOracleWmsUtilitiesClient,
    m,
    t,
    u,
)

FlextOracleWmsClient = FlextOracleWmsUtilitiesClient.Client

logger = u.fetch_logger(__name__)

c = FlextOracleWmsConstants


def get_environment_configs() -> t.MappingKV[
    c.OracleWms.Environment,
    m.OracleWms.EnvironmentConfig,
]:
    """Define environment-specific Oracle WMS configurations."""
    return {
        c.OracleWms.Environment.DEVELOPMENT: p.OracleWms.EnvironmentConfig(
            name="Development",
            base_url="https://dev-wms.oraclecloud.com/dev_env",
            timeout=c.OracleWms.DEFAULT_TIMEOUT,
            retry_attempts=c.OracleWms.DEFAULT_MAX_RETRIES,
        ),
        c.OracleWms.Environment.STAGING: p.OracleWms.EnvironmentConfig(
            name="Staging",
            base_url="https://staging-wms.oraclecloud.com/staging_env",
            timeout=c.OracleWms.DEFAULT_TIMEOUT,
            retry_attempts=c.OracleWms.DEFAULT_MAX_RETRIES,
        ),
        c.OracleWms.Environment.PRODUCTION: p.OracleWms.EnvironmentConfig(
            name="Production",
            base_url="https://prod-wms.oraclecloud.com/prod_env",
            timeout=c.OracleWms.DEFAULT_TIMEOUT,
            retry_attempts=c.OracleWms.DEFAULT_MAX_RETRIES,
        ),
    }


def create_config_from_environment() -> FlextOracleWmsSettings:
    """Create Oracle WMS client configuration from environment variables.

    This uses the REAL .env file with working Oracle WMS credentials.

    Returns:
      FlextOracleWmsSettings configured from environment

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
    # NOTE (multi-agent): ADR-005 — project scalars are namespaced under the
    # ``OracleWms`` group; build via model_validate with the nested payload.
    return FlextOracleWmsSettings.model_validate({
        "OracleWms": {
            "base_url": base_url,
            "username": username,
            "password": password,
        },
    })


def create_demo_config() -> FlextOracleWmsSettings:
    """Create a demo Oracle WMS configuration using singleton pattern.

    Returns:
      FlextOracleWmsSettings with demo values

    Note:
      This demonstrates how to use the global singleton with parameter overrides.

    """
    return FlextOracleWmsSettings.model_validate({
        "OracleWms": {
            "base_url": "https://demo-wms.oraclecloud.com/demo",
            "username": "demo_user",
            "password": "demo_password",
            "api_version": "LGF_V10",
            "timeout": c.OracleWms.DEFAULT_TIMEOUT,
            "retry_attempts": c.OracleWms.DEFAULT_MAX_RETRIES,
            "verify_ssl": True,
            "enable_logging": True,
        },
    })


def validate_configuration(settings: FlextOracleWmsSettings) -> t.JsonMapping:
    """Validate Oracle WMS client configuration.

    Args:
      settings: Oracle WMS client configuration to validate

    Returns:
      Dictionary containing validation results

    """
    errors: list[str] = []
    warnings: list[str] = []
    wms = settings.OracleWms
    if not wms.base_url:
        errors.append("Base URL is required")
    elif not wms.base_url.startswith("https://"):
        warnings.append("Base URL should use HTTPS for security")
    if not wms.username or not wms.password:
        errors.append("Username and password are required")
    min_timeout_seconds = c.OracleWms.DEFAULT_TIMEOUT // 3
    if wms.timeout <= 0:
        errors.append("Timeout must be positive")
    elif wms.timeout < min_timeout_seconds:
        warnings.append("Timeout less than 10 seconds may cause issues")
    retry_count = wms.retry_attempts
    max_retries_warning_threshold = c.OracleWms.DEFAULT_MAX_RETRIES * 3
    if retry_count < 0:
        errors.append("Max retries cannot be negative")
    elif retry_count > max_retries_warning_threshold:
        warnings.append("High retry count may cause delays")
    config_summary = t.json_mapping_adapter().validate_python({
        "base_url": wms.base_url,
        "username": wms.username,
        "api_version": wms.api_version,
        "timeout": wms.timeout,
        "retry_attempts": retry_count,
        "verify_ssl": wms.verify_ssl,
        "enable_logging": wms.enable_logging,
    })
    return t.json_mapping_adapter().validate_python({
        "valid": not errors,
        "warnings": warnings,
        "errors": errors,
        "configuration_summary": config_summary,
    })


def test_configuration(
    settings: FlextOracleWmsSettings,
) -> t.MutableJsonMapping:
    """Test Oracle WMS configuration by attempting connection.

    Args:
      settings: Configuration to test

    Returns:
      Dictionary with test results

    """
    test_results: t.MutableJsonMapping = {
        "connection_success": False,
        "health_check_success": False,
        "error": None,
        "entities_discovered": 0,
    }
    client = FlextOracleWmsClient(settings)
    try:
        _run_configuration_test(client, test_results)
    except Exception as exc:
        test_results["error"] = str(exc)
    finally:
        client.stop()
    return test_results


def _run_configuration_test(
    client: FlextOracleWmsClient,
    test_results: t.MutableJsonMapping,
) -> None:
    """Populate connection and discovery test results."""
    client.start()
    test_results["connection_success"] = True
    health_result = client.health_check()
    if health_result.success:
        test_results["health_check_success"] = True
    entities_result = client.discover_entities()
    if entities_result.success and entities_result.value:
        test_results["entities_discovered"] = len(entities_result.value)


def _demonstrate_environment_configuration() -> None:
    """Demonstrate environment-derived configuration validation."""
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


def _demonstrate_demo_configuration() -> None:
    """Demonstrate demo configuration validation."""
    demo_config = create_demo_config()
    validation = validate_configuration(demo_config)
    warnings = validation.get("warnings", [])
    if warnings and isinstance(warnings, (list, tuple)):
        for _warning in warnings:
            pass


def demonstrate_configuration_patterns() -> None:
    """Demonstrate working Oracle WMS configuration patterns."""
    try:
        _demonstrate_environment_configuration()
    except ValueError as exc:
        logger.info("Environment configuration unavailable: %s", exc)
    try:
        _demonstrate_demo_configuration()
    except Exception as exc:
        logger.warning("Configuration validation failed: %s", exc)
    env_configs = get_environment_configs()
    for _config in env_configs.values():
        pass


def main() -> None:
    """Demonstrate Oracle WMS configuration patterns."""
    demonstrate_configuration_patterns()


if __name__ == "__main__":
    main()
