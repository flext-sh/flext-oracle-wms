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
from typing import TYPE_CHECKING, Final

from dotenv import load_dotenv

from flext_core import FlextContainer
from flext_oracle_wms import (
    FlextOracleWmsSettings,
    FlextOracleWmsUtilitiesClient,
    p,
    t,
    u,
)
from flext_oracle_wms.errors import FlextOracleWmsErrors

if TYPE_CHECKING:
    from collections.abc import (
        Sequence,
    )

FlextOracleWmsClient = FlextOracleWmsUtilitiesClient.Client

MAX_ENTITIES_TO_SHOW: Final[int] = 5
MAX_VALUE_DISPLAY_LENGTH: Final[int] = 50
logger = u.fetch_logger(__name__)
project_root = Path(__file__).parent.parent
env_file = project_root / ".env"
if env_file.exists():
    load_dotenv(env_file)


def setup_client_config() -> None:
    """Set up Oracle WMS client configuration in global container.

    This function demonstrates how to configure the global singleton
    with environment variables and parameter overrides.
    """
    container = FlextContainer.shared()
    # NOTE (multi-agent): ADR-005 — project scalars are namespaced under the
    # ``OracleWms`` group; env vars use the nested ``ORACLEWMS__`` delimiter.
    settings = FlextOracleWmsSettings.model_validate({
        "OracleWms": {
            "base_url": os.getenv(
                "FLEXT_ORACLE_WMS_ORACLEWMS__BASE_URL",
                "https://wms.oraclecloud.com",
            ),
            "username": os.getenv("FLEXT_ORACLE_WMS_ORACLEWMS__USERNAME", ""),
            "password": os.getenv("FLEXT_ORACLE_WMS_ORACLEWMS__PASSWORD", ""),
        },
    })
    _ = container.bind(
        "FlextOracleWmsSettings",
        settings.model_dump(mode="python"),
    )


def discover_wms_entities(
    client: FlextOracleWmsClient,
) -> p.Result[t.StrSequence]:
    """Discover available Oracle WMS entities.

    Args:
      client: Configured Oracle WMS client

    Returns:
      r containing list of discovered entities or error details

    """
    result = client.discover_entities()
    if result.success:
        entities = result.value
        for entity in entities[:5]:
            logger.debug("Processing entity: %s", entity)
        if len(entities) > MAX_ENTITIES_TO_SHOW:
            logger.debug(
                "Additional entities omitted from preview: %s",
                len(entities) - MAX_ENTITIES_TO_SHOW,
            )
        return result
    return result


def query_entity_data(
    client: FlextOracleWmsClient,
    entity_name: str,
) -> p.Result[Sequence[t.StrMapping]]:
    """Query data from a specific Oracle WMS entity.

    Args:
      client: Configured Oracle WMS client
      entity_name: Name of the entity to query

    Returns:
      r containing entity data or error details

    """
    result = client.get_entity_data(entity_name=entity_name, limit=10)
    if result.success:
        data = result.value
        if data:
            sample_record: t.StrMapping = data[0]
            field_names: list[str] = list(sample_record.keys())[:5]
            for field in field_names:
                try:
                    value_str = sample_record.get(field, "N/A")
                    if len(value_str) > MAX_VALUE_DISPLAY_LENGTH:
                        _ = value_str[:MAX_VALUE_DISPLAY_LENGTH] + "..."
                    else:
                        _ = value_str
                except (KeyError, ValueError, TypeError) as e:
                    logger.debug("Display formatting failed: %s", e)
        return result
    return result


def demonstrate_error_handling(client: FlextOracleWmsClient) -> None:
    """Demonstrate proper error handling patterns with r."""
    result = client.get_entity_data("NON_EXISTENT_ENTITY")
    if (
        result.failure
        and result.error
        and (
            "not found" in result.error.lower()
            or "authentication" in result.error.lower()
            or "timeout" in result.error.lower()
        )
    ):
        logger.info(f"Expected error handled: {result.error}")


def run_basic_usage() -> None:
    """Run the basic Oracle WMS usage flow."""
    setup_client_config()
    client = FlextOracleWmsClient()
    start_result = client.start()
    if not start_result.success:
        return
    entities_result = discover_wms_entities(client)
    if entities_result.success:
        entities = entities_result.value
        if entities:
            query_entity_data(client, entities[0])
    demonstrate_error_handling(client)


def main() -> None:
    """Demonstrate basic Oracle WMS usage patterns.

    This function demonstrates:
    1. Configuration using singleton pattern
    2. Client initialization with global settings
    3. Entity discovery
    4. Data querying
    5. Error handling patterns
    """
    try:
        run_basic_usage()
    except FlextOracleWmsErrors.Error:
        logger.exception("Error in basic usage example")
    except ValueError:
        logger.exception("Configuration error")
    except (RuntimeError, OSError):
        if os.getenv("FLEXT_DEBUG_MODE", "").lower() in {"true", "1", "yes"}:
            raise


if __name__ == "__main__":
    os.environ.setdefault("FLEXT_LOG_LEVEL", "info")
    main()
