import os
import sys

# Ensure local src is importable when running tests from repo root or package dir
pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if pkg_root not in sys.path:
    sys.path.insert(0, pkg_root)
