"""Example usage of the new declarative Oracle WMS Client.

This demonstrates the declarative approach with massive code reduction.
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from flext_oracle_wms import (
    FlextOracleWmsApi,
    FlextOracleWmsSettings,
    t,
    u,
)
from flext_oracle_wms.utilities import FlextOracleWmsUtilitiesClient

logger = u.fetch_logger(__name__)

FlextOracleWmsClient = FlextOracleWmsUtilitiesClient.Client


def load_env_config() -> t.MutableJsonMapping | None:
    """Load configuration from .env file."""
    env_path = Path("flext-tap-oracle-wms/.env")
    if not env_path.exists():
        return None
    settings: t.MutableStrMapping = {}
    with env_path.open(encoding="utf-8") as f:
        for line in f:
            stripped_line = line.strip()
            if (
                stripped_line
                and (not stripped_line.startswith("#"))
                and ("=" in stripped_line)
            ):
                key, value = stripped_line.split("=", 1)
                settings[key.strip()] = value.strip()
    base_url = settings.get("ORACLE_WMS_BASE_URL", "")
    if base_url:
        try:
            parsed = urlparse(base_url)
            path_parts = parsed.path.strip("/").split("/")
            if path_parts and path_parts[-1]:
                logger.debug(f"Environment detected in URL: {path_parts[-1]}")
        except (ValueError, AttributeError) as e:
            logger.debug("Failed to parse environment from URL: %s", e)
    return {
        "oracle_wms_base_url": base_url,
        "oracle_wms_username": settings.get("ORACLE_WMS_USERNAME", ""),
        "oracle_wms_password": settings.get("ORACLE_WMS_PASSWORD", ""),
        "api_version": "LGF_V10",
        "oracle_wms_timeout": int(settings.get("ORACLE_WMS_TIMEOUT", "30")),
        "oracle_wms_max_retries": int(settings.get("ORACLE_WMS_MAX_RETRIES", "3")),
        "oracle_wms_verify_ssl": settings.get("ORACLE_WMS_VERIFY_SSL", "true").lower()
        == "true",
        "oracle_wms_enable_logging": settings.get(
            "ORACLE_WMS_ENABLE_REQUEST_LOGGING",
            "true",
        ).lower()
        == "true",
    }


def main() -> None:
    """Demonstrate declarative Oracle WMS Client usage."""
    env_config = load_env_config()
    if not env_config or not all([
        env_config.get("oracle_wms_base_url"),
        env_config.get("oracle_wms_username"),
        env_config.get("oracle_wms_password"),
    ]):
        return
    settings = FlextOracleWmsSettings.model_validate({
        "base_url": str(env_config["oracle_wms_base_url"]),
        "username": str(env_config["oracle_wms_username"]),
        "password": str(env_config["oracle_wms_password"]),
        "api_version": str(env_config["api_version"]),
        "timeout": int(str(env_config["oracle_wms_timeout"])),
        "max_retries": int(str(env_config["oracle_wms_max_retries"])),
        "verify_ssl": bool(env_config["oracle_wms_verify_ssl"]),
        "enable_logging": bool(env_config["oracle_wms_enable_logging"]),
    })
    client = FlextOracleWmsClient(settings)
    try:
        run_client_flow(client)
    except Exception as exc:
        logger.warning("Test execution encountered error: %s", exc)
        raise
    finally:
        client.stop()


def run_client_flow(client: FlextOracleWmsClient) -> None:
    """Run the declarative example client flow."""
    start_result = client.start()
    if not start_result.success:
        return
    categories: t.MutableMappingKV[str, t.MutableSequenceOf[str]] = {}
    for api in FlextOracleWmsApi.api_endpoints().values():
        if api.category not in categories:
            categories[api.category] = []
        categories[api.category].append(api.name)
    for _category, _apis in categories.items():
        pass
    client.health_check()
    client.discover_entities()
    for entity in ["company", "facility", "item"]:
        result = client.get_entity_data(entity, limit=3)
        if result.success:
            data = result.value
            if isinstance(data, list):
                for record in data:
                    if isinstance(record, dict):
                        record.get("count", str(len(data)))
    client.health_check()
    client.update_oblpn_tracking_number(
        oblpn_id="TEST123",
        tracking_number="TRACK123",
    )
    lpn_result = client.create_lpn(lpn_nbr="TEST_LPN", qty=10)
    if lpn_result.failure:
        logger.debug(f"LPN creation failed as expected: {lpn_result.error}")


if __name__ == "__main__":
    main()
