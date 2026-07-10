"""Service base for flext-oracle-wms tests."""

from __future__ import annotations

from typing import override

from flext_tests import s as tests_s

from flext_oracle_wms import m
from tests.settings import TestsFlextOracleWmsSettings


class TestsFlextOracleWmsServiceBase(tests_s):
    """Oracle WMS test service base with source and test settings namespaces."""

    @classmethod
    @override
    def fetch_settings(cls) -> TestsFlextOracleWmsSettings:
        """Return the typed Oracle WMS+Tests settings singleton."""

    @classmethod
    @override
    def _runtime_bootstrap_options(cls) -> m.RuntimeBootstrapOptions:
        return m.RuntimeBootstrapOptions(settings_type=TestsFlextOracleWmsSettings)


s = TestsFlextOracleWmsServiceBase

__all__: list[str] = ["TestsFlextOracleWmsServiceBase", "s"]
