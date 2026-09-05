"""Public Oracle WMS owner and composition contracts.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_oracle_wms import (
    FlextOracleWmsConfig,
    FlextOracleWmsSettings,
    config,
    settings,
)
from flext_tests import tm

if TYPE_CHECKING:
    from flext_oracle_wms import FlextOracleWmsApi, p


class TestsFlextOracleWmsHelpersCore:
    """Observable contracts of the public settings, config, and API owners."""

    def test_settings_fixture_is_the_public_settings_owner(
        self, oracle_wms_settings: FlextOracleWmsSettings
    ) -> None:
        """Tests consume the same typed settings singleton as production."""
        tm.that(oracle_wms_settings, is_=FlextOracleWmsSettings)
        assert oracle_wms_settings is settings

    def test_config_fixture_is_the_public_config_owner(
        self, oracle_wms_config: p.OracleWms.Config
    ) -> None:
        """Tests consume the validated config projection without copying it."""
        tm.that(config, is_=FlextOracleWmsConfig)
        assert oracle_wms_config is config.oracle_wms

    def test_real_public_api_executes(
        self, oracle_wms_api: FlextOracleWmsApi
    ) -> None:
        """The injected public composition root reports readiness."""
        result = oracle_wms_api.execute()

        tm.ok(result)
        tm.that(result.unwrap(), eq=True)


__all__: list[str] = ["TestsFlextOracleWmsHelpersCore"]
