"""FlextOracleWms Configuration Class - Single Responsibility Principle.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Oracle WMS configuration management with proper prefixing and
Clean Architecture principles.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

# Import from flext-core root namespace as required
from flext_core import FlextEntity, FlextResult
from pydantic import Field


class FlextOracleWmsConfig(FlextEntity):
    """FlextOracleWms configuration management.

    Provides comprehensive configuration management for Oracle WMS
    operations following SOLID principles.
    """

    base_url: str = Field(..., description="Oracle WMS API base URL")
    username: str = Field(..., description="Oracle WMS username")
    password: str = Field(..., description="Oracle WMS password")
    api_version: str = Field(default="v10", description="Oracle WMS API version")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    retries: int = Field(default=3, description="Number of retry attempts")
    page_size: int = Field(default=100, description="Default page size")
    max_page_size: int = Field(default=1000, description="Maximum page size")
    flatten_enabled: bool = Field(default=True, description="Enable data flattening")
    flatten_separator: str = Field(default="__", description="Flattening separator")

    def validate_connection_info(self) -> FlextResult[bool]:
        """Validate connection configuration.

        Returns:
            FlextResult with validation status

        """
        try:
            if not self.base_url:
                return FlextResult.fail("Base URL is required")

            if not self.username:
                return FlextResult.fail("Username is required")

            if not self.password:
                return FlextResult.fail("Password is required")

            if not self.base_url.startswith(("http://", "https://")):
                return FlextResult.fail("Invalid base URL format")

            if self.timeout <= 0:
                return FlextResult.fail("Timeout must be positive")

            if self.retries < 0:
                return FlextResult.fail("Retries must be non-negative")

            return FlextResult.ok(True)

        except Exception as e:
            return FlextResult.fail(f"Configuration validation failed: {e}")

    def get_connection_info(self) -> FlextResult[dict[str, Any]]:
        """Get connection information dictionary.

        Returns:
            FlextResult with connection info

        """
        try:
            connection_info = {
                "base_url": self.base_url,
                "username": self.username,
                "password": self.password,
                "api_version": self.api_version,
                "timeout": self.timeout,
                "retries": self.retries,
            }
            return FlextResult.ok(connection_info)

        except Exception as e:
            return FlextResult.fail(f"Connection info extraction failed: {e}")

    def get_pagination_config(self) -> FlextResult[dict[str, Any]]:
        """Get pagination configuration.

        Returns:
            FlextResult with pagination config

        """
        try:
            pagination_config = {
                "page_size": self.page_size,
                "max_page_size": self.max_page_size,
            }
            return FlextResult.ok(pagination_config)

        except Exception as e:
            return FlextResult.fail(f"Pagination config extraction failed: {e}")

    def get_flattening_config(self) -> FlextResult[dict[str, Any]]:
        """Get flattening configuration.

        Returns:
            FlextResult with flattening config

        """
        try:
            flattening_config = {
                "enabled": self.flatten_enabled,
                "separator": self.flatten_separator,
            }
            return FlextResult.ok(flattening_config)

        except Exception as e:
            return FlextResult.fail(f"Flattening config extraction failed: {e}")
