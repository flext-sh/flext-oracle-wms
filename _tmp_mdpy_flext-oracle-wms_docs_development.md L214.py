# from flext-oracle-wms/docs/development.md:214
from __future__ import annotations


def test_real_connection():
    settings = FlextOracleWmsModuleSettings.for_testing()  # Uses test.example.com
    # Connection tests expect network failures with test settings
