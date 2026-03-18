"""Unit tests for FlextOracleWmsConstants class.

Tests the constants module against actual source structure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextConstants
from flext_tests import tm

from flext_oracle_wms.constants import FlextOracleWmsConstants

OracleWMSAuthMethod = FlextOracleWmsConstants.OracleWMSAuthMethod


class TestFlextOracleWmsConstants:
    """Test cases for FlextOracleWmsConstants class."""

    def test_class_inheritance(self) -> None:
        """Test that FlextOracleWmsConstants follows proper inheritance patterns."""
        tm.that(issubclass(FlextOracleWmsConstants, FlextConstants), eq=True)

    def test_application_constants(self) -> None:
        """Test application metadata via APP_METADATA dict."""
        meta = FlextOracleWmsConstants.APP_METADATA
        tm.that(meta["name"] == "flext-wms", eq=True)
        tm.that(meta["description"] == "FLEXT Generic WMS Integration", eq=True)
        tm.that(meta["author"] == "FLEXT Team", eq=True)
        tm.that(meta["license"] == "MIT", eq=True)

    def test_api_constants(self) -> None:
        """Test API-related constants via API_CONFIG dict."""
        api = FlextOracleWmsConstants.API_CONFIG
        tm.that(api["version_default"] == "v1", eq=True)
        tm.that(isinstance(api["base_url_default"], str), eq=True)
        tm.that(isinstance(api["timeout_default"], int), eq=True)
        tm.that(api["max_retries"] == 3, eq=True)

    def test_authentication_constants(self) -> None:
        """Test authentication constants via AUTH_CONFIG dict."""
        auth = FlextOracleWmsConstants.AUTH_CONFIG
        tm.that(auth["basic"] == OracleWMSAuthMethod.BASIC, eq=True)
        tm.that(auth["oauth2"] == OracleWMSAuthMethod.OAUTH2, eq=True)
        tm.that(auth["api_key"] == OracleWMSAuthMethod.API_KEY, eq=True)

    def test_entity_type_constants(self) -> None:
        """Test ENTITY_TYPES tuple derived from WmsEntityType enum."""
        entity_types = tuple(FlextOracleWmsConstants.WmsEntityType)
        tm.that(isinstance(entity_types, tuple), eq=True)
        tm.that("inventory" in entity_types, eq=True)
        tm.that("orders" in entity_types, eq=True)
        tm.that("shipments" in entity_types, eq=True)
        tm.that("picking" in entity_types, eq=True)
        tm.that("locations" in entity_types, eq=True)
        tm.that("items" in entity_types, eq=True)

    def test_batch_processing_constants(self) -> None:
        """Test batch processing constants via PROCESSING_CONFIG dict."""
        proc = FlextOracleWmsConstants.PROCESSING_CONFIG
        tm.that(proc["default_batch_size"] >= 1000, eq=True)
        tm.that(proc["max_batch_size"] >= 10000, eq=True)
        tm.that(proc["default_page_size"] == FlextConstants.Defaults.PAGE_SIZE, eq=True)

    def test_cache_constants(self) -> None:
        """Test caching constants via PROCESSING_CONFIG dict."""
        proc = FlextOracleWmsConstants.PROCESSING_CONFIG
        tm.that(proc["cache_ttl_default"] == 3600, eq=True)
        tm.that(proc["cache_max_size"] == 10000, eq=True)
        tm.that(proc["cache_cleanup_interval"] == 300, eq=True)

    def test_error_handling_constants(self) -> None:
        """Test error handling constants via PROCESSING_CONFIG dict."""
        proc = FlextOracleWmsConstants.PROCESSING_CONFIG
        tm.that(proc["max_retry_attempts"] == 3, eq=True)
        tm.that(proc["retry_delay_base"] == 1, eq=True)
        tm.that(proc["retry_delay_max"] == 60, eq=True)

    def test_performance_constants(self) -> None:
        """Test performance threshold constants via PROCESSING_CONFIG dict."""
        proc = FlextOracleWmsConstants.PROCESSING_CONFIG
        tm.that(proc["performance_warning_threshold"] == 5000, eq=True)
        tm.that(proc["performance_critical_threshold"] == 10000, eq=True)

    def test_environment_constants(self) -> None:
        """Test environment constants via ENVIRONMENTS dict."""
        envs = FlextOracleWmsConstants.ENVIRONMENTS
        tm.that(envs["default"] == "default", eq=True)
        tm.that(envs["test"] == "test", eq=True)
        tm.that(envs["production"] == "production", eq=True)

    def test_nested_oracle_wms_constants(self) -> None:
        """Test nested OracleWms class constants (connection-related)."""
        connection = FlextOracleWmsConstants.OracleWms
        tm.that(hasattr(connection, "DEFAULT_TIMEOUT"), eq=True)
        tm.that(hasattr(connection, "DEFAULT_MAX_RETRIES"), eq=True)
        tm.that(hasattr(connection, "DEFAULT_RETRY_DELAY"), eq=True)
        tm.that(hasattr(connection, "DEFAULT_POOL_SIZE"), eq=True)
        tm.that(hasattr(connection, "MAX_POOL_SIZE"), eq=True)

    def test_nested_wms_entities_constants(self) -> None:
        """Test nested WmsEntities class constants."""
        wms_entities = FlextOracleWmsConstants.WmsEntities
        tm.that(hasattr(wms_entities, "TYPES"), eq=True)
        tm.that(isinstance(wms_entities.TYPES, tuple), eq=True)
        tm.that(len(wms_entities.TYPES) > 0, eq=True)
        tm.that(hasattr(wms_entities, "MAX_ENTITY_NAME_LENGTH"), eq=True)
        tm.that(hasattr(wms_entities, "ENTITY_NAME_PATTERN"), eq=True)

    def test_nested_processing_constants(self) -> None:
        """Test nested WmsProcessing class constants."""
        processing = FlextOracleWmsConstants.WmsProcessing
        tm.that(hasattr(processing, "DEFAULT_BATCH_SIZE"), eq=True)
        tm.that(hasattr(processing, "MAX_BATCH_SIZE"), eq=True)
        tm.that(hasattr(processing, "DEFAULT_PAGE_SIZE"), eq=True)
        tm.that(hasattr(processing, "MAX_SCHEMA_DEPTH"), eq=True)

    def test_nested_filtering_constants(self) -> None:
        """Test nested Filtering class constants."""
        filtering = FlextOracleWmsConstants.Filtering
        tm.that(hasattr(filtering, "MAX_FILTER_CONDITIONS"), eq=True)

    def test_nested_error_messages_constants(self) -> None:
        """Test nested ErrorMessages class via MESSAGES dict."""
        error_messages = FlextOracleWmsConstants.ErrorMessages
        tm.that(hasattr(error_messages, "MESSAGES"), eq=True)
        msgs = error_messages.MESSAGES
        tm.that("entity_validation_failed" in msgs, eq=True)
        tm.that("discovery_failed" in msgs, eq=True)
        tm.that("invalid_response" in msgs, eq=True)

    def test_nested_authentication_constants(self) -> None:
        """Test nested Authentication class constants."""
        auth = FlextOracleWmsConstants.Authentication
        tm.that(hasattr(auth, "MIN_TOKEN_LENGTH"), eq=True)
        tm.that(hasattr(auth, "MIN_API_KEY_LENGTH"), eq=True)

    def test_nested_api_constants(self) -> None:
        """Test nested Api class via CONFIG dict."""
        api = FlextOracleWmsConstants.Api
        tm.that(hasattr(api, "CONFIG"), eq=True)
        config = api.CONFIG
        tm.that("default_timeout" in config, eq=True)
        tm.that("min_http_status_code" in config, eq=True)
        tm.that("max_http_status_code" in config, eq=True)

    def test_entity_type_enum(self) -> None:
        """Test WmsEntityType enum."""
        entity_type = FlextOracleWmsConstants.WmsEntityType
        tm.that(entity_type.INVENTORY == "inventory", eq=True)
        tm.that(entity_type.ORDERS == "orders", eq=True)
        tm.that(entity_type.SHIPMENTS == "shipments", eq=True)
        tm.that(entity_type.PICKING == "picking", eq=True)
        tm.that(entity_type.LOCATIONS == "locations", eq=True)
        tm.that(entity_type.ITEMS == "items", eq=True)

    def test_api_version_enum(self) -> None:
        """Test WmsApiVersion enum."""
        api_version = FlextOracleWmsConstants.WmsApiVersion
        tm.that(api_version.V1 == "v1", eq=True)
        tm.that(api_version.V2 == "v2", eq=True)
        tm.that(api_version.V3 == "v3", eq=True)
        tm.that(api_version.LEGACY == "legacy", eq=True)

    def test_operation_status_enum(self) -> None:
        """Test WmsOperationStatus enum."""
        status = FlextOracleWmsConstants.WmsOperationStatus
        tm.that(status.PENDING == "pending", eq=True)
        tm.that(status.RUNNING == "running", eq=True)
        tm.that(status.SUCCESS == "success", eq=True)
        tm.that(status.ERROR == "error", eq=True)
        tm.that(status.TIMEOUT == "timeout", eq=True)
        tm.that(status.CANCELLED == "cancelled", eq=True)

    def test_data_quality_enum(self) -> None:
        """Test WmsDataQuality enum."""
        quality = FlextOracleWmsConstants.WmsDataQuality
        tm.that(quality.HIGH == "high", eq=True)
        tm.that(quality.MEDIUM == "medium", eq=True)
        tm.that(quality.LOW == "low", eq=True)
        tm.that(quality.UNKNOWN == "unknown", eq=True)

    def test_filter_operator_enum(self) -> None:
        """Test WmsFilterOperator enum."""
        operator = FlextOracleWmsConstants.WmsFilterOperator
        tm.that(operator.EQ == "eq", eq=True)
        tm.that(operator.NE == "ne", eq=True)
        tm.that(operator.GT == "gt", eq=True)
        tm.that(operator.GTE == "gte", eq=True)
        tm.that(operator.LT == "lt", eq=True)
        tm.that(operator.LTE == "lte", eq=True)
        tm.that(operator.IN == "in", eq=True)
        tm.that(operator.NOT_IN == "not_in", eq=True)
        tm.that(operator.CONTAINS == "contains", eq=True)

    def test_page_mode_enum(self) -> None:
        """Test WmsPageMode enum."""
        mode = FlextOracleWmsConstants.WmsPageMode
        tm.that(mode.APPEND == "append", eq=True)
        tm.that(mode.REPLACE == "replace", eq=True)
        tm.that(mode.MERGE == "merge", eq=True)

    def test_write_mode_enum(self) -> None:
        """Test WmsWriteMode enum."""
        mode = FlextOracleWmsConstants.WmsWriteMode
        tm.that(mode.INSERT == "insert", eq=True)
        tm.that(mode.UPDATE == "update", eq=True)
        tm.that(mode.UPSERT == "upsert", eq=True)
        tm.that(mode.DELETE == "delete", eq=True)

    def test_module_level_auth_method_enum(self) -> None:
        """Test module-level OracleWMSAuthMethod enum."""
        tm.that(OracleWMSAuthMethod.BASIC == "basic", eq=True)
        tm.that(OracleWMSAuthMethod.OAUTH2 == "oauth2", eq=True)
        tm.that(OracleWMSAuthMethod.API_KEY == "api_key", eq=True)
        tm.that(OracleWMSAuthMethod.BEARER == "bearer", eq=True)

    def test_endpoint_discovery_strategy_enum(self) -> None:
        """Test EndpointDiscoveryStrategy enum."""
        strategy = FlextOracleWmsConstants.EndpointDiscoveryStrategy
        tm.that(strategy.API_BASED == "api_based", eq=True)
        tm.that(strategy.SCHEMA_BASED == "schema_based", eq=True)

    def test_flext_wms_version(self) -> None:
        """Test FLEXT_WMS_VERSION constant."""
        tm.that(isinstance(FlextOracleWmsConstants.FLEXT_WMS_VERSION, str), eq=True)
        tm.that(FlextOracleWmsConstants.FLEXT_WMS_VERSION == "0.9.0", eq=True)

    def test_wms_pagination_constants(self) -> None:
        """Test WmsPagination class constants."""
        pagination = FlextOracleWmsConstants.WmsPagination
        tm.that(pagination.DEFAULT_PAGE_SIZE == 100, eq=True)


__all__ = ["TestFlextOracleWmsConstants"]
