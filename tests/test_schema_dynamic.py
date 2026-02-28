"""Test Oracle WMS constants and enum functionality.

Replaces legacy dynamic schema tests (module removed).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_oracle_wms import FlextOracleWmsConstants, OracleWMSAuthMethod


class TestFlextOracleWmsConstants:
    """Test the Oracle WMS constants class."""

    def test_version_constant(self) -> None:
        """Test WMS version is defined."""
        assert isinstance(FlextOracleWmsConstants.FLEXT_WMS_VERSION, str)
        assert len(FlextOracleWmsConstants.FLEXT_WMS_VERSION) > 0

    def test_api_config(self) -> None:
        """Test API config dict is populated."""
        cfg = FlextOracleWmsConstants.API_CONFIG
        assert "version_default" in cfg
        assert "base_url_default" in cfg
        assert "timeout_default" in cfg
        assert "max_retries" in cfg

    def test_processing_config(self) -> None:
        """Test processing config dict is populated."""
        cfg = FlextOracleWmsConstants.PROCESSING_CONFIG
        assert "default_batch_size" in cfg
        assert "max_batch_size" in cfg
        assert "default_page_size" in cfg

    def test_environments(self) -> None:
        """Test environment dict is populated."""
        envs = FlextOracleWmsConstants.ENVIRONMENTS
        assert "default" in envs
        assert "test" in envs
        assert "production" in envs


class TestWmsEnums:
    """Test WMS StrEnum types."""

    def test_wms_entity_type_values(self) -> None:
        """Test WmsEntityType has expected members."""
        et = FlextOracleWmsConstants.WmsEntityType
        assert et.INVENTORY == "inventory"
        assert et.ORDERS == "orders"
        assert et.SHIPMENTS == "shipments"

    def test_wms_api_version_values(self) -> None:
        """Test WmsApiVersion has expected members."""
        av = FlextOracleWmsConstants.WmsApiVersion
        assert av.V1 == "v1"
        assert av.V2 == "v2"
        assert av.V3 == "v3"
        assert av.LEGACY == "legacy"

    def test_wms_api_category_values(self) -> None:
        """Test WmsApiCategory has expected members."""
        ac = FlextOracleWmsConstants.WmsApiCategory
        assert ac.INVENTORY == "inventory"
        assert ac.ORDERS == "orders"
        assert ac.SHIPPING == "shipping"
        assert ac.RECEIVING == "receiving"
        assert ac.REPORTING == "reporting"

    def test_wms_filter_operator_values(self) -> None:
        """Test WmsFilterOperator has expected members."""
        fo = FlextOracleWmsConstants.WmsFilterOperator
        assert fo.EQ == "eq"
        assert fo.NE == "ne"
        assert fo.GT == "gt"
        assert fo.IN == "in"

    def test_wms_operation_status_values(self) -> None:
        """Test WmsOperationStatus has expected members."""
        os_ = FlextOracleWmsConstants.WmsOperationStatus
        assert os_.PENDING == "pending"
        assert os_.SUCCESS == "success"
        assert os_.ERROR == "error"

    def test_oracle_wms_auth_method(self) -> None:
        """Test OracleWMSAuthMethod has expected members."""
        assert OracleWMSAuthMethod.BASIC == "basic"
        assert OracleWMSAuthMethod.OAUTH2 == "oauth2"
        assert OracleWMSAuthMethod.API_KEY == "api_key"
        assert OracleWMSAuthMethod.BEARER == "bearer"


class TestNestedConstants:
    """Test nested constant classes."""

    def test_filtering_max_conditions(self) -> None:
        """Test filtering constants."""
        assert FlextOracleWmsConstants.Filtering.MAX_FILTER_CONDITIONS == 50

    def test_wms_entities_max_name(self) -> None:
        """Test entity name length limit."""
        assert FlextOracleWmsConstants.WmsEntities.MAX_ENTITY_NAME_LENGTH == 100

    def test_wms_processing_defaults(self) -> None:
        """Test processing defaults."""
        assert FlextOracleWmsConstants.WmsProcessing.MAX_SCHEMA_DEPTH == 10

    def test_entity_types_tuple(self) -> None:
        """Test ENTITY_TYPES generated from StrEnum."""
        et = tuple(FlextOracleWmsConstants.WmsEntityType)
        assert isinstance(et, tuple)
        assert "inventory" in et
        assert "orders" in et

    def test_wms_entities_types_from_enum(self) -> None:
        """Test WmsEntities.TYPES generated from StrEnum names."""
        types = tuple(member.name for member in FlextOracleWmsConstants.WmsEntityType)
        assert isinstance(types, tuple)
        assert "INVENTORY" in types
        assert "ORDERS" in types
