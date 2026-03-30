# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Init module.

This module is part of the FLEXT ecosystem. Docstrings follow PEP 257 and Google style.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from examples.tests import (
        conftest_project as conftest_project,
        test_declarative_example as test_declarative_example,
    )
    from examples.tests.test_declarative_example import (
        load_env_config as load_env_config,
        logger as logger,
        main as main,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "conftest_project": ["examples.tests.conftest_project", ""],
    "load_env_config": ["examples.tests.test_declarative_example", "load_env_config"],
    "logger": ["examples.tests.test_declarative_example", "logger"],
    "main": ["examples.tests.test_declarative_example", "main"],
    "test_declarative_example": ["examples.tests.test_declarative_example", ""],
}

_EXPORTS: Sequence[str] = [
    "conftest_project",
    "load_env_config",
    "logger",
    "main",
    "test_declarative_example",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
