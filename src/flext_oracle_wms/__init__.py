# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext oracle wms package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_oracle_wms.__version__ import (
    __all__,
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_oracle_wms import (
        _utilities,
        api,
        auth,
        client,
        constants,
        discovery,
        errors,
        filtering,
        http_client,
        models,
        protocols,
        settings,
        typings,
        utilities,
        wms_api,
        wms_auth,
        wms_client,
        wms_discovery,
        wms_exceptions,
    )
    from flext_oracle_wms._utilities import (
        DISCOVERY_FAILURE,
        DISCOVERY_SUCCESS,
        FlextOracleWmsDataValidationError,
        FlextOracleWmsFilterOperator,
        FlextOracleWmsOperatorFilter,
        FlextOracleWmsUtilitiesAuth,
        FlextOracleWmsUtilitiesClient,
        FlextOracleWmsUtilitiesDiscovery,
        FlextOracleWmsUtilitiesHttpClient,
    )
    from flext_oracle_wms.api import FlextOracleWmsApi
    from flext_oracle_wms.constants import (
        FlextOracleWmsConstants,
        FlextOracleWmsConstants as c,
    )
    from flext_oracle_wms.errors import (
        FlextOracleWmsExceptions,
        FlextOracleWmsShipmentError,
    )
    from flext_oracle_wms.filtering import FlextOracleWmsFilter
    from flext_oracle_wms.http_client import FlextHttpClient, create_flext_http_client
    from flext_oracle_wms.models import FlextOracleWmsModels, FlextOracleWmsModels as m
    from flext_oracle_wms.protocols import (
        FlextOracleWmsProtocols,
        FlextOracleWmsProtocols as p,
    )
    from flext_oracle_wms.settings import (
        FlextOracleWmsClientSettings,
        FlextOracleWmsSettings,
    )
    from flext_oracle_wms.typings import FlextOracleWmsTypes, FlextOracleWmsTypes as t
    from flext_oracle_wms.utilities import (
        FlextOracleWmsUtilities,
        FlextOracleWmsUtilities as u,
    )
    from flext_oracle_wms.wms_auth import FlextOracleWmsAuthenticator
    from flext_oracle_wms.wms_client import FlextOracleWmsClient
    from flext_oracle_wms.wms_discovery import FlextOracleWmsEntityDiscovery

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    ("flext_oracle_wms._utilities",),
    {
        "FlextHttpClient": "flext_oracle_wms.http_client",
        "FlextOracleWmsApi": "flext_oracle_wms.api",
        "FlextOracleWmsAuthenticator": "flext_oracle_wms.wms_auth",
        "FlextOracleWmsClient": "flext_oracle_wms.wms_client",
        "FlextOracleWmsClientSettings": "flext_oracle_wms.settings",
        "FlextOracleWmsConstants": "flext_oracle_wms.constants",
        "FlextOracleWmsEntityDiscovery": "flext_oracle_wms.wms_discovery",
        "FlextOracleWmsExceptions": "flext_oracle_wms.errors",
        "FlextOracleWmsFilter": "flext_oracle_wms.filtering",
        "FlextOracleWmsModels": "flext_oracle_wms.models",
        "FlextOracleWmsProtocols": "flext_oracle_wms.protocols",
        "FlextOracleWmsSettings": "flext_oracle_wms.settings",
        "FlextOracleWmsShipmentError": "flext_oracle_wms.errors",
        "FlextOracleWmsTypes": "flext_oracle_wms.typings",
        "FlextOracleWmsUtilities": "flext_oracle_wms.utilities",
        "_utilities": "flext_oracle_wms._utilities",
        "api": "flext_oracle_wms.api",
        "auth": "flext_oracle_wms.auth",
        "c": ("flext_oracle_wms.constants", "FlextOracleWmsConstants"),
        "client": "flext_oracle_wms.client",
        "constants": "flext_oracle_wms.constants",
        "create_flext_http_client": "flext_oracle_wms.http_client",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "discovery": "flext_oracle_wms.discovery",
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "errors": "flext_oracle_wms.errors",
        "filtering": "flext_oracle_wms.filtering",
        "h": ("flext_core.handlers", "FlextHandlers"),
        "http_client": "flext_oracle_wms.http_client",
        "m": ("flext_oracle_wms.models", "FlextOracleWmsModels"),
        "models": "flext_oracle_wms.models",
        "p": ("flext_oracle_wms.protocols", "FlextOracleWmsProtocols"),
        "protocols": "flext_oracle_wms.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "settings": "flext_oracle_wms.settings",
        "t": ("flext_oracle_wms.typings", "FlextOracleWmsTypes"),
        "typings": "flext_oracle_wms.typings",
        "u": ("flext_oracle_wms.utilities", "FlextOracleWmsUtilities"),
        "utilities": "flext_oracle_wms.utilities",
        "wms_api": "flext_oracle_wms.wms_api",
        "wms_auth": "flext_oracle_wms.wms_auth",
        "wms_client": "flext_oracle_wms.wms_client",
        "wms_discovery": "flext_oracle_wms.wms_discovery",
        "wms_exceptions": "flext_oracle_wms.wms_exceptions",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    [
        "__all__",
        "__author__",
        "__author_email__",
        "__description__",
        "__license__",
        "__title__",
        "__url__",
        "__version__",
        "__version_info__",
    ],
)
