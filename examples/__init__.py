# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Examples package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from examples import tests
    from examples.tests import conftest_project, test_declarative_example
    from examples.tests.test_declarative_example import *

from examples.tests import _LAZY_IMPORTS as _TESTS_LAZY

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    **_TESTS_LAZY,
    "tests": "examples.tests",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
