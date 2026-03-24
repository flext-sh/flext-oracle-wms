"""Example usage of the new declarative Oracle WMS Client.

This demonstrates the declarative approach with massive code reduction.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from urllib.parse import urlparse

from flext_core import FlextLogger

from flext_oracle_wms import (
    FLEXT_ORACLE_WMS_APIS,
    FlextOracleWmsApiVersion,
    FlextOracleWmsClient,
    FlextOracleWmsClientSettings,
)
from tests import t

logger = FlextLogger(__name__)


def load_env_config() -> t.ContainerMapping | None:
    """Load configuration from .env file."""
    env_path = Path("flext-tap-oracle-wms/.env")
    if not env_path.exists():
        return None
    config: t.StrMapping = {}
    with env_path.open(encoding="utf-8") as f:
        for line in f:
            stripped_line = line.strip()
            if (
                stripped_line
                and (not stripped_line.startswith("#"))
                and ("=" in stripped_line)
            ):
                key, value = stripped_line.split("=", 1)
                config[key.strip()] = value.strip()
    base_url = config.get("ORACLE_WMS_BASE_URL", "")
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
        "oracle_wms_username": config.get("ORACLE_WMS_USERNAME"),
        "oracle_wms_password": config.get("ORACLE_WMS_PASSWORD"),
        "api_version": FlextOracleWmsApiVersion.LGF_V10,
        "oracle_wms_timeout": int(config.get("ORACLE_WMS_TIMEOUT", "30")),
        "oracle_wms_max_retries": int(config.get("ORACLE_WMS_MAX_RETRIES", "3")),
        "oracle_wms_verify_ssl": config.get("ORACLE_WMS_VERIFY_SSL", "true").lower()
        == "true",
        "oracle_wms_enable_logging": config.get(
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
    config = FlextOracleWmsClientSettings({
        "base_url": str(env_config["oracle_wms_base_url"]),
        "username": str(env_config["oracle_wms_username"]),
        "password": str(env_config["oracle_wms_password"]),
        "api_version": env_config["api_version"],
        "timeout": int(str(env_config["oracle_wms_timeout"])),
        "retry_attempts": int(str(env_config["oracle_wms_max_retries"])),
        "enable_ssl_verification": bool(env_config["oracle_wms_verify_ssl"]),
        "enable_audit_logging": bool(env_config["oracle_wms_enable_logging"]),
    })
    client = FlextOracleWmsClient(config)
    try:
        start_result = client.start()
        if not start_result.is_success:
            return
        categories: Mapping[str, t.StrSequence] = {}
        for api in FLEXT_ORACLE_WMS_APIS.values():
            if api.category not in categories:
                categories[api.category] = []
            categories[api.category].append(api.name)
        for _category, _apis in categories.items():
            pass
        health_result = client.health_check()
        if health_result.is_success:
            pass
        entities_result = client.discover_entities()
        if entities_result.is_success:
            pass
        for entity in ["company", "facility", "item"]:
            result = client.get_entity_data(entity, limit=3)
            if result.is_success:
                data = result.value
                if isinstance(data, dict):
                    results = data.get("results", [])
                    if isinstance(results, list):
                        data.get("count", len(results))
                elif isinstance(data, list):
                    len(data)
        health_result = client.health_check()
        if health_result.is_success:
            pass
        client.update_oblpn_tracking_number(
            oblpn_id="TEST123",
            tracking_number="TRACK123",
        )
        lpn_result = client.create_lpn(lpn_nbr="TEST_LPN", qty=10)
        if lpn_result.is_failure:
            logger.debug(f"LPN creation failed as expected: {lpn_result.error}")
    except Exception as e:
        logger.warning("Test execution encountered error: %s", e)
        raise
    finally:
        client.stop()


if __name__ == "__main__":
    main()
