"""Comprehensive test coverage for Oracle WMS discovery module.

This test file provides extensive coverage for discovery.py, focusing on:
- FlextOracleWmsEntityDiscovery class functionality (all discovery strategies)
- Entity discovery with multiple endpoints and error handling
- Schema discovery and field type inference
- Pattern-based filtering and deduplication
- Caching functionality and performance optimization
- Strategy and Command pattern implementations

Target: Increase discovery.py coverage from 15% to 85%+
"""

import math
from unittest.mock import AsyncMock, Mock, patch

import pytest
from flext_core import FlextResult

from flext_oracle_wms import (
    DISCOVERY_FAILURE,
    DISCOVERY_SUCCESS,
    DiscoveryContext,
    EndpointDiscoveryStrategy,
    EntityResponseParser,
    FlextOracleWmsDefaults,
    FlextOracleWmsDiscoveryResult,
    FlextOracleWmsEntity,
    FlextOracleWmsEntityDiscovery,
    flext_oracle_wms_create_entity_discovery,
)


class TestDiscoveryConstants:
    """Test discovery constants."""

    def test_discovery_constants(self) -> None:
        """Test discovery boolean constants."""
        assert DISCOVERY_SUCCESS is True
        assert DISCOVERY_FAILURE is False


class TestDiscoveryContext:
    """Test DiscoveryContext parameter object."""

    def test_discovery_context_creation(self) -> None:
        """Test creating DiscoveryContext."""
        context = DiscoveryContext(
            include_patterns=["company", "facility"],
            exclude_patterns=["test_*"],
            all_entities=[],
            errors=[],
        )

        assert context.include_patterns == ["company", "facility"]
        assert context.exclude_patterns == ["test_*"]
        assert context.all_entities == []
        assert context.errors == []

    def test_discovery_context_with_data(self) -> None:
        """Test DiscoveryContext with existing data."""
        entities = [
            FlextOracleWmsEntity(
                name="company",
                endpoint="/api/company",
                description="Company entity",
            ),
            FlextOracleWmsEntity(
                name="facility",
                endpoint="/api/facility",
                description="Facility entity",
            ),
        ]
        errors = ["API timeout error", "Authentication failed"]

        context = DiscoveryContext(
            include_patterns=None,
            exclude_patterns=None,
            all_entities=entities,
            errors=errors,
        )

        assert context.include_patterns is None
        assert context.exclude_patterns is None
        assert len(context.all_entities) == 2
        assert len(context.errors) == 2


class TestEndpointDiscoveryStrategy:
    """Test EndpointDiscoveryStrategy implementation."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.mock_discovery = Mock(spec=FlextOracleWmsEntityDiscovery)
        self.strategy = EndpointDiscoveryStrategy(self.mock_discovery)
        self.mock_api_client = AsyncMock()
        self.context = DiscoveryContext(
            include_patterns=None,
            exclude_patterns=None,
            all_entities=[],
            errors=[],
        )

    @pytest.mark.asyncio
    async def test_execute_discovery_step_success(self) -> None:
        """Test successful discovery step execution."""
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = FlextOracleWmsDefaults.HTTP_OK
        mock_response.data = {"entities": ["company", "facility"]}

        self.mock_api_client.get.return_value = FlextResult[None].ok(mock_response)

        # Mock entity parsing
        mock_entities = [
            FlextOracleWmsEntity(
                name="company",
                endpoint="/api/company",
                description="Company",
            ),
            FlextOracleWmsEntity(
                name="facility",
                endpoint="/api/facility",
                description="Facility",
            ),
        ]

        with patch.object(
            EntityResponseParser,
            "parse_entities_response",
        ) as mock_parse:
            mock_parse.return_value = FlextResult[None].ok(mock_entities)

            result = await self.strategy.execute_discovery_step(
                self.context,
                self.mock_api_client,
                "/api/entities",
            )

            assert result.success
            assert result.data is True
            assert len(self.context.all_entities) == 2

    @pytest.mark.asyncio
    async def test_execute_discovery_step_api_failure(self) -> None:
        """Test discovery step with API failure."""
        self.mock_api_client.get.return_value = FlextResult[None].fail(
            "API connection failed",
        )

        result = await self.strategy.execute_discovery_step(
            self.context,
            self.mock_api_client,
            "/api/entities",
        )

        assert result.success
        assert result.data is False
        assert len(self.context.errors) > 0
        assert "API connection failed" in self.context.errors[0]

    @pytest.mark.asyncio
    async def test_execute_discovery_step_invalid_response(self) -> None:
        """Test discovery step with invalid response structure."""
        # Mock invalid response (missing required attributes)
        mock_response = Mock()
        del mock_response.status_code  # Remove required attribute

        self.mock_api_client.get.return_value = FlextResult[None].ok(mock_response)

        result = await self.strategy.execute_discovery_step(
            self.context,
            self.mock_api_client,
            "/api/entities",
        )

        assert result.success
        assert result.data is False
        assert len(self.context.errors) > 0

    @pytest.mark.asyncio
    async def test_execute_discovery_step_http_error(self) -> None:
        """Test discovery step with HTTP error status."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.data = {"error": "Not found"}

        self.mock_api_client.get.return_value = FlextResult[None].ok(mock_response)

        result = await self.strategy.execute_discovery_step(
            self.context,
            self.mock_api_client,
            "/api/entities",
        )

        assert result.success
        assert result.data is False
        assert any("HTTP 404" in error for error in self.context.errors)

    @pytest.mark.asyncio
    async def test_execute_discovery_step_exception(self) -> None:
        """Test discovery step with exception."""
        self.mock_api_client.get.side_effect = Exception("Network error")

        result = await self.strategy.execute_discovery_step(
            self.context,
            self.mock_api_client,
            "/api/entities",
        )

        assert result.success
        assert result.data is False
        assert any("Exception calling" in error for error in self.context.errors)

    @pytest.mark.asyncio
    async def test_make_api_request_success(self) -> None:
        """Test successful API request."""
        mock_response = Mock()
        mock_response.status_code = 200

        self.mock_api_client.get.return_value = FlextResult[None].ok(mock_response)

        result = await self.strategy._make_api_request(
            self.mock_api_client,
            "/api/test",
        )

        assert result.success
        assert result.data == mock_response

    @pytest.mark.asyncio
    async def test_make_api_request_failure(self) -> None:
        """Test failed API request."""
        self.mock_api_client.get.return_value = FlextResult[None].fail("Connection timeout")

        result = await self.strategy._make_api_request(
            self.mock_api_client,
            "/api/test",
        )

        assert result.is_failure
        assert "Failed to call /api/test" in result.error

    @pytest.mark.asyncio
    async def test_make_api_request_no_data(self) -> None:
        """Test API request with no response data."""
        self.mock_api_client.get.return_value = FlextResult[None].ok(None)

        result = await self.strategy._make_api_request(
            self.mock_api_client,
            "/api/test",
        )

        assert result.is_failure
        assert "No response data from /api/test" in result.error

    def test_validate_response_success(self) -> None:
        """Test successful response validation."""
        mock_response = Mock()
        mock_response.status_code = FlextOracleWmsDefaults.HTTP_OK
        mock_response.data = {"entities": []}

        result = self.strategy._validate_response(mock_response, "/api/test")

        assert result.success
        assert result.data == mock_response

    def test_validate_response_none(self) -> None:
        """Test response validation with None."""
        result = self.strategy._validate_response(None, "/api/test")

        assert result.is_failure
        assert "No response data from /api/test" in result.error

    def test_validate_response_missing_attributes(self) -> None:
        """Test response validation with missing attributes."""
        mock_response = Mock()
        del mock_response.status_code  # Remove required attribute

        result = self.strategy._validate_response(mock_response, "/api/test")

        assert result.is_failure
        assert "Invalid response structure" in result.error

    def test_validate_response_bad_status(self) -> None:
        """Test response validation with bad HTTP status."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.data = {"error": "Internal server error"}

        result = self.strategy._validate_response(mock_response, "/api/test")

        assert result.is_failure
        assert "HTTP 500" in result.error


class TestEntityResponseParser:
    """Test EntityResponseParser command pattern."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.mock_discovery = Mock(spec=FlextOracleWmsEntityDiscovery)
        self.parser = EntityResponseParser(self.mock_discovery)

    @pytest.mark.asyncio
    async def test_parse_entities_response_delegation(self) -> None:
        """Test that parser delegates to discovery instance."""
        mock_entities = [
            FlextOracleWmsEntity(
                name="test",
                endpoint="/api/test",
                description="Test entity",
            ),
        ]
        self.mock_discovery._parse_entities_response.return_value = FlextResult[None].ok(
            mock_entities,
        )

        response_data = {"entities": ["test"]}
        result = await self.parser.parse_entities_response(
            response_data,
            "/api/entities",
        )

        assert result.success
        assert result.data == mock_entities
        self.mock_discovery._parse_entities_response.assert_called_once_with(
            response_data,
            "/api/entities",
        )


class TestFlextOracleWmsEntityDiscovery:
    """Test main FlextOracleWmsEntityDiscovery class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.mock_api_client = AsyncMock()
        self.discovery = FlextOracleWmsEntityDiscovery(
            api_client=self.mock_api_client,
            environment="test_env",
        )

    def test_initialization_default(self) -> None:
        """Test discovery initialization with default parameters."""
        discovery = FlextOracleWmsEntityDiscovery(
            api_client=self.mock_api_client,
            environment="prod",
        )

        assert discovery.api_client == self.mock_api_client
        assert discovery.cache_manager is None
        assert discovery.environment == "prod"
        assert len(discovery.discovery_endpoints) > 0
        assert all("prod" in endpoint for endpoint in discovery.discovery_endpoints)

    def test_initialization_with_cache(self) -> None:
        """Test discovery initialization with cache manager."""
        mock_cache = Mock()
        discovery = FlextOracleWmsEntityDiscovery(
            api_client=self.mock_api_client,
            cache_manager=mock_cache,
            environment="test",
        )

        assert discovery.cache_manager == mock_cache

    def test_discovery_endpoints_generation(self) -> None:
        """Test that discovery endpoints are properly generated."""
        expected_patterns = [
            "/test_env/wms/lgfapi/v10/entity/",
            "/test_env/wms/lgfapi/v11/entity/",
            "/test_env/api/entities/",
            "/test_env/api/v1/entities/",
            "/test_env/entities/",
            "/test_env/metadata/entities/",
            "/test_env/schema/entities/",
        ]

        assert self.discovery.discovery_endpoints == expected_patterns

    @pytest.mark.asyncio
    async def test_discover_all_entities_fresh_discovery(self) -> None:
        """Test fresh entity discovery without cache."""
        # Mock the _perform_discovery method
        mock_entities = [
            FlextOracleWmsEntity(
                name="company",
                endpoint="/api/company",
                description="Company",
            ),
            FlextOracleWmsEntity(
                name="facility",
                endpoint="/api/facility",
                description="Facility",
            ),
        ]

        mock_discovery_result = FlextOracleWmsDiscoveryResult(
            entities=mock_entities,
            total_count=2,
            timestamp="2024-01-01T00:00:00",
            has_errors=False,
            errors=[],
        )

        with patch.object(self.discovery, "_perform_discovery") as mock_perform:
            mock_perform.return_value = FlextResult[None].ok(mock_discovery_result)

            result = await self.discovery.discover_all_entities()

            assert result.success
            assert result.data.total_count == 2
            assert len(result.data.entities) == 2
            assert result.data.discovery_duration_ms is not None

    @pytest.mark.asyncio
    async def test_discover_all_entities_with_patterns(self) -> None:
        """Test entity discovery with include/exclude patterns."""
        include_patterns = ["comp*", "fac*"]
        exclude_patterns = ["test_*"]

        mock_discovery_result = FlextOracleWmsDiscoveryResult(
            entities=[],
            total_count=0,
            timestamp="2024-01-01T00:00:00",
            has_errors=False,
            errors=[],
        )

        with patch.object(self.discovery, "_perform_discovery") as mock_perform:
            mock_perform.return_value = FlextResult[None].ok(mock_discovery_result)

            result = await self.discovery.discover_all_entities(
                include_patterns=include_patterns,
                exclude_patterns=exclude_patterns,
            )

            assert result.success
            mock_perform.assert_called_once_with(include_patterns, exclude_patterns)

    @pytest.mark.asyncio
    async def test_discover_all_entities_with_cache_hit(self) -> None:
        """Test entity discovery with cache hit."""
        mock_cache = Mock()
        self.discovery.cache_manager = mock_cache

        cached_result = FlextOracleWmsDiscoveryResult(
            entities=[],
            total_count=0,
            timestamp="2024-01-01T00:00:00",
            has_errors=False,
            errors=[],
        )

        with patch.object(self.discovery, "_get_cached_discovery") as mock_cache_get:
            mock_cache_get.return_value = FlextResult[None].ok(cached_result)

            result = await self.discovery.discover_all_entities(use_cache=True)

            assert result.success
            assert result.data == cached_result

    @pytest.mark.asyncio
    async def test_discover_all_entities_cache_miss(self) -> None:
        """Test entity discovery with cache miss."""
        mock_cache = Mock()
        self.discovery.cache_manager = mock_cache

        mock_discovery_result = FlextOracleWmsDiscoveryResult(
            entities=[],
            total_count=0,
            timestamp="2024-01-01T00:00:00",
            has_errors=False,
            errors=[],
        )

        with (
            patch.object(self.discovery, "_get_cached_discovery") as mock_cache_get,
            patch.object(self.discovery, "_perform_discovery") as mock_perform,
            patch.object(self.discovery, "_cache_discovery_result") as mock_cache_set,
        ):
            mock_cache_get.return_value = FlextResult[None].fail("Cache miss")
            mock_perform.return_value = FlextResult[None].ok(mock_discovery_result)

            result = await self.discovery.discover_all_entities(use_cache=True)

            assert result.success
            mock_cache_set.assert_called_once()

    @pytest.mark.asyncio
    async def test_discover_all_entities_discovery_failure(self) -> None:
        """Test entity discovery with discovery failure."""
        with patch.object(self.discovery, "_perform_discovery") as mock_perform:
            mock_perform.return_value = FlextResult[None].fail("Discovery failed")

            result = await self.discovery.discover_all_entities()

            assert result.is_failure
            assert "Discovery failed" in result.error

    @pytest.mark.asyncio
    async def test_discover_all_entities_no_data(self) -> None:
        """Test entity discovery with no data returned."""
        with patch.object(self.discovery, "_perform_discovery") as mock_perform:
            mock_perform.return_value = FlextResult[None].ok(None)

            result = await self.discovery.discover_all_entities()

            assert result.is_failure
            assert "Discovery returned no data" in result.error

    @pytest.mark.asyncio
    async def test_discover_entity_schema_success(self) -> None:
        """Test successful entity schema discovery."""
        mock_entity = FlextOracleWmsEntity(
            name="company",
            endpoint="/api/company",
            description="Company entity",
            fields={"id": {"type": "integer"}, "name": {"type": "string"}},
        )

        with patch.object(self.discovery, "_discover_single_entity") as mock_discover:
            mock_discover.return_value = FlextResult[None].ok(mock_entity)

            result = await self.discovery.discover_entity_schema("company")

            assert result.success
            assert result.data == mock_entity

    @pytest.mark.asyncio
    async def test_discover_entity_schema_with_cache(self) -> None:
        """Test entity schema discovery with cache."""
        mock_cache = Mock()
        self.discovery.cache_manager = mock_cache

        mock_entity = FlextOracleWmsEntity(
            name="company",
            endpoint="/api/company",
            description="Company entity",
        )

        with patch.object(self.discovery, "_get_cached_entity") as mock_cache_get:
            mock_cache_get.return_value = FlextResult[None].ok(mock_entity)

            result = await self.discovery.discover_entity_schema(
                "company",
                use_cache=True,
            )

            assert result.success
            assert result.data == mock_entity

    @pytest.mark.asyncio
    async def test_discover_entity_schema_cache_and_store(self) -> None:
        """Test entity schema discovery with cache miss and storage."""
        mock_cache = Mock()
        self.discovery.cache_manager = mock_cache

        mock_entity = FlextOracleWmsEntity(
            name="company",
            endpoint="/api/company",
            description="Company entity",
        )

        with (
            patch.object(self.discovery, "_get_cached_entity") as mock_cache_get,
            patch.object(self.discovery, "_discover_single_entity") as mock_discover,
            patch.object(self.discovery, "_cache_entity_result") as mock_cache_set,
        ):
            mock_cache_get.return_value = FlextResult[None].fail("Cache miss")
            mock_discover.return_value = FlextResult[None].ok(mock_entity)

            result = await self.discovery.discover_entity_schema(
                "company",
                use_cache=True,
            )

            assert result.success
            mock_cache_set.assert_called_once()

    @pytest.mark.asyncio
    async def test_perform_discovery_success(self) -> None:
        """Test successful discovery performance."""
        # Mock strategy execution
        with patch.object(
            EndpointDiscoveryStrategy,
            "execute_discovery_step",
        ) as mock_step:
            mock_step.return_value = FlextResult[None].ok(True)

            with patch.object(self.discovery, "_apply_post_processing") as mock_process:
                mock_entities = [
                    FlextOracleWmsEntity(
                        name="test",
                        endpoint="/api/test",
                        description="Test",
                    ),
                ]
                mock_process.return_value = mock_entities

                result = await self.discovery._perform_discovery()

                assert result.success
                assert len(result.data.entities) == 1

    @pytest.mark.asyncio
    async def test_perform_discovery_with_patterns(self) -> None:
        """Test discovery with include/exclude patterns."""
        include_patterns = ["comp*"]
        exclude_patterns = ["test_*"]

        with patch.object(
            EndpointDiscoveryStrategy,
            "execute_discovery_step",
        ) as mock_step:
            mock_step.return_value = FlextResult[None].ok(True)

            with patch.object(self.discovery, "_apply_post_processing") as mock_process:
                mock_process.return_value = []

                result = await self.discovery._perform_discovery(
                    include_patterns,
                    exclude_patterns,
                )

                assert result.success
                # Verify context was created with patterns
                mock_process.assert_called_once()
                context_arg = mock_process.call_args[0][0]
                assert context_arg.include_patterns == include_patterns
                assert context_arg.exclude_patterns == exclude_patterns

    def test_apply_post_processing_no_filters(self) -> None:
        """Test post-processing without filters."""
        entities = [
            FlextOracleWmsEntity(
                name="company",
                endpoint="/api/company",
                description="Company",
            ),
            FlextOracleWmsEntity(
                name="facility",
                endpoint="/api/facility",
                description="Facility",
            ),
        ]

        context = DiscoveryContext(
            include_patterns=None,
            exclude_patterns=None,
            all_entities=entities,
            errors=[],
        )

        result = self.discovery._apply_post_processing(context)

        assert len(result) == 2
        assert result == entities

    def test_apply_post_processing_with_filters(self) -> None:
        """Test post-processing with filters."""
        entities = [
            FlextOracleWmsEntity(
                name="company",
                endpoint="/api/company",
                description="Company",
            ),
            FlextOracleWmsEntity(
                name="facility",
                endpoint="/api/facility",
                description="Facility",
            ),
            FlextOracleWmsEntity(
                name="test_entity",
                endpoint="/api/test",
                description="Test",
            ),
        ]

        context = DiscoveryContext(
            include_patterns=["comp*", "fac*"],
            exclude_patterns=["test_*"],
            all_entities=entities,
            errors=[],
        )

        with patch.object(self.discovery, "_filter_entities") as mock_filter:
            filtered_entities = entities[:2]  # Remove test_entity
            mock_filter.return_value = filtered_entities

            with patch.object(self.discovery, "_deduplicate_entities") as mock_dedup:
                mock_dedup.return_value = filtered_entities

                result = self.discovery._apply_post_processing(context)

                assert len(result) == 2
                mock_filter.assert_called_once()
                mock_dedup.assert_called_once()

    def test_create_discovery_result(self) -> None:
        """Test discovery result creation."""
        entities = [
            FlextOracleWmsEntity(
                name="company",
                endpoint="/api/company",
                description="Company",
            ),
        ]

        context = DiscoveryContext(
            include_patterns=None,
            exclude_patterns=None,
            all_entities=[],
            errors=["Some error"],
        )

        result = self.discovery._create_discovery_result(entities, context)

        assert result.success
        assert result.data.total_count == 1
        assert result.data.has_errors is True
        assert len(result.data.errors) == 1

    def test_extract_entity_list_from_dict_entities(self) -> None:
        """Test entity list extraction from dict with 'entities' key."""
        response_data = {"entities": ["company", "facility", "item"]}

        result = self.discovery._extract_entity_list_from_response(
            response_data,
            "/api/test",
        )

        assert result.success
        assert result.data == ["company", "facility", "item"]

    def test_extract_entity_list_from_dict_results(self) -> None:
        """Test entity list extraction from dict with 'results' key."""
        response_data = {"results": ["order", "shipment"]}

        result = self.discovery._extract_entity_list_from_response(
            response_data,
            "/api/test",
        )

        assert result.success
        assert result.data == ["order", "shipment"]

    def test_extract_entity_list_from_dict_data(self) -> None:
        """Test entity list extraction from dict with 'data' key."""
        response_data = {"data": ["location", "inventory"]}

        result = self.discovery._extract_entity_list_from_response(
            response_data,
            "/api/test",
        )

        assert result.success
        assert result.data == ["location", "inventory"]

    def test_extract_entity_list_from_dict_keys(self) -> None:
        """Test entity list extraction from dict keys."""
        response_data = {"company": {}, "facility": {}, "item": {}}

        result = self.discovery._extract_entity_list_from_response(
            response_data,
            "/api/test",
        )

        assert result.success
        assert set(result.data) == {"company", "facility", "item"}

    def test_extract_entity_list_from_list(self) -> None:
        """Test entity list extraction from direct list."""
        response_data = ["company", "facility", "item"]

        result = self.discovery._extract_entity_list_from_response(
            response_data,
            "/api/test",
        )

        assert result.success
        assert result.data == response_data

    def test_extract_entity_list_unexpected_format(self) -> None:
        """Test entity list extraction with unexpected format."""
        response_data = "unexpected_string"

        result = self.discovery._extract_entity_list_from_response(
            response_data,
            "/api/test",
        )

        assert result.is_failure
        assert "Unexpected response format" in result.error

    def test_create_entity_from_string_name(self) -> None:
        """Test entity creation from string name."""
        entity = self.discovery._create_entity_from_string_name("company")

        assert entity.name == "company"
        assert entity.endpoint == "/test_env/wms/lgfapi/v10/entity/company/"
        assert entity.description == "Oracle WMS entity: company"

    def test_create_entity_from_metadata_complete(self) -> None:
        """Test entity creation from complete metadata."""
        metadata = {
            "name": "company",
            "endpoint": "/custom/endpoint",
            "description": "Custom description",
            "primary_key": "id",
            "replication_key": "updated_at",
            "supports_incremental": True,
            "fields": {"id": {"type": "integer"}, "name": {"type": "string"}},
        }

        entity = self.discovery._create_entity_from_metadata(metadata)

        assert entity is not None
        assert entity.name == "company"
        assert entity.endpoint == "/custom/endpoint"
        assert entity.description == "Custom description"
        assert entity.primary_key == "id"
        assert entity.replication_key == "updated_at"
        assert entity.supports_incremental is True
        assert entity.fields == {"id": {"type": "integer"}, "name": {"type": "string"}}

    def test_create_entity_from_metadata_minimal(self) -> None:
        """Test entity creation from minimal metadata."""
        metadata = {"name": "facility"}

        entity = self.discovery._create_entity_from_metadata(metadata)

        assert entity is not None
        assert entity.name == "facility"
        assert entity.endpoint == "/test_env/wms/lgfapi/v10/entity/facility/"
        assert entity.description == "Oracle WMS entity: facility"
        assert entity.primary_key is None
        assert entity.replication_key is None
        assert entity.supports_incremental is False

    def test_create_entity_from_metadata_alternative_name_key(self) -> None:
        """Test entity creation with alternative name key."""
        metadata = {"entity_name": "item"}

        entity = self.discovery._create_entity_from_metadata(metadata)

        assert entity is not None
        assert entity.name == "item"

    def test_create_entity_from_metadata_no_name(self) -> None:
        """Test entity creation with no name returns None."""
        metadata = {"description": "Entity without name"}

        entity = self.discovery._create_entity_from_metadata(metadata)

        assert entity is None

    def test_create_entity_from_metadata_invalid_fields(self) -> None:
        """Test entity creation with invalid fields type."""
        metadata = {
            "name": "test",
            "fields": "invalid_fields_type",  # Should be dict
        }

        entity = self.discovery._create_entity_from_metadata(metadata)

        assert entity is not None
        assert entity.fields is None

    @pytest.mark.asyncio
    async def test_parse_entities_response_string_list(self) -> None:
        """Test parsing entities from string list."""
        response_data = {"entities": ["company", "facility"]}

        result = await self.discovery._parse_entities_response(
            response_data,
            "/api/test",
        )

        assert result.success
        assert len(result.data) == 2
        assert all(isinstance(entity, FlextOracleWmsEntity) for entity in result.data)
        assert result.data[0].name == "company"
        assert result.data[1].name == "facility"

    @pytest.mark.asyncio
    async def test_parse_entities_response_metadata_list(self) -> None:
        """Test parsing entities from metadata list."""
        response_data = {
            "results": [
                {"name": "company", "description": "Company entity"},
                {"name": "facility", "description": "Facility entity"},
            ],
        }

        result = await self.discovery._parse_entities_response(
            response_data,
            "/api/test",
        )

        assert result.success
        assert len(result.data) == 2
        assert result.data[0].description == "Company entity"
        assert result.data[1].description == "Facility entity"

    @pytest.mark.asyncio
    async def test_parse_entities_response_mixed_types(self) -> None:
        """Test parsing entities from mixed string and metadata."""
        response_data = {
            "entities": [
                "company",
                {"name": "facility", "description": "Facility entity"},
                "item",
            ],
        }

        result = await self.discovery._parse_entities_response(
            response_data,
            "/api/test",
        )

        assert result.success
        assert len(result.data) == 3

    @pytest.mark.asyncio
    async def test_parse_entities_response_empty_list(self) -> None:
        """Test parsing entities from empty response."""
        with patch.object(
            self.discovery,
            "_extract_entity_list_from_response",
        ) as mock_extract:
            mock_extract.return_value = FlextResult[None].ok(None)

            result = await self.discovery._parse_entities_response({}, "/api/test")

            assert result.success
            assert result.data == []

    @pytest.mark.asyncio
    async def test_parse_entities_response_extraction_failure(self) -> None:
        """Test parsing entities with extraction failure."""
        with patch.object(
            self.discovery,
            "_extract_entity_list_from_response",
        ) as mock_extract:
            mock_extract.return_value = FlextResult[None].fail("Extraction failed")

            result = await self.discovery._parse_entities_response({}, "/api/test")

            assert result.is_failure
            assert "Extraction failed" in result.error

    @pytest.mark.asyncio
    async def test_discover_single_entity_success(self) -> None:
        """Test successful single entity discovery."""
        mock_response = Mock()
        mock_response.status_code = FlextOracleWmsDefaults.HTTP_OK
        mock_response.data = {
            "results": [{"id": 1, "name": "Test Company", "status": "active"}],
        }

        self.mock_api_client.get.return_value = FlextResult[None].ok(mock_response)

        result = await self.discovery._discover_single_entity("company")

        assert result.success
        assert result.data.name == "company"
        assert result.data.fields is not None

    @pytest.mark.asyncio
    async def test_discover_single_entity_all_endpoints_fail(self) -> None:
        """Test single entity discovery when all endpoints fail."""
        self.mock_api_client.get.return_value = FlextResult[None].fail("Connection failed")

        result = await self.discovery._discover_single_entity("company")

        assert result.success
        assert result.data.name == "company"
        assert result.data.description == "Oracle WMS entity: company"

    @pytest.mark.asyncio
    async def test_discover_single_entity_http_error(self) -> None:
        """Test single entity discovery with HTTP error."""
        mock_response = Mock()
        mock_response.status_code = 404

        self.mock_api_client.get.return_value = FlextResult[None].ok(mock_response)

        result = await self.discovery._discover_single_entity("nonexistent")

        assert result.success
        assert result.data.name == "nonexistent"

    @pytest.mark.asyncio
    async def test_extract_entity_schema_from_results(self) -> None:
        """Test schema extraction from results array."""
        response_data = {
            "results": [
                {
                    "id": 1,
                    "name": "Test Company",
                    "status": "active",
                    "score": 95.5,
                    "is_verified": True,
                },
            ],
        }

        result = await self.discovery._extract_entity_schema(
            response_data,
            "company",
            "/api/company",
        )

        assert result.success
        assert result.data.name == "company"
        assert result.data.fields is not None
        assert "id" in result.data.fields
        assert "name" in result.data.fields
        assert result.data.fields["id"]["type"] == "integer"
        assert result.data.fields["name"]["type"] == "string"
        assert result.data.fields["score"]["type"] == "number"
        assert result.data.fields["is_verified"]["type"] == "boolean"

    @pytest.mark.asyncio
    async def test_extract_entity_schema_from_data(self) -> None:
        """Test schema extraction from data array."""
        response_data = {
            "data": [{"facility_code": "FAC001", "location": {"city": "New York"}}],
        }

        result = await self.discovery._extract_entity_schema(
            response_data,
            "facility",
            "/api/facility",
        )

        assert result.success
        assert result.data.fields["facility_code"]["type"] == "string"
        assert result.data.fields["location"]["type"] == "object"

    @pytest.mark.asyncio
    async def test_extract_entity_schema_no_sample_data(self) -> None:
        """Test schema extraction with no sample data."""
        response_data = {"results": []}

        result = await self.discovery._extract_entity_schema(
            response_data,
            "empty",
            "/api/empty",
        )

        assert result.success
        assert result.data.fields == {}

    def test_infer_field_type_all_types(self) -> None:
        """Test field type inference for all supported types."""
        assert self.discovery._infer_field_type(None) == "string"
        assert self.discovery._infer_field_type(True) == "boolean"
        assert self.discovery._infer_field_type(False) == "boolean"
        assert self.discovery._infer_field_type(42) == "integer"
        assert self.discovery._infer_field_type(math.pi) == "number"
        assert self.discovery._infer_field_type("text") == "string"
        assert self.discovery._infer_field_type({"key": "value"}) == "object"
        assert self.discovery._infer_field_type([1, 2, 3]) == "object"

    def test_filter_entities_include_patterns(self) -> None:
        """Test entity filtering with include patterns."""
        entities = [
            FlextOracleWmsEntity(
                name="company",
                endpoint="/api/company",
                description="Company",
            ),
            FlextOracleWmsEntity(
                name="facility",
                endpoint="/api/facility",
                description="Facility",
            ),
            FlextOracleWmsEntity(name="item", endpoint="/api/item", description="Item"),
            FlextOracleWmsEntity(
                name="order",
                endpoint="/api/order",
                description="Order",
            ),
        ]

        include_patterns = ["comp.*", "fac.*"]

        result = self.discovery._filter_entities(
            entities,
            include_patterns=include_patterns,
        )

        assert len(result) == 2
        assert all(entity.name in {"company", "facility"} for entity in result)

    def test_filter_entities_exclude_patterns(self) -> None:
        """Test entity filtering with exclude patterns."""
        entities = [
            FlextOracleWmsEntity(
                name="company",
                endpoint="/api/company",
                description="Company",
            ),
            FlextOracleWmsEntity(
                name="test_entity",
                endpoint="/api/test",
                description="Test",
            ),
            FlextOracleWmsEntity(
                name="temp_data",
                endpoint="/api/temp",
                description="Temp",
            ),
        ]

        exclude_patterns = ["test_.*", "temp_.*"]

        result = self.discovery._filter_entities(
            entities,
            exclude_patterns=exclude_patterns,
        )

        assert len(result) == 1
        assert result[0].name == "company"

    def test_filter_entities_both_patterns(self) -> None:
        """Test entity filtering with both include and exclude patterns."""
        entities = [
            FlextOracleWmsEntity(
                name="company",
                endpoint="/api/company",
                description="Company",
            ),
            FlextOracleWmsEntity(
                name="company_test",
                endpoint="/api/company_test",
                description="Company Test",
            ),
            FlextOracleWmsEntity(
                name="facility",
                endpoint="/api/facility",
                description="Facility",
            ),
            FlextOracleWmsEntity(name="item", endpoint="/api/item", description="Item"),
        ]

        include_patterns = ["comp.*"]
        exclude_patterns = [".*_test"]

        result = self.discovery._filter_entities(
            entities,
            include_patterns,
            exclude_patterns,
        )

        assert len(result) == 1
        assert result[0].name == "company"

    def test_filter_entities_case_insensitive(self) -> None:
        """Test entity filtering is case insensitive."""
        entities = [
            FlextOracleWmsEntity(
                name="Company",
                endpoint="/api/company",
                description="Company",
            ),
            FlextOracleWmsEntity(
                name="FACILITY",
                endpoint="/api/facility",
                description="Facility",
            ),
        ]

        include_patterns = ["comp.*"]

        result = self.discovery._filter_entities(
            entities,
            include_patterns=include_patterns,
        )

        assert len(result) == 1
        assert result[0].name == "Company"

    def test_filter_entities_no_patterns(self) -> None:
        """Test entity filtering with no patterns returns all entities."""
        entities = [
            FlextOracleWmsEntity(
                name="company",
                endpoint="/api/company",
                description="Company",
            ),
            FlextOracleWmsEntity(
                name="facility",
                endpoint="/api/facility",
                description="Facility",
            ),
        ]

        result = self.discovery._filter_entities(entities)

        assert len(result) == 2
        assert result == entities

    def test_deduplicate_entities(self) -> None:
        """Test entity deduplication by name."""
        entities = [
            FlextOracleWmsEntity(
                name="company",
                endpoint="/api/company1",
                description="Company 1",
            ),
            FlextOracleWmsEntity(
                name="facility",
                endpoint="/api/facility",
                description="Facility",
            ),
            FlextOracleWmsEntity(
                name="company",
                endpoint="/api/company2",
                description="Company 2",
            ),
            FlextOracleWmsEntity(name="item", endpoint="/api/item", description="Item"),
            FlextOracleWmsEntity(
                name="facility",
                endpoint="/api/facility2",
                description="Facility 2",
            ),
        ]

        result = self.discovery._deduplicate_entities(entities)

        assert len(result) == 3
        unique_names = {entity.name for entity in result}
        assert unique_names == {"company", "facility", "item"}

        # Should keep first occurrence
        company_entity = next(e for e in result if e.name == "company")
        assert company_entity.endpoint == "/api/company1"

    def test_deduplicate_entities_no_duplicates(self) -> None:
        """Test entity deduplication with no duplicates."""
        entities = [
            FlextOracleWmsEntity(
                name="company",
                endpoint="/api/company",
                description="Company",
            ),
            FlextOracleWmsEntity(
                name="facility",
                endpoint="/api/facility",
                description="Facility",
            ),
        ]

        result = self.discovery._deduplicate_entities(entities)

        assert len(result) == 2
        assert result == entities

    @pytest.mark.asyncio
    async def test_get_cached_discovery_not_implemented(self) -> None:
        """Test cached discovery returns not implemented."""
        result = await self.discovery._get_cached_discovery("test_key")

        assert result.is_failure
        assert "Cache not implemented" in result.error

    @pytest.mark.asyncio
    async def test_cache_discovery_result_no_op(self) -> None:
        """Test cache discovery result is no-op."""
        mock_result = FlextOracleWmsDiscoveryResult(
            entities=[],
            total_count=0,
            timestamp="2024-01-01T00:00:00",
            has_errors=False,
            errors=[],
        )

        # Should not raise any errors
        await self.discovery._cache_discovery_result("test_key", mock_result)

    @pytest.mark.asyncio
    async def test_get_cached_entity_not_implemented(self) -> None:
        """Test cached entity returns not implemented."""
        result = await self.discovery._get_cached_entity("test_key")

        assert result.is_failure
        assert "Cache not implemented" in result.error

    @pytest.mark.asyncio
    async def test_cache_entity_result_no_op(self) -> None:
        """Test cache entity result is no-op."""
        mock_entity = FlextOracleWmsEntity(
            name="test",
            endpoint="/api/test",
            description="Test entity",
        )

        # Should not raise any errors
        await self.discovery._cache_entity_result("test_key", mock_entity)


class TestFactoryFunction:
    """Test factory function for entity discovery."""

    def test_create_entity_discovery_default(self) -> None:
        """Test creating entity discovery with default parameters."""
        mock_api_client = AsyncMock()

        discovery = flext_oracle_wms_create_entity_discovery(
            api_client=mock_api_client,
            environment="prod",
        )

        assert discovery.api_client == mock_api_client
        assert discovery.environment == "prod"
        assert discovery.cache_manager is not None
        assert discovery.cache_manager["enabled"] is True
        assert discovery.cache_manager["ttl"] == 300

    def test_create_entity_discovery_custom(self) -> None:
        """Test creating entity discovery with custom parameters."""
        mock_api_client = AsyncMock()

        discovery = flext_oracle_wms_create_entity_discovery(
            api_client=mock_api_client,
            environment="test",
            enable_caching=True,
            cache_ttl=600,
        )

        assert discovery.environment == "test"
        assert discovery.cache_manager["ttl"] == 600

    def test_create_entity_discovery_no_cache(self) -> None:
        """Test creating entity discovery without caching."""
        mock_api_client = AsyncMock()

        discovery = flext_oracle_wms_create_entity_discovery(
            api_client=mock_api_client,
            environment="dev",
            enable_caching=False,
        )

        assert discovery.cache_manager is None


class TestErrorHandling:
    """Test error handling throughout discovery module."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.mock_api_client = AsyncMock()
        self.discovery = FlextOracleWmsEntityDiscovery(
            api_client=self.mock_api_client,
            environment="test",
        )

    @pytest.mark.asyncio
    async def test_discover_all_entities_exception(self) -> None:
        """Test discover_all_entities handles exceptions."""
        with patch.object(self.discovery, "_perform_discovery") as mock_perform:
            mock_perform.side_effect = Exception("Unexpected error")

            # Should raise exception via handle_operation_exception
            with pytest.raises(Exception):
                await self.discovery.discover_all_entities()

    @pytest.mark.asyncio
    async def test_discover_entity_schema_exception(self) -> None:
        """Test discover_entity_schema handles exceptions."""
        with patch.object(self.discovery, "_discover_single_entity") as mock_discover:
            mock_discover.side_effect = Exception("Schema error")

            # Should raise exception via handle_operation_exception
            with pytest.raises(Exception):
                await self.discovery.discover_entity_schema("test")

    @pytest.mark.asyncio
    async def test_parse_entities_response_exception(self) -> None:
        """Test _parse_entities_response handles exceptions."""
        with patch.object(
            self.discovery,
            "_extract_entity_list_from_response",
        ) as mock_extract:
            mock_extract.side_effect = Exception("Parse error")

            # Should raise exception via handle_operation_exception
            with pytest.raises(Exception):
                await self.discovery._parse_entities_response({}, "/api/test")

    @pytest.mark.asyncio
    async def test_extract_entity_schema_exception(self) -> None:
        """Test _extract_entity_schema handles exceptions."""
        # Mock the method to raise an exception during field inference
        with patch.object(self.discovery, "_infer_field_type") as mock_infer:
            mock_infer.side_effect = Exception("Type inference error")

            response_data = {"results": [{"id": 1, "name": "test"}]}

            # Should raise exception via handle_operation_exception
            with pytest.raises(Exception):
                await self.discovery._extract_entity_schema(
                    response_data,
                    "test",
                    "/api/test",
                )


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.mock_api_client = AsyncMock()
        self.discovery = FlextOracleWmsEntityDiscovery(
            api_client=self.mock_api_client,
            environment="",  # Edge case: empty environment
        )

    def test_empty_environment_endpoint_generation(self) -> None:
        """Test endpoint generation with empty environment."""
        # Should still generate endpoints with empty environment
        assert len(self.discovery.discovery_endpoints) > 0
        assert all(
            endpoint.startswith("/") for endpoint in self.discovery.discovery_endpoints
        )

    @pytest.mark.asyncio
    async def test_discover_all_entities_empty_response(self) -> None:
        """Test discovery with empty response from all endpoints."""
        with patch.object(
            EndpointDiscoveryStrategy,
            "execute_discovery_step",
        ) as mock_step:
            mock_step.return_value = FlextResult[None].ok(False)

            result = await self.discovery.discover_all_entities()

            assert result.success
            assert result.data.total_count == 0
            assert len(result.data.entities) == 0

    def test_filter_entities_empty_patterns(self) -> None:
        """Test filtering with empty pattern lists."""
        entities = [
            FlextOracleWmsEntity(
                name="company",
                endpoint="/api/company",
                description="Company",
            ),
        ]

        result = self.discovery._filter_entities(
            entities,
            include_patterns=[],
            exclude_patterns=[],
        )

        assert len(result) == 1
        assert result == entities

    def test_create_entity_from_metadata_edge_cases(self) -> None:
        """Test entity creation with edge case metadata."""
        # Empty metadata
        assert self.discovery._create_entity_from_metadata({}) is None

        # Metadata with empty name
        assert self.discovery._create_entity_from_metadata({"name": ""}) is None

        # Metadata with None values
        metadata = {
            "name": "test",
            "endpoint": None,
            "description": None,
            "primary_key": None,
            "replication_key": None,
            "supports_incremental": None,
        }

        entity = self.discovery._create_entity_from_metadata(metadata)
        assert entity is not None
        assert entity.name == "test"
