"""Unit tests for FlextOracleWmsConstants class.

Tests the constants module following FLEXT standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextConstants

from flext_oracle_wms.constants import FlextOracleWmsConstants


class TestFlextOracleWmsConstants:
    """Test cases for FlextOracleWmsConstants class."""

    def test_class_inheritance(self) -> None:
        """Test that FlextOracleWmsConstants follows proper inheritance patterns."""
        # FlextOracleWmsConstants should inherit from FlextConstants
        assert issubclass(FlextOracleWmsConstants, FlextConstants)

    def test_application_constants(self) -> None:
        """Test application metadata constants."""
        assert FlextOracleWmsConstants.APPLICATION_NAME == "flext-oracle-wms"
        assert (
            FlextOracleWmsConstants.APPLICATION_DESCRIPTION
            == "FLEXT Oracle WMS Cloud Integration"
        )
        assert FlextOracleWmsConstants.APPLICATION_AUTHOR == "FLEXT Team"
        assert FlextOracleWmsConstants.APPLICATION_LICENSE == "MIT"

    def test_api_constants(self) -> None:
        """Test API-related constants."""
        assert FlextOracleWmsConstants.API_VERSION_DEFAULT == "v2"
        assert (
            FlextOracleWmsConstants.API_BASE_URL_DEFAULT
            == "https://wms.oraclecloud.com"
        )
        assert FlextOracleWmsConstants.API_TIMEOUT_DEFAULT >= 30  # At least 30 seconds
        assert FlextOracleWmsConstants.API_MAX_RETRIES == 3

    def test_authentication_constants(self) -> None:
        """Test authentication constants."""
        assert FlextOracleWmsConstants.AUTH_METHOD_BASIC == "basic"
        assert FlextOracleWmsConstants.AUTH_METHOD_OAUTH2 == "oauth2"
        assert FlextOracleWmsConstants.AUTH_METHOD_API_KEY == "api_key"
        assert FlextOracleWmsConstants.OAUTH2_SCOPE_DEFAULT == "wms.read wms.write"

    def test_entity_type_constants(self) -> None:
        """Test entity type constants."""
        assert FlextOracleWmsConstants.ENTITY_TYPE_INVENTORY == "inventory"
        assert FlextOracleWmsConstants.ENTITY_TYPE_ORDER == "order"
        assert FlextOracleWmsConstants.ENTITY_TYPE_SHIPMENT == "shipment"
        assert FlextOracleWmsConstants.ENTITY_TYPE_PICKING == "picking"
        assert FlextOracleWmsConstants.ENTITY_TYPE_LOCATION == "location"
        assert FlextOracleWmsConstants.ENTITY_TYPE_ITEM == "item"

    def test_batch_processing_constants(self) -> None:
        """Test batch processing constants."""
        assert FlextOracleWmsConstants.DEFAULT_BATCH_SIZE >= 1000
        assert FlextOracleWmsConstants.MAX_BATCH_SIZE >= 10000
        assert FlextOracleWmsConstants.DEFAULT_PAGE_SIZE == 100

    def test_cache_constants(self) -> None:
        """Test caching constants."""
        assert FlextOracleWmsConstants.CACHE_TTL_DEFAULT == 3600  # 1 hour
        assert FlextOracleWmsConstants.CACHE_MAX_SIZE == 10000
        assert FlextOracleWmsConstants.CACHE_CLEANUP_INTERVAL == 300  # 5 minutes

    def test_error_handling_constants(self) -> None:
        """Test error handling constants."""
        assert FlextOracleWmsConstants.MAX_RETRY_ATTEMPTS == 3
        assert FlextOracleWmsConstants.RETRY_DELAY_BASE == 1
        assert FlextOracleWmsConstants.RETRY_DELAY_MAX == 60

    def test_performance_constants(self) -> None:
        """Test performance threshold constants."""
        assert FlextOracleWmsConstants.PERFORMANCE_WARNING_THRESHOLD == 5000
        assert FlextOracleWmsConstants.PERFORMANCE_CRITICAL_THRESHOLD == 10000

    def test_environment_constants(self) -> None:
        """Test environment constants."""
        assert FlextOracleWmsConstants.DEFAULT_ENVIRONMENT == "default"
        assert FlextOracleWmsConstants.TEST_ENVIRONMENT == "test"
        assert FlextOracleWmsConstants.ENVIRONMENT == "production"

    def test_nested_connection_constants(self) -> None:
        """Test nested Connection class constants."""
        connection = FlextOracleWmsConstants.Connection

        assert hasattr(connection, "DEFAULT_TIMEOUT")
        assert hasattr(connection, "DEFAULT_MAX_RETRIES")
        assert hasattr(connection, "DEFAULT_RETRY_DELAY")
        assert hasattr(connection, "DEFAULT_POOL_SIZE")
        assert hasattr(connection, "MAX_POOL_SIZE")

    def test_nested_wms_entities_constants(self) -> None:
        """Test nested WmsEntities class constants."""
        wms_entities = FlextOracleWmsConstants.WmsEntities

        assert hasattr(wms_entities, "TYPES")
        assert isinstance(wms_entities.TYPES, list)
        assert len(wms_entities.TYPES) > 0
        assert hasattr(wms_entities, "MAX_ENTITY_NAME_LENGTH")
        assert hasattr(wms_entities, "ENTITY_NAME_PATTERN")

    def test_nested_processing_constants(self) -> None:
        """Test nested Processing class constants."""
        processing = FlextOracleWmsConstants.Processing

        assert hasattr(processing, "DEFAULT_BATCH_SIZE")
        assert hasattr(processing, "MAX_BATCH_SIZE")
        assert hasattr(processing, "DEFAULT_PAGE_SIZE")
        assert hasattr(processing, "MAX_SCHEMA_DEPTH")

    def test_nested_filtering_constants(self) -> None:
        """Test nested Filtering class constants."""
        filtering = FlextOracleWmsConstants.Filtering

        assert hasattr(filtering, "MAX_FILTER_CONDITIONS")

    def test_nested_error_messages_constants(self) -> None:
        """Test nested ErrorMessages class constants."""
        error_messages = FlextOracleWmsConstants.ErrorMessages

        assert hasattr(error_messages, "ENTITY_VALIDATION_FAILED")
        assert hasattr(error_messages, "DISCOVERY_FAILED")
        assert hasattr(error_messages, "INVALID_RESPONSE")

    def test_nested_authentication_constants(self) -> None:
        """Test nested Authentication class constants."""
        auth = FlextOracleWmsConstants.Authentication

        assert hasattr(auth, "MIN_TOKEN_LENGTH")
        assert hasattr(auth, "MIN_API_KEY_LENGTH")

    def test_nested_api_constants(self) -> None:
        """Test nested Api class constants."""
        api = FlextOracleWmsConstants.Api

        assert hasattr(api, "DEFAULT_TIMEOUT")
        assert hasattr(api, "MIN_HTTP_STATUS_CODE")
        assert hasattr(api, "MAX_HTTP_STATUS_CODE")

    def test_entity_type_enum(self) -> None:
        """Test OracleWMSEntityType enum."""
        entity_type = FlextOracleWmsConstants.OracleWMSEntityType

        assert entity_type.INVENTORY == "inventory"
        assert entity_type.ORDER == "order"
        assert entity_type.SHIPMENT == "shipment"
        assert entity_type.PICKING == "picking"
        assert entity_type.LOCATION == "location"
        assert entity_type.ITEM == "item"

    def test_api_version_enum(self) -> None:
        """Test OracleWMSApiVersion enum."""
        api_version = FlextOracleWmsConstants.OracleWMSApiVersion

        assert api_version.V1 == "v1"
        assert api_version.V2 == "v2"
        assert api_version.LGF_V10 == "v10"
        assert api_version.LEGACY == "legacy"

    def test_operation_status_enum(self) -> None:
        """Test OracleWMSOperationStatus enum."""
        status = FlextOracleWmsConstants.OracleWMSOperationStatus

        assert status.PENDING == "pending"
        assert status.RUNNING == "running"
        assert status.SUCCESS == "success"
        assert status.ERROR == "error"
        assert status.TIMEOUT == "timeout"
        assert status.CANCELLED == "cancelled"

    def test_data_quality_enum(self) -> None:
        """Test OracleWMSDataQuality enum."""
        quality = FlextOracleWmsConstants.OracleWMSDataQuality

        assert quality.HIGH == "high"
        assert quality.MEDIUM == "medium"
        assert quality.LOW == "low"
        assert quality.UNKNOWN == "unknown"

    def test_filter_operator_enum(self) -> None:
        """Test OracleWMSFilterOperator enum."""
        operator = FlextOracleWmsConstants.OracleWMSFilterOperator

        assert operator.EQ == "eq"
        assert operator.NE == "ne"
        assert operator.GT == "gt"
        assert operator.GTE == "gte"
        assert operator.LT == "lt"
        assert operator.LTE == "lte"
        assert operator.IN == "in"
        assert operator.NOT_IN == "not_in"
        assert operator.CONTAINS == "contains"

    def test_page_mode_enum(self) -> None:
        """Test OracleWMSPageMode enum."""
        mode = FlextOracleWmsConstants.OracleWMSPageMode

        assert mode.APPEND == "append"
        assert mode.REPLACE == "replace"
        assert mode.MERGE == "merge"

    def test_write_mode_enum(self) -> None:
        """Test OracleWMSWriteMode enum."""
        mode = FlextOracleWmsConstants.OracleWMSWriteMode

        assert mode.INSERT == "insert"
        assert mode.UPDATE == "update"
        assert mode.UPSERT == "upsert"
        assert mode.DELETE == "delete"

    def test_module_level_auth_method_enum(self) -> None:
        """Test module-level OracleWMSAuthMethod enum."""
        from flext_oracle_wms.constants import OracleWMSAuthMethod

        assert OracleWMSAuthMethod.BASIC == "basic"
        assert OracleWMSAuthMethod.OAUTH2 == "oauth2"
        assert OracleWMSAuthMethod.API_KEY == "api_key"


__all__ = ["TestFlextOracleWmsConstants"]
