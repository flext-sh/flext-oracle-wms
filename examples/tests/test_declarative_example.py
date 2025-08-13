"""Example usage of the new declarative Oracle WMS Client.

This demonstrates the declarative approach with massive code reduction.
"""

import asyncio
from pathlib import Path

from flext_oracle_wms.api_catalog import FLEXT_ORACLE_WMS_APIS, FlextOracleWmsApiVersion
from flext_oracle_wms.client import FlextOracleWmsClient
from flext_oracle_wms.config import FlextOracleWmsClientConfig


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
    print("🚀 Oracle WMS Cloud Client - Declarative Implementation Demo")
    print("=" * 60)

    # Load configuration
    env_config = load_env_config()
    if not env_config or not all(
        [
            env_config.get("base_url"),
            env_config.get("username"),
            env_config.get("password"),
        ],
    ):
        print("❌ No valid .env configuration found - skipping demo")
        return

    # Create client configuration
    config = FlextOracleWmsClientConfig(**env_config)
    client = FlextOracleWmsClient(config)

    try:
        # Start the client
        print("🔧 Starting Oracle WMS client...")
        start_result = await client.start()
        if not start_result.success:
            print(f"❌ Failed to start client: {start_result.error}")
            return
        print("✅ Client started successfully")

        # Show API catalog
        print(
            f"\n�� API Catalog: {len(FLEXT_ORACLE_WMS_APIS)} Oracle WMS Cloud APIs loaded",
        )

        # Categorize APIs
        categories = {}
        for api in FLEXT_ORACLE_WMS_APIS.values():
            if api.category not in categories:
                categories[api.category] = []
            categories[api.category].append(api.name)

        for category, apis in categories.items():
            print(f"  📁 {category}: {len(apis)} APIs")

        # Health check
        print("\n🏥 Health Check...")
        health_result = await client.health_check()
        if health_result.success:
            health_data = health_result.data
            print(
                f"✅ Service: {health_data['service']} - Status: {health_data['status']}",
            )
        else:
            print(f"❌ Health check failed: {health_result.error}")

        # Get available entities
        print("\n📋 Available Entities...")
        entities_result = await client.get_all_entities()
        if entities_result.success:
            entities = entities_result.data
            print(f"✅ Found {len(entities)} entities: {', '.join(entities[:5])}...")
        else:
            print(f"❌ Failed to get entities: {entities_result.error}")

        # Test LGF API v10 - Get entity data
        print("\n📊 LGF API v10 - Data Extraction...")
        for entity in ["company", "facility", "item"]:
            print(f"  🔍 Testing {entity}...")
            result = await client.get_entity_data(entity, limit=3)

            if result.success:
                data = result.data
                count = data.get("count", len(data.get("results", [])))
                print(f"    ✅ {entity}: {count} records available")
            else:
                print(f"    ⚠️ {entity}: {result.error}")

        # Test automation APIs (dry run)
        print("\n🤖 Automation APIs (Structure Test)...")

        # Test entity status
        status_result = await client.get_entity_status(entity="company", key="test")
        print(
            f"  📊 Entity Status: {'✅ OK' if status_result.success else '⚠️ Expected failure'}",
        )

        # Test OBLPN tracking (will fail, but tests structure)
        tracking_result = await client.update_oblpn_tracking_number(
            company_code="TEST",
            facility_code="TEST",
            oblpn_nbr="TEST123",
            tracking_nbr="TRACK123",
        )
        print(
            f"  📦 OBLPN Tracking: {'✅ OK' if tracking_result.success else '⚠️ Expected failure'}",
        )

        # Test LPN creation (will fail, but tests structure)
        lpn_result = await client.create_lpn(lpn_nbr="TEST_LPN", qty=10)
        print(
            f"  📋 LPN Creation: {'✅ OK' if lpn_result.success else '⚠️ Expected failure'}",
        )

        print("\n🎉 Declarative Oracle WMS Client Demo Complete!")
        print("💡 Key Benefits:")
        print("  • 25+ APIs defined declaratively")
        print("  • Built on flext-api infrastructure")
        print("  • Type-safe with flext-core patterns")
        print("  • Async/await support")
        print("  • Comprehensive error handling")
        print("  • Easy to extend and maintain")

    except Exception as e:
        print(f"❌ Demo failed: {e}")

    finally:
        # Cleanup
        print("\n🧹 Cleaning up...")
        await client.stop()
        print("✅ Client stopped")


if __name__ == "__main__":
    asyncio.run(main())
