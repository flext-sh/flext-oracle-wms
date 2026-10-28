"""Compose the canonical layer-zero WMS configuration declarations.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_oracle_wms.config_models import FlextModelsOracleWmsConfig as _ConfigModels


class FlextModelsOracleWmsConfig(_ConfigModels):
    """Expose the single configuration schema owner through the model family."""


__all__: list[str] = ["FlextModelsOracleWmsConfig"]
