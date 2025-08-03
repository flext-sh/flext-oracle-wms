"""Oracle WMS Mock Server - Realistic responses based on Oracle documentation.

This module provides realistic mock responses for Oracle WMS Cloud API v10 (LGF)
based on the official Oracle documentation 25A. Used for testing when real
credentials are not available.

Referência: https://docs.oracle.com/en/cloud/saas/warehouse-management/25a/owmre/
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from flext_core import FlextResult, get_logger

logger = get_logger(__name__)


class OracleWmsMockServer:
    """Mock server simulating Oracle WMS Cloud API v10 responses."""

    def __init__(self, mock_environment: str = "mock_test") -> None:
        """Initialize Oracle WMS mock server."""
        self.environment = mock_environment
        self.mock_data = self._initialize_mock_data()

    def _initialize_mock_data(self) -> dict[str, Any]:
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
                    "mod_date": "2024-12-01T10:30:00Z",
                },
                {
                    "facility_code": "WH002",
                    "facility_name": "Warehouse 002",
                    "company_code": "TEST_CO",
                    "status": "Active",
                    "address": "456 Storage Blvd, City, State",
                    "create_date": "2024-01-15T08:00:00Z",
                    "mod_date": "2024-11-20T16:45:00Z",
                },
            ],
            "inventory_data": [
                {
                    "item_code": "ITEM001",
                    "facility_code": "DC001",
                    "location": "A-01-01",
                    "qty_on_hand": 150.0,
                    "qty_allocated": 25.0,
                    "qty_available": 125.0,
                    "unit_of_measure": "EA",
                    "last_count_date": "2024-12-01T09:00:00Z",
                },
                {
                    "item_code": "ITEM002",
                    "facility_code": "DC001",
                    "location": "B-02-03",
                    "qty_on_hand": 75.0,
                    "qty_allocated": 10.0,
                    "qty_available": 65.0,
                    "unit_of_measure": "EA",
                    "last_count_date": "2024-11-28T14:30:00Z",
                },
            ],
        }

    def mock_health_check(self) -> dict[str, Any]:
        """Mock health check response."""
        return {
            "service": "FlextOracleWmsClient",
            "status": "healthy",
            "base_url": f"https://mock.wms.oracle.com/{self.environment}",
            "environment": self.environment,
            "api_version": "v10",
            "test_call_success": True,
            "available_apis": 22,
            "discovered_entities": len(self.mock_data["entities"]),
            "mock_mode": True,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    def mock_entity_discovery(self) -> dict[str, Any]:
        """Mock entity discovery response following Oracle LGF v10 format."""
        return {
            "count": len(self.mock_data["entities"]),
            "results": [
                {"name": entity, "type": "entity", "status": "available"}
                for entity in self.mock_data["entities"]
            ],
            "page_number": 1,
            "page_count": 1,
            "next_page": None,
            "previous_page": None,
        }

    def mock_entity_data(self, entity_name: str, limit: int = 10) -> dict[str, Any]:
        """Mock entity data response following Oracle LGF v10 pagination format."""
        if entity_name == "company":
            data = self.mock_data["company_data"][:limit]
        elif entity_name == "facility":
            data = self.mock_data["facility_data"][:limit]
        elif entity_name == "inventory":
            data = self.mock_data["inventory_data"][:limit]
        else:
            # Generic mock data for other entities
            data = [
                {
                    "id": f"{entity_name.upper()}_{i:03d}",
                    "name": f"Mock {entity_name.title()} {i}",
                    "status": "Active",
                    "create_date": "2024-01-01T00:00:00Z",
                    "mod_date": "2024-12-01T10:30:00Z",
                }
                for i in range(1, min(limit + 1, 6))
            ]

        return {
            "count": len(data),
            "results": data,
            "page_number": 1,
            "page_count": 1,
            "next_page": None,
            "previous_page": None,
            "entity_type": entity_name,
            "extracted_at": datetime.now(UTC).isoformat(),
        }

    def mock_async_task_status(self, task_id: str | None = None) -> dict[str, Any]:
        """Mock async task status response following Oracle 25A format."""
        mock_task_id = task_id or str(uuid4())

        return {
            "task_id": mock_task_id,
            "status": "COMPLETED",
            "progress": 100,
            "total_records": 250,
            "processed_records": 250,
            "failed_records": 0,
            "start_time": "2024-12-01T10:00:00Z",
            "end_time": "2024-12-01T10:02:30Z",
            "duration_seconds": 150,
            "output_location": f"https://objectstore.oracle.com/exports/{mock_task_id}.json",
            "format": "JSON",
        }

    def mock_data_extract_response(self) -> dict[str, Any]:
        """Mock data extract to object store response (Oracle 25A feature)."""
        task_id = str(uuid4())

        return {
            "task_id": task_id,
            "status": "SUBMITTED",
            "message": "Data extraction task submitted successfully",
            "estimated_completion": "2024-12-01T10:05:00Z",
            "status_check_url": f"/lgfapi/v10/data_extract/export_async_status?task_id={task_id}",
        }

    def get_mock_response(
        self,
        api_name: str,
        **kwargs: object,
    ) -> FlextResult[dict[str, object]]:
        """Get mock response for specified API."""
        try:
            if api_name == "health_check":
                return FlextResult.ok(self.mock_health_check())
            if api_name == "discover_entities":
                return FlextResult.ok(self.mock_entity_discovery())
            if api_name == "get_entity_data":
                entity_name = str(kwargs.get("entity_name", "company"))
                limit_value = kwargs.get("limit", 10)
                limit = int(limit_value) if isinstance(limit_value, (int, str)) else 10
                return FlextResult.ok(self.mock_entity_data(entity_name, limit))
            if api_name == "lgf_async_task_status":
                task_id = (
                    str(kwargs.get("task_id"))
                    if kwargs.get("task_id") is not None
                    else None
                )
                return FlextResult.ok(self.mock_async_task_status(task_id))
            if api_name == "lgf_data_extract":
                return FlextResult.ok(self.mock_data_extract_response())
            return FlextResult.fail(f"Mock not implemented for API: {api_name}")

        except Exception as e:
            logger.exception(f"Mock response generation failed for {api_name}: {e}")
            return FlextResult.fail(f"Mock error: {e}")


# Global mock server instance
_mock_server: OracleWmsMockServer | None = None


def get_mock_server(environment: str = "mock_test") -> OracleWmsMockServer:
    """Get global mock server instance."""
    global _mock_server
    if _mock_server is None:
        _mock_server = OracleWmsMockServer(environment)
    return _mock_server


def enable_mock_mode() -> None:
    """Enable mock mode for Oracle WMS client."""
    logger.info("Oracle WMS Mock Mode enabled - using realistic mock responses")


def disable_mock_mode() -> None:
    """Disable mock mode for Oracle WMS client."""
    logger.info("Oracle WMS Mock Mode disabled - using real API calls")
