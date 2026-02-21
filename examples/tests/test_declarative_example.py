"""Example usage of the new declarative Oracle WMS Client.

This demonstrates the declarative approach with massive code reduction.
"""

from pathlib import Path
from urllib.parse import urlparse

from flext_oracle_wms import t
from flext_core import FlextLogger
from flext_oracle_wms import (
    FLEXT_ORACLE_WMS_APIS,
    FlextOracleWmsApiVersion,
    FlextOracleWmsClient,
    FlextOracleWmsClientSettings,
)

logger = FlextLogger(__name__)


def load_env_config() -> dict[str, t.GeneralValueType] | None:
    """Load configuration from .env file."""
    env_path = Path("flext-tap-oracle-wms/.env")
    if not env_path.exists():
        return None

    config = {}
    with env_path.open(encoding="utf-8") as f:
        for line in f:
            stripped_line = line.strip()
            if (
                stripped_line
                and not stripped_line.startswith("#")
                and "=" in stripped_line
            ):
                key, value = stripped_line.split("=", 1)
                config[key.strip()] = value.strip()

    # Extract environment from URL dynamically
    base_url = config.get("ORACLE_WMS_BASE_URL", "")
    if base_url:
        try:
            # Extract the last path component as environment
            # URL format: https://invalid.wms.ocs.oraclecloud.com/company_unknow
            parsed = urlparse(base_url)
            path_parts = parsed.path.strip("/").split("/")
            if path_parts and path_parts[-1]:
                # Environment extracted from URL path but not used
                logger.debug(f"Environment detected in URL: {path_parts[-1]}")
        except (ValueError, AttributeError) as e:
            # URL parsing failed, continue with default config
            logger.debug("Failed to parse environment from URL: %s", e)

    return {
        "oracle_wms_base_url": base_url,
        "oracle_wms_username": config.get("ORACLE_WMS_USERNAME"),
        "oracle_wms_password": config.get("ORACLE_WMS_PASSWORD"),
        "api_version": FlextOracleWmsApiVersion.LGF_V10,  # Enum value
        "oracle_wms_timeout": int(config.get("ORACLE_WMS_TIMEOUT", "30")),
        "oracle_wms_max_retries": int(config.get("ORACLE_WMS_MAX_RETRIES", "3")),
        "oracle_wms_verify_ssl": config.get("ORACLE_WMS_VERIFY_SSL", "true").lower()
        == "true",
        "oracle_wms_enable_logging": config.get(
            "ORACLE_WMS_ENABLE_REQUEST_LOGGING",
            "true",
        ).lower()
        == "true",
    }


def main() -> None:
    """Demonstrate declarative Oracle WMS Client usage."""
    # Load configuration
    env_config = load_env_config()
    if not env_config or not all(
        [
            env_config.get("oracle_wms_base_url"),
            env_config.get("oracle_wms_username"),
            env_config.get("oracle_wms_password"),
        ],
    ):
        return

    # Create client configuration
    config = FlextOracleWmsClientSettings.model_validate({
        "base_url": str(env_config["oracle_wms_base_url"]),
        "username": str(env_config["oracle_wms_username"]),
        "password": str(env_config["oracle_wms_password"]),
        "api_version": env_config["api_version"],
        "timeout": int(str(env_config["oracle_wms_timeout"])),
        "retry_attempts": int(str(env_config["oracle_wms_max_retries"])),
        "enable_ssl_verification": bool(env_config["oracle_wms_verify_ssl"]),
        "enable_audit_logging": bool(env_config["oracle_wms_enable_logging"]),
    })
    client = FlextOracleWmsClient(config)

    try:
        # Start the client
        start_result = client.start()
        if not start_result.is_success:
            return

        # Show API catalog

        # Categorize APIs
        categories: dict[str, list[str]] = {}
        for api in FLEXT_ORACLE_WMS_APIS.values():
            if api.category not in categories:
                categories[api.category] = []
            categories[api.category].append(api.name)

        for _category, _apis in categories.items():
            pass

        # Health check
        health_result = client.health_check()
        if health_result.is_success:
            pass

        # Get available entities
        entities_result = client.discover_entities()
        if entities_result.is_success:
            pass

        # Test LGF API v10 - Get entity data
        for entity in ["company", "facility", "item"]:
            result = client.get_entity_data(entity, limit=3)

            if result.is_success:
                data = result.value
                if isinstance(data, dict):
                    results = data.get("results", [])
                    if isinstance(results, list):
                        data.get("count", len(results))
                elif isinstance(data, list):
                    len(data)

        # Test automation APIs (dry run)

        # Test entity status (using health check as alternative)
        health_result = client.health_check()
        if health_result.is_success:
            pass

        # Test OBLPN tracking (will fail, but tests structure)
        client.update_oblpn_tracking_number(
            oblpn_id="TEST123",
            tracking_number="TRACK123",
        )

        # Test LPN creation (will fail, but tests structure)
        lpn_result = client.create_lpn(lpn_nbr="TEST_LPN", qty=10)
        if lpn_result.is_failure:
            logger.debug(f"LPN creation failed as expected: {lpn_result.error}")

    except Exception as e:
        # Log the exception for debugging purposes
        logger.warning("Test execution encountered error: %s", e)
        # Re-raise to ensure test failures are visible
        raise

    finally:
        # Cleanup
        client.stop()


if __name__ == "__main__":
    main()
