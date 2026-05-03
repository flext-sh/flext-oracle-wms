"""Test Oracle WMS constants and enum functionality.

Replaces legacy dynamic schema tests (module removed).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from tests import c


class TestsFlextOracleWmsSchemaDynamic:
    """Test the Oracle WMS constants class."""

    def test_version_constant(self) -> None:
        """Test WMS version is defined."""
        assert isinstance(c.OracleWms.FLEXT_WMS_VERSION, str)
        assert c.OracleWms.FLEXT_WMS_VERSION

    def test_api_config(self) -> None:
        """Test API settings dict is populated."""
        cfg = c.OracleWms.API_CONFIG
        assert "version_default" in cfg
        assert "base_url_default" in cfg
        assert "timeout_default" in cfg
        assert "max_retries" in cfg

    def test_processing_config(self) -> None:
        """Test processing settings dict is populated."""
        cfg = c.OracleWms.PROCESSING_CONFIG
        assert "default_batch_size" in cfg
        assert "max_batch_size" in cfg
        assert "default_page_size" in cfg

    def test_environments(self) -> None:
        """Test environment dict is populated."""
        envs = c.OracleWms.ENVIRONMENTS
        assert "default" in envs
        assert "test" in envs
        assert "production" in envs

    def test_wms_filter_operator_values(self) -> None:
        """Test WmsFilterOperator has expected members."""
        fo = c.OracleWms.WmsFilterOperator
        assert fo.EQ == "eq"
        assert fo.NE == "ne"
        assert fo.GT == "gt"
        assert fo.IN == "in"

    def test_oracle_wms_auth_method(self) -> None:
        """Test OracleWMSAuthMethod has expected members."""
        assert c.OracleWms.OracleWMSAuthMethod.BASIC == "basic"
        assert c.OracleWms.OracleWMSAuthMethod.OAUTH2 == "oauth2"
        assert c.OracleWms.OracleWMSAuthMethod.API_KEY == "api_key"
        assert c.OracleWms.OracleWMSAuthMethod.BEARER == "bearer"

    def test_filtering_max_conditions(self) -> None:
        """Test filtering constants."""
        assert c.OracleWms.Filtering.MAX_FILTER_CONDITIONS == 50

    def test_wms_entities_max_name(self) -> None:
        """Test entity name length limit."""
        assert c.OracleWms.WmsEntities.MAX_ENTITY_NAME_LENGTH == 100

    def test_wms_processing_defaults(self) -> None:
        """Test processing defaults."""
        assert c.OracleWms.WmsProcessing.MAX_SCHEMA_DEPTH == 10
