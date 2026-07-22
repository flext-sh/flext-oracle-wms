"""Runtime settings for flext-oracle-wms tests."""

from __future__ import annotations

from flext_oracle_wms import FlextOracleWmsSettings
from flext_tests import FlextTestsSettings


class TestsFlextOracleWmsSettings(FlextOracleWmsSettings, FlextTestsSettings):
    """Oracle WMS settings extended with the shared test namespace."""


__all__: list[str] = ["TestsFlextOracleWmsSettings"]
