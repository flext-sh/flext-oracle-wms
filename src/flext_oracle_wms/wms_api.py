"""Oracle WMS API - Consolidated API Catalog and Mock Server.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Consolidated Oracle WMS API definitions and mock server functionality.
This module combines api_catalog.py + mock_server.py into unified API management.

Features:
- Complete Oracle WMS Cloud API endpoint catalog
- Realistic mock server for testing and development
- Type-safe API definitions with comprehensive validation
- Enterprise integration patterns with FLEXT ecosystem
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from flext_core import FlextResult, get_logger

from flext_oracle_wms.models import (
    FlextOracleWmsApiCategory,
    FlextOracleWmsApiEndpoint,
    FlextOracleWmsApiVersion,
)

logger = get_logger(__name__)


# =============================================================================
# ORACLE WMS CLOUD API CATALOG - Complete API Definitions
# =============================================================================

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
    # === DATA EXTRACT APIS ===
    "lgf_entity_extract": FlextOracleWmsApiEndpoint(
        name="lgf_entity_extract",
        method="GET",
        path="/entity/{entity_name}/",
        version=FlextOracleWmsApiVersion.LGF_V10,
        category=FlextOracleWmsApiCategory.DATA_EXTRACT,
        description="Extract entity data using Oracle WMS LGF v10 API",
        since_version="10.0",
    ),
    "legacy_entity_extract": FlextOracleWmsApiEndpoint(
        name="legacy_entity_extract",
        method="GET",
        path="/extract_data/{entity_name}/",
        version=FlextOracleWmsApiVersion.LEGACY,
        category=FlextOracleWmsApiCategory.DATA_EXTRACT,
        description="Legacy entity data extraction",
        since_version="6.1",
    ),
    # === ENTITY OPERATIONS APIS ===
    "entity_discovery": FlextOracleWmsApiEndpoint(
        name="entity_discovery",
        method="GET",
        path="/entity/",
        version=FlextOracleWmsApiVersion.LGF_V10,
        category=FlextOracleWmsApiCategory.ENTITY_OPERATIONS,
        description="Discover available entities in Oracle WMS",
        since_version="10.0",
    ),
    "entity_metadata": FlextOracleWmsApiEndpoint(
        name="entity_metadata",
        method="GET",
        path="/entity/{entity_name}/metadata/",
        version=FlextOracleWmsApiVersion.LGF_V10,
        category=FlextOracleWmsApiCategory.ENTITY_OPERATIONS,
        description="Get entity metadata and schema information",
        since_version="10.0",
    ),
}


# =============================================================================
# ORACLE WMS MOCK SERVER - Testing and Development Support
# =============================================================================


class OracleWmsMockServer:
    """Mock server simulating Oracle WMS Cloud API v10 responses."""

    def __init__(self, mock_environment: str = "mock_test") -> None:
        """Initialize Oracle WMS mock server."""
        self.environment = mock_environment
        self.mock_data = self._initialize_mock_data()

    def _initialize_mock_data(self) -> dict[str, object]:
        """Initialize realistic mock data based on Oracle WMS documentation."""
        return {
            "entities": [
                "company",
                "facility",
                "item",
                "order_hdr",
                "order_dtl",
                "allocation",
                "inventory",
                "location",
                "wave",
                "shipment",
                "receipt",
                "task",
                "container",
                "lpn",
                "pick_slip",
                "manifest",
            ],
            "company_data": [
                {
                    "company_code": "DEMO_COMPANY",
                    "company_name": "Demo Oracle WMS Company",
                    "status": "Active",
                    "create_date": "2024-01-01T00:00:00Z",
                    "mod_date": "2024-12-01T10:30:00Z",
                    "create_user": "SYSTEM",
                    "mod_user": "ADMIN",
                },
                {
                    "company_code": "TEST_CO",
                    "company_name": "Test Company Ltd",
                    "status": "Active",
                    "create_date": "2024-01-15T08:00:00Z",
                    "mod_date": "2024-11-15T14:20:00Z",
                    "create_user": "SYSTEM",
                    "mod_user": "SETUP_USER",
                },
            ],
            "facility_data": [
                {
                    "facility_code": "DC001",
                    "facility_name": "Distribution Center 001",
                    "company_code": "DEMO_COMPANY",
                    "status": "Active",
                    "address": "123 Warehouse Ave, City, State",
                    "create_date": "2024-01-01T00:00:00Z",
                    "mod_date": "2024-11-01T16:45:00Z",
                    "create_user": "SYSTEM",
                    "mod_user": "FACILITY_ADMIN",
                },
                {
                    "facility_code": "WH002",
                    "facility_name": "Warehouse 002",
                    "company_code": "TEST_CO",
                    "status": "Active",
                    "address": "456 Storage Blvd, Town, Region",
                    "create_date": "2024-02-01T09:30:00Z",
                    "mod_date": "2024-10-15T11:20:00Z",
                    "create_user": "SETUP_USER",
                    "mod_user": "WH_MANAGER",
                },
            ],
            "item_data": [
                {
                    "item_id": "ITEM001",
                    "item_description": "Demo Product 001",
                    "company_code": "DEMO_COMPANY",
                    "item_type": "NORMAL",
                    "status": "Active",
                    "unit_of_measure": "EA",
                    "weight": 1.5,
                    "volume": 0.001,
                    "create_date": "2024-01-01T00:00:00Z",
                    "mod_date": "2024-10-01T12:00:00Z",
                },
                {
                    "item_id": "SKU123",
                    "item_description": "Test SKU 123",
                    "company_code": "TEST_CO",
                    "item_type": "NORMAL",
                    "status": "Active",
                    "unit_of_measure": "PCS",
                    "weight": 0.8,
                    "volume": 0.0005,
                    "create_date": "2024-02-15T08:30:00Z",
                    "mod_date": "2024-09-20T14:15:00Z",
                },
            ],
        }

    def get_mock_response(
        self, endpoint: str, entity_name: str | None = None,
    ) -> FlextResult[dict[str, object]]:
        """Generate mock response for Oracle WMS API endpoint."""
        try:
            if endpoint == "entity_discovery":
                return self._mock_entity_discovery()
            if endpoint == "entity_data" and entity_name:
                return self._mock_entity_data(entity_name)
            if endpoint == "entity_metadata" and entity_name:
                return self._mock_entity_metadata(entity_name)
            return FlextResult.fail(f"Unknown mock endpoint: {endpoint}")
        except Exception as e:
            logger.exception("Mock server error")
            return FlextResult.fail(f"Mock server error: {e}")

    def _mock_entity_discovery(self) -> FlextResult[dict[str, object]]:
        """Mock entity discovery response."""
        entities = [
            {
                "name": entity_name,
                "description": f"Oracle WMS {entity_name} entity",
                "endpoint": f"/entity/{entity_name}/",
                "supports_extract": True,
                "supports_insert": entity_name in {"order_hdr", "order_dtl", "item"},
                "primary_key": self._get_mock_primary_key(entity_name),
            }
            for entity_name in (
                self.mock_data["entities"]
                if isinstance(self.mock_data["entities"], list)
                else []
            )
        ]

        return FlextResult.ok(
            {
                "entities": entities,
                "total_count": len(entities),
                "discovered_at": datetime.now(UTC).isoformat(),
                "api_version": "v10",
                "mock_environment": self.environment,
            },
        )

    def _mock_entity_data(self, entity_name: str) -> FlextResult[dict[str, object]]:
        """Mock entity data response."""
        data_key = f"{entity_name}_data"
        mock_records = self.mock_data.get(data_key, [])

        entities_list = (
            self.mock_data["entities"]
            if isinstance(self.mock_data["entities"], list)
            else []
        )
        if not mock_records and entity_name in entities_list:
            # Generate generic mock data for entities without specific mock data
            mock_records = [
                {
                    "id": str(uuid4())[:8],
                    f"{entity_name}_code": f"MOCK_{entity_name.upper()}_001",
                    f"{entity_name}_name": f"Mock {entity_name.title()} 001",
                    "status": "Active",
                    "create_date": "2024-01-01T00:00:00Z",
                    "mod_date": datetime.now(UTC).isoformat(),
                    "create_user": "MOCK_USER",
                    "mod_user": "MOCK_USER",
                },
            ]

        return FlextResult.ok(
            {
                "results": mock_records,
                "result_count": len(mock_records)
                if hasattr(mock_records, "__len__")
                else 0,
                "page_count": 1,
                "page_nbr": 1,
                "entity_name": entity_name,
                "extracted_at": datetime.now(UTC).isoformat(),
            },
        )

    def _mock_entity_metadata(self, entity_name: str) -> FlextResult[dict[str, object]]:
        """Mock entity metadata response."""
        base_fields = {
            "id": {"type": "string", "description": "Unique identifier"},
            f"{entity_name}_code": {
                "type": "string",
                "description": f"{entity_name} code",
            },
            f"{entity_name}_name": {
                "type": "string",
                "description": f"{entity_name} name",
            },
            "status": {"type": "string", "description": "Status"},
            "create_date": {"type": "datetime", "description": "Creation date"},
            "mod_date": {"type": "datetime", "description": "Modification date"},
            "create_user": {"type": "string", "description": "Created by user"},
            "mod_user": {"type": "string", "description": "Modified by user"},
        }

        # Add entity-specific fields
        entity_specific_fields = self._get_entity_specific_fields(entity_name)
        base_fields.update(entity_specific_fields)

        return FlextResult.ok(
            {
                "entity_name": entity_name,
                "fields": base_fields,
                "primary_key": self._get_mock_primary_key(entity_name),
                "replication_key": "mod_date",
                "supports_incremental": True,
                "description": f"Oracle WMS {entity_name} entity metadata",
            },
        )

    def _get_mock_primary_key(self, entity_name: str) -> str:
        """Get mock primary key for entity."""
        primary_key_map = {
            "company": "company_code",
            "facility": "facility_code",
            "item": "item_id",
            "order_hdr": "order_id",
            "order_dtl": "order_line_id",
            "inventory": "inventory_id",
            "location": "location_id",
        }
        return primary_key_map.get(entity_name, f"{entity_name}_id")

    def _get_entity_specific_fields(
        self, entity_name: str,
    ) -> dict[str, dict[str, str]]:
        """Get entity-specific mock fields."""
        entity_fields = {
            "company": {
                "company_code": {"type": "string", "description": "Company code"},
                "company_name": {"type": "string", "description": "Company name"},
            },
            "facility": {
                "facility_code": {"type": "string", "description": "Facility code"},
                "facility_name": {"type": "string", "description": "Facility name"},
                "company_code": {
                    "type": "string",
                    "description": "Parent company code",
                },
                "address": {"type": "string", "description": "Facility address"},
            },
            "item": {
                "item_id": {"type": "string", "description": "Item identifier"},
                "item_description": {
                    "type": "string",
                    "description": "Item description",
                },
                "item_type": {"type": "string", "description": "Item type"},
                "unit_of_measure": {"type": "string", "description": "Unit of measure"},
                "weight": {"type": "number", "description": "Item weight"},
                "volume": {"type": "number", "description": "Item volume"},
            },
        }
        return entity_fields.get(entity_name, {})


# =============================================================================
# MOCK SERVER FACTORY FUNCTION
# =============================================================================


def get_mock_server(environment: str = "mock_test") -> OracleWmsMockServer:
    """Get Oracle WMS mock server instance."""
    return OracleWmsMockServer(environment)


# =============================================================================
# EXPORTS
# =============================================================================

__all__: list[str] = [
    # API Catalog
    "FLEXT_ORACLE_WMS_APIS",
    "FlextOracleWmsApiCategory",
    "FlextOracleWmsApiEndpoint",
    "FlextOracleWmsApiVersion",
    # Mock Server
    "OracleWmsMockServer",
    "get_mock_server",
]
