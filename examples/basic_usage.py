"""Example: Basic Oracle WMS Client Usage.

This example demonstrates fundamental Oracle WMS Cloud integration patterns
using the flext-oracle-wms library, including client initialization,
entity discovery, and basic data querying.

Requirements:
    - Oracle WMS Cloud instance access
    - Valid authentication credentials (username/password or API key)
    - Network connectivity to Oracle WMS Cloud

Environment Variables:
    - FLEXT_ORACLE_WMS_BASE_URL: Oracle WMS Cloud base URL
    - FLEXT_ORACLE_WMS_USERNAME: Authentication username
    - FLEXT_ORACLE_WMS_PASSWORD: Authentication password
    - FLEXT_ORACLE_WMS_AUTH_METHOD: Authentication method (basic, bearer, api_key)

Usage:
    python examples/basic_usage.py
"""

import asyncio
import os
from pathlib import Path
from typing import Any

from flext_core import FlextResult

# Display configuration constants
MAX_ENTITIES_TO_SHOW = 5
MAX_VALUE_DISPLAY_LENGTH = 50

from flext_oracle_wms import (
    FlextOracleWmsApiVersion,
    FlextOracleWmsClient,
    FlextOracleWmsClientConfig,
    FlextOracleWmsEntity,
    FlextOracleWmsError,
)

# Load .env file from project root
try:
    
       project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    if env_file.exists():
      load_dotenv(env_file)
      print(f"✅ Loaded environment from {env_file}")
except ImportError:
    print("⚠️ python-dotenv not installed. Install with: pip install python-dotenv")
    print("   Using system environment variables only.")


def create_client_config() -> FlextOracleWmsClientConfig:
    """Create Oracle WMS client configuration from environment variables."""
    # Validate required environment variables
    base_url = os.getenv("ORACLE_WMS_BASE_URL") or os.getenv(
      "FLEXT_ORACLE_WMS_BASE_URL",
    )
    username = os.getenv("ORACLE_WMS_USERNAME") or os.getenv(
      "FLEXT_ORACLE_WMS_USERNAME",
    )
    password = os.getenv("ORACLE_WMS_PASSWORD") or os.getenv(
      "FLEXT_ORACLE_WMS_PASSWORD",
    )

    if not all([base_url, username, password]):
      msg = (
          "Missing required environment variables. Please set:\n"
          "- ORACLE_WMS_BASE_URL (or FLEXT_ORACLE_WMS_BASE_URL)\n"
          "- ORACLE_WMS_USERNAME (or FLEXT_ORACLE_WMS_USERNAME)\n"
          "- ORACLE_WMS_PASSWORD (or FLEXT_ORACLE_WMS_PASSWORD)"
      )
      raise ValueError(msg)

    # Create configuration with environment-driven settings
    return FlextOracleWmsClientConfig(
      base_url=base_url,
      username=username,
      password=password,
      environment=os.getenv("ORACLE_WMS_ENVIRONMENT", "raizen_test"),
      api_version=FlextOracleWmsApiVersion.LGF_V10,
      timeout=float(os.getenv("ORACLE_WMS_TIMEOUT", "30")),
      max_retries=int(os.getenv("ORACLE_WMS_MAX_RETRIES", "3")),
      verify_ssl=True,
      enable_logging=True,
    )


async def discover_wms_entities(
    client: FlextOracleWmsClient,
) -> FlextResult[list[FlextOracleWmsEntity]]:
    """Discover available Oracle WMS entities.

    Args:
      client: Configured Oracle WMS client

    Returns:
      FlextResult containing list of discovered entities or error details

    """
    print("🔍 Discovering Oracle WMS entities...")

    result = await client.discover_entities()

    if result.success:
      entities = result.data
      print(f"✅ Successfully discovered {len(entities)} WMS entities")

      # Display entity information
      for entity in entities[:5]:  # Show first 5 entities
          # entities are strings (entity names), not objects
          entity_name = (
              entity
              if isinstance(entity, str)
              else getattr(entity, "name", str(entity))
          )
          print(f"   📦 {entity_name}")
          # Additional info only available if entity is an object
          if hasattr(entity, "description") and getattr(entity, "description", None):
              print(f"      Description: {entity.description}")
          if hasattr(entity, "entity_type"):
              print(f"      Type: {entity.entity_type}")

      if len(entities) > MAX_ENTITIES_TO_SHOW:
          print(f"   ... and {len(entities) - MAX_ENTITIES_TO_SHOW} more entities")

      return result
    print(f"❌ Entity discovery failed: {result.error}")
    return result


async def query_entity_data(
    client: FlextOracleWmsClient,
    entity_name: str,
) -> FlextResult[list[dict[str, Any]]]:
    """Query data from a specific Oracle WMS entity.

    Args:
      client: Configured Oracle WMS client
      entity_name: Name of the entity to query

    Returns:
      FlextResult containing entity data or error details

    """
    print(f"📊 Querying data from entity: {entity_name}")

    # Query with basic parameters
    result = await client.get_entity_data(
      entity_name=entity_name,
      limit=10,  # Limit results for example
    )

    if result.success:
      data = result.data
      print(
          f"✅ Successfully retrieved {len(data) if data else 0} records from {entity_name}",
      )

      # Display sample data structure with safety checks
      if data:
          # Check if data is list-like or dict-like
          if isinstance(data, (list, tuple)) and len(data) > 0:
              sample_record = data[0]
          elif isinstance(data, dict):
              # If data is a dict, use it as the sample record
              sample_record = data
          else:
              print(f"   📋 Unexpected data type: {type(data)}")
              print(f"   📋 Raw data: {str(data)[:200]}")
              return result

          # Safety check: ensure sample_record is a dict-like object
          if hasattr(sample_record, "keys") or isinstance(sample_record, dict):
              field_names = list(sample_record.keys())[:5]  # Show first 5 fields
              print(f"   📋 Sample fields: {', '.join(field_names)}")

              # Show sample values (first record, first few fields)
              print("   🔍 Sample data:")
              for field in field_names:
                  try:
                      value = (
                          sample_record.get(field, "N/A")
                          if hasattr(sample_record, "get")
                          else getattr(sample_record, field, "N/A")
                      )
                      # Truncate long values for display
                      display_value = (
                          str(value)[:MAX_VALUE_DISPLAY_LENGTH] + "..."
                          if len(str(value)) > MAX_VALUE_DISPLAY_LENGTH
                          else str(value)
                      )
                      print(f"      {field}: {display_value}")
                  except Exception as e:
                      print(f"      {field}: <Error reading field: {e}>")
          else:
              print(f"   📋 Raw data type: {type(sample_record)}")
              print(f"   📋 Raw data: {str(sample_record)[:100]}")
      elif data is not None:
          print(f"   📋 Empty result set (length: {len(data)})")
      else:
          print("   📋 No data returned (data is None)")

      return result
    print(f"❌ Data query failed for {entity_name}: {result.error}")
    return result


async def demonstrate_error_handling(client: FlextOracleWmsClient) -> None:
    """Demonstrate proper error handling patterns with FlextResult."""
    print("🧪 Demonstrating error handling...")

    # Attempt to query a non-existent entity
    result = await client.get_entity_data("NON_EXISTENT_ENTITY")

    if result.is_failure:
      print("✅ Error handling working correctly:")
      print(f"   Error: {result.error}")

      # Check for specific error types
      if "not found" in result.error.lower():
          print("   📝 This is expected - entity does not exist")
      elif "authentication" in result.error.lower():
          print("   🔐 Authentication issue detected")
      elif "timeout" in result.error.lower():
          print("   ⏱️ Timeout issue detected")
      else:
          print("   ❓ Other error type")
    else:
      print("⚠️  Expected error but got success - this is unusual")


async def main() -> None:
    """Main example function demonstrating basic Oracle WMS usage patterns.

    This function demonstrates:
    1. Configuration from environment variables
    2. Client initialization
    3. Entity discovery
    4. Data querying
    5. Error handling patterns
    """
    print("🚀 FLEXT Oracle WMS - Basic Usage Example")
    print("=" * 50)

    try:
      # Step 1: Create configuration
      print("⚙️  Creating Oracle WMS client configuration...")
      config = create_client_config()
      print(f"   Base URL: {config.base_url}")
      print(f"   API Version: {config.api_version}")
      print(f"   Timeout: {config.timeout}s")

      # Step 2: Initialize client
      print("\n🔧 Initializing Oracle WMS client...")
      client = FlextOracleWmsClient(config)

      # Start the client (required for API operations)
      start_result = await client.start()
      if start_result.success:
          print("   Client started successfully")
      else:
          print(f"   ❌ Failed to start client: {start_result.error}")
          return

      # Step 3: Discover entities
      print("\n" + "=" * 50)
      entities_result = await discover_wms_entities(client)

      if entities_result.success:
          entities = entities_result.data

          # Step 4: Query data from first available entity
          if entities:
              print("\n" + "=" * 50)
              first_entity = entities[0]
              # first_entity is a string (entity name), not an object
              entity_name = (
                  first_entity
                  if isinstance(first_entity, str)
                  else getattr(first_entity, "name", str(first_entity))
              )
              await query_entity_data(client, entity_name)

      # Step 5: Demonstrate error handling
      print("\n" + "=" * 50)
      await demonstrate_error_handling(client)

      print("\n✅ Basic usage example completed successfully!")
      print("\n💡 Next steps:")
      print("   - Explore entity_discovery.py for advanced discovery patterns")
      print("   - Check inventory_queries.py for specialized inventory operations")
      print("   - Review authentication.py for different auth methods")

    except ValueError as e:
      print(f"❌ Configuration error: {e}")
      print("\n💡 Setup instructions:")
      print("   1. Set required environment variables:")
      print(
          "      export FLEXT_ORACLE_WMS_BASE_URL='https://your-wms.oraclecloud.com'",
      )
      print("      export FLEXT_ORACLE_WMS_USERNAME='your_username'")
      print("      export FLEXT_ORACLE_WMS_PASSWORD='your_password'")
      print("   2. Run the example again")

    except FlextOracleWmsError as e:
      print(f"❌ Oracle WMS error: {e}")
      print("   Check your credentials and network connectivity")

    except Exception as e:
      print(f"❌ Unexpected error: {e}")
      print(f"   Error type: {type(e)}")
      print(f"   Error details: {e!r}")
      print("   Please check the error details and try again")
      # Re-raise for debugging in development
      if os.getenv("FLEXT_DEBUG_MODE", "").lower() in {"true", "1", "yes"}:
          raise


if __name__ == "__main__":
    # Set debug logging for example
    os.environ.setdefault("FLEXT_LOG_LEVEL", "info")

    print("Starting basic Oracle WMS usage example...")
    asyncio.run(main())
