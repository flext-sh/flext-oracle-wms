"""Flext-oracle-wms config models (m facade; no project-specific imports).

Typed, frozen shapes for the ``config/*.yaml`` business-rule SSOT. This module
imports only the ``flext_core.m`` facade — the ``_config.py`` facade validates the
model-less YAML slices into these classes and exposes the ready objects under
``config.oracle_wms.<domain>``. Adding a new config domain = add a nested model
here and a validated field on ``Root`` (cosmos-main ``_models/config.py`` shape).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import m


class FlextOracleWmsConfigModels:
    """Namespace of typed flext-oracle-wms config models (pure Pydantic)."""

    class Http(m.BaseModel):
        """HTTP response-classification thresholds."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        bad_request_threshold: int

    class Api(m.BaseModel):
        """Runtime API connection defaults."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        version_default: str
        timeout_default: int
        max_retries: int
        retry_delay: int

    class Processing(m.BaseModel):
        """Batch/page/schema processing limits."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        default_batch_size: int
        max_batch_size: int
        default_page_size: int
        max_schema_depth: int

    class Filtering(m.BaseModel):
        """Query-filter construction limits."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        max_filter_conditions: int

    class Entities(m.BaseModel):
        """Entity-name validation rules."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        max_entity_name_length: int

    class Auth(m.BaseModel):
        """OAuth2 authentication policy."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        oauth2_token_endpoint: str
        oauth2_scope_default: str

    class Environments(m.BaseModel):
        """Named Oracle WMS environment base URLs."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        default: str
        test: str
        production: str

    class ApiEndpoint(m.BaseModel):
        """A single validated Oracle WMS API endpoint definition."""

        model_config = m.ConfigDict(frozen=True, extra="forbid")

        name: str
        method: str
        path: str
        version: str
        category: str
        description: str
        since_version: str

    class Root(m.BaseModel):
        """Root oracle-wms runtime config validated from ``config/*.yaml``."""

        model_config = m.ConfigDict(frozen=True, extra="ignore")

        http: FlextOracleWmsConfigModels.Http
        api: FlextOracleWmsConfigModels.Api
        processing: FlextOracleWmsConfigModels.Processing
        filtering: FlextOracleWmsConfigModels.Filtering
        entities: FlextOracleWmsConfigModels.Entities
        auth: FlextOracleWmsConfigModels.Auth
        environments: FlextOracleWmsConfigModels.Environments
        api_endpoints: dict[str, FlextOracleWmsConfigModels.ApiEndpoint]


__all__: list[str] = ["FlextOracleWmsConfigModels"]
