"""Oracle WMS Cloud API Catalog - Declarative API Definitions.

Comprehensive catalog of Oracle WMS Cloud APIs based on official 25B documentation.
Provides declarative endpoint definitions with categorization, versioning, and
comprehensive metadata for enterprise Oracle WMS integration.

Key Features:
    - Complete API endpoint catalog with official Oracle WMS Cloud paths
    - Categorized APIs (Setup, Automation, Data Extract, Entity Operations)
    - Version-aware endpoint management (Legacy and LGF v10)
    - Type-safe API definitions with comprehensive validation
    - Enterprise integration patterns with FLEXT ecosystem

Architecture:
    Built on FLEXT ValueObject patterns with comprehensive domain validation:
    - FlextOracleWmsApiEndpoint: Individual API definitions with metadata
    - FlextOracleWmsApiCategory: Logical grouping of related operations
    - FlextOracleWmsApiVersion: Version management for API evolution
    - Declarative catalog supporting dynamic API discovery

Reference:
    Oracle WMS Cloud REST API Documentation
    https://docs.oracle.com/en/cloud/saas/warehouse-management/25b/owmre/index.html

Author: FLEXT Development Team
Version: 0.9.0
License: MIT
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from flext_core import FlextResult, FlextValueObject


class FlextOracleWmsApiVersion(StrEnum):
    """Oracle WMS API versions."""

    LEGACY = "legacy"  # /wms/api/
    LGF_V10 = "v10"  # /wms/lgfapi/v10/


class FlextOracleWmsApiCategory(StrEnum):
    """Oracle WMS API categories from official documentation."""

    SETUP_TRANSACTIONAL = "setup_transactional"
    AUTOMATION_OPERATIONS = "automation_operations"
    DATA_EXTRACT = "data_extract"
    ENTITY_OPERATIONS = "entity_operations"


@dataclass(frozen=True)
class FlextOracleWmsApiEndpoint(FlextValueObject):
    """Declarative API endpoint definition."""

    name: str
    method: str
    path: str
    version: FlextOracleWmsApiVersion
    category: FlextOracleWmsApiCategory
    description: str
    since_version: str = "6.1"

    def get_full_path(self, environment: str) -> str:
        """Get full API path with environment."""
        if self.version == FlextOracleWmsApiVersion.LGF_V10:
            return f"/{environment}/wms/lgfapi/v10{self.path}"
        return f"/{environment}/wms/api{self.path}"

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate Oracle WMS API endpoint business rules."""
        validation_errors = []

        if not self.name:
            validation_errors.append("API name cannot be empty")
        if not self.method:
            validation_errors.append("HTTP method cannot be empty")
        if not self.path:
            validation_errors.append("API path cannot be empty")
        if self.method not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
            validation_errors.append(f"Invalid HTTP method: {self.method}")
        if not self.path.startswith("/"):
            validation_errors.append("API path must start with /")
        if not self.description:
            validation_errors.append("API description cannot be empty")

        if validation_errors:
            return FlextResult.fail("; ".join(validation_errors))
        return FlextResult.ok(None)


# ==============================================================================
# ORACLE WMS CLOUD API CATALOG - ALL 25+ APIS FROM DOCUMENTATION
# ==============================================================================

FLEXT_ORACLE_WMS_APIS = {
    # === SETUP AND TRANSACTIONAL DATA APIS ===
    "lgf_init_stage_interface": FlextOracleWmsApiEndpoint(
        name="lgf_init_stage_interface",
        method="POST",
        path="/init_stage_interface/{entity_name}/",
        version=FlextOracleWmsApiVersion.LGF_V10,
        category=FlextOracleWmsApiCategory.SETUP_TRANSACTIONAL,
        description="Main API for input data integration. "
        "Pass data in to validate and process (Oracle v10 LGF API)",
        since_version="10.0",
    ),
    "run_stage_interface": FlextOracleWmsApiEndpoint(
        name="run_stage_interface",
        method="POST",
        path="/run_stage_interface/",
        version=FlextOracleWmsApiVersion.LEGACY,
        category=FlextOracleWmsApiCategory.SETUP_TRANSACTIONAL,
        description="Trigger validation & processing of data already in stage tables",
        since_version="6.1",
    ),
    "update_output_interface": FlextOracleWmsApiEndpoint(
        name="update_output_interface",
        method="POST",
        path="/update_output_interface/",
        version=FlextOracleWmsApiVersion.LEGACY,
        category=FlextOracleWmsApiCategory.SETUP_TRANSACTIONAL,
        description=(
            "Set status and error message if any on a transmitted output interface"
        ),
        since_version="8.0.0",
    ),
    # === AUTOMATION & OPERATIONS APIS ===
    "update_oblpn_tracking_number": FlextOracleWmsApiEndpoint(
        name="update_oblpn_tracking_number",
        method="POST",
        path="/update_oblpn_tracking_nbr/",
        version=FlextOracleWmsApiVersion.LEGACY,
        category=FlextOracleWmsApiCategory.AUTOMATION_OPERATIONS,
        description="Update tracking number and other OBLPN parcel stats",
        since_version="6.1",
    ),
    "update_oblpn_dimensions": FlextOracleWmsApiEndpoint(
        name="update_oblpn_dimensions",
        method="POST",
        path="/update_oblpn_dims/",
        version=FlextOracleWmsApiVersion.LEGACY,
        category=FlextOracleWmsApiCategory.AUTOMATION_OPERATIONS,
        description="Update OBLPN weight, volume etc",
        since_version="6.2",
    ),
    "ship_oblpn": FlextOracleWmsApiEndpoint(
        name="ship_oblpn",
        method="POST",
        path="/ship_oblpn/",
        version=FlextOracleWmsApiVersion.LEGACY,
        category=FlextOracleWmsApiCategory.AUTOMATION_OPERATIONS,
        description="Ship an eligible OBLPN in WMS",
        since_version="6.2",
    ),
    "get_next_number": FlextOracleWmsApiEndpoint(
        name="get_next_number",
        method="GET",
        path="/get_next_numbers/",
        version=FlextOracleWmsApiVersion.LEGACY,
        category=FlextOracleWmsApiCategory.AUTOMATION_OPERATIONS,
        description="Get next number from specified counter",
        since_version="7.0.0",
    ),
    "get_status": FlextOracleWmsApiEndpoint(
        name="get_status",
        method="GET",
        path="/get_status/",
        version=FlextOracleWmsApiVersion.LEGACY,
        category=FlextOracleWmsApiCategory.AUTOMATION_OPERATIONS,
        description="Get status of an entity",
        since_version="7.0.0",
    ),
    "assign_oblpn_to_load": FlextOracleWmsApiEndpoint(
        name="assign_oblpn_to_load",
        method="POST",
        path="/assign_oblpn_to_load/",
        version=FlextOracleWmsApiVersion.LEGACY,
        category=FlextOracleWmsApiCategory.AUTOMATION_OPERATIONS,
        description="Assign OBLPN(s) to a new or existing Load",
        since_version="7.0.0",
    ),
    "create_lpn": FlextOracleWmsApiEndpoint(
        name="create_lpn",
        method="POST",
        path="/create_lpn/",
        version=FlextOracleWmsApiVersion.LEGACY,
        category=FlextOracleWmsApiCategory.AUTOMATION_OPERATIONS,
        description="Create a single SKU IBLPN and associated inventory",
        since_version="7.0.1",
    ),
    "receive_lpn": FlextOracleWmsApiEndpoint(
        name="receive_lpn",
        method="POST",
        path="/receive_lpn/",
        version=FlextOracleWmsApiVersion.LEGACY,
        category=FlextOracleWmsApiCategory.AUTOMATION_OPERATIONS,
        description="Receive and optionally xdock an IBLPN",
        since_version="7.0.1",
    ),
    # === ENTITY OPERATIONS APIS ===
    "extended_property": FlextOracleWmsApiEndpoint(
        name="extended_property",
        method="GET",
        path="/extended_property/{entity_name}/{key}/{extended_property}",
        version=FlextOracleWmsApiVersion.LEGACY,
        category=FlextOracleWmsApiCategory.ENTITY_OPERATIONS,
        description="Fetch an extended property for the requested entity",
        since_version="8.0.1",
    ),
    "entity_update": FlextOracleWmsApiEndpoint(
        name="entity_update",
        method="PATCH",
        path="/entity/{entity_name}/{key}/{sequence_number}/",
        version=FlextOracleWmsApiVersion.LEGACY,
        category=FlextOracleWmsApiCategory.ENTITY_OPERATIONS,
        description="Updates certain attributes of an entity",
        since_version="8.0.2",
    ),
    "object_inquiry": FlextOracleWmsApiEndpoint(
        name="object_inquiry",
        method="GET",
        path="/entity/{entity_name}/{key}/",
        version=FlextOracleWmsApiVersion.LEGACY,
        category=FlextOracleWmsApiCategory.ENTITY_OPERATIONS,
        description="Returns a standardized representation of the queried object",
        since_version="8.0.2",
    ),
    # === LGF API V10 - DATA EXTRACTION & ENTITIES ===
    "lgf_entity_list": FlextOracleWmsApiEndpoint(
        name="lgf_entity_list",
        method="GET",
        path="/entity/{entity_name}/",
        version=FlextOracleWmsApiVersion.LGF_V10,
        category=FlextOracleWmsApiCategory.DATA_EXTRACT,
        description="Get entity data with pagination and filtering",
        since_version="10.0",
    ),
    "lgf_entity_discovery": FlextOracleWmsApiEndpoint(
        name="lgf_entity_discovery",
        method="GET",
        path="/entity/",
        version=FlextOracleWmsApiVersion.LGF_V10,
        category=FlextOracleWmsApiCategory.DATA_EXTRACT,
        description="Discover all available entities in Oracle WMS",
        since_version="10.0",
    ),
    "lgf_entity_get": FlextOracleWmsApiEndpoint(
        name="lgf_entity_get",
        method="GET",
        path="/entity/{entity_name}/{id}/",
        version=FlextOracleWmsApiVersion.LGF_V10,
        category=FlextOracleWmsApiCategory.DATA_EXTRACT,
        description="Get specific entity record by ID",
        since_version="10.0",
    ),
    "lgf_data_extract": FlextOracleWmsApiEndpoint(
        name="lgf_data_extract",
        method="POST",
        path="/data_extract/push_to_object_store/",
        version=FlextOracleWmsApiVersion.LGF_V10,
        category=FlextOracleWmsApiCategory.DATA_EXTRACT,
        description="Extract data to cloud object store",
        since_version="25A",
    ),
    "lgf_async_task_status": FlextOracleWmsApiEndpoint(
        name="lgf_async_task_status",
        method="GET",
        path="/data_extract/export_async_status/",
        version=FlextOracleWmsApiVersion.LGF_V10,
        category=FlextOracleWmsApiCategory.DATA_EXTRACT,
        description="Check aggregated async task status",
        since_version="25A",
    ),
    # === ORACLE 2025 ADDITIONAL ENDPOINTS FROM LATEST DOCUMENTATION ===
    "lgf_async_task_entity": FlextOracleWmsApiEndpoint(
        name="lgf_async_task_entity",
        method="GET",
        path="/entity/lgf_async_task/{id}/",
        version=FlextOracleWmsApiVersion.LGF_V10,
        category=FlextOracleWmsApiCategory.ENTITY_OPERATIONS,
        description="Get specific async task entity by ID (Oracle 2025 documentation)",
        since_version="25A",
    ),
    "lgf_async_task_head": FlextOracleWmsApiEndpoint(
        name="lgf_async_task_head",
        method="HEAD",
        path="/entity/lgf_async_task/{id}/",
        version=FlextOracleWmsApiVersion.LGF_V10,
        category=FlextOracleWmsApiCategory.ENTITY_OPERATIONS,
        description="Check async task entity existence (Oracle 2025 documentation)",
        since_version="25A",
    ),
    "lgf_async_task_list": FlextOracleWmsApiEndpoint(
        name="lgf_async_task_list",
        method="GET",
        path="/entity/lgf_async_task/",
        version=FlextOracleWmsApiVersion.LGF_V10,
        category=FlextOracleWmsApiCategory.ENTITY_OPERATIONS,
        description="List all async task entities (Oracle 2025 documentation)",
        since_version="25A",
    ),
}
