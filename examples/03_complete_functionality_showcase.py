"""Complete Oracle WMS Functionality Showcase - ALL Features Demonstrated.

This example demonstrates EVERY major functionality of the flext-oracle-wms library
as specifically requested by the user: "FOQUE MUITO NOS EXEMPLES/ PARA FUNCIONAR
COM TODA A FUNCIONALIDADE DO CODIGO"

Features Demonstrated:
    1. Client Configuration and Initialization
    2. Entity Discovery (320+ entities)
    3. Data Retrieval and Querying
    4. Authentication Methods
    5. API Catalog Management
    6. Error Handling and Recovery
    7. Health Monitoring
    8. Performance Tracking
    9. Cache Management
    10. Enterprise Features

Usage:
    python examples/03_complete_functionality_showcase.py

Requirements:
    - .env file with Oracle WMS credentials
    - Network connectivity to Oracle WMS Cloud
    - All FLEXT dependencies installed
"""

from __future__ import annotations

import os
import time
import traceback
from collections.abc import Sequence
from pathlib import Path

from dotenv import load_dotenv
from flext_core import FlextLogger, r

from flext_oracle_wms.constants import FlextOracleWmsConstants as c
from flext_oracle_wms.models import FlextOracleWmsModels as m
from flext_oracle_wms.settings import FlextOracleWmsClientSettings
from flext_oracle_wms.typings import FlextOracleWmsTypes as t
from flext_oracle_wms.wms_api import FlextOracleWmsApi
from flext_oracle_wms.wms_auth import FlextOracleWmsAuthenticator
from flext_oracle_wms.wms_client import FlextOracleWmsClient
from flext_oracle_wms.wms_exceptions import FlextOracleWmsError

logger = FlextLogger(__name__)


def load_config_from_environment() -> FlextOracleWmsClientSettings:
    """Load configuration from .env file."""
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)
    base_url = os.getenv("ORACLE_WMS_BASE_URL")
    username = os.getenv("ORACLE_WMS_USERNAME")
    password = os.getenv("ORACLE_WMS_PASSWORD")
    if not all([base_url, username, password]):
        msg = "Missing required environment variables: ORACLE_WMS_BASE_URL, ORACLE_WMS_USERNAME, ORACLE_WMS_PASSWORD"
        raise ValueError(msg)
    if base_url is None or username is None or password is None:
        msg = "Required environment variables cannot be None"
        raise ValueError(msg)
    return FlextOracleWmsClientSettings.model_validate({
        "base_url": base_url,
        "username": username,
        "password": password,
        "api_version": "LGF_V10",
        "timeout": c.OracleWms.DEFAULT_TIMEOUT,
        "max_retries": c.OracleWms.DEFAULT_MAX_RETRIES,
        "verify_ssl": True,
        "enable_logging": True,
    })


def showcase_1_client_initialization(
    config: FlextOracleWmsClientSettings,
) -> FlextOracleWmsClient:
    """Feature 1: Client Configuration and Initialization."""
    client = FlextOracleWmsClient(config)
    start_result = client.start()
    if start_result.is_success:
        pass
    else:
        msg = f"Failed to start client: {start_result.error}"
        raise FlextOracleWmsError(msg)
    return client


def showcase_2_entity_discovery(client: FlextOracleWmsClient) -> list[str]:
    """Feature 2: Entity Discovery (320+ entities)."""
    entities_result = client.discover_entities()
    if not entities_result.is_success:
        return []
    entity_dicts = entities_result.value or []
    entities: list[str] = [
        str(entity.get("name", "Unknown")) if isinstance(entity, dict) else str(entity)
        for entity in entity_dicts
    ]
    batch_size_val = c.OracleWms.PROCESSING_CONFIG.get("default_batch_size", 100)
    max_entities_to_show = (
        int(batch_size_val) // 5 if isinstance(batch_size_val, int) else 20
    )
    for _i, _entity in enumerate(entities[:max_entities_to_show]):
        pass
    if len(entities) > max_entities_to_show:
        pass
    sample_entities = {
        "Core Entities": ["company", "facility", "item", "location"],
        "Inventory": ["inventory", "inventory_status", "inventory_txn"],
        "Orders": ["order_hdr", "order_dtl", "order_status"],
        "Warehouse": ["wave", "task", "work_order", "work_assignment"],
        "Shipping": ["shipment", "container", "manifest", "carrier"],
    }
    for category_entities in sample_entities.values():
        available = [e_name for e_name in category_entities if e_name in entities]
        if available:
            pass
    return entities


def showcase_3_data_retrieval(
    client: FlextOracleWmsClient,
    entities: list[str],
) -> dict[str, t.ContainerValue]:
    """Feature 3: Data Retrieval and Querying."""
    sample_data: dict[str, t.ContainerValue] = {}
    test_entities = ["company", "facility", "item"]
    for entity_name in test_entities:
        if entity_name not in entities:
            continue
        data_result = client.get_entity_data(entity_name, limit=5)
        if data_result.is_success:
            data = data_result.value
            if isinstance(data, list) and data:
                first_record = data[0]
                if isinstance(first_record, dict):
                    len(first_record)
                sample_data[entity_name] = str(len(data))
    if "company" in sample_data:
        filtered_result = client.get_entity_data(
            entity_name="company",
            limit=3,
            filters={"active": "Y"},
        )
        if filtered_result.is_success:
            pass
    return sample_data


def showcase_4_authentication(config: FlextOracleWmsClientSettings) -> None:
    """Feature 4: Authentication Methods."""
    auth_config = m.OracleWms.AuthSettings(
        method=c.OracleWms.OracleWMSAuthMethod.BASIC,
        username=getattr(config, "username", "invalid"),
        password=getattr(config, "password", "invalid"),
    )
    validation_result = auth_config.validate_business_rules()
    if validation_result.is_success:
        pass
    authenticator = FlextOracleWmsAuthenticator(auth_config)
    headers_result = authenticator.get_auth_headers()
    if hasattr(headers_result, "is_success") and headers_result.is_success:
        pass
    for _method in c.OracleWms.OracleWMSAuthMethod.__members__.values():
        pass


def showcase_5_api_catalog(client: FlextOracleWmsClient) -> None:
    """Feature 5: API Catalog Management."""
    categories: dict[str, list[str]] = {}
    for api_name, api_info in FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS.items():
        category = api_info.category
        if category not in categories:
            categories[category] = []
        categories[category].append(api_name)
    for apis in categories.values():
        max_apis_to_show = c.OracleWms.DEFAULT_MAX_RETRIES
        for _api in apis[:max_apis_to_show]:
            pass
        if len(apis) > max_apis_to_show:
            pass
    {api.version for api in FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS.values()}
    for category in c.OracleWms.WmsApiCategory.__members__.values():
        category_apis = client.get_apis_by_category(category)
        if category_apis:
            pass


def showcase_6_error_handling(client: FlextOracleWmsClient) -> None:
    """Feature 6: Error Handling and Recovery."""
    invalid_result = client.get_entity_data("invalid_entity_xyz123")
    if not invalid_result.is_success:
        pass
    api_result = client.call_api("non_existent_api_xyz")
    if not api_result.is_success:
        pass
    try:
        invalid_config = FlextOracleWmsClientSettings.model_validate({
            "base_url": "invalid-url",
            "username": "",
            "password": "",
            "api_version": "LGF_V10",
            "timeout": 30,
            "max_retries": 3,
            "verify_ssl": True,
            "enable_logging": True,
        })
        validation = invalid_config.validate_config()
        if not validation.is_success:
            logger.info(f"Expected validation failure: {validation.error}")
    except Exception as exc:
        logger.warning("Error handling demonstration: %s", str(exc))


def showcase_7_health_monitoring(
    client: FlextOracleWmsClient,
) -> dict[str, t.ContainerValue]:
    """Feature 7: Health Monitoring."""
    health_result = client.health_check()
    if health_result.is_success:
        response = health_result.value
        health_data: dict[str, t.ContainerValue] = {"status_code": response.status_code}
        return health_data
    return {}


def showcase_8_performance_tracking(
    client: FlextOracleWmsClient,
    entities: list[str],
) -> None:
    """Feature 8: Performance Tracking."""
    min_entities_for_concurrent_test = c.OracleWms.DEFAULT_MAX_RETRIES
    if len(entities) >= min_entities_for_concurrent_test:
        test_entities = entities[:min_entities_for_concurrent_test]
        start_time = time.time()
        results: list[r[Sequence[t.StrMapping]]] = []
        for entity in test_entities:
            result = client.get_entity_data(entity, limit=2)
            results.append(result)
        end_time = time.time()
        end_time - start_time
        successful_requests = sum(
            1
            for result in results
            if hasattr(result, "is_success") and result.is_success
        )
        if successful_requests > 0:
            pass
    if "company" in entities:
        page_sizes = [1, 5, 10]
        for page_size in page_sizes:
            start_time = time.time()
            result = client.get_entity_data("company", limit=page_size)
            end_time = time.time()
            if result.is_success:
                pass


def showcase_9_cache_management(client: FlextOracleWmsClient) -> None:
    """Feature 9: Cache Management."""
    start_time = time.time()
    first_result = client.discover_entities()
    first_time = time.time() - start_time
    start_time = time.time()
    second_result = client.discover_entities()
    second_time = time.time() - start_time
    if first_result.is_success and second_result.is_success:
        first_count = len(first_result.value or [])
        second_count = len(second_result.value or [])
        if second_time < first_time:
            pass
        if first_count == second_count:
            pass


def showcase_10_enterprise_features(
    _client: FlextOracleWmsClient,
    config: FlextOracleWmsClientSettings,
) -> None:
    """Feature 10: Enterprise Features."""


def main() -> int:
    """Main showcase execution."""
    try:
        config = load_config_from_environment()
        client = showcase_1_client_initialization(config)
        entities = showcase_2_entity_discovery(client)
        showcase_3_data_retrieval(client, entities)
        showcase_4_authentication(config)
        showcase_5_api_catalog(client)
        showcase_6_error_handling(client)
        showcase_7_health_monitoring(client)
        showcase_8_performance_tracking(client, entities)
        showcase_9_cache_management(client)
        showcase_10_enterprise_features(client, config)
        client.stop()
    except (RuntimeError, OSError, ValueError):
        traceback.print_exc()
        return 1
    return 0


if __name__ == "__main__":
    main()
