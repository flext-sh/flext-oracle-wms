# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Examples package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

from examples.tests import _LAZY_IMPORTS as _CHILD_LAZY_0

if TYPE_CHECKING:
    from examples.tests import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    **_CHILD_LAZY_0,
    "tests": "examples.tests",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
