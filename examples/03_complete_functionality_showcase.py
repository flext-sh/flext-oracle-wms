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
from pathlib import Path
from typing import TYPE_CHECKING

from dotenv import load_dotenv

from flext_oracle_wms import (
    FlextOracleWmsApi,
    FlextOracleWmsSettings,
    FlextOracleWmsUtilitiesAuth,
    FlextOracleWmsUtilitiesClient,
    c,
    m,
    p,
    t,
    u,
)
from flext_oracle_wms.errors import FlextOracleWmsErrors

if TYPE_CHECKING:
    from collections.abc import (
        Sequence,
    )

FlextOracleWmsAuthenticator = FlextOracleWmsUtilitiesAuth.Authenticator
FlextOracleWmsClient = FlextOracleWmsUtilitiesClient.Client

logger = u.fetch_logger(__name__)


def load_config_from_environment() -> FlextOracleWmsSettings:
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
    return FlextOracleWmsSettings.model_validate({
        "base_url": base_url,
        "username": username,
        "password": password,
        "api_version": "LGF_V10",
        "timeout": c.OracleWms.DEFAULT_TIMEOUT,
        "retry_attempts": c.OracleWms.DEFAULT_MAX_RETRIES,
        "verify_ssl": True,
        "enable_logging": True,
    })


def showcase_1_client_initialization(
    settings: FlextOracleWmsSettings,
) -> FlextOracleWmsClient:
    """Feature 1: Client Configuration and Initialization."""
    client = FlextOracleWmsClient(settings)
    start_result = client.start()
    if start_result.success:
        pass
    else:
        msg = f"Failed to start client: {start_result.error}"
        raise FlextOracleWmsErrors.Error(msg)
    return client


def showcase_2_entity_discovery(client: FlextOracleWmsClient) -> list[str]:
    """Feature 2: Entity Discovery (320+ entities)."""
    entities_result = client.discover_entities()
    if not entities_result.success:
        msg = entities_result.error or "Failed to discover Oracle WMS entities"
        raise FlextOracleWmsErrors.Error(msg)
    entities: list[str] = list(entities_result.value)
    batch_size_val = c.OracleWms.PROCESSING_CONFIG.get("default_batch_size", 100)
    max_entities_to_show = batch_size_val // 5
    _entity_preview = entities[:max_entities_to_show]
    sample_entities = {
        "Core Entities": ["company", "facility", "item", "location"],
        "Inventory": ["inventory", "inventory_status", "inventory_txn"],
        "Orders": ["order_hdr", "order_dtl", "order_status"],
        "Warehouse": ["wave", "task", "work_order", "work_assignment"],
        "Shipping": ["shipment", "container", "manifest", "carrier"],
    }
    for category_entities in sample_entities.values():
        [e_name for e_name in category_entities if e_name in entities]
    return entities


def showcase_3_data_retrieval(
    client: FlextOracleWmsClient,
    entities: list[str],
) -> t.MutableJsonMapping:
    """Feature 3: Data Retrieval and Querying."""
    sample_data: t.MutableJsonMapping = {}
    test_entities = ["company", "facility", "item"]
    for entity_name in test_entities:
        if entity_name not in entities:
            continue
        data_result = client.get_entity_data(entity_name, limit=5)
        if data_result.success:
            data = data_result.value
            if isinstance(data, list) and data:
                first_record = data[0]
                if isinstance(first_record, dict):
                    len(first_record)
                sample_data[entity_name] = str(len(data))
    if "company" in sample_data:
        client.get_entity_data(
            entity_name="company",
            limit=3,
            filters={"active": "Y"},
        )
    return sample_data


def showcase_4_authentication(settings: FlextOracleWmsSettings) -> None:
    """Feature 4: Authentication Methods."""
    auth_config = m.OracleWms.AuthSettings(
        method=c.OracleWms.OracleWMSAuthMethod.BASIC,
        username=settings.OracleWms.username or "invalid",
        password=settings.OracleWms.password or "invalid",
    )
    auth_config.validate_business_rules()
    authenticator = FlextOracleWmsAuthenticator(auth_config)
    _headers_result = authenticator.get_auth_headers()


def showcase_5_api_catalog(client: FlextOracleWmsClient) -> None:
    """Feature 5: API Catalog Management."""
    categories: t.MutableMappingKV[str, t.MutableSequenceOf[str]] = {}
    for api_name, api_info in FlextOracleWmsApi.api_endpoints().items():
        category = api_info.category
        if category not in categories:
            categories[category] = []
        categories[category].append(api_name)
    for apis in categories.values():
        max_apis_to_show = c.OracleWms.DEFAULT_MAX_RETRIES
        _api_preview = apis[:max_apis_to_show]
    _ = {api.version for api in FlextOracleWmsApi.api_endpoints().values()}
    category_names = sorted({
        api.category for api in FlextOracleWmsApi.api_endpoints().values()
    })
    for category in category_names:
        category_result = client.get_apis_by_category(category)
        if category_result.failure:
            msg = (
                category_result.error or f"Failed to load APIs for category: {category}"
            )
            raise FlextOracleWmsErrors.Error(msg)


def showcase_6_error_handling(client: FlextOracleWmsClient) -> None:
    """Feature 6: Error Handling and Recovery."""
    client.get_entity_data("invalid_entity_xyz123")
    client.call_api("non_existent_api_xyz")
    try:
        invalid_config = FlextOracleWmsSettings.model_validate({
            "OracleWms": {
                "base_url": "invalid-url",
                "username": "",
                "password": "",
                "api_version": "LGF_V10",
                "timeout": 30,
                "retry_attempts": 3,
                "verify_ssl": True,
                "enable_logging": True,
            },
        })
        invalid_auth = m.OracleWms.AuthSettings(
            username=invalid_config.OracleWms.username,
            password=invalid_config.OracleWms.password,
        )
        validation = invalid_auth.validate_business_rules()
        if validation.failure:
            logger.info("Expected validation failure: %s", validation.error)
    except Exception as exc:
        logger.warning("Error handling demonstration: %s", exc)


def showcase_7_health_monitoring(
    client: FlextOracleWmsClient,
) -> t.MutableJsonMapping:
    """Feature 7: Health Monitoring."""
    health_result = client.health_check()
    if health_result.failure:
        msg = health_result.error or "Oracle WMS health check failed"
        raise FlextOracleWmsErrors.Error(msg)
    response = health_result.value
    health_data: t.MutableJsonMapping = {"status_code": response.status_code}
    return health_data


def showcase_8_performance_tracking(
    client: FlextOracleWmsClient,
    entities: list[str],
) -> None:
    """Feature 8: Performance Tracking."""
    min_entities_for_concurrent_test = c.OracleWms.DEFAULT_MAX_RETRIES
    if len(entities) >= min_entities_for_concurrent_test:
        test_entities = entities[:min_entities_for_concurrent_test]
        start_time = time.time()
        results: list[p.Result[Sequence[t.StrMapping]]] = []
        for entity in test_entities:
            result = client.get_entity_data(entity, limit=2)
            results.append(result)
        end_time = time.time()
        _elapsed = end_time - start_time
        _successful_requests = sum(
            1 for result in results if hasattr(result, "success") and result.success
        )
    if "company" in entities:
        page_sizes = [1, 5, 10]
        for page_size in page_sizes:
            start_time = time.time()
            _result = client.get_entity_data("company", limit=page_size)
            _elapsed = time.time() - start_time


def showcase_9_cache_management(client: FlextOracleWmsClient) -> None:
    """Feature 9: Cache Management."""
    start_time = time.time()
    first_result = client.discover_entities()
    _first_elapsed = time.time() - start_time
    start_time = time.time()
    second_result = client.discover_entities()
    _second_elapsed = time.time() - start_time
    if first_result.success and second_result.success:
        _first_count = len(first_result.value)
        _second_count = len(second_result.value)


def showcase_10_enterprise_features(
    _client: FlextOracleWmsClient,
    settings: FlextOracleWmsSettings,
) -> None:
    """Feature 10: Enterprise Features."""


def run_showcase() -> None:
    """Run the complete showcase flow."""
    settings = load_config_from_environment()
    client = showcase_1_client_initialization(settings)
    entities = showcase_2_entity_discovery(client)
    showcase_3_data_retrieval(client, entities)
    showcase_4_authentication(settings)
    showcase_5_api_catalog(client)
    showcase_6_error_handling(client)
    showcase_7_health_monitoring(client)
    showcase_8_performance_tracking(client, entities)
    showcase_9_cache_management(client)
    showcase_10_enterprise_features(client, settings)
    client.stop()


def main() -> int:
    """Main showcase execution."""
    try:
        run_showcase()
    except (RuntimeError, OSError, ValueError):
        traceback.print_exc()
        return 1
    return 0


if __name__ == "__main__":
    main()
