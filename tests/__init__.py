# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests.constants import (
        TestsFlextOracleWmsConstants,
        TestsFlextOracleWmsConstants as c,
    )
    from tests.models import TestsFlextOracleWmsModels, TestsFlextOracleWmsModels as m
    from tests.protocols import (
        TestsFlextOracleWmsProtocols,
        TestsFlextOracleWmsProtocols as p,
    )
    from tests.typings import TestsFlextOracleWmsTypes, TestsFlextOracleWmsTypes as t
    from tests.utilities import (
        TestsFlextOracleWmsUtilities,
        TestsFlextOracleWmsUtilities as u,
    )
_LAZY_IMPORTS = {
    "TestsFlextOracleWmsConstants": ("tests.constants", "TestsFlextOracleWmsConstants"),
    "TestsFlextOracleWmsModels": ("tests.models", "TestsFlextOracleWmsModels"),
    "TestsFlextOracleWmsProtocols": ("tests.protocols", "TestsFlextOracleWmsProtocols"),
    "TestsFlextOracleWmsTypes": ("tests.typings", "TestsFlextOracleWmsTypes"),
    "TestsFlextOracleWmsUtilities": ("tests.utilities", "TestsFlextOracleWmsUtilities"),
    "c": ("tests.constants", "TestsFlextOracleWmsConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("tests.models", "TestsFlextOracleWmsModels"),
    "p": ("tests.protocols", "TestsFlextOracleWmsProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("tests.typings", "TestsFlextOracleWmsTypes"),
    "u": ("tests.utilities", "TestsFlextOracleWmsUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "TestsFlextOracleWmsConstants",
    "TestsFlextOracleWmsModels",
    "TestsFlextOracleWmsProtocols",
    "TestsFlextOracleWmsTypes",
    "TestsFlextOracleWmsUtilities",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
