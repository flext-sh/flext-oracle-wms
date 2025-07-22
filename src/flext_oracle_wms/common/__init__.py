"""Oracle WMS Common Package - Shared utilities and standardized exports.

This package provides common utilities, base classes, and shared functionality
for Oracle WMS integrations across all modules. It standardizes the export
patterns used by filtering and singer packages.

Copyright (c) 2025 FLEXT Contributors
SPX-License-Identifier: MIT
"""

from __future__ import annotations


def create_standard_exports(
    module_name: str,
    exports: list[str],
) -> tuple[list[str], str]:
    """Create standardized __all__ exports and docstring for Oracle WMS modules.

    Args:
        module_name: Name of the module (e.g., "Filtering", "Singer SDK")
        exports: List of export names

    Returns:
        Tuple of (__all__ list, formatted docstring)

    """
    docstring = f"""Oracle WMS {module_name} Package - Strict compliance with mandatory capabilities.

This package provides {module_name.lower()} strict compliance for Oracle WMS integrations
with mandatory capabilities as required.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

    return exports, docstring


__all__ = [
    "create_standard_exports",
]
