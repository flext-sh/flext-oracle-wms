"""Example usage of the new declarative Oracle WMS Client.

This demonstrates the declarative approach with massive code reduction.
"""

import asyncio
from pathlib import Path

from ...flext_oracle_wms import (
    FLEXT_ORACLE_WMS_APIS,
    FlextOracleWmsApiVersion,
    FlextOracleWmsClient,
    FlextOracleWmsClientConfig,
)


def load_env_config():
    """Load configuration from .env file."""
    env_path = Path("flext-tap-oracle-wms/.env")
    if not env_path.exists():
        return None

    config = {}
    with env_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()

    # Extract environment from URL dynamically
    base_url = config.get("ORACLE_WMS_BASE_URL", "")
    environment = "default"  # fallback
    if base_url:
        try:
            # Extract the last path component as environment
            # URL format: https://ta29.wms.ocs.oraclecloud.com/raizen_test
            from urllib.parse import urlparse

            parsed = urlparse(base_url)
            path_parts = parsed.path.strip("/").split("/")
            if path_parts and path_parts[-1]:
                environment = path_parts[-1]
        except Exception:
            environment = "default"

    return {
        "base_url": base_url,
        "username": config.get("ORACLE_WMS_USERNAME"),
        "password": config.get("ORACLE_WMS_PASSWORD"),
        "environment": environment,  # Dynamic extraction from URL
        "api_version": FlextOracleWmsApiVersion.LGF_V10,  # Enum value
        "timeout": float(config.get("ORACLE_WMS_TIMEOUT", "30")),
        "max_retries": int(config.get("ORACLE_WMS_MAX_RETRIES", "3")),
        "verify_ssl": config.get("ORACLE_WMS_VERIFY_SSL", "true").lower() == "true",
        "enable_logging": config.get(
            "ORACLE_WMS_ENABLE_REQUEST_LOGGING",
            "true",
        ).lower()
        == "true",
    }


async def main() -> None:
    """Demonstrate declarative Oracle WMS Client usage."""
    # Load configuration
    env_config = load_env_config()
    if not env_config or not all(
        [
            env_config.get("base_url"),
            env_config.get("username"),
            env_config.get("password"),
        ],
    ):
        return

    # Create client configuration
    config = FlextOracleWmsClientConfig(**env_config)
    client = FlextOracleWmsClient(config)

    try:
        # Start the client
        start_result = await client.start()
        if not start_result.success:
            return

        # Show API catalog

        # Categorize APIs
        categories = {}
        for api in FLEXT_ORACLE_WMS_APIS.values():
            if api.category not in categories:
                categories[api.category] = []
            categories[api.category].append(api.name)

        for _category, _apis in categories.items():
            pass

        # Health check
        health_result = await client.health_check()
        if health_result.success:
            pass

        # Get available entities
        entities_result = await client.get_all_entities()
        if entities_result.success:
            pass

        # Test LGF API v10 - Get entity data
        for entity in ["company", "facility", "item"]:
            result = await client.get_entity_data(entity, limit=3)

            if result.success:
                data = result.data
                data.get("count", len(data.get("results", [])))

        # Test automation APIs (dry run)

        # Test entity status
        await client.get_entity_status(entity="company", key="test")

        # Test OBLPN tracking (will fail, but tests structure)
        await client.update_oblpn_tracking_number(
            company_code="TEST",
            facility_code="TEST",
            oblpn_nbr="TEST123",
            tracking_nbr="TRACK123",
        )

        # Test LPN creation (will fail, but tests structure)
        await client.create_lpn(lpn_nbr="TEST_LPN", qty=10)

    except Exception:
        pass

    finally:
        # Cleanup
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())
