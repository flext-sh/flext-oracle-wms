"""Unit tests for FlextOracleWmsConstants class.

Tests the constants module against actual source structure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextConstants
from flext_tests import u

from flext_oracle_wms.constants import FlextOracleWmsConstants

OracleWMSAuthMethod = FlextOracleWmsConstants.OracleWMSAuthMethod


class TestFlextOracleWmsConstants:
    """Test cases for FlextOracleWmsConstants class."""

    def test_class_inheritance(self) -> None:
        """Test that FlextOracleWmsConstants follows proper inheritance patterns."""
        u.Tests.Matchers.that(
            issubclass(FlextOracleWmsConstants, FlextConstants), eq=True
        )

    def test_application_constants(self) -> None:
        """Test application metadata via APP_METADATA dict."""
        meta = FlextOracleWmsConstants.APP_METADATA
        u.Tests.Matchers.that(meta["name"] == "flext-wms", eq=True)
        u.Tests.Matchers.that(
            meta["description"] == "FLEXT Generic WMS Integration", eq=True
        )
        u.Tests.Matchers.that(meta["author"] == "FLEXT Team", eq=True)
        u.Tests.Matchers.that(meta["license"] == "MIT", eq=True)

    def test_api_constants(self) -> None:
        """Test API-related constants via API_CONFIG dict."""
        api = FlextOracleWmsConstants.API_CONFIG
        u.Tests.Matchers.that(api["version_default"] == "v1", eq=True)
        u.Tests.Matchers.that(isinstance(api["base_url_default"], str), eq=True)
        u.Tests.Matchers.that(isinstance(api["timeout_default"], int), eq=True)
        u.Tests.Matchers.that(api["max_retries"] == 3, eq=True)

    def test_authentication_constants(self) -> None:
        """Test authentication constants via AUTH_CONFIG dict."""
        auth = FlextOracleWmsConstants.AUTH_CONFIG
        u.Tests.Matchers.that(auth["basic"] == OracleWMSAuthMethod.BASIC, eq=True)
        u.Tests.Matchers.that(auth["oauth2"] == OracleWMSAuthMethod.OAUTH2, eq=True)
        u.Tests.Matchers.that(auth["api_key"] == OracleWMSAuthMethod.API_KEY, eq=True)

    def test_entity_type_constants(self) -> None:
        """Test ENTITY_TYPES tuple derived from WmsEntityType enum."""
        entity_types = tuple(FlextOracleWmsConstants.WmsEntityType)
        u.Tests.Matchers.that(isinstance(entity_types, tuple), eq=True)
        u.Tests.Matchers.that("inventory" in entity_types, eq=True)
        u.Tests.Matchers.that("orders" in entity_types, eq=True)
        u.Tests.Matchers.that("shipments" in entity_types, eq=True)
        u.Tests.Matchers.that("picking" in entity_types, eq=True)
        u.Tests.Matchers.that("locations" in entity_types, eq=True)
        u.Tests.Matchers.that("items" in entity_types, eq=True)

    def test_batch_processing_constants(self) -> None:
        """Test batch processing constants via PROCESSING_CONFIG dict."""
        proc = FlextOracleWmsConstants.PROCESSING_CONFIG
        u.Tests.Matchers.that(proc["default_batch_size"] >= 1000, eq=True)
        u.Tests.Matchers.that(proc["max_batch_size"] >= 10000, eq=True)
        u.Tests.Matchers.that(
            proc["default_page_size"] == FlextConstants.PAGE_SIZE, eq=True
        )

    def test_cache_constants(self) -> None:
        """Test caching constants via PROCESSING_CONFIG dict."""
        proc = FlextOracleWmsConstants.PROCESSING_CONFIG
        u.Tests.Matchers.that(proc["cache_ttl_default"] == 3600, eq=True)
        u.Tests.Matchers.that(proc["cache_max_size"] == 10000, eq=True)
        u.Tests.Matchers.that(proc["cache_cleanup_interval"] == 300, eq=True)

    def test_error_handling_constants(self) -> None:
        """Test error handling constants via PROCESSING_CONFIG dict."""
        proc = FlextOracleWmsConstants.PROCESSING_CONFIG
        u.Tests.Matchers.that(proc["max_retry_attempts"] == 3, eq=True)
        u.Tests.Matchers.that(proc["retry_delay_base"] == 1, eq=True)
        u.Tests.Matchers.that(proc["retry_delay_max"] == 60, eq=True)

    def test_performance_constants(self) -> None:
        """Test performance threshold constants via PROCESSING_CONFIG dict."""
        proc = FlextOracleWmsConstants.PROCESSING_CONFIG
        u.Tests.Matchers.that(proc["performance_warning_threshold"] == 5000, eq=True)
        u.Tests.Matchers.that(proc["performance_critical_threshold"] == 10000, eq=True)

    def test_environment_constants(self) -> None:
        """Test environment constants via ENVIRONMENTS dict."""
        envs = FlextOracleWmsConstants.ENVIRONMENTS
        u.Tests.Matchers.that(envs["default"] == "default", eq=True)
        u.Tests.Matchers.that(envs["test"] == "test", eq=True)
        u.Tests.Matchers.that(envs["production"] == "production", eq=True)

    def test_nested_oracle_wms_constants(self) -> None:
        """Test nested OracleWms class constants (connection-related)."""
        connection = FlextOracleWmsConstants.OracleWms
        u.Tests.Matchers.that(hasattr(connection, "DEFAULT_TIMEOUT"), eq=True)
        u.Tests.Matchers.that(hasattr(connection, "DEFAULT_MAX_RETRIES"), eq=True)
        u.Tests.Matchers.that(hasattr(connection, "DEFAULT_RETRY_DELAY"), eq=True)
        u.Tests.Matchers.that(hasattr(connection, "DEFAULT_POOL_SIZE"), eq=True)
        u.Tests.Matchers.that(hasattr(connection, "MAX_POOL_SIZE"), eq=True)

    def test_nested_wms_entities_constants(self) -> None:
        """Test nested WmsEntities class constants."""
        wms_entities = FlextOracleWmsConstants.WmsEntities
        u.Tests.Matchers.that(hasattr(wms_entities, "TYPES"), eq=True)
        u.Tests.Matchers.that(isinstance(wms_entities.TYPES, tuple), eq=True)
        u.Tests.Matchers.that(len(wms_entities.TYPES) > 0, eq=True)
        u.Tests.Matchers.that(hasattr(wms_entities, "MAX_ENTITY_NAME_LENGTH"), eq=True)
        u.Tests.Matchers.that(hasattr(wms_entities, "ENTITY_NAME_PATTERN"), eq=True)

    def test_nested_processing_constants(self) -> None:
        """Test nested WmsProcessing class constants."""
        processing = FlextOracleWmsConstants.WmsProcessing
        u.Tests.Matchers.that(hasattr(processing, "DEFAULT_BATCH_SIZE"), eq=True)
        u.Tests.Matchers.that(hasattr(processing, "MAX_BATCH_SIZE"), eq=True)
        u.Tests.Matchers.that(hasattr(processing, "DEFAULT_PAGE_SIZE"), eq=True)
        u.Tests.Matchers.that(hasattr(processing, "MAX_SCHEMA_DEPTH"), eq=True)

    def test_nested_filtering_constants(self) -> None:
        """Test nested Filtering class constants."""
        filtering = FlextOracleWmsConstants.Filtering
        u.Tests.Matchers.that(hasattr(filtering, "MAX_FILTER_CONDITIONS"), eq=True)

    def test_nested_error_messages_constants(self) -> None:
        """Test nested ErrorMessages class via MESSAGES dict."""
        error_messages = FlextOracleWmsConstants.ErrorMessages
        u.Tests.Matchers.that(hasattr(error_messages, "MESSAGES"), eq=True)
        msgs = error_messages.MESSAGES
        u.Tests.Matchers.that("entity_validation_failed" in msgs, eq=True)
        u.Tests.Matchers.that("discovery_failed" in msgs, eq=True)
        u.Tests.Matchers.that("invalid_response" in msgs, eq=True)

    def test_nested_authentication_constants(self) -> None:
        """Test nested Authentication class constants."""
        auth = FlextOracleWmsConstants.Authentication
        u.Tests.Matchers.that(hasattr(auth, "MIN_TOKEN_LENGTH"), eq=True)
        u.Tests.Matchers.that(hasattr(auth, "MIN_API_KEY_LENGTH"), eq=True)

    def test_nested_api_constants(self) -> None:
        """Test nested Api class via CONFIG dict."""
        api = FlextOracleWmsConstants.Api
        u.Tests.Matchers.that(hasattr(api, "CONFIG"), eq=True)
        config = api.CONFIG
        u.Tests.Matchers.that("default_timeout" in config, eq=True)
        u.Tests.Matchers.that("min_http_status_code" in config, eq=True)
        u.Tests.Matchers.that("max_http_status_code" in config, eq=True)

    def test_entity_type_enum(self) -> None:
        """Test WmsEntityType enum."""
        entity_type = FlextOracleWmsConstants.WmsEntityType
        u.Tests.Matchers.that(entity_type.INVENTORY == "inventory", eq=True)
        u.Tests.Matchers.that(entity_type.ORDERS == "orders", eq=True)
        u.Tests.Matchers.that(entity_type.SHIPMENTS == "shipments", eq=True)
        u.Tests.Matchers.that(entity_type.PICKING == "picking", eq=True)
        u.Tests.Matchers.that(entity_type.LOCATIONS == "locations", eq=True)
        u.Tests.Matchers.that(entity_type.ITEMS == "items", eq=True)

    def test_api_version_enum(self) -> None:
        """Test WmsApiVersion enum."""
        api_version = FlextOracleWmsConstants.WmsApiVersion
        u.Tests.Matchers.that(api_version.V1 == "v1", eq=True)
        u.Tests.Matchers.that(api_version.V2 == "v2", eq=True)
        u.Tests.Matchers.that(api_version.V3 == "v3", eq=True)
        u.Tests.Matchers.that(api_version.LEGACY == "legacy", eq=True)

    def test_operation_status_enum(self) -> None:
        """Test WmsOperationStatus enum."""
        status = FlextOracleWmsConstants.WmsOperationStatus
        u.Tests.Matchers.that(status.PENDING == "pending", eq=True)
        u.Tests.Matchers.that(status.RUNNING == "running", eq=True)
        u.Tests.Matchers.that(status.SUCCESS == "success", eq=True)
        u.Tests.Matchers.that(status.ERROR == "error", eq=True)
        u.Tests.Matchers.that(status.TIMEOUT == "timeout", eq=True)
        u.Tests.Matchers.that(status.CANCELLED == "cancelled", eq=True)

    def test_data_quality_enum(self) -> None:
        """Test WmsDataQuality enum."""
        quality = FlextOracleWmsConstants.WmsDataQuality
        u.Tests.Matchers.that(quality.HIGH == "high", eq=True)
        u.Tests.Matchers.that(quality.MEDIUM == "medium", eq=True)
        u.Tests.Matchers.that(quality.LOW == "low", eq=True)
        u.Tests.Matchers.that(quality.UNKNOWN == "unknown", eq=True)

    def test_filter_operator_enum(self) -> None:
        """Test WmsFilterOperator enum."""
        operator = FlextOracleWmsConstants.WmsFilterOperator
        u.Tests.Matchers.that(operator.EQ == "eq", eq=True)
        u.Tests.Matchers.that(operator.NE == "ne", eq=True)
        u.Tests.Matchers.that(operator.GT == "gt", eq=True)
        u.Tests.Matchers.that(operator.GTE == "gte", eq=True)
        u.Tests.Matchers.that(operator.LT == "lt", eq=True)
        u.Tests.Matchers.that(operator.LTE == "lte", eq=True)
        u.Tests.Matchers.that(operator.IN == "in", eq=True)
        u.Tests.Matchers.that(operator.NOT_IN == "not_in", eq=True)
        u.Tests.Matchers.that(operator.CONTAINS == "contains", eq=True)

    def test_page_mode_enum(self) -> None:
        """Test WmsPageMode enum."""
        mode = FlextOracleWmsConstants.WmsPageMode
        u.Tests.Matchers.that(mode.APPEND == "append", eq=True)
        u.Tests.Matchers.that(mode.REPLACE == "replace", eq=True)
        u.Tests.Matchers.that(mode.MERGE == "merge", eq=True)

    def test_write_mode_enum(self) -> None:
        """Test WmsWriteMode enum."""
        mode = FlextOracleWmsConstants.WmsWriteMode
        u.Tests.Matchers.that(mode.INSERT == "insert", eq=True)
        u.Tests.Matchers.that(mode.UPDATE == "update", eq=True)
        u.Tests.Matchers.that(mode.UPSERT == "upsert", eq=True)
        u.Tests.Matchers.that(mode.DELETE == "delete", eq=True)

    def test_module_level_auth_method_enum(self) -> None:
        """Test module-level OracleWMSAuthMethod enum."""
        u.Tests.Matchers.that(OracleWMSAuthMethod.BASIC == "basic", eq=True)
        u.Tests.Matchers.that(OracleWMSAuthMethod.OAUTH2 == "oauth2", eq=True)
        u.Tests.Matchers.that(OracleWMSAuthMethod.API_KEY == "api_key", eq=True)
        u.Tests.Matchers.that(OracleWMSAuthMethod.BEARER == "bearer", eq=True)

    def test_endpoint_discovery_strategy_enum(self) -> None:
        """Test EndpointDiscoveryStrategy enum."""
        strategy = FlextOracleWmsConstants.EndpointDiscoveryStrategy
        u.Tests.Matchers.that(strategy.API_BASED == "api_based", eq=True)
        u.Tests.Matchers.that(strategy.SCHEMA_BASED == "schema_based", eq=True)

    def test_flext_wms_version(self) -> None:
        """Test FLEXT_WMS_VERSION constant."""
        u.Tests.Matchers.that(
            isinstance(FlextOracleWmsConstants.FLEXT_WMS_VERSION, str), eq=True
        )
        u.Tests.Matchers.that(
            FlextOracleWmsConstants.FLEXT_WMS_VERSION == "0.9.0", eq=True
        )

    def test_wms_pagination_constants(self) -> None:
        """Test WmsPagination class constants."""
        pagination = FlextOracleWmsConstants.WmsPagination
        u.Tests.Matchers.that(pagination.DEFAULT_PAGE_SIZE == 100, eq=True)


__all__ = ["TestFlextOracleWmsConstants"]
