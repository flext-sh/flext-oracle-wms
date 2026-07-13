"""Oracle WMS Configuration Singleton Example.

This example demonstrates how to use FlextOracleWmsSettings as a singleton
that extends flext-core's FlextSettings singleton pattern.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import os

from flext_oracle_wms import (
    FlextOracleWmsConstants,
    FlextOracleWmsSettings,
    FlextOracleWmsUtilitiesClient,
    u,
)

FlextOracleWmsClient = FlextOracleWmsUtilitiesClient.Client

logger = u.fetch_logger(__name__)


def demonstrate_singleton_config() -> None:
    """Demonstrate Oracle WMS configuration singleton usage with dynamic parameters."""
    logger.info("=== Oracle WMS Configuration Singleton Demo ===")
    logger.info("1. Using global singleton instance with defaults...")
    settings = FlextOracleWmsSettings.fetch_global()
    logger.info("   Base URL: %s", settings.OracleWms.base_url)
    logger.info("   Config Type: %s", type(settings).__name__)
    logger.info("2. Updating global singleton with new parameters...")
    updated_config = FlextOracleWmsSettings.update_global(
        OracleWms={"timeout": 60, "retry_attempts": 5},
    )
    logger.info("   Updated Timeout: %s", updated_config.OracleWms.timeout)
    logger.info("   Updated Max Retries: %s", updated_config.OracleWms.retry_attempts)
    logger.info("   Same instance? %s", settings is updated_config)
    logger.info("3. Creating isolated clone with overrides...")
    env_config = FlextOracleWmsSettings.fetch_global(
        overrides={
            "OracleWms": {
                "timeout": float(FlextOracleWmsConstants.OracleWms.DEFAULT_TIMEOUT * 3),
            },
        },
    )
    logger.info("   Oracle WMS URL: %s", env_config.OracleWms.base_url)
    logger.info("   Username: %s", env_config.OracleWms.username)
    logger.info("   Timeout: %s", env_config.OracleWms.timeout)
    logger.info("4. Creating configuration for different environment...")
    new_config = FlextOracleWmsSettings.fetch_global(
        overrides={
            "OracleWms": {
                "base_url": "https://new-environment.wms.oraclecloud.com/test",
                "username": "NEW_USER",
                "password": "NEW_PASSWORD",
                "timeout": float(
                    FlextOracleWmsConstants.OracleWms.DEFAULT_TIMEOUT * 4,
                ),
            },
        },
    )
    logger.info("   New Base URL: %s", new_config.OracleWms.base_url)
    logger.info("   New Username: %s", new_config.OracleWms.username)
    logger.info("   New Timeout: %s", new_config.OracleWms.timeout)
    logger.info("5. Resetting global instance...")
    FlextOracleWmsSettings.reset_for_testing()
    fresh_config = FlextOracleWmsSettings.fetch_global(
        overrides={
            "OracleWms": {
                "base_url": "https://fresh.wms.oraclecloud.com/fresh",
                "username": "FRESH_USER",
                "password": "FRESH_PASSWORD",
            },
        },
    )
    logger.info("   Fresh Base URL: %s", fresh_config.OracleWms.base_url)
    logger.info("   Fresh Username: %s", fresh_config.OracleWms.username)
    logger.info("6. Creating testing configuration...")
    test_config = FlextOracleWmsSettings.model_validate({
        "OracleWms": {
            "base_url": "https://test-wms.example.com",
            "timeout": 30.0,
            "username": "test_user",
            "password": "test_password",
        },
    })
    logger.info("   Test URL: %s", test_config.OracleWms.base_url)
    logger.info("   Test Username: %s", test_config.OracleWms.username)
    logger.info("7. Round-tripping configuration through model_dump...")
    redumped = FlextOracleWmsSettings.model_validate(test_config.model_dump())
    if redumped.OracleWms.base_url == test_config.OracleWms.base_url:
        logger.info("   Configuration round-trip passed")
    else:
        logger.error("   Configuration round-trip drifted")
    logger.info("8. Creating client with configuration...")
    try:
        client = FlextOracleWmsClient(settings=test_config)
        logger.info("   Client created successfully with settings")
        logger.info("   Client settings URL: %s", client.settings.OracleWms.base_url)
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
        "   export FLEXT_ORACLE_WMS_ORACLEWMS__BASE_URL='https://your-wms.oraclecloud.com'",
    )
    logger.info("   export FLEXT_ORACLE_WMS_ORACLEWMS__USERNAME='your_username'")
    logger.info("   export FLEXT_ORACLE_WMS_ORACLEWMS__PASSWORD='your_password'")
    logger.info("   export FLEXT_ORACLE_WMS_ORACLEWMS__TIMEOUT='60'")
    logger.info("   export FLEXT_ORACLE_WMS_ORACLEWMS__RETRY_ATTEMPTS='5'")


def main() -> None:
    """Demonstrate singleton configuration."""
    try:
        demonstrate_singleton_config()
        demonstrate_environment_variables()
    except (RuntimeError, OSError, ValueError):
        logger.exception("Demo failed")
        raise


if __name__ == "__main__":
    main()
