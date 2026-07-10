"""Runtime settings for flext-oracle-wms tests."""

from __future__ import annotations

from flext_tests import FlextTestsSettings

from flext_oracle_wms import FlextOracleWmsSettings


class TestsFlextOracleWmsSettings(FlextOracleWmsSettings, FlextTestsSettings):
    """Oracle WMS settings extended with the shared test namespace."""


__all__: list[str] = ["TestsFlextOracleWmsSettings"]
