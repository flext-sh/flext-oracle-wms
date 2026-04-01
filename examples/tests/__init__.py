# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Init module.

This module is part of the FLEXT ecosystem. Docstrings follow PEP 257 and Google style.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from examples.tests.test_declarative_example import load_env_config, logger, main

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "conftest_project": "examples.tests.conftest_project",
    "load_env_config": "examples.tests.test_declarative_example",
    "logger": "examples.tests.test_declarative_example",
    "main": "examples.tests.test_declarative_example",
    "test_declarative_example": "examples.tests.test_declarative_example",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
