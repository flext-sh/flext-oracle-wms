# AUTO-GENERATED FILE — Regenerate with: make gen
"""Package version and metadata for flext-oracle-wms.

Subclass of ``FlextVersion`` — overrides only ``_metadata``.
All derived attributes (``__version__``, ``__title__``, etc.) are
computed automatically via ``FlextVersion.__init_subclass__``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib.metadata import PackageMetadata, metadata

from flext_core import FlextVersion, t


class FlextOracleWmsVersion(FlextVersion):
    """flext-oracle-wms version — MRO-derived from FlextVersion."""

    _metadata: PackageMetadata | t.StrMapping = metadata("flext-oracle-wms")


__version__ = FlextOracleWmsVersion.__version__
__version_info__ = FlextOracleWmsVersion.__version_info__
__title__ = FlextOracleWmsVersion.__title__
__description__ = FlextOracleWmsVersion.__description__
__author__ = FlextOracleWmsVersion.__author__
__author_email__ = FlextOracleWmsVersion.__author_email__
__license__ = FlextOracleWmsVersion.__license__
__url__ = FlextOracleWmsVersion.__url__
__all__: list[str] = [
    "FlextOracleWmsVersion",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
]
