"""Behavioral contract for the validated ``config.OracleWms.*`` domains.

The business-rule SSOT lives in ``config/oracle-wms.yaml`` and is validated into
the frozen ``FlextOracleWmsConfigModels`` shapes, exposed as typed objects under
``config.OracleWms.<domain>`` (never a model-less dict subscript).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

from flext_oracle_wms import config

__all__ = ["TestsFlextOracleWmsConfigDomains"]


class TestsFlextOracleWmsConfigDomains:
    """Public behavior of the validated config domains."""

    @pytest.mark.unit
    def test_http_domain_exposes_bad_request_threshold(self) -> None:
        """The http domain carries the validated bad-request threshold."""
        assert config.OracleWms.http.bad_request_threshold == 400

    @pytest.mark.unit
    def test_api_domain_exposes_connection_defaults(self) -> None:
        """The api domain carries version/timeout/retry defaults."""
        api = config.OracleWms.api
        assert api.version_default == "v1"
        assert api.timeout_default == 30
        assert api.max_retries == 3
        assert api.retry_delay == 1

    @pytest.mark.unit
    def test_processing_domain_exposes_batch_and_page_sizes(self) -> None:
        """The processing domain carries batch/page/schema-depth rules."""
        proc = config.OracleWms.processing
        assert proc.default_batch_size == 1000
        assert proc.max_batch_size == 10000
        assert proc.default_page_size == 10
        assert proc.max_schema_depth == 10

    @pytest.mark.unit
    def test_filtering_domain_exposes_max_conditions(self) -> None:
        """The filtering domain carries the max-condition limit."""
        assert config.OracleWms.filtering.max_filter_conditions == 50

    @pytest.mark.unit
    def test_entities_domain_exposes_name_length(self) -> None:
        """The entities domain carries the max entity-name length."""
        assert config.OracleWms.entities.max_entity_name_length == 100

    @pytest.mark.unit
    def test_auth_domain_exposes_oauth2_policy(self) -> None:
        """The auth domain carries the OAuth2 endpoint and default scope."""
        auth = config.OracleWms.auth
        assert auth.oauth2_token_endpoint == "/oauth2/token"
        assert auth.oauth2_scope_default == "read write"

    @pytest.mark.unit
    def test_environments_domain_exposes_named_urls(self) -> None:
        """The environments domain maps named environments to base URLs."""
        envs = config.OracleWms.environments
        assert envs.default == "http://localhost:8080"
        assert envs.test == "https://test-wms.example.com"
        assert envs.production == "https://prod-wms.example.com"

    @pytest.mark.unit
    def test_api_endpoints_domain_exposes_validated_catalog(self) -> None:
        """The api_endpoints domain maps endpoint names to validated models."""
        endpoint = config.OracleWms.api_endpoints["test"]
        assert endpoint.name == "test"
        assert endpoint.method == "GET"
        assert endpoint.path == "/test/"
        assert endpoint.version == "v1"
