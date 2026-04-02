"""Unit tests for c class.

Tests the constants module against actual source structure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextConstants
from tests import c


class Testc:
    """Test cases for c class."""

    def test_class_inheritance(self) -> None:
        """Test that c follows proper inheritance patterns."""
        assert issubclass(c, FlextConstants)

    def test_flext_wms_version(self) -> None:
        """Test FLEXT_WMS_VERSION constant."""
        assert isinstance(c.OracleWms.FLEXT_WMS_VERSION, str)
        assert c.OracleWms.FLEXT_WMS_VERSION

    def test_api_constants(self) -> None:
        """Test API-related constants via API_CONFIG dict."""
        api = c.OracleWms.API_CONFIG
        assert api["version_default"] == "v1"
        assert isinstance(api["base_url_default"], str)
        assert isinstance(api["timeout_default"], int)
        assert api["max_retries"] == 3

    def test_processing_config(self) -> None:
        """Test processing config dict is populated."""
        proc = c.OracleWms.PROCESSING_CONFIG
        assert "default_batch_size" in proc
        assert "max_batch_size" in proc
        assert "default_page_size" in proc

    def test_environments(self) -> None:
        """Test environment dict is populated."""
        envs = c.OracleWms.ENVIRONMENTS
        assert "default" in envs
        assert "test" in envs
        assert "production" in envs

    def test_authentication_constants(self) -> None:
        """Test authentication constants via AUTH_CONFIG dict."""
        auth = c.OracleWms.AUTH_CONFIG
        assert auth["basic"] == c.OracleWms.OracleWMSAuthMethod.BASIC
        assert auth["oauth2"] == c.OracleWms.OracleWMSAuthMethod.OAUTH2
        assert auth["api_key"] == c.OracleWms.OracleWMSAuthMethod.API_KEY

    def test_entity_type_constants(self) -> None:
        """Test ENTITY_TYPES tuple derived from WmsEntityType enum."""
        entity_types = tuple(c.OracleWms.WmsEntityType)
        assert isinstance(entity_types, tuple)
        assert "inventory" in entity_types
        assert "orders" in entity_types
        assert "shipments" in entity_types
        assert "picking" in entity_types
        assert "locations" in entity_types
        assert "items" in entity_types

    def test_nested_oracle_wms_constants(self) -> None:
        """Test nested OracleWms class constants (connection-related)."""
        connection = c.OracleWms
        assert hasattr(connection, "DEFAULT_TIMEOUT")
        assert hasattr(connection, "DEFAULT_MAX_RETRIES")
        assert hasattr(connection, "DEFAULT_RETRY_DELAY")
        assert hasattr(connection, "MAX_POOL_SIZE")

    def test_nested_wms_entities_constants(self) -> None:
        """Test nested WmsEntities class constants."""
        wms_entities = c.WmsEntities
        assert hasattr(wms_entities, "MAX_ENTITY_NAME_LENGTH")
        assert hasattr(wms_entities, "ENTITY_NAME_PATTERN")

    def test_nested_processing_constants(self) -> None:
        """Test nested WmsProcessing class constants."""
        processing = c.WmsProcessing
        assert hasattr(processing, "DEFAULT_BATCH_SIZE")
        assert hasattr(processing, "MAX_BATCH_SIZE")
        assert hasattr(processing, "DEFAULT_PAGE_SIZE")
        assert hasattr(processing, "MAX_SCHEMA_DEPTH")

    def test_nested_filtering_constants(self) -> None:
        """Test nested Filtering class constants."""
        filtering = c.Filtering
        assert hasattr(filtering, "MAX_FILTER_CONDITIONS")

    def test_nested_error_messages_constants(self) -> None:
        """Test nested ErrorMessages class via MESSAGES dict."""
        error_messages = c.ErrorMessages
        assert hasattr(error_messages, "MESSAGES")
        msgs = error_messages.MESSAGES
        assert "entity_validation_failed" in msgs
        assert "discovery_failed" in msgs
        assert "invalid_response" in msgs

    def test_nested_authentication_constants(self) -> None:
        """Test nested Authentication class constants."""
        auth = c.Authentication
        assert hasattr(auth, "MIN_TOKEN_LENGTH")
        assert hasattr(auth, "MIN_API_KEY_LENGTH")

    def test_nested_api_constants(self) -> None:
        """Test nested Api class via CONFIG dict."""
        api = c.Api
        assert hasattr(api, "CONFIG")
        config = api.CONFIG
        assert "default_timeout" in config
        assert "min_http_status_code" in config
        assert "max_http_status_code" in config

    def test_entity_type_enum(self) -> None:
        """Test WmsEntityType enum."""
        entity_type = c.OracleWms.WmsEntityType
        assert entity_type.INVENTORY == "inventory"
        assert entity_type.ORDERS == "orders"
        assert entity_type.SHIPMENTS == "shipments"
        assert entity_type.PICKING == "picking"
        assert entity_type.LOCATIONS == "locations"
        assert entity_type.ITEMS == "items"

    def test_api_version_enum(self) -> None:
        """Test WmsApiVersion enum."""
        api_version = c.OracleWms.WmsApiVersion
        assert api_version.V1 == "v1"
        assert api_version.V2 == "v2"
        assert api_version.V3 == "v3"
        assert api_version.LEGACY == "legacy"

    def test_operation_status_enum(self) -> None:
        """Test WmsOperationStatus enum."""
        status = c.OracleWms.WmsOperationStatus
        assert status.PENDING == "pending"
        assert status.RUNNING == "running"
        assert status.SUCCESS == "success"
        assert status.ERROR == "error"
        assert status.TIMEOUT == "timeout"
        assert status.CANCELLED == "cancelled"

    def test_data_quality_enum(self) -> None:
        """Test WmsDataQuality enum."""
        quality = c.OracleWms.WmsDataQuality
        assert quality.HIGH == "high"
        assert quality.MEDIUM == "medium"
        assert quality.LOW == "low"
        assert quality.UNKNOWN == "unknown"

    def test_filter_operator_enum(self) -> None:
        """Test WmsFilterOperator enum."""
        operator = c.OracleWms.WmsFilterOperator
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
        mode = c.OracleWms.WmsPageMode
        assert mode.APPEND == "append"
        assert mode.REPLACE == "replace"
        assert mode.MERGE == "merge"

    def test_write_mode_enum(self) -> None:
        """Test WmsWriteMode enum."""
        mode = c.OracleWms.WmsWriteMode
        assert mode.INSERT == "insert"
        assert mode.UPDATE == "update"
        assert mode.UPSERT == "upsert"
        assert mode.DELETE == "delete"

    def test_module_level_auth_method_enum(self) -> None:
        """Test module-level OracleWMSAuthMethod enum."""
        assert c.OracleWms.OracleWMSAuthMethod.BASIC == "basic"
        assert c.OracleWms.OracleWMSAuthMethod.OAUTH2 == "oauth2"
        assert c.OracleWms.OracleWMSAuthMethod.API_KEY == "api_key"
        assert c.OracleWms.OracleWMSAuthMethod.BEARER == "bearer"

    def test_endpoint_discovery_strategy_enum(self) -> None:
        """Test EndpointDiscoveryStrategy enum."""
        strategy = c.OracleWms.EndpointDiscoveryStrategy
        assert strategy.API_BASED == "api_based"
        assert strategy.SCHEMA_BASED == "schema_based"

    def test_wms_pagination_constants(self) -> None:
        """Test WmsPagination class constants."""
        pagination = c.WmsPagination
        assert pagination.DEFAULT_PAGE_SIZE == 100


__all__ = ["Testc"]
