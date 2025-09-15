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

from flext_core import FlextLogger, FlextResult, FlextTypes

from flext_oracle_wms import (
    FlextOracleWmsClient,
    FlextOracleWmsClientConfig,
    FlextOracleWmsError,
)

# Constants for example display
MAX_ENTITIES_TO_SHOW = 5
MAX_VALUE_DISPLAY_LENGTH = 50

# Initialize logger
logger = FlextLogger(__name__)

# Load .env file from project root
try:
    from dotenv import load_dotenv

    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    pass


def create_client_config() -> FlextOracleWmsClientConfig:
    """Create Oracle WMS client configuration using singleton pattern.

    This function demonstrates how to use the global singleton configuration
    with environment variables and parameter overrides.
    """
    # Method 1: Use global singleton with environment variables
    env_result = FlextOracleWmsClientConfig.create_from_environment()

    if env_result.success:
        # Cast the generic FlextConfig to Oracle WMS specific config
        return FlextOracleWmsClientConfig(**env_result.value.model_dump())

    # Method 2: Fallback to global singleton with default values
    # if environment variables are not set
    return FlextOracleWmsClientConfig.get_oracle_wms_global_instance()


async def discover_wms_entities(
    client: FlextOracleWmsClient,
) -> FlextResult[list[FlextTypes.Core.Dict]]:
    """Discover available Oracle WMS entities.

    Args:
      client: Configured Oracle WMS client

    Returns:
      FlextResult containing list of discovered entities or error details

    """
    result = await client.discover_entities()

    if result.success:
        entities = result.data
        if entities is None:
            return result

        # Display entity information
        for entity in entities[:5]:  # Show first 5 entities
            # entities are dictionaries with name field
            entity_display = entity.get("name", "Unknown") if isinstance(entity, dict) else str(entity)
            logger.debug(f"Processing entity: {entity_display}")
            # Additional info only available if entity is an object
            if hasattr(entity, "description") and getattr(entity, "description", None):
                pass
            if hasattr(entity, "entity_type"):
                pass

        if entities and len(entities) > MAX_ENTITIES_TO_SHOW:
            pass

        return result
    return result


async def query_entity_data(
    client: FlextOracleWmsClient,
    entity_name: str,
) -> FlextResult[FlextTypes.Core.Dict | list[FlextTypes.Core.Dict]]:
    """Query data from a specific Oracle WMS entity.

    Args:
      client: Configured Oracle WMS client
      entity_name: Name of the entity to query

    Returns:
      FlextResult containing entity data or error details

    """
    # Query with basic parameters
    result = await client.get_entity_data(
        entity_name=entity_name,
        limit=10,  # Limit results for example
    )

    if result.success:
        data = result.data

        # Display sample data structure with safety checks
        if data:
            # Check if data is list-like or dict-like
            if isinstance(data, (list, tuple)) and len(data) > 0:
                sample_record = data[0]
            elif isinstance(data, dict):
                # If data is a dict, use it as the sample record
                sample_record = data
            else:
                return result

            # Safety check: ensure sample_record is a dict-like object
            if hasattr(sample_record, "keys") or isinstance(sample_record, dict):
                field_names = list(sample_record.keys())[:5]  # Show first 5 fields

                # Show sample values (first record, first few fields)
                for field in field_names:
                    try:
                        value = (
                            sample_record.get(field, "N/A")
                            if hasattr(sample_record, "get")
                            else getattr(sample_record, field, "N/A")
                        )
                        # Truncate long values for display
                        (
                            str(value)[:MAX_VALUE_DISPLAY_LENGTH] + "..."
                            if len(str(value)) > MAX_VALUE_DISPLAY_LENGTH
                            else str(value)
                        )
                    except (KeyError, ValueError, TypeError) as e:
                        logger.debug(f"Display formatting failed: {e}")
        elif data is not None:
            pass

        return result
    return result


async def demonstrate_error_handling(client: FlextOracleWmsClient) -> None:
    """Demonstrate proper error handling patterns with FlextResult."""
    # Attempt to query a non-existent entity
    result = await client.get_entity_data("NON_EXISTENT_ENTITY")

    if result.is_failure and result.error and (
        "not found" in result.error.lower()
        or "authentication" in result.error.lower()
        or "timeout" in result.error.lower()
    ):
        logger.info(f"Expected error handled: {result.error}")


async def main() -> None:
    """Main example function demonstrating basic Oracle WMS usage patterns.

    This function demonstrates:
    1. Configuration using singleton pattern
    2. Client initialization with global config
    3. Entity discovery
    4. Data querying
    5. Error handling patterns
    """
    try:
        # Step 1: Create configuration using singleton pattern
        config = create_client_config()
        print(f"Using configuration: {config.oracle_wms_base_url}")

        # Step 2: Initialize client (can use global singleton automatically)
        # Option A: Use explicit config
        client = FlextOracleWmsClient(config)

        # Option B: Use global singleton (no config parameter needed)
        # client = FlextOracleWmsClient()  # Uses global singleton automatically

        # Start the client (required for API operations)
        start_result = await client.start()
        if start_result.success:
            pass
        else:
            return

        # Step 3: Discover entities
        entities_result = await discover_wms_entities(client)

        if entities_result.success:
            entities = entities_result.data
            print(f"Successfully discovered {len(entities) if entities else 0} entities")

            # Step 4: Query data from first available entity
            if entities:
                first_entity = entities[0]
                # first_entity is a dictionary with entity information
                entity_name = (
                    first_entity.get("name", "Unknown")
                    if isinstance(first_entity, dict)
                    else str(first_entity)
                )
                await query_entity_data(client, str(entity_name))
        else:
            # Handle case when Oracle WMS is not available
            print(f"Entity discovery failed: {entities_result.error}")
            print("This is expected when Oracle WMS is not available or configured")

        # Step 5: Demonstrate error handling
        await demonstrate_error_handling(client)

        print("Example completed successfully")

    except ValueError:
        pass

    except FlextOracleWmsError:
        pass

    except Exception:
        # Re-raise for debugging in development
        if os.getenv("FLEXT_DEBUG_MODE", "").lower() in {"true", "1", "yes"}:
            raise


if __name__ == "__main__":
    # Set debug logging for example
    os.environ.setdefault("FLEXT_LOG_LEVEL", "info")

    asyncio.run(main())
