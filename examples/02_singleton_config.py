#!/usr/bin/env python3
"""Oracle WMS Configuration Singleton Example.

This example demonstrates how to use FlextOracleWmsSettings as a singleton
that extends flext-core's FlextSettings singleton pattern.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

import os

from flext import FlextLogger
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsSettings
from flext_oracle_wms.constants import FlextOracleWmsConstants

logger = FlextLogger(__name__)


def demonstrate_singleton_config() -> None:
    """Demonstrate Oracle WMS configuration singleton usage with dynamic parameters."""
    logger.info("=== Oracle WMS Configuration Singleton Demo ===")

    # Method 1: Use the global singleton instance with default values
    logger.info("1. Using global singleton instance with defaults...")
    config = FlextOracleWmsSettings()
    logger.info(f"   Base URL: {config.base_url}")
    logger.info(f"   Environment: {config.environment}")
    logger.info(f"   App Name: {config.app_name}")
    logger.info(f"   Config Type: {type(config).__name__}")

    # Method 2: Create new config instance with different parameters
    logger.info("2. Updating global singleton with new parameters...")
    updated_config = FlextOracleWmsSettings(timeout=60, retry_attempts=5)
    logger.info(f"   Updated Timeout: {updated_config.timeout}")
    logger.info(f"   Updated Max Retries: {updated_config.retry_attempts}")
    logger.info(f"   Same instance? {config is updated_config}")

    # Method 3: Create from environment variables with overrides
    logger.info("3. Creating from environment with overrides...")
    env_config = FlextOracleWmsSettings(
        timeout=FlextOracleWmsConstants.Connection.DEFAULT_TIMEOUT * 3,
        enable_ssl_verification=False,
    )
    logger.info(f"   Oracle WMS URL: {env_config.base_url}")
    logger.info(f"   Username: {env_config.username}")
    logger.info(f"   Timeout: {env_config.timeout}")
    logger.info(f"   Verify SSL: {env_config.enable_ssl_verification}")

    # Method 4: Create new configuration for different environment
    logger.info("4. Creating configuration for different environment...")
    new_config = FlextOracleWmsSettings(
        base_url="https://new-environment.wms.oraclecloud.com/test",
        username="NEW_USER",
        password="NEW_PASSWORD",
        timeout=FlextOracleWmsConstants.Connection.DEFAULT_TIMEOUT * 4,
    )
    if new_config:
        logger.info(f"   New Base URL: {new_config.base_url}")
        logger.info(f"   New Username: {new_config.username}")
        logger.info(f"   New Timeout: {new_config.timeout}")
    else:
        logger.error("   Failed to create new configuration")

    # Method 5: Reset and create fresh instance
    logger.info("5. Resetting global instance...")
    # Note: reset_global_instance doesn't exist, using new instance
    fresh_config = FlextOracleWmsSettings(
        base_url="https://fresh.wms.oraclecloud.com/fresh",
        username="FRESH_USER",
        password="FRESH_PASSWORD",
    )
    logger.info(f"   Fresh Base URL: {fresh_config.base_url}")
    logger.info(f"   Fresh Username: {fresh_config.username}")

    # Method 6: Create testing configuration
    logger.info("6. Creating testing configuration...")
    test_config = FlextOracleWmsSettings(use_mock=True)
    logger.info(f"   Test URL: {test_config.base_url}")
    logger.info(f"   Test Username: {test_config.username}")
    logger.info(f"   Use Mock: {test_config.use_mock}")

    # Demonstrate configuration validation
    logger.info("7. Validating configuration...")
    validation_result = test_config.validate_business_rules()
    if validation_result.is_success:
        logger.info("   ✅ Configuration validation passed")
    else:
        logger.error(
            f"   ❌ Configuration validation failed: {validation_result.error}",
        )

    # Demonstrate environment extraction
    logger.info("8. Extracting environment from URL...")
    env_from_url = test_config.extract_environment_from_url()
    logger.info("   Extracted environment: %s", env_from_url)

    # Demonstrate client creation with singleton config (no config parameter)
    logger.info("9. Creating client with global singleton configuration...")
    try:
        # Client will automatically use the global singleton config
        client = FlextOracleWmsClient()  # No config parameter needed!
        logger.info("   ✅ Client created successfully with global config")
        logger.info(f"   Client config URL: {client.config.base_url}")

        # Test health check
        health_result = client.health_check()
        if health_result.is_success:
            logger.info("   ✅ Health check passed")
            logger.info(f"   Service: {health_result.value.get('service', 'Unknown')}")
        else:
            logger.error(f"   ❌ Health check failed: {health_result.error}")

    except Exception:
        logger.exception("   ❌ Failed to create client")

    logger.info("=== Demo Complete ===")


def demonstrate_environment_variables() -> None:
    """Demonstrate how environment variables affect configuration."""
    logger.info("=== Environment Variables Demo ===")

    # Show current environment variables
    logger.info("Current Oracle WMS environment variables:")
    oracle_wms_vars = {
        key: value
        for key, value in os.environ.items()
        if key.startswith(("FLEXT_", "ORACLE_WMS_"))
    }

    if oracle_wms_vars:
        for key, value in oracle_wms_vars.items():
            # Mask sensitive values
            display_value = value
            if "PASSWORD" in key or "SECRET" in key or "KEY" in key:
                display_value = "***"
            logger.info("   %s: %s", key, display_value)
    else:
        logger.info("   No Oracle WMS environment variables found")

    # Show how to set environment variables for testing
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
    except Exception:
        logger.exception("Demo failed")
        raise


if __name__ == "__main__":
    main()
