"""CLI entrypoint for flext-oracle-wms — preserves the declared console script.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence


def main(args: Sequence[str] | None = None) -> int:
    """Console-script entry point — commands are not implemented yet.

    Args:
        args: Raw CLI argument sequence, accepted and ignored.

    Returns:
        Process exit code.

    """
    _ = args
    return 0


__all__: list[str] = ["main"]
