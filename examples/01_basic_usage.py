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

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from flext_core import FlextContainer, FlextLogger, r

from flext_oracle_wms import (
    FlextOracleWmsClient,
    FlextOracleWmsExceptions,
    FlextOracleWmsSettings,
    t,
)

MAX_ENTITIES_TO_SHOW = 5
MAX_VALUE_DISPLAY_LENGTH = 50
logger = FlextLogger(__name__)
project_root = Path(__file__).parent.parent
env_file = project_root / ".env"
if env_file.exists():
    load_dotenv(env_file)


def setup_client_config() -> None:
    """Set up Oracle WMS client configuration in global container.

    This function demonstrates how to configure the global singleton
    with environment variables and parameter overrides.
    """
    container = FlextContainer.get_global()
    config = FlextOracleWmsSettings(
        base_url=os.getenv("FLEXT_ORACLE_WMS_BASE_URL", "https://wms.oraclecloud.com"),
        username=os.getenv("FLEXT_ORACLE_WMS_USERNAME"),
        password=os.getenv("FLEXT_ORACLE_WMS_PASSWORD"),
    )
    _ = container.register("FlextOracleWmsSettings", config)


def discover_wms_entities(
    client: FlextOracleWmsClient,
) -> r[list[dict[str, t.NormalizedValue]]]:
    """Discover available Oracle WMS entities.

    Args:
      client: Configured Oracle WMS client

    Returns:
      r containing list of discovered entities or error details

    """
    result = client.discover_entities()
    if result.is_success:
        entities = result.value
        if entities is None:
            return result
        for entity in entities[:5]:
            entity_display = (
                entity.get("name", "Unknown")
                if isinstance(entity, dict)
                else str(entity)
            )
            logger.debug("Processing entity: %s", entity_display)
            if hasattr(entity, "description") and getattr(entity, "description", None):
                pass
            if hasattr(entity, "entity_type"):
                pass
        if entities and len(entities) > MAX_ENTITIES_TO_SHOW:
            pass
        return result
    return result


def query_entity_data(
    client: FlextOracleWmsClient, entity_name: str
) -> r[list[dict[str, t.NormalizedValue]]]:
    """Query data from a specific Oracle WMS entity.

    Args:
      client: Configured Oracle WMS client
      entity_name: Name of the entity to query

    Returns:
      r containing entity data or error details

    """
    result = client.get_entity_data(entity_name=entity_name, limit=10)
    if result.is_success:
        data = result.value
        if data:
            if isinstance(data, (list, tuple)) and len(data) > 0:
                sample_record = data[0]
            elif isinstance(data, dict):
                sample_record = data
            else:
                return result
            if hasattr(sample_record, "keys") or isinstance(sample_record, dict):
                field_names = list(sample_record.keys())[:5]
                for field in field_names:
                    try:
                        value = (
                            sample_record.get(field, "N/A")
                            if hasattr(sample_record, "get")
                            else getattr(sample_record, field, "N/A")
                        )
                        str(value)[:MAX_VALUE_DISPLAY_LENGTH] + "..." if len(
                            str(value)
                        ) > MAX_VALUE_DISPLAY_LENGTH else str(value)
                    except (KeyError, ValueError, TypeError) as e:
                        logger.debug("Display formatting failed: %s", e)
        elif data is not None:
            pass
        return result
    return result


def demonstrate_error_handling(client: FlextOracleWmsClient) -> None:
    """Demonstrate proper error handling patterns with r."""
    result = client.get_entity_data("NON_EXISTENT_ENTITY")
    if (
        result.is_failure
        and result.error
        and (
            "not found" in result.error.lower()
            or "authentication" in result.error.lower()
            or "timeout" in result.error.lower()
        )
    ):
        logger.info(f"Expected error handled: {result.error}")


def main() -> None:
    """Main example function demonstrating basic Oracle WMS usage patterns.

    This function demonstrates:
    1. Configuration using singleton pattern
    2. Client initialization with global config
    3. Entity discovery
    4. Data querying
    5. Error handling patterns
    """
    try:
        setup_client_config()
        client = FlextOracleWmsClient()
        start_result = client.start()
        if start_result.is_success:
            pass
        else:
            return
        entities_result = discover_wms_entities(client)
        if entities_result.is_success:
            entities = entities_result.value
            if entities:
                first_entity = entities[0]
                entity_name = (
                    first_entity.get("name", "Unknown")
                    if isinstance(first_entity, dict)
                    else str(first_entity)
                )
                query_entity_data(client, str(entity_name))
        demonstrate_error_handling(client)
    except FlextOracleWmsExceptions.BaseError:
        logger.exception("Oracle WMS error")
    except ValueError:
        logger.exception("Configuration error")
    except Exception:
        if os.getenv("FLEXT_DEBUG_MODE", "").lower() in {"true", "1", "yes"}:
            raise


if __name__ == "__main__":
    os.environ.setdefault("FLEXT_LOG_LEVEL", "info")
    main()
