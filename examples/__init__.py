# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Examples package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
    from examples import tests
    from examples.tests import (
        conftest_project,
        load_env_config,
        logger,
        main,
        test_declarative_example,
    )
    from flext_core import FlextTypes

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    ("examples.tests",),
    {
        "tests": "examples.tests",
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
