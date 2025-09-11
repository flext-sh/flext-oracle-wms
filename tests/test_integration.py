"""Real Integration Tests - Validates ACTUAL Oracle WMS functionality.

These tests use REAL Oracle WMS credentials from .env to validate that the code
actually works in practice, not just passes mocked unit tests.

CRITICAL: These tests validate BUSINESS FUNCTIONALITY, not just code coverage.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import asyncio
import os
import subprocess
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv
from flext_core import FlextTypes

from flext_oracle_wms import (
    FlextOracleWmsApiVersion,
    FlextOracleWmsClient,
    FlextOracleWmsClientConfig,
)

# Load environment variables from .env file
load_dotenv()


class TestRealOracleWMSIntegration:
    """Integration tests with REAL Oracle WMS using .env credentials."""

    @classmethod
    def setup_class(cls) -> None:
        """Load real environment for integration tests."""
        try:
            project_root = Path(__file__).parent.parent
            env_file = project_root / ".env"
            if env_file.exists():
                load_dotenv(env_file)
            else:
                pytest.skip("No .env file found - skipping real integration tests")
        except ImportError:
            pytest.skip("python-dotenv not available - skipping real integration tests")

    def test_real_environment_loaded(self) -> None:
        """Test that real Oracle WMS environment is properly loaded."""
        required_vars = [
            "ORACLE_WMS_BASE_URL",
            "ORACLE_WMS_USERNAME",
            "ORACLE_WMS_PASSWORD",
            "ORACLE_WMS_ENVIRONMENT",
        ]

        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            pytest.skip(f"Missing required environment variables: {missing_vars}")

        # Validate that we have real Oracle WMS credentials
        base_url = os.getenv("ORACLE_WMS_BASE_URL")
        assert "oraclecloud.com" in base_url
        assert os.getenv("ORACLE_WMS_USERNAME") != ""
        assert os.getenv("ORACLE_WMS_PASSWORD") != ""

    def test_real_client_configuration(self) -> None:
        """Test that client configuration works with real environment."""
        config = FlextOracleWmsClientConfig(
            base_url=os.getenv("ORACLE_WMS_BASE_URL"),
            username=os.getenv("ORACLE_WMS_USERNAME"),
            password=os.getenv("ORACLE_WMS_PASSWORD"),
            environment=os.getenv("ORACLE_WMS_ENVIRONMENT"),
            api_version=FlextOracleWmsApiVersion.LGF_V10,
            timeout=float(os.getenv("ORACLE_WMS_TIMEOUT", "30")),
            max_retries=int(os.getenv("ORACLE_WMS_MAX_RETRIES", "3")),
            verify_ssl=os.getenv("ORACLE_WMS_VERIFY_SSL", "true").lower() == "true",
            enable_logging=True,
        )

        # Validate configuration is properly set
        assert "oraclecloud.com" in config.base_url
        assert config.username != ""
        assert config.password != ""
        assert config.environment != ""
        assert config.timeout > 0

    @pytest.mark.asyncio
    async def test_real_client_lifecycle(self) -> None:
        """Test complete client lifecycle with REAL Oracle WMS."""
        # Skip if no environment
        if not os.getenv("ORACLE_WMS_BASE_URL"):
            pytest.skip("No real Oracle WMS environment configured")

        config = FlextOracleWmsClientConfig(
            base_url=os.getenv("ORACLE_WMS_BASE_URL"),
            username=os.getenv("ORACLE_WMS_USERNAME"),
            password=os.getenv("ORACLE_WMS_PASSWORD"),
            environment=os.getenv("ORACLE_WMS_ENVIRONMENT"),
            api_version=FlextOracleWmsApiVersion.LGF_V10,
            timeout=30.0,
            max_retries=3,
            verify_ssl=True,
            enable_logging=True,
        )

        client = FlextOracleWmsClient(config)

        try:
            # Test client start
            await client.start()

            # Test health check with REAL Oracle WMS
            health_result = await client.health_check()
            assert health_result.success
            assert isinstance(health_result.data, dict)
            health_data = health_result.data
            assert health_data.get("service") == "FlextOracleWmsClient"
            # In real environment, should be healthy if connection works

            # Test entity discovery with REAL Oracle WMS
            entities_result = await client.discover_entities()
            assert entities_result.success
            assert isinstance(entities_result.data, list)
            entities = entities_result.data
            assert len(entities) > 0  # Should discover real entities

            # Validate we got real Oracle WMS entities (not fallback)
            expected_entities = ["company", "facility", "item", "order_hdr"]
            found_entities = [e for e in expected_entities if e in entities]
            assert len(found_entities) > 0, (
                f"Expected Oracle WMS entities not found in {entities[:10]}"
            )

        finally:
            # Always cleanup
            await client.stop()

    @pytest.mark.asyncio
    async def test_real_entity_data_retrieval(self) -> None:
        """Test retrieving REAL data from Oracle WMS entities."""
        if not os.getenv("ORACLE_WMS_BASE_URL"):
            pytest.skip("No real Oracle WMS environment configured")

        config = FlextOracleWmsClientConfig(
            base_url=os.getenv("ORACLE_WMS_BASE_URL"),
            username=os.getenv("ORACLE_WMS_USERNAME"),
            password=os.getenv("ORACLE_WMS_PASSWORD"),
            environment=os.getenv("ORACLE_WMS_ENVIRONMENT"),
            api_version=FlextOracleWmsApiVersion.LGF_V10,
            timeout=30.0,
            max_retries=3,
            verify_ssl=True,
            enable_logging=True,
        )

        client = FlextOracleWmsClient(config)

        try:
            await client.start()

            # Test with a known working entity (from basic_usage.py results)
            entity_result = await client.get_entity_data("action_code", limit=5)
            assert entity_result.success
            assert isinstance(entity_result.data, dict)

            # Validate we got real Oracle WMS data structure
            data = entity_result.data
            assert "result_count" in data or "results" in data or len(data) > 0

        finally:
            await client.stop()

    @pytest.mark.asyncio
    async def test_real_error_handling(self) -> None:
        """Test error handling with REAL Oracle WMS (non-existent entity)."""
        if not os.getenv("ORACLE_WMS_BASE_URL"):
            pytest.skip("No real Oracle WMS environment configured")

        config = FlextOracleWmsClientConfig(
            base_url=os.getenv("ORACLE_WMS_BASE_URL"),
            username=os.getenv("ORACLE_WMS_USERNAME"),
            password=os.getenv("ORACLE_WMS_PASSWORD"),
            environment=os.getenv("ORACLE_WMS_ENVIRONMENT"),
            api_version=FlextOracleWmsApiVersion.LGF_V10,
            timeout=30.0,
            max_retries=3,
            verify_ssl=True,
            enable_logging=True,
        )

        client = FlextOracleWmsClient(config)

        try:
            await client.start()

            # Test with non-existent entity - should fail gracefully
            bad_result = await client.get_entity_data("non_existent_entity_xyz")
            assert bad_result.is_failure
            assert "404" in bad_result.error or "not found" in bad_result.error.lower()

        finally:
            await client.stop()

    def test_real_api_catalog_availability(self) -> None:
        """Test that API catalog has real Oracle WMS endpoints."""
        config = FlextOracleWmsClientConfig(
            base_url="https://test.example.com",  # Dummy URL for catalog test
            username="test",
            password="test",
            environment="test",
            api_version=FlextOracleWmsApiVersion.LGF_V10,
            timeout=30.0,
            max_retries=3,
            verify_ssl=True,
            enable_logging=True,
        )

        client = FlextOracleWmsClient(config)

        # Test API catalog
        apis = client.get_available_apis()
        assert isinstance(apis, dict)
        assert len(apis) > 0

        # Validate we have real Oracle WMS APIs
        api_names = list(apis.keys())
        expected_apis = ["lgf_entity_list", "lgf_init_stage_interface", "ship_oblpn"]
        found_apis = [api for api in expected_apis if api in api_names]
        assert len(found_apis) > 0, f"Expected Oracle WMS APIs not found in {api_names}"


@pytest.mark.integration
class TestExamplesIntegration:
    """Test that examples/ actually work with real functionality."""

    def test_basic_usage_example_works(self) -> None:
        """Test that basic_usage.py actually executes successfully."""
        # Run basic_usage.py as subprocess to validate it works
        async def _run(
            cmd_list: FlextTypes.Core.StringList,
            cwd: str | None = None,
        ) -> tuple[int, str, str]:
            process = await asyncio.create_subprocess_exec(
                *cmd_list,
                cwd=cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            return process.returncode, stdout.decode(), stderr.decode()

        rc, out, err = asyncio.run(
            _run(
                [sys.executable, "examples/01_basic_usage.py"],
                cwd="/home/marlonsc/flext/flext-oracle-wms",
            ),
        )

        # Should complete successfully
        assert rc == 0, f"basic_usage.py failed: {err}"

        # Should contain expected success messages
        output = out
        assert "Successfully discovered" in output
        assert "entities" in output.lower()
        assert "completed successfully" in output.lower()

    def test_configuration_example_works(self) -> None:
        """Test that 02_configuration.py now works after refactoring."""
        # Run 02_configuration.py to test it works
        result = subprocess.run(
            [sys.executable, "examples/02_configuration.py"],
            check=False,
            cwd="/home/marlonsc/flext/flext-oracle-wms",
            capture_output=True,
            text=True,
        )
        rc, out, err = result.returncode, result.stdout, result.stderr

        # Should now succeed after refactoring
        assert rc == 0, f"configuration.py failed: {err}"

        # Should contain expected success messages
        output = out
        assert "Configuration examples completed successfully" in output
        assert "Environment configuration created successfully" in output
        assert "Configuration is valid and ready for use" in output
