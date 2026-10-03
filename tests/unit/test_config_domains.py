"""Behavioral contract for the validated ``config.oracle_wms.*`` domains.

The business-rule SSOT lives in ``config/oracle-wms.yaml`` and is validated into
the frozen ``FlextOracleWmsConfigModels`` shapes, exposed as typed objects under
``config.oracle_wms.<domain>`` (never a model-less dict subscript).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_oracle_wms import config


class TestsFlextOracleWmsConfigDomains:
    """Public behavior of the validated config domains."""

    @staticmethod
    @pytest.mark.unit
    def test_http_domain_exposes_bad_request_threshold() -> None:
        """The http domain carries the validated bad-request threshold."""
        tm.that(config.oracle_wms.http.bad_request_threshold, eq=400)

    @staticmethod
    @pytest.mark.unit
    def test_api_domain_exposes_connection_defaults() -> None:
        """The api domain carries version/timeout/retry defaults."""
        api = config.oracle_wms.api
        tm.that(api.version_default, eq="v1")
        tm.that(api.timeout_default, eq=30)
        tm.that(api.max_retries, eq=3)
        tm.that(api.retry_delay, eq=1)

    @staticmethod
    @pytest.mark.unit
    def test_processing_domain_exposes_batch_and_page_sizes() -> None:
        """The processing domain carries batch/page/schema-depth rules."""
        proc = config.oracle_wms.processing
        tm.that(proc.default_batch_size, eq=1000)
        tm.that(proc.max_batch_size, eq=10000)
        tm.that(proc.default_page_size, eq=10)
        tm.that(proc.max_schema_depth, eq=10)

    @staticmethod
    @pytest.mark.unit
    def test_filtering_domain_exposes_max_conditions() -> None:
        """The filtering domain carries the max-condition limit."""
        tm.that(config.oracle_wms.filtering.max_filter_conditions, eq=50)

    @staticmethod
    @pytest.mark.unit
    def test_entities_domain_exposes_name_length() -> None:
        """The entities domain carries the max entity-name length."""
        tm.that(config.oracle_wms.entities.max_entity_name_length, eq=100)

    @staticmethod
    @pytest.mark.unit
    def test_auth_domain_exposes_oauth2_policy() -> None:
        """The auth domain carries the OAuth2 endpoint and default scope."""
        auth = config.oracle_wms.auth
        tm.that(auth.oauth2_token_endpoint, eq="/oauth2/token")
        tm.that(auth.oauth2_scope_default, eq="read write")

    @staticmethod
    @pytest.mark.unit
    def test_environments_domain_exposes_named_urls() -> None:
        """The environments domain maps named environments to base URLs."""
        envs = config.oracle_wms.environments
        tm.that(envs.default, eq="http://localhost:8080")
        tm.that(envs.test, eq="https://test-wms.example.com")
        tm.that(envs.production, eq="https://prod-wms.example.com")

    @staticmethod
    @pytest.mark.unit
    def test_api_endpoints_domain_exposes_validated_catalog() -> None:
        """The api_endpoints domain maps endpoint names to validated models."""
        endpoint = config.oracle_wms.api_endpoints["test"]
        tm.that(endpoint.name, eq="test")
        tm.that(endpoint.method, eq="GET")
        tm.that(endpoint.path, eq="/test/")
        tm.that(endpoint.version, eq="v1")
