"""Sitecustomize module.
This module is part of the FLEXT ecosystem. Docstrings follow PEP 257 and Google style.
"""

import os
import pathlib
import sys

# Ensure local src is importable when running tests from repo root or package dir
pkg_root = pathlib.Path(
    os.path.join(pathlib.Path(__file__).parent, "..", "src"),
).resolve()
if pkg_root not in sys.path:
    sys.path.insert(0, pkg_root)
