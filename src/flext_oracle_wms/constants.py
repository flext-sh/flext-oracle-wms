"""FLEXT WMS Constants - Generic WMS constants with patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_api import FlextApiConstants

from flext_oracle_wms._constants.base import FlextOracleWmsConstantsBase
from flext_oracle_wms._constants.values import FlextOracleWmsConstantsValues


class FlextOracleWmsConstants(FlextApiConstants):
    """Generic WMS constants class with composition patterns.

    Uses Python 3.13+ syntax, reduces declarations through patterns.
    One class per module following SOLID principles. Generic for any WMS system.
    """

    class OracleWms(
        FlextOracleWmsConstantsBase,
        FlextOracleWmsConstantsValues.OracleWms,
    ):
        """WMS connection constants - composed from base.

        Every scalar, mapping, enum and nested namespace is owned by
        ``flext_oracle_wms._constants`` (base and values) and inherited
        through this facade subclass.
        """


c = FlextOracleWmsConstants

__all__: tuple[str, ...] = ("FlextOracleWmsConstants", "c")
