"""Flext-oracle-wms layer-zero configuration schemas.

Typed, frozen shapes for the ``config/*.yaml`` business-rule SSOT. This module
imports only Pydantic. ``FlextOracleWmsConfig`` declares one
typed field per YAML domain and exposes the validated objects as
``config.<domain>``. Adding a new config domain = add a nested model here and a
typed field on ``FlextOracleWmsConfig``.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class FlextModelsOracleWmsConfig:
    """Namespace of typed flext-oracle-wms config models (pure Pydantic)."""

    class Http(BaseModel):
        """HTTP response-classification thresholds."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        bad_request_threshold: int

    class Api(BaseModel):
        """Runtime API connection defaults."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        version_default: str
        timeout_default: int
        max_retries: int
        retry_delay: int

    class Processing(BaseModel):
        """Batch/page/schema processing limits."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        default_batch_size: int
        max_batch_size: int
        default_page_size: int
        max_schema_depth: int

    class Filtering(BaseModel):
        """Query-filter construction limits."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        max_filter_conditions: int

    class Entities(BaseModel):
        """Entity-name validation rules."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        max_entity_name_length: int

    class Auth(BaseModel):
        """OAuth2 authentication policy."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        oauth2_token_endpoint: str
        oauth2_scope_default: str

    class Environments(BaseModel):
        """Named Oracle WMS environment base URLs."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        default: str
        test: str
        production: str

    class ApiEndpoint(BaseModel):
        """A single validated Oracle WMS API endpoint definition."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        name: str
        method: str
        path: str
        version: str
        category: str
        description: str
        since_version: str


__all__: list[str] = ["FlextModelsOracleWmsConfig"]
