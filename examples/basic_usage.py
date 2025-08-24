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
    from dotenv import load_dotenv
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    pass


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
    result = await client.discover_entities()

    if result.success:
        entities = result.data

        # Display entity information
        for entity in entities[:5]:  # Show first 5 entities
            # entities are strings (entity names), not objects
            (
                entity
                if isinstance(entity, str)
                else getattr(entity, "name", str(entity))
            )
            # Additional info only available if entity is an object
            if hasattr(entity, "description") and getattr(entity, "description", None):
                pass
            if hasattr(entity, "entity_type"):
                pass

        if len(entities) > MAX_ENTITIES_TO_SHOW:
            pass

        return result
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
                    except Exception:
                        pass
        elif data is not None:
            pass

        return result
    return result


async def demonstrate_error_handling(client: FlextOracleWmsClient) -> None:
    """Demonstrate proper error handling patterns with FlextResult."""
    # Attempt to query a non-existent entity
    result = await client.get_entity_data("NON_EXISTENT_ENTITY")

    if result.is_failure:

        # Check for specific error types
        if "not found" in result.error.lower() or "authentication" in result.error.lower() or "timeout" in result.error.lower():
            pass


async def main() -> None:
    """Main example function demonstrating basic Oracle WMS usage patterns.

    This function demonstrates:
    1. Configuration from environment variables
    2. Client initialization
    3. Entity discovery
    4. Data querying
    5. Error handling patterns
    """
    try:
        # Step 1: Create configuration
        config = create_client_config()

        # Step 2: Initialize client
        client = FlextOracleWmsClient(config)

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

            # Step 4: Query data from first available entity
            if entities:
                first_entity = entities[0]
                # first_entity is a string (entity name), not an object
                entity_name = (
                    first_entity
                    if isinstance(first_entity, str)
                    else getattr(first_entity, "name", str(first_entity))
                )
                await query_entity_data(client, entity_name)

        # Step 5: Demonstrate error handling
        await demonstrate_error_handling(client)

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
