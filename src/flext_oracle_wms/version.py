"""Project metadata for flext oracle wms."""

from __future__ import annotations

from typing import Final

# Simple version management without flext_core.metadata dependency
__version__: Final[str] = "0.9.9"
__version_info__: Final[tuple[int, int, int]] = (0, 9, 9)


# Backward compatibility - simple version class
class FlextOracleWmsVersion:
    """Structured metadata for the flext oracle wms distribution."""

    version: str = __version__
    version_info: tuple[int, int, int] = __version_info__

    @classmethod
    def current(cls) -> FlextOracleWmsVersion:
        """Return canonical metadata."""
        return cls()


VERSION: Final[FlextOracleWmsVersion] = FlextOracleWmsVersion.current()

__all__ = ["VERSION", "FlextOracleWmsVersion", "__version__", "__version_info__"]
