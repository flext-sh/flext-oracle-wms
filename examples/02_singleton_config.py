"""Oracle WMS Configuration Singleton Example.

This example demonstrates how to use FlextOracleWmsSettings as a singleton
that extends flext-core's FlextSettings singleton pattern.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os

from flext_core import FlextLogger

from flext_oracle_wms.constants import FlextOracleWmsConstants
from flext_oracle_wms.settings import (
    FlextOracleWmsSettings,
)
from flext_oracle_wms.wms_client import FlextOracleWmsClient

logger = FlextLogger(__name__)


def demonstrate_singleton_config() -> None:
    """Demonstrate Oracle WMS configuration singleton usage with dynamic parameters."""
    logger.info("=== Oracle WMS Configuration Singleton Demo ===")
    logger.info("1. Using global singleton instance with defaults...")
    config = FlextOracleWmsSettings()
    logger.info("   Base URL: %s", config.base_url)
    logger.info("   Config Type: %s", type(config).__name__)
    logger.info("2. Updating global singleton with new parameters...")
    updated_config = FlextOracleWmsSettings(timeout=60, retry_attempts=5)
    logger.info("   Updated Timeout: %s", str(updated_config.timeout))
    logger.info("   Updated Max Retries: %s", str(updated_config.retry_attempts))
    logger.info("   Same instance? %s", str(config is updated_config))
    logger.info("3. Creating from environment with overrides...")
    env_config = FlextOracleWmsSettings(
        timeout=float(FlextOracleWmsConstants.OracleWms.DEFAULT_TIMEOUT * 3),
    )
    logger.info("   Oracle WMS URL: %s", env_config.base_url)
    logger.info("   Username: %s", env_config.username)
    logger.info("   Timeout: %s", str(env_config.timeout))
    logger.info("4. Creating configuration for different environment...")
    new_config = FlextOracleWmsSettings(
        base_url="https://new-environment.wms.oraclecloud.com/test",
        username="NEW_USER",
        password="NEW_PASSWORD",
        timeout=float(FlextOracleWmsConstants.OracleWms.DEFAULT_TIMEOUT * 4),
    )
    if new_config:
        logger.info("   New Base URL: %s", new_config.base_url)
        logger.info("   New Username: %s", new_config.username)
        logger.info("   New Timeout: %s", str(new_config.timeout))
    else:
        logger.error("   Failed to create new configuration")
    logger.info("5. Resetting global instance...")
    fresh_config = FlextOracleWmsSettings(
        base_url="https://fresh.wms.oraclecloud.com/fresh",
        username="FRESH_USER",
        password="FRESH_PASSWORD",
    )
    logger.info("   Fresh Base URL: %s", fresh_config.base_url)
    logger.info("   Fresh Username: %s", fresh_config.username)
    logger.info("6. Creating testing configuration...")
    test_config = FlextOracleWmsSettings(use_mock=True)
    logger.info("   Test URL: %s", test_config.base_url)
    logger.info("   Test Username: %s", test_config.username)
    logger.info("   Use Mock: %s", str(test_config.use_mock))
    logger.info("7. Validating configuration...")
    validation_result = test_config.validate_config()
    if validation_result.is_success:
        logger.info("   Configuration validation passed")
    else:
        logger.error(
            "   Configuration validation failed: %s", str(validation_result.error)
        )
    logger.info("8. Creating client with configuration...")
    try:
        client = FlextOracleWmsClient(config=test_config)
        logger.info("   Client created successfully with config")
        logger.info("   Client config URL: %s", client.config.base_url)
    except (RuntimeError, OSError, ValueError):
        logger.exception("   Failed to create client")
    logger.info("=== Demo Complete ===")


def demonstrate_environment_variables() -> None:
    """Demonstrate how environment variables affect configuration."""
    logger.info("=== Environment Variables Demo ===")
    logger.info("Current Oracle WMS environment variables:")
    oracle_wms_vars = {
        key: value
        for key, value in os.environ.items()
        if key.startswith(("FLEXT_", "ORACLE_WMS_"))
    }
    if oracle_wms_vars:
        for key, value in oracle_wms_vars.items():
            display_value = value
            if "PASSWORD" in key or "SECRET" in key or "KEY" in key:
                display_value = "***"
            logger.info("   %s: %s", key, display_value)
    else:
        logger.info("   No Oracle WMS environment variables found")
    logger.info("\nTo set Oracle WMS environment variables:")
    logger.info(
        "   export FLEXT_ORACLE_WMS_BASE_URL='https://your-wms.oraclecloud.com'",
    )
    logger.info("   export FLEXT_ORACLE_WMS_USERNAME='your_username'")
    logger.info("   export FLEXT_ORACLE_WMS_PASSWORD='your_password'")
    logger.info("   export FLEXT_ORACLE_WMS_TIMEOUT='60'")
    logger.info("   export FLEXT_ORACLE_WMS_MAX_RETRIES='5'")


def main() -> None:
    """Main function."""
    try:
        demonstrate_singleton_config()
        demonstrate_environment_variables()
    except (RuntimeError, OSError, ValueError):
        logger.exception("Demo failed")
        raise


if __name__ == "__main__":
    main()
