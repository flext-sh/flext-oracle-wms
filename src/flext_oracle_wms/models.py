"""Essential Oracle WMS Models - Only what's actually used.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Minimal models using flext-core standards.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from flext_oracle_wms.constants import (
    FlextOracleWmsDefaults,
    FlextOracleWmsErrorMessages,
)
from flext_oracle_wms.exceptions import (
    FlextOracleWmsDataValidationError,
)
from flext_oracle_wms.helpers import (
    validate_dict_parameter,
    validate_records_list,
    validate_string_parameter,
)


@dataclass(frozen=True)
class FlextOracleWmsEntity:
    """Oracle WMS entity model - USED BY DISCOVERY."""

    name: str
    endpoint: str
    description: str | None = None
    fields: dict[str, object] | None = field(default_factory=dict)
    primary_key: str | None = None
    replication_key: str | None = None
    supports_incremental: bool = False

    def validate_business_rules(self) -> None:
        """Validate entity business rules.

        Raises:
            FlextOracleWmsDataValidationError: If entity data is invalid

        """
        # Use DRY validation functions from helpers.py
        try:
            validate_string_parameter(self.name, "entity name")
            validate_string_parameter(self.endpoint, "entity endpoint")
        except FlextOracleWmsDataValidationError as e:
            # Re-raise with entity-specific context
            msg: str = f"{FlextOracleWmsErrorMessages.ENTITY_VALIDATION_FAILED}: {e}"
            raise FlextOracleWmsDataValidationError(msg) from e

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
    discovery_duration_ms: float = 0.0
    has_errors: bool = False
    errors: list[str] = field(default_factory=list)
    api_version: str | None = None

    def validate_business_rules(self) -> None:
        """Validate discovery result.

        Raises:
            FlextOracleWmsDataValidationError: If discovery result is invalid

        """
        # Use DRY validation functions from helpers.py
        try:
            validate_records_list(self.entities, "entities")
        except FlextOracleWmsDataValidationError as e:
            # Re-raise with discovery-specific context
            msg: str = f"{FlextOracleWmsErrorMessages.DISCOVERY_FAILED}: {e}"
            raise FlextOracleWmsDataValidationError(msg) from e

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
            entity.validate_business_rules()


@dataclass(frozen=True)
class FlextOracleWmsApiResponse:
    """Oracle WMS API response wrapper - USED BY CLIENT."""

    data: dict[str, object] = field(default_factory=dict)
    status_code: int = 200
    success: bool = True
    error_message: str | None = None

    def validate_business_rules(self) -> None:
        """Validate API response.

        Raises:
            FlextOracleWmsDataValidationError: If API response is invalid

        """
        # Use DRY validation functions from helpers.py
        try:
            validate_dict_parameter(self.data, "data")
        except FlextOracleWmsDataValidationError as e:
            # Re-raise with API response specific context
            msg: str = f"{FlextOracleWmsErrorMessages.INVALID_RESPONSE}: {e}"
            raise FlextOracleWmsDataValidationError(msg) from e

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
