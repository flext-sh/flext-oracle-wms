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
from flext_tests import tm

__all__ = ["TestsFlextOracleWmsConfigDomains"]


class TestsFlextOracleWmsConfigDomains:
    """Public behavior of the validated config domains."""

    @pytest.mark.unit
    def test_http_domain_exposes_bad_request_threshold(self) -> None:
        """The http domain carries the validated bad-request threshold."""
        tm.that(config.OracleWms.http.bad_request_threshold, eq=400)

    @pytest.mark.unit
    def test_api_domain_exposes_connection_defaults(self) -> None:
        """The api domain carries version/timeout/retry defaults."""
        api = config.OracleWms.api
        tm.that(api.version_default, eq="v1")
        tm.that(api.timeout_default, eq=30)
        tm.that(api.max_retries, eq=3)
        tm.that(api.retry_delay, eq=1)

    @pytest.mark.unit
    def test_processing_domain_exposes_batch_and_page_sizes(self) -> None:
        """The processing domain carries batch/page/schema-depth rules."""
        proc = config.OracleWms.processing
        tm.that(proc.default_batch_size, eq=1000)
        tm.that(proc.max_batch_size, eq=10000)
        tm.that(proc.default_page_size, eq=10)
        tm.that(proc.max_schema_depth, eq=10)

    @pytest.mark.unit
    def test_filtering_domain_exposes_max_conditions(self) -> None:
        """The filtering domain carries the max-condition limit."""
        tm.that(config.OracleWms.filtering.max_filter_conditions, eq=50)

    @pytest.mark.unit
    def test_entities_domain_exposes_name_length(self) -> None:
        """The entities domain carries the max entity-name length."""
        tm.that(config.OracleWms.entities.max_entity_name_length, eq=100)

    @pytest.mark.unit
    def test_auth_domain_exposes_oauth2_policy(self) -> None:
        """The auth domain carries the OAuth2 endpoint and default scope."""
        auth = config.OracleWms.auth
        tm.that(auth.oauth2_token_endpoint, eq="/oauth2/token")
        tm.that(auth.oauth2_scope_default, eq="read write")

    @pytest.mark.unit
    def test_environments_domain_exposes_named_urls(self) -> None:
        """The environments domain maps named environments to base URLs."""
        envs = config.OracleWms.environments
        tm.that(envs.default, eq="http://localhost:8080")
        tm.that(envs.test, eq="https://test-wms.example.com")
        tm.that(envs.production, eq="https://prod-wms.example.com")

    @pytest.mark.unit
    def test_api_endpoints_domain_exposes_validated_catalog(self) -> None:
        """The api_endpoints domain maps endpoint names to validated models."""
        endpoint = config.OracleWms.api_endpoints["test"]
        tm.that(endpoint.name, eq="test")
        tm.that(endpoint.method, eq="GET")
        tm.that(endpoint.path, eq="/test/")
        tm.that(endpoint.version, eq="v1")
