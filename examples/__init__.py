# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Examples package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from examples.tests import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "conftest_project": "examples.tests.conftest_project",
    "load_env_config": "examples.tests.test_declarative_example",
    "logger": "examples.tests.test_declarative_example",
    "main": "examples.tests.test_declarative_example",
    "test_declarative_example": "examples.tests.test_declarative_example",
    "tests": "examples.tests",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
