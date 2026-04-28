# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Oracle Wms package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_api import d, e, h, r, s, x

    from flext_oracle_wms.__version__ import (
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_oracle_wms._utilities.auth import FlextOracleWmsUtilitiesAuth
    from flext_oracle_wms._utilities.client import FlextOracleWmsUtilitiesClient
    from flext_oracle_wms._utilities.discovery import FlextOracleWmsUtilitiesDiscovery
    from flext_oracle_wms._utilities.filtering import FlextOracleWmsUtilitiesFiltering
    from flext_oracle_wms._utilities.http_client import (
        FlextOracleWmsUtilitiesHttpClient,
    )
    from flext_oracle_wms.api import FlextOracleWmsApi, oracle_wms
    from flext_oracle_wms.client_settings import FlextOracleWmsClientSettings
    from flext_oracle_wms.constants import FlextOracleWmsConstants, c
    from flext_oracle_wms.errors import (
        FlextOracleWmsApiError,
        FlextOracleWmsAuthenticationError,
        FlextOracleWmsConfigurationError,
        FlextOracleWmsConnectionError,
        FlextOracleWmsEntityNotFoundError,
        FlextOracleWmsError,
        FlextOracleWmsValidationError,
    )
    from flext_oracle_wms.models import FlextOracleWmsModels, m
    from flext_oracle_wms.protocols import FlextOracleWmsProtocols, p
    from flext_oracle_wms.settings import FlextOracleWmsSettings
    from flext_oracle_wms.typings import FlextOracleWmsTypes, t
    from flext_oracle_wms.utilities import FlextOracleWmsUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    ("._utilities",),
    build_lazy_import_map(
        {
            ".__version__": (
                "__author__",
                "__author_email__",
                "__description__",
                "__license__",
                "__title__",
                "__url__",
                "__version__",
                "__version_info__",
            ),
            "._utilities.auth": ("FlextOracleWmsUtilitiesAuth",),
            "._utilities.client": ("FlextOracleWmsUtilitiesClient",),
            "._utilities.discovery": ("FlextOracleWmsUtilitiesDiscovery",),
            "._utilities.filtering": ("FlextOracleWmsUtilitiesFiltering",),
            "._utilities.http_client": ("FlextOracleWmsUtilitiesHttpClient",),
            ".api": (
                "FlextOracleWmsApi",
                "oracle_wms",
            ),
            ".client_settings": ("FlextOracleWmsClientSettings",),
            ".constants": (
                "FlextOracleWmsConstants",
                "c",
            ),
            ".errors": (
                "FlextOracleWmsApiError",
                "FlextOracleWmsAuthenticationError",
                "FlextOracleWmsConfigurationError",
                "FlextOracleWmsConnectionError",
                "FlextOracleWmsEntityNotFoundError",
                "FlextOracleWmsError",
                "FlextOracleWmsValidationError",
            ),
            ".models": (
                "FlextOracleWmsModels",
                "m",
            ),
            ".protocols": (
                "FlextOracleWmsProtocols",
                "p",
            ),
            ".settings": ("FlextOracleWmsSettings",),
            ".typings": (
                "FlextOracleWmsTypes",
                "t",
            ),
            ".utilities": (
                "FlextOracleWmsUtilities",
                "u",
            ),
            "flext_api": (
                "d",
                "e",
                "h",
                "r",
                "s",
                "x",
            ),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "FlextOracleWmsApi",
    "FlextOracleWmsApiError",
    "FlextOracleWmsAuthenticationError",
    "FlextOracleWmsClientSettings",
    "FlextOracleWmsConfigurationError",
    "FlextOracleWmsConnectionError",
    "FlextOracleWmsConstants",
    "FlextOracleWmsEntityNotFoundError",
    "FlextOracleWmsError",
    "FlextOracleWmsModels",
    "FlextOracleWmsProtocols",
    "FlextOracleWmsSettings",
    "FlextOracleWmsTypes",
    "FlextOracleWmsUtilities",
    "FlextOracleWmsUtilitiesAuth",
    "FlextOracleWmsUtilitiesClient",
    "FlextOracleWmsUtilitiesDiscovery",
    "FlextOracleWmsUtilitiesFiltering",
    "FlextOracleWmsUtilitiesHttpClient",
    "FlextOracleWmsValidationError",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "d",
    "e",
    "h",
    "m",
    "oracle_wms",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
]
