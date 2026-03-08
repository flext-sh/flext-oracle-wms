"""FLEXT Oracle WMS Models - Pydantic v2 namespaced models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextModels, t


class FlextOracleWmsModels(FlextModels):
    """Oracle WMS models with namespaced OracleWms domain.

    Access via m.OracleWms.Entity, m.OracleWms.ApiResponse after inheritance.
    """

    def __init_subclass__(cls, **kwargs: t.ContainerValue) -> None:
        """Allow downstream projects to inherit FlextOracleWmsModels for namespace composition."""
        super().__init_subclass__(**kwargs)

    class OracleWms:
        """Oracle WMS domain namespace — m.OracleWms.*."""


__all__ = ["FlextOracleWmsModels"]
