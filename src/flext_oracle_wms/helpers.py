"""Oracle WMS Essential Helper Functions.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Only essential helper functions that are actually used.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any
from urllib.parse import urljoin, urlparse

from flext_core import FlextResult, get_logger

from flext_oracle_wms.constants import (
    FlextOracleWmsDefaults,
    FlextOracleWmsResponseFields,
)
from flext_oracle_wms.exceptions import (
    FlextOracleWmsError,
)

if TYPE_CHECKING:
    from flext_oracle_wms.types import (
        TOracleWmsApiVersion,
        TOracleWmsEnvironment,
        TOracleWmsRecord,
    )

logger = get_logger(__name__)


def flext_oracle_wms_normalize_url(base_url: str, path: str) -> str:
    """Normalize and join URL paths.

    Args:
        base_url: Base URL to normalize
        path: Path to join with base URL

    Returns:
        Normalized complete URL

    Raises:
        FlextOracleWmsError: If URL normalization fails

    """
    if not isinstance(base_url, str) or not isinstance(path, str):
        msg = "URL and path must be strings"
        raise FlextOracleWmsError(msg)

    if not base_url.strip():
        msg = "Base URL cannot be empty"
        raise FlextOracleWmsError(msg)

    try:
        if not base_url.endswith("/"):
            base_url += "/"
        path = path.lstrip("/")
        return urljoin(base_url, path)
    except Exception as e:
        msg = f"Failed to normalize URL: {e}"
        raise FlextOracleWmsError(msg) from e


def flext_oracle_wms_extract_environment_from_url(url: str) -> TOracleWmsEnvironment:
    """Extract environment name from Oracle WMS URL.

    Args:
        url: Oracle WMS URL to parse

    Returns:
        Environment name extracted from URL path

    Raises:
        FlextOracleWmsError: If URL parsing fails

    """
    if not isinstance(url, str) or not url.strip():
        msg = "URL cannot be empty"
        raise FlextOracleWmsError(msg)

    try:
        parsed = urlparse(url)
        path_parts = [part for part in parsed.path.strip("/").split("/") if part]
        return (
            path_parts[0] if path_parts else FlextOracleWmsDefaults.DEFAULT_ENVIRONMENT
        )
    except Exception as e:
        logger.warning(f"Failed to parse environment from URL {url}: {e}")
        return FlextOracleWmsDefaults.DEFAULT_ENVIRONMENT


def flext_oracle_wms_build_entity_url(
    base_url: str,
    environment: TOracleWmsEnvironment,
    entity_name: str,
    api_version: TOracleWmsApiVersion = FlextOracleWmsDefaults.DEFAULT_API_VERSION,
) -> str:
    """Build URL for Oracle WMS entity endpoint.

    Args:
        base_url: Base URL of the Oracle WMS instance
        environment: Environment name
        entity_name: Name of the entity
        api_version: API version to use

    Returns:
        Complete entity URL

    Raises:
        FlextOracleWmsError: If URL building fails

    """
    if not all(
        isinstance(arg, str) and arg.strip()
        for arg in [base_url, environment, entity_name]
    ):
        msg = "All URL components must be non-empty strings"
        raise FlextOracleWmsError(msg)

    try:
        path = f"/{environment}/wms/lgfapi/{api_version}/entity/{entity_name}/"
        return flext_oracle_wms_normalize_url(base_url, path)
    except Exception as e:
        msg = f"Failed to build entity URL: {e}"
        raise FlextOracleWmsError(msg) from e


def flext_oracle_wms_validate_entity_name(entity_name: str) -> FlextResult[str]:
    """Validate Oracle WMS entity name.

    Args:
        entity_name: Entity name to validate

    Returns:
        FlextResult with validated and normalized entity name

    """
    if not isinstance(entity_name, str):
        return FlextResult.fail("Entity name must be a string")

    if not entity_name.strip():
        return FlextResult.fail("Entity name cannot be empty")

    cleaned = entity_name.strip().lower()

    # Use constants for validation
    if len(cleaned) > FlextOracleWmsDefaults.MAX_ENTITY_NAME_LENGTH:
        return FlextResult.fail(
            f"Entity name too long (max {FlextOracleWmsDefaults.MAX_ENTITY_NAME_LENGTH} characters)"
        )

    if not re.match(FlextOracleWmsDefaults.ENTITY_NAME_PATTERN, cleaned):
        return FlextResult.fail(f"Invalid entity name format: {entity_name}")

    return FlextResult.ok(cleaned)


def flext_oracle_wms_validate_api_response(
    response_data: dict[str, Any],
) -> FlextResult[dict[str, Any]]:
    """Validate Oracle WMS API response structure.

    Args:
        response_data: Response data to validate

    Returns:
        FlextResult with validated response data

    """
    if not isinstance(response_data, dict):
        return FlextResult.fail("Response must be a dictionary")

    # Check for error indicators using constants
    if "error" in response_data:
        error_msg = response_data.get("error", "Unknown error")
        return FlextResult.fail(f"API error: {error_msg}")

    # Check for error messages
    message = response_data.get("message", "")
    if isinstance(message, str) and "error" in message.lower():
        return FlextResult.fail(f"API error: {message}")

    return FlextResult.ok(response_data)


def flext_oracle_wms_extract_pagination_info(
    response_data: dict[str, Any],
) -> dict[str, Any]:
    """Extract pagination information from API response.

    Args:
        response_data: API response data

    Returns:
        Dictionary containing pagination information

    Raises:
        FlextOracleWmsError: If pagination extraction fails

    """
    if not isinstance(response_data, dict):
        msg = "Response data must be a dictionary"
        raise FlextOracleWmsError(msg)

    try:
        return {
            "current_page": response_data.get(
                FlextOracleWmsResponseFields.PAGE_NUMBER, 1
            ),
            "total_pages": response_data.get(
                FlextOracleWmsResponseFields.PAGE_COUNT, 1
            ),
            "total_results": response_data.get(
                FlextOracleWmsResponseFields.RESULT_COUNT, 0
            ),
            "has_next": bool(response_data.get(FlextOracleWmsResponseFields.NEXT_PAGE)),
            "has_previous": bool(
                response_data.get(FlextOracleWmsResponseFields.PREVIOUS_PAGE)
            ),
            "next_url": response_data.get(FlextOracleWmsResponseFields.NEXT_PAGE),
            "previous_url": response_data.get(
                FlextOracleWmsResponseFields.PREVIOUS_PAGE
            ),
        }
    except Exception as e:
        msg = f"Failed to extract pagination info: {e}"
        raise FlextOracleWmsError(msg) from e


def flext_oracle_wms_format_timestamp(timestamp: str | None = None) -> str:
    """Format timestamp for Oracle WMS operations.

    Args:
        timestamp: Optional timestamp string to format

    Returns:
        ISO formatted timestamp string

    """
    if timestamp:
        try:
            if isinstance(timestamp, str) and timestamp.strip():
                return timestamp.strip()
            return str(timestamp)
        except Exception:
            logger.warning(f"Failed to format provided timestamp: {timestamp}")

    return datetime.now(UTC).isoformat()


def flext_oracle_wms_chunk_records(
    records: list[TOracleWmsRecord],
    chunk_size: int = FlextOracleWmsDefaults.DEFAULT_PAGE_SIZE,
) -> list[list[TOracleWmsRecord]]:
    """Split records into chunks for batch processing.

    Args:
        records: List of records to chunk
        chunk_size: Size of each chunk

    Returns:
        List of record chunks

    Raises:
        FlextOracleWmsError: If chunking parameters are invalid

    """
    if not isinstance(records, list):
        msg = "Records must be a list"
        raise FlextOracleWmsError(msg)

    if chunk_size <= 0:
        msg = "Chunk size must be positive"
        raise FlextOracleWmsError(msg)

    if chunk_size > FlextOracleWmsDefaults.MAX_PAGE_SIZE:
        msg = f"Chunk size cannot exceed {FlextOracleWmsDefaults.MAX_PAGE_SIZE}"
        raise FlextOracleWmsError(msg)

    try:
        chunks = []
        for i in range(0, len(records), chunk_size):
            chunk = records[i : i + chunk_size]
            chunks.append(chunk)
        return chunks
    except Exception as e:
        msg = f"Failed to chunk records: {e}"
        raise FlextOracleWmsError(msg) from e
