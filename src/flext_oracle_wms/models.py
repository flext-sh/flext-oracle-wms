"""Essential Oracle WMS Models - Only what's actually used.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Minimal models using flext-core standards.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from flext_oracle_wms.constants import (
    FlextOracleWmsDefaults,
    FlextOracleWmsErrorMessages,
)
from flext_oracle_wms.exceptions import (
    FlextOracleWmsDataValidationError,
)


@dataclass(frozen=True)
class FlextOracleWmsEntity:
    """Oracle WMS entity model - USED BY DISCOVERY."""

    name: str
    endpoint: str
    description: str | None = None
    fields: dict[str, Any] | None = field(default_factory=dict)
    primary_key: str | None = None
    replication_key: str | None = None
    supports_incremental: bool = False

    def validate_domain_rules(self) -> None:
        """Validate entity domain rules.

        Raises:
            FlextOracleWmsDataValidationError: If entity data is invalid

        """
        if not isinstance(self.name, str) or not self.name.strip():
            msg = (
                f"{FlextOracleWmsErrorMessages.ENTITY_VALIDATION_FAILED}: "
                "Entity name cannot be empty"
            )
            raise FlextOracleWmsDataValidationError(msg)

        if not isinstance(self.endpoint, str) or not self.endpoint.strip():
            msg = (
                f"{FlextOracleWmsErrorMessages.ENTITY_VALIDATION_FAILED}: "
                "Entity endpoint cannot be empty"
            )
            raise FlextOracleWmsDataValidationError(msg)

        if not self.endpoint.startswith("/"):
            msg = (
                f"{FlextOracleWmsErrorMessages.ENTITY_VALIDATION_FAILED}: "
                "Entity endpoint must start with /"
            )
            raise FlextOracleWmsDataValidationError(msg)

        max_length = FlextOracleWmsDefaults.MAX_ENTITY_NAME_LENGTH
        if len(self.name) > max_length:
            msg = (
                f"{FlextOracleWmsErrorMessages.ENTITY_VALIDATION_FAILED}: "
                f"Entity name too long (max {max_length} characters)"
            )
            raise FlextOracleWmsDataValidationError(msg)


@dataclass(frozen=True)
class FlextOracleWmsDiscoveryResult:
    """Oracle WMS discovery result - USED BY DISCOVERY."""

    entities: list[FlextOracleWmsEntity] = field(default_factory=list)
    total_count: int = 0
    timestamp: str = ""
    api_version: str | None = None

    def validate_domain_rules(self) -> None:
        """Validate discovery result.

        Raises:
            FlextOracleWmsDataValidationError: If discovery result is invalid

        """
        if not isinstance(self.entities, list):
            msg = (
                f"{FlextOracleWmsErrorMessages.DISCOVERY_FAILED}: "
                "Entities must be a list"
            )
            raise FlextOracleWmsDataValidationError(msg)

        if self.total_count < 0:
            msg = (
                f"{FlextOracleWmsErrorMessages.DISCOVERY_FAILED}: "
                "Total count cannot be negative"
            )
            raise FlextOracleWmsDataValidationError(msg)

        if self.entities and len(self.entities) != self.total_count:
            msg = (
                f"{FlextOracleWmsErrorMessages.DISCOVERY_FAILED}: Entity count mismatch"
            )
            raise FlextOracleWmsDataValidationError(msg)

        # Validate all entities
        for entity in self.entities:
            if not isinstance(entity, FlextOracleWmsEntity):
                msg = (
                    f"{FlextOracleWmsErrorMessages.DISCOVERY_FAILED}: "
                    "Invalid entity type"
                )
                raise FlextOracleWmsDataValidationError(msg)
            entity.validate_domain_rules()


@dataclass(frozen=True)
class FlextOracleWmsApiResponse:
    """Oracle WMS API response wrapper - USED BY CLIENT."""

    data: dict[str, Any] = field(default_factory=dict)
    status_code: int = 200
    success: bool = True
    error_message: str | None = None

    def validate_domain_rules(self) -> None:
        """Validate API response.

        Raises:
            FlextOracleWmsDataValidationError: If API response is invalid

        """
        if not isinstance(self.data, dict):
            msg = (
                f"{FlextOracleWmsErrorMessages.INVALID_RESPONSE}: "
                "Data must be a dictionary"
            )
            raise FlextOracleWmsDataValidationError(msg)

        if not isinstance(self.status_code, int):
            msg = (
                f"{FlextOracleWmsErrorMessages.INVALID_RESPONSE}: "
                "Status code must be an integer"
            )
            raise FlextOracleWmsDataValidationError(msg)

        min_code = FlextOracleWmsDefaults.MIN_HTTP_STATUS_CODE
        max_code = FlextOracleWmsDefaults.MAX_HTTP_STATUS_CODE
        if self.status_code < min_code or self.status_code > max_code:
            msg = (
                f"{FlextOracleWmsErrorMessages.INVALID_RESPONSE}: "
                f"Invalid HTTP status code: {self.status_code}"
            )
            raise FlextOracleWmsDataValidationError(msg)

        if not self.success and not self.error_message:
            msg = (
                f"{FlextOracleWmsErrorMessages.INVALID_RESPONSE}: "
                "Failed response must have error message"
            )
            raise FlextOracleWmsDataValidationError(msg)
