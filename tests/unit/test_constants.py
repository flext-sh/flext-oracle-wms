"""Unit tests for FlextOracleWmsConstants class.

Tests the constants module against actual source structure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextConstants

from flext_oracle_wms.constants import FlextOracleWmsConstants, OracleWMSAuthMethod


class TestFlextOracleWmsConstants:
    """Test cases for FlextOracleWmsConstants class."""

    def test_class_inheritance(self) -> None:
        """Test that FlextOracleWmsConstants follows proper inheritance patterns."""
        assert issubclass(FlextOracleWmsConstants, FlextConstants)

    def test_application_constants(self) -> None:
        """Test application metadata via APP_METADATA dict."""
        meta = FlextOracleWmsConstants.APP_METADATA
        assert meta["name"] == "flext-wms"
        assert meta["description"] == "FLEXT Generic WMS Integration"
        assert meta["author"] == "FLEXT Team"
        assert meta["license"] == "MIT"

    def test_api_constants(self) -> None:
        """Test API-related constants via API_CONFIG dict."""
        api = FlextOracleWmsConstants.API_CONFIG
        assert api["version_default"] == "v1"
        assert isinstance(api["base_url_default"], str)
        assert isinstance(api["timeout_default"], int)
        assert api["max_retries"] == 3

    def test_authentication_constants(self) -> None:
        """Test authentication constants via AUTH_CONFIG dict."""
        auth = FlextOracleWmsConstants.AUTH_CONFIG
        assert auth["basic"] == OracleWMSAuthMethod.BASIC
        assert auth["oauth2"] == OracleWMSAuthMethod.OAUTH2
        assert auth["api_key"] == OracleWMSAuthMethod.API_KEY

    def test_entity_type_constants(self) -> None:
        """Test ENTITY_TYPES tuple derived from WmsEntityType enum."""
        entity_types = FlextOracleWmsConstants.ENTITY_TYPES
        assert isinstance(entity_types, tuple)
        assert "inventory" in entity_types
        assert "orders" in entity_types
        assert "shipments" in entity_types
        assert "picking" in entity_types
        assert "locations" in entity_types
        assert "items" in entity_types

    def test_batch_processing_constants(self) -> None:
        """Test batch processing constants via PROCESSING_CONFIG dict."""
        proc = FlextOracleWmsConstants.PROCESSING_CONFIG
        assert proc["default_batch_size"] >= 1000
        assert proc["max_batch_size"] >= 10000
        assert proc["default_page_size"] == FlextConstants.Defaults.PAGE_SIZE

    def test_cache_constants(self) -> None:
        """Test caching constants via PROCESSING_CONFIG dict."""
        proc = FlextOracleWmsConstants.PROCESSING_CONFIG
        assert proc["cache_ttl_default"] == 3600
        assert proc["cache_max_size"] == 10000
        assert proc["cache_cleanup_interval"] == 300

    def test_error_handling_constants(self) -> None:
        """Test error handling constants via PROCESSING_CONFIG dict."""
        proc = FlextOracleWmsConstants.PROCESSING_CONFIG
        assert proc["max_retry_attempts"] == 3
        assert proc["retry_delay_base"] == 1
        assert proc["retry_delay_max"] == 60

    def test_performance_constants(self) -> None:
        """Test performance threshold constants via PROCESSING_CONFIG dict."""
        proc = FlextOracleWmsConstants.PROCESSING_CONFIG
        assert proc["performance_warning_threshold"] == 5000
        assert proc["performance_critical_threshold"] == 10000

    def test_environment_constants(self) -> None:
        """Test environment constants via ENVIRONMENTS dict."""
        envs = FlextOracleWmsConstants.ENVIRONMENTS
        assert envs["default"] == "default"
        assert envs["test"] == "test"
        assert envs["production"] == "production"

    def test_nested_oracle_wms_constants(self) -> None:
        """Test nested OracleWms class constants (connection-related)."""
        connection = FlextOracleWmsConstants.OracleWms

        assert hasattr(connection, "DEFAULT_TIMEOUT")
        assert hasattr(connection, "DEFAULT_MAX_RETRIES")
        assert hasattr(connection, "DEFAULT_RETRY_DELAY")
        assert hasattr(connection, "DEFAULT_POOL_SIZE")
        assert hasattr(connection, "MAX_POOL_SIZE")

    def test_nested_wms_entities_constants(self) -> None:
        """Test nested WmsEntities class constants."""
        wms_entities = FlextOracleWmsConstants.WmsEntities

        assert hasattr(wms_entities, "TYPES")
        assert isinstance(wms_entities.TYPES, tuple)
        assert len(wms_entities.TYPES) > 0
        assert hasattr(wms_entities, "MAX_ENTITY_NAME_LENGTH")
        assert hasattr(wms_entities, "ENTITY_NAME_PATTERN")

    def test_nested_processing_constants(self) -> None:
        """Test nested WmsProcessing class constants."""
        processing = FlextOracleWmsConstants.WmsProcessing

        assert hasattr(processing, "DEFAULT_BATCH_SIZE")
        assert hasattr(processing, "MAX_BATCH_SIZE")
        assert hasattr(processing, "DEFAULT_PAGE_SIZE")
        assert hasattr(processing, "MAX_SCHEMA_DEPTH")

    def test_nested_filtering_constants(self) -> None:
        """Test nested Filtering class constants."""
        filtering = FlextOracleWmsConstants.Filtering

        assert hasattr(filtering, "MAX_FILTER_CONDITIONS")

    def test_nested_error_messages_constants(self) -> None:
        """Test nested ErrorMessages class via MESSAGES dict."""
        error_messages = FlextOracleWmsConstants.ErrorMessages

        assert hasattr(error_messages, "MESSAGES")
        msgs = error_messages.MESSAGES
        assert "entity_validation_failed" in msgs
        assert "discovery_failed" in msgs
        assert "invalid_response" in msgs

    def test_nested_authentication_constants(self) -> None:
        """Test nested Authentication class constants."""
        auth = FlextOracleWmsConstants.Authentication

        assert hasattr(auth, "MIN_TOKEN_LENGTH")
        assert hasattr(auth, "MIN_API_KEY_LENGTH")

    def test_nested_api_constants(self) -> None:
        """Test nested Api class via CONFIG dict."""
        api = FlextOracleWmsConstants.Api

        assert hasattr(api, "CONFIG")
        config = api.CONFIG
        assert "default_timeout" in config
        assert "min_http_status_code" in config
        assert "max_http_status_code" in config

    def test_entity_type_enum(self) -> None:
        """Test WmsEntityType enum."""
        entity_type = FlextOracleWmsConstants.WmsEntityType

        assert entity_type.INVENTORY == "inventory"
        assert entity_type.ORDERS == "orders"
        assert entity_type.SHIPMENTS == "shipments"
        assert entity_type.PICKING == "picking"
        assert entity_type.LOCATIONS == "locations"
        assert entity_type.ITEMS == "items"

    def test_api_version_enum(self) -> None:
        """Test WmsApiVersion enum."""
        api_version = FlextOracleWmsConstants.WmsApiVersion

        assert api_version.V1 == "v1"
        assert api_version.V2 == "v2"
        assert api_version.V3 == "v3"
        assert api_version.LEGACY == "legacy"

    def test_operation_status_enum(self) -> None:
        """Test WmsOperationStatus enum."""
        status = FlextOracleWmsConstants.WmsOperationStatus

        assert status.PENDING == "pending"
        assert status.RUNNING == "running"
        assert status.SUCCESS == "success"
        assert status.ERROR == "error"
        assert status.TIMEOUT == "timeout"
        assert status.CANCELLED == "cancelled"

    def test_data_quality_enum(self) -> None:
        """Test WmsDataQuality enum."""
        quality = FlextOracleWmsConstants.WmsDataQuality

        assert quality.HIGH == "high"
        assert quality.MEDIUM == "medium"
        assert quality.LOW == "low"
        assert quality.UNKNOWN == "unknown"

    def test_filter_operator_enum(self) -> None:
        """Test WmsFilterOperator enum."""
        operator = FlextOracleWmsConstants.WmsFilterOperator

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
        """Test WmsPageMode enum."""
        mode = FlextOracleWmsConstants.WmsPageMode

        assert mode.APPEND == "append"
        assert mode.REPLACE == "replace"
        assert mode.MERGE == "merge"

    def test_write_mode_enum(self) -> None:
        """Test WmsWriteMode enum."""
        mode = FlextOracleWmsConstants.WmsWriteMode

        assert mode.INSERT == "insert"
        assert mode.UPDATE == "update"
        assert mode.UPSERT == "upsert"
        assert mode.DELETE == "delete"

    def test_module_level_auth_method_enum(self) -> None:
        """Test module-level OracleWMSAuthMethod enum."""
        assert OracleWMSAuthMethod.BASIC == "basic"
        assert OracleWMSAuthMethod.OAUTH2 == "oauth2"
        assert OracleWMSAuthMethod.API_KEY == "api_key"
        assert OracleWMSAuthMethod.BEARER == "bearer"

    def test_endpoint_discovery_strategy_enum(self) -> None:
        """Test EndpointDiscoveryStrategy enum."""
        strategy = FlextOracleWmsConstants.EndpointDiscoveryStrategy

        assert strategy.API_BASED == "api_based"
        assert strategy.SCHEMA_BASED == "schema_based"

    def test_flext_wms_version(self) -> None:
        """Test FLEXT_WMS_VERSION constant."""
        assert isinstance(FlextOracleWmsConstants.FLEXT_WMS_VERSION, str)
        assert FlextOracleWmsConstants.FLEXT_WMS_VERSION == "0.9.0"

    def test_wms_pagination_constants(self) -> None:
        """Test WmsPagination class constants."""
        pagination = FlextOracleWmsConstants.WmsPagination

        assert pagination.DEFAULT_PAGE_SIZE == 100


__all__ = ["TestFlextOracleWmsConstants"]
