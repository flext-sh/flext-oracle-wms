# Python Module Organization & Semantic Patterns

**FLEXT Oracle WMS Module Architecture & Best Practices for Enterprise Integration**

This document defines the module organization patterns for flext-oracle-wms, following FLEXT ecosystem standards established by flext-core. It provides comprehensive guidance for Clean Architecture implementation, Domain-Driven Design patterns, and Oracle WMS-specific integration requirements.

---

## 🏗️ **Module Architecture Overview**

FLEXT Oracle WMS implements a **layered Clean Architecture** that integrates Oracle WMS Cloud REST APIs with FLEXT ecosystem patterns. The module structure supports enterprise-grade Oracle integration while maintaining consistency with the 32-project FLEXT ecosystem.

### **Core Design Principles**

1. **FLEXT Ecosystem Consistency**: All patterns align with flext-core standards
2. **Oracle WMS Specialization**: Domain-specific Oracle WMS patterns and optimizations
3. **Clean Architecture Compliance**: Clear separation of infrastructure, application, and domain concerns
4. **Railway-Oriented Programming**: FlextResult[T] threading through all Oracle operations
5. **Enterprise Integration**: Production-ready patterns for Oracle WMS Cloud connectivity

---

## 📁 **Current Module Structure & Assessment**

### **Current Implementation (Needs Refactoring)**

```python
src/flext_oracle_wms/
├── __init__.py              # ✅ Public API gateway (comprehensive exports)
├── client.py                # 🔄 Mixed concerns (Infrastructure + Application)
├── api_catalog.py           # ✅ Infrastructure Layer (API endpoint definitions)
├── authentication.py        # ✅ Infrastructure Layer (Oracle WMS auth patterns)
├── config.py               # ✅ Infrastructure Layer (Pydantic configuration)
├── discovery.py            # 🔄 Mixed concerns (Application + Infrastructure)
├── cache.py                # ✅ Infrastructure Layer (Enterprise caching)
├── dynamic.py              # 🔄 Application Layer (schema processing)
├── filtering.py            # 🔄 Application Layer (query building)
├── flattening.py           # 🔄 Application Layer (data transformation)
├── helpers.py              # ✅ Infrastructure Layer (utility functions)
├── models.py               # ⚠️ Anemic Domain Models (needs enhancement)
├── types.py                # ✅ Domain Layer (type definitions)
├── constants.py            # ✅ Domain Layer (Oracle WMS constants)
└── exceptions.py           # ✅ Domain Layer (exception hierarchy)
```

**Legend**: ✅ Correct | 🔄 Mixed Concerns | ⚠️ Needs Enhancement

### **Architecture Compliance Assessment**

| Layer              | Current State | Target State | Critical Issues                       |
| ------------------ | ------------- | ------------ | ------------------------------------- |
| **Domain**         | 40%           | 90%          | Anemic models, missing business logic |
| **Application**    | 30%           | 90%          | Mixed with infrastructure concerns    |
| **Infrastructure** | 80%           | 95%          | Well-separated technical concerns     |
| **Presentation**   | 60%           | 90%          | Client interface needs separation     |

---

## 🎯 **Target Module Structure (Clean Architecture)**

### **Domain Layer** - Oracle WMS Business Logic

```python
src/flext_oracle_wms/
├── domain/                           # Domain Layer
│   ├── __init__.py                   # Domain exports
│   ├── entities/                     # Business Entities
│   │   ├── __init__.py               # Entity exports
│   │   ├── inventory_item.py         # Rich inventory domain entity
│   │   ├── shipment.py               # Shipment aggregate root
│   │   ├── warehouse_location.py     # Location entity with business rules
│   │   ├── order.py                  # Order management entity
│   │   └── wms_entity_base.py        # Base WMS entity patterns
│   ├── value_objects/               # Value Objects
│   │   ├── __init__.py               # Value object exports
│   │   ├── item_number.py            # WMS item number with validation
│   │   ├── quantity.py               # Inventory quantity with business rules
│   │   ├── location_code.py          # Warehouse location identifier
│   │   ├── organization_code.py      # Oracle organization identifier
│   │   └── tracking_number.py        # Shipment tracking with validation
│   ├── repositories/                # Repository Interfaces (Abstract)
│   │   ├── __init__.py               # Repository interface exports
│   │   ├── wms_repository.py         # Core WMS data repository interface
│   │   ├── inventory_repository.py   # Inventory-specific repository
│   │   ├── shipment_repository.py    # Shipment repository interface
│   │   └── cache_repository.py       # Cache abstraction interface
│   ├── services/                    # Domain Services
│   │   ├── __init__.py               # Domain service exports
│   │   ├── inventory_service.py      # Inventory business logic
│   │   ├── shipment_service.py       # Shipment orchestration
│   │   ├── warehouse_service.py      # Warehouse operations
│   │   └── sync_service.py           # Cross-system synchronization
│   └── events/                      # Domain Events
│       ├── __init__.py               # Event exports
│       ├── inventory_events.py       # Inventory domain events
│       ├── shipment_events.py        # Shipment lifecycle events
│       └── warehouse_events.py       # Warehouse operation events
```

**Responsibility**: Pure business logic with Oracle WMS domain rules and invariants.

**Domain Entity Pattern**:

```python
from flext_core import FlextEntity, FlextResult
from flext_oracle_wms.domain.value_objects import ItemNumber, Quantity, LocationCode

class InventoryItem(FlextEntity):
    """Rich inventory domain entity with business behaviors."""

    def __init__(
        self,
        item_number: ItemNumber,
        quantity: Quantity,
        location: LocationCode,
        organization_code: str
    ):
        super().__init__()
        self._item_number = item_number
        self._quantity = quantity
        self._location = location
        self._organization_code = organization_code
        self._reserved_quantity = Quantity(0)

    def adjust_quantity(self, adjustment: QuantityAdjustment) -> FlextResult[None]:
        """Business logic for inventory quantity adjustments."""
        if not self._can_adjust(adjustment):
            return FlextResult[None].fail("Insufficient quantity for adjustment")

        self._quantity = self._quantity.add(adjustment.delta)
        self._record_domain_event(InventoryAdjusted(
            item_number=self._item_number,
            adjustment=adjustment,
            new_quantity=self._quantity
        ))
        return FlextResult[None].ok(None)

    def reserve_quantity(self, reservation: QuantityReservation) -> FlextResult[None]:
        """Reserve inventory for order fulfillment."""
        available = self._quantity.subtract(self._reserved_quantity)
        if available.value < reservation.quantity.value:
            return FlextResult[None].fail("Insufficient available quantity")

        self._reserved_quantity = self._reserved_quantity.add(reservation.quantity)
        self._record_domain_event(QuantityReserved(
            item_number=self._item_number,
            reservation=reservation
        ))
        return FlextResult[None].ok(None)

    def can_fulfill_order(self, required_quantity: Quantity) -> bool:
        """Domain business rule for order fulfillment capability."""
        available = self._quantity.subtract(self._reserved_quantity)
        return available.value >= required_quantity.value
```

### **Application Layer** - Use Cases and Orchestration

```python
src/flext_oracle_wms/
├── application/                      # Application Layer
│   ├── __init__.py                   # Application exports
│   ├── use_cases/                   # Use Cases
│   │   ├── __init__.py               # Use case exports
│   │   ├── discover_entities.py     # Entity discovery use case
│   │   ├── query_inventory.py       # Inventory query use case
│   │   ├── sync_inventory.py        # Inventory synchronization use case
│   │   ├── process_shipment.py      # Shipment processing use case
│   │   └── generate_catalog.py      # Singer catalog generation use case
│   ├── services/                    # Application Services
│   │   ├── __init__.py               # Application service exports
│   │   ├── wms_orchestrator.py      # WMS operation orchestration
│   │   ├── schema_processor.py      # Dynamic schema processing
│   │   ├── data_transformer.py      # Data transformation service
│   │   └── catalog_generator.py     # Singer catalog generation
│   ├── dtos/                       # Data Transfer Objects
│   │   ├── __init__.py               # DTO exports
│   │   ├── entity_dto.py            # Entity data transport
│   │   ├── query_dto.py             # Query request/response DTOs
│   │   ├── sync_dto.py              # Synchronization DTOs
│   │   └── catalog_dto.py           # Singer catalog DTOs
│   └── commands/                    # CQRS Command Patterns
│       ├── __init__.py               # Command exports
│       ├── inventory_commands.py     # Inventory operation commands
│       ├── discovery_commands.py    # Entity discovery commands
│       └── sync_commands.py         # Synchronization commands
```

**Responsibility**: Orchestrate domain operations and coordinate infrastructure services.

**Use Case Pattern**:

```python
from flext_core import FlextResult
from flext_oracle_wms.domain.repositories import InventoryRepository
from flext_oracle_wms.application.dtos import QueryInventoryRequest, QueryInventoryResponse

class QueryInventoryUseCase:
    """Query inventory data with business rule application."""

    def __init__(
        self,
        inventory_repository: InventoryRepository,
        logger: FlextLogger
    ):
        self._inventory_repository = inventory_repository
        self._logger = logger

    async def execute(
        self,
        request: QueryInventoryRequest
    ) -> FlextResult[QueryInventoryResponse]:
        """Execute inventory query with business validation."""

        self._logger.info(
            "Starting inventory query",
            correlation_id=request.correlation_id,
            entity_name=request.entity_name
        )

        # Validate query parameters using domain rules
        validation_result = self._validate_query(request)
        if validation_result.is_failure:
            return validation_result

        # Execute repository query
        inventory_result = await self._inventory_repository.query_inventory(
            entity_name=request.entity_name,
            filters=request.filters,
            organization_code=request.organization_code
        )

        if inventory_result.is_failure:
            self._logger.error(
                "Inventory query failed",
                correlation_id=request.correlation_id,
                error=inventory_result.error
            )
            return FlextResult[None].fail(f"Query failed: {inventory_result.error}")

        # Transform to response DTO
        inventory_items = inventory_result.data
        response = QueryInventoryResponse(
            items=[item.to_dto() for item in inventory_items],
            total_count=len(inventory_items),
            query_metadata=request.to_metadata()
        )

        self._logger.info(
            "Inventory query completed",
            correlation_id=request.correlation_id,
            items_found=len(inventory_items)
        )

        return FlextResult[None].ok(response)
```

### **Infrastructure Layer** - External System Integration

```python
src/flext_oracle_wms/
├── infrastructure/                   # Infrastructure Layer
│   ├── __init__.py                   # Infrastructure exports
│   ├── api/                         # External API Integration
│   │   ├── __init__.py               # API client exports
│   │   ├── wms_api_client.py         # Oracle WMS REST API client
│   │   ├── authentication/          # Authentication Providers
│   │   │   ├── __init__.py           # Auth provider exports
│   │   │   ├── basic_auth.py         # Basic authentication
│   │   │   ├── bearer_auth.py        # Bearer token authentication
│   │   │   └── api_key_auth.py       # API key authentication
│   │   ├── endpoints/               # API Endpoint Definitions
│   │   │   ├── __init__.py           # Endpoint exports
│   │   │   ├── inventory_endpoints.py # Inventory API endpoints
│   │   │   ├── shipment_endpoints.py  # Shipment API endpoints
│   │   │   └── discovery_endpoints.py # Entity discovery endpoints
│   │   └── response_mappers/        # API Response Mapping
│   │       ├── __init__.py           # Mapper exports
│   │       ├── inventory_mapper.py   # Inventory response mapping
│   │       └── entity_mapper.py      # Entity response mapping
│   ├── repositories/               # Repository Implementations
│   │   ├── __init__.py               # Repository implementation exports
│   │   ├── wms_repository_impl.py    # WMS repository implementation
│   │   ├── inventory_repository_impl.py # Inventory repository impl
│   │   ├── cache_repository_impl.py  # Cache repository implementation
│   │   └── oracle_db_repository.py   # Oracle database repository
│   ├── cache/                      # Caching Infrastructure
│   │   ├── __init__.py               # Cache exports
│   │   ├── cache_manager.py          # Cache management
│   │   ├── cache_strategies.py       # Caching strategies
│   │   └── redis_cache.py            # Redis cache implementation
│   ├── config/                     # Configuration Management
│   │   ├── __init__.py               # Config exports
│   │   ├── settings.py               # Main settings
│   │   ├── environment.py            # Environment configuration
│   │   └── validation.py            # Configuration validation
│   └── monitoring/                 # Observability Infrastructure
│       ├── __init__.py               # Monitoring exports
│       ├── metrics.py                # Custom metrics collection
│       ├── health_checks.py          # Health check implementations
│       └── tracing.py                # Distributed tracing setup
```

**Responsibility**: Handle external system integration, persistence, and technical concerns.

**Repository Implementation Pattern**:

```python
from flext_core import FlextResult
from flext_oracle_wms.domain.repositories import InventoryRepository
from flext_oracle_wms.domain.entities import InventoryItem
from flext_oracle_wms.infrastructure.api import WmsApiClient

class InventoryRepositoryImpl(InventoryRepository):
    """Inventory repository implementation using Oracle WMS API."""

    def __init__(
        self,
        api_client: WmsApiClient,
        cache_repository: CacheRepository,
        logger: FlextLogger
    ):
        self._api_client = api_client
        self._cache = cache_repository
        self._logger = logger

    async def query_inventory(
        self,
        entity_name: str,
        filters: Dict[str, Any],
        organization_code: str
    ) -> FlextResult[List[InventoryItem]]:
        """Query inventory with caching and error handling."""

        cache_key = self._build_cache_key(entity_name, filters, organization_code)

        # Try cache first
        cached_result = await self._cache.get(cache_key)
        if cached_result.success and cached_result.data:
            self._logger.debug("Inventory data retrieved from cache", cache_key=cache_key)
            return FlextResult[None].ok(cached_result.data)

        # Query Oracle WMS API
        api_result = await self._api_client.query_entity(
            entity_name=entity_name,
            filters=filters,
            organization_code=organization_code
        )

        if api_result.is_failure:
            return FlextResult[None].fail(f"API query failed: {api_result.error}")

        # Map API response to domain entities
        inventory_items = []
        for item_data in api_result.data:
            entity_result = InventoryItem.from_api_response(item_data)
            if entity_result.success:
                inventory_items.append(entity_result.data)
            else:
                self._logger.warning(
                    "Failed to map inventory item",
                    item_data=item_data,
                    error=entity_result.error
                )

        # Cache successful results
        await self._cache.set(cache_key, inventory_items, ttl=300)

        return FlextResult[None].ok(inventory_items)
```

### **Presentation Layer** - Client Interface

```python
src/flext_oracle_wms/
├── presentation/                     # Presentation Layer
│   ├── __init__.py                   # Presentation exports
│   ├── client/                      # Client Interface
│   │   ├── __init__.py               # Client exports
│   │   ├── wms_client.py             # Main client interface
│   │   ├── client_factory.py         # Client factory patterns
│   │   └── mock_client.py            # Mock client for testing
│   ├── dto_mappers/                # DTO Mapping
│   │   ├── __init__.py               # Mapper exports
│   │   ├── entity_mapper.py          # Entity to DTO mapping
│   │   ├── response_mapper.py        # Response DTO mapping
│   │   └── request_mapper.py         # Request DTO mapping
│   └── validators/                 # Input Validation
│       ├── __init__.py               # Validator exports
│       ├── request_validator.py      # Request validation
│       └── config_validator.py       # Configuration validation
```

**Responsibility**: Provide clean client interface and handle input/output transformation.

**Client Interface Pattern**:

```python
from flext_core import FlextResult
from flext_oracle_wms.application.use_cases import (
    DiscoverEntitiesUseCase,
    QueryInventoryUseCase
)
from flext_oracle_wms.presentation.dto_mappers import EntityMapper, ResponseMapper

class FlextOracleWmsClient:
    """Enterprise Oracle WMS client with Clean Architecture patterns."""

    def __init__(
        self,
        config: FlextOracleWmsClientConfig,
        container: FlextContainer
    ):
        self._config = config
        self._discover_entities_use_case = container.resolve(DiscoverEntitiesUseCase)
        self._query_inventory_use_case = container.resolve(QueryInventoryUseCase)
        self._entity_mapper = container.resolve(EntityMapper)
        self._response_mapper = container.resolve(ResponseMapper)

    async def discover_entities(
        self,
        organization_code: Optional[str] = None
    ) -> FlextResult[List[WmsEntity]]:
        """Discover available WMS entities with proper error handling."""

        request = DiscoverEntitiesRequest(
            organization_code=organization_code or self._config.organization_code,
            correlation_id=self._generate_correlation_id()
        )

        use_case_result = await self._discover_entities_use_case.execute(request)

        if use_case_result.is_failure:
            return FlextResult[None].fail(use_case_result.error)

        # Map to presentation DTOs
        entities = [
            self._entity_mapper.to_dto(entity)
            for entity in use_case_result.data.entities
        ]

        return FlextResult[None].ok(entities)

    async def query_inventory_data(
        self,
        entity_name: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> FlextResult[List[Dict[str, Any]]]:
        """Query inventory data with business rule validation."""

        request = QueryInventoryRequest(
            entity_name=entity_name,
            filters=filters or {},
            organization_code=self._config.organization_code,
            correlation_id=self._generate_correlation_id()
        )

        use_case_result = await self._query_inventory_use_case.execute(request)

        if use_case_result.is_failure:
            return FlextResult[None].fail(use_case_result.error)

        # Map to API response format
        inventory_data = [
            self._response_mapper.inventory_item_to_dict(item)
            for item in use_case_result.data.items
        ]

        return FlextResult[None].ok(inventory_data)
```

---

## 🎯 **Semantic Naming Conventions**

### **Public API Naming (FlextOracleWmsXxx)**

All public exports use the `FlextOracleWms` prefix for namespace clarity:

```python
# Core client and configuration
FlextOracleWmsClient              # Main client interface
FlextOracleWmsClientConfig        # Client configuration
FlextOracleWmsModuleConfig        # Module-level configuration

# Authentication and API
FlextOracleWmsAuthenticator       # Authentication provider
FlextOracleWmsApiClient           # Low-level API client
FlextOracleWmsApiEndpoint         # API endpoint definition
FlextOracleWmsApiCategory         # API category grouping

# Domain entities and value objects
FlextOracleWmsEntity              # Base WMS entity
FlextOracleWmsInventoryItem       # Inventory domain entity
FlextOracleWmsShipment            # Shipment aggregate root
FlextOracleWmsItemNumber          # Item number value object
FlextOracleWmsQuantity            # Quantity value object

# Discovery and processing
FlextOracleWmsEntityDiscovery     # Entity discovery service
FlextOracleWmsDynamicProcessor    # Dynamic schema processor
FlextOracleWmsFilter              # Query filter builder

# Caching and utilities
FlextOracleWmsCacheManager        # Enterprise caching
FlextOracleWmsResponseMapper      # Response transformation
```

**Rationale**: Clear namespace prevents conflicts with other Oracle libraries and FLEXT ecosystem projects.

### **Module-Level Naming**

```python
# Domain layer modules
inventory_item.py             # InventoryItem entity and related patterns
shipment.py                  # Shipment aggregate root
item_number.py               # ItemNumber value object
quantity.py                  # Quantity value object with business rules

# Application layer modules
discover_entities.py         # DiscoverEntitiesUseCase
query_inventory.py          # QueryInventoryUseCase
wms_orchestrator.py         # WmsOrchestratorService

# Infrastructure layer modules
wms_api_client.py           # Oracle WMS API client implementation
inventory_repository_impl.py # Inventory repository implementation
cache_manager.py            # Cache management implementation
```

**Pattern**: Clear, descriptive names indicating primary responsibility and architectural layer.

### **Internal Naming (\_xxx)**

```python
# Internal implementation modules
_api_client_base.py         # Internal API client base
_cache_strategies.py        # Internal caching strategies
_response_parser.py         # Internal response parsing

# Internal functions and classes
def _validate_organization_code(code: str) -> bool:
    """Internal organization code validation"""

def _build_cache_key(*args: Any) -> str:
    """Internal cache key generation"""

class _InternalApiResponse:
    """Internal API response wrapper"""
```

**Rule**: Underscore prefix indicates internal implementation not exposed in public API.

---

## 📦 **Import Patterns & Best Practices**

### **Recommended Import Styles**

#### **1. Primary Pattern (Recommended for Users)**

```python
# Import from main package - gets everything needed
from flext_oracle_wms import (
    FlextOracleWmsClient,
    FlextOracleWmsClientConfig,
    FlextOracleWmsEntity
)

# Use patterns directly
config = FlextOracleWmsClientConfig(
    base_url="https://wms.oraclecloud.com",
    username="user",
    password="pass"
)
client = FlextOracleWmsClient(config)
```

#### **2. Layer-Specific Pattern (For Advanced Usage)**

```python
# Import from specific layers for clarity
from flext_oracle_wms.domain.entities import InventoryItem
from flext_oracle_wms.application.use_cases import QueryInventoryUseCase
from flext_oracle_wms.infrastructure.repositories import InventoryRepositoryImpl

# Explicit layer separation
```

#### **3. FLEXT Integration Pattern**

```python
# Import FLEXT foundation with Oracle WMS
from flext_core import FlextResult, FlextContainer, FlextLogger
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsClientConfig

# Integrated usage with FLEXT patterns
async def process_wms_data(
    container: FlextContainer,
    logger: FlextLogger
) -> FlextResult[List[InventoryItem]]:
    wms_client = container.resolve(FlextOracleWmsClient)
    result = await wms_client.query_inventory_data("INVENTORY")

    if result.success:
        logger.info("Successfully processed WMS data", count=len(result.data))
    return result
```

### **Anti-Patterns (Forbidden)**

```python
# ❌ Don't import everything
from flext_oracle_wms import *

# ❌ Don't import internal modules
from flext_oracle_wms.infrastructure.api._api_client_base import _InternalClient

# ❌ Don't bypass layers inappropriately
from flext_oracle_wms.infrastructure.repositories import InventoryRepositoryImpl
# Instead use dependency injection through application layer

# ❌ Don't alias core types
from flext_oracle_wms import FlextOracleWmsClient as WmsClient  # Confusing
```

---

## 🏛️ **Oracle WMS Architectural Patterns**

### **Oracle WMS Domain Modeling**

```python
# Oracle WMS specific domain patterns
from flext_core import FlextEntity, FlextValueObject, FlextResult

class OracleOrganization(FlextValueObject):
    """Oracle organization with validation."""
    code: str
    name: str

    def __post_init__(self):
        if not self.code or len(self.code) > 3:
            raise ValueError("Invalid organization code")

class WmsLocation(FlextEntity):
    """Warehouse location entity with Oracle WMS rules."""

    def __init__(
        self,
        location_code: str,
        subinventory: str,
        organization: OracleOrganization
    ):
        super().__init__()
        self._location_code = location_code
        self._subinventory = subinventory
        self._organization = organization
        self._is_picking_enabled = False
        self._is_receiving_enabled = False

    def enable_picking(self) -> FlextResult[None]:
        """Enable picking operations with business rules."""
        if not self._validate_picking_requirements():
            return FlextResult[None].fail("Location does not meet picking requirements")

        self._is_picking_enabled = True
        self._record_domain_event(LocationPickingEnabled(
            location_code=self._location_code,
            organization=self._organization
        ))
        return FlextResult[None].ok(None)

class InventoryTransaction(FlextEntity):
    """Oracle WMS inventory transaction."""

    def __init__(
        self,
        transaction_type: TransactionType,
        item_number: ItemNumber,
        quantity: Quantity,
        location: WmsLocation
    ):
        super().__init__()
        self._transaction_type = transaction_type
        self._item_number = item_number
        self._quantity = quantity
        self._location = location
        self._transaction_date = datetime.utcnow()
        self._status = TransactionStatus.PENDING

    def process(self) -> FlextResult[None]:
        """Process transaction with Oracle WMS business rules."""
        validation_result = self._validate_transaction()
        if validation_result.is_failure:
            return validation_result

        self._status = TransactionStatus.PROCESSED
        self._record_domain_event(TransactionProcessed(
            transaction_id=self.id,
            transaction_type=self._transaction_type,
            item_number=self._item_number,
            quantity=self._quantity
        ))
        return FlextResult[None].ok(None)
```

### **Oracle WMS API Integration Patterns**

```python
# Oracle WMS specific API patterns
from flext_oracle_wms.infrastructure.api import WmsApiClient
from flext_core import FlextResult

class OracleWmsApiClient(WmsApiClient):
    """Oracle WMS Cloud REST API client with enterprise patterns."""

    async def query_inventory_transactions(
        self,
        organization_code: str,
        date_from: datetime,
        date_to: datetime,
        transaction_types: List[str] = None
    ) -> FlextResult[List[Dict[str, Any]]]:
        """Query inventory transactions with Oracle-specific parameters."""

        # Build Oracle WMS specific query parameters
        params = {
            "OrganizationCode": organization_code,
            "TransactionDateFrom": date_from.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "TransactionDateTo": date_to.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "q": self._build_oracle_query_filter(transaction_types)
        }

        # Oracle WMS specific headers
        headers = {
            "REST-Framework-Version": "6",
            "Content-Type": "application/vnd.oracle.adf.resourceitem+json"
        }

        response = await self._http_client.get(
            "/inventoryTransactions",
            params=params,
            headers=headers
        )

        if response.status_code != 200:
            return FlextResult[None].fail(
                f"Oracle WMS API error: {response.status_code} - {response.text}"
            )

        # Parse Oracle ADF response format
        oracle_response = response.json()
        if "items" not in oracle_response:
            return FlextResult[None].fail("Invalid Oracle WMS response format")

        return FlextResult[None].ok(oracle_response["items"])

    def _build_oracle_query_filter(self, transaction_types: List[str]) -> str:
        """Build Oracle ADF query filter syntax."""
        if not transaction_types:
            return ""

        # Oracle ADF filter syntax: TransactionType in ('TYPE1','TYPE2')
        types_str = "','".join(transaction_types)
        return f"TransactionType in ('{types_str}')"
```

### **Singer Protocol Integration**

```python
# Singer protocol patterns for Oracle WMS
from singer import Catalog, Stream, Schema
from flext_oracle_wms.domain.entities import InventoryItem

async def generate_oracle_wms_catalog(
    client: FlextOracleWmsClient,
    organization_code: str
) -> FlextResult[Catalog]:
    """Generate Singer catalog for Oracle WMS entities."""

    entities_result = await client.discover_entities()
    if entities_result.is_failure:
        return FlextResult[None].fail(f"Entity discovery failed: {entities_result.error}")

    streams = []
    for entity in entities_result.data:
        # Get Oracle WMS specific schema
        schema_result = await client.get_entity_schema(entity.name)
        if schema_result.is_failure:
            continue

        # Convert Oracle schema to Singer schema
        singer_schema = _convert_oracle_schema_to_singer(schema_result.data)

        stream = Stream(
            tap_stream_id=f"{organization_code}_{entity.name}",
            schema=singer_schema,
            table_name=entity.name,
            metadata={
                "oracle-wms-entity": entity.name,
                "organization-code": organization_code,
                "replication-method": "INCREMENTAL",
                "replication-key": "LastUpdateDate",
                "inclusion": "available"
            }
        )
        streams.append(stream)

    catalog = Catalog(streams=streams)
    return FlextResult[None].ok(catalog)

def _convert_oracle_schema_to_singer(oracle_schema: Dict[str, Any]) -> Schema:
    """Convert Oracle WMS schema to Singer schema format."""
    properties = {}

    for field_name, field_info in oracle_schema.get("fields", {}).items():
        oracle_type = field_info.get("type", "string")
        singer_type = _map_oracle_type_to_singer(oracle_type)

        properties[field_name] = {
            "type": ["null", singer_type] if field_info.get("nullable", True) else [singer_type],
            "description": field_info.get("description", ""),
            "oracle-wms-type": oracle_type,
            "oracle-wms-precision": field_info.get("precision"),
            "oracle-wms-scale": field_info.get("scale")
        }

    return Schema.from_dict({
        "type": "object",
        "properties": properties
    })
```

---

## 🔄 **Railway-Oriented Programming with Oracle WMS**

### **Oracle WMS Operation Chaining**

```python
# Oracle WMS specific FlextResult patterns
async def sync_inventory_workflow(
    client: FlextOracleWmsClient,
    organization_code: str,
    target_system: TargetSystem
) -> FlextResult[SyncResult]:
    """Complete inventory synchronization workflow."""

    return await (
        # Discover Oracle WMS entities
        client.discover_entities()
        .flat_map_async(lambda entities: _filter_inventory_entities(entities))

        # Query inventory data for each entity
        .flat_map_async(lambda entities: _query_all_inventory_data(client, entities, organization_code))

        # Transform data for target system
        .flat_map_async(lambda inventory_data: _transform_for_target_system(inventory_data, target_system))

        # Validate business rules
        .flat_map_async(lambda transformed_data: _validate_business_rules(transformed_data))

        # Load to target system
        .flat_map_async(lambda validated_data: target_system.load_inventory(validated_data))

        # Generate sync report
        .map_async(lambda load_result: _generate_sync_report(load_result))
    )

async def _filter_inventory_entities(entities: List[WmsEntity]) -> FlextResult[List[WmsEntity]]:
    """Filter entities to inventory-related only."""
    inventory_entities = [
        entity for entity in entities
        if entity.category in ["INVENTORY", "INVENTORY_TRANSACTIONS", "STOCK_LEVELS"]
    ]

    if not inventory_entities:
        return FlextResult[None].fail("No inventory entities found")

    return FlextResult[None].ok(inventory_entities)

async def _query_all_inventory_data(
    client: FlextOracleWmsClient,
    entities: List[WmsEntity],
    organization_code: str
) -> FlextResult[Dict[str, List[Dict[str, Any]]]]:
    """Query data for all inventory entities."""

    inventory_data = {}

    for entity in entities:
        entity_result = await client.query_entity_data(
            entity_name=entity.name,
            filters={"OrganizationCode": organization_code}
        )

        if entity_result.is_failure:
            return FlextResult[None].fail(f"Failed to query {entity.name}: {entity_result.error}")

        inventory_data[entity.name] = entity_result.data

    return FlextResult[None].ok(inventory_data)
```

### **Error Aggregation for Oracle WMS**

```python
# Oracle WMS specific error handling
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class WmsValidationError:
    """Oracle WMS validation error."""
    entity_name: str
    field_name: str
    error_message: str
    oracle_error_code: Optional[str] = None

def validate_oracle_wms_data(
    entity_data: Dict[str, List[Dict[str, Any]]]
) -> FlextResult[Dict[str, List[Dict[str, Any]]]]:
    """Validate Oracle WMS data with error aggregation."""

    validation_errors: List[WmsValidationError] = []

    for entity_name, records in entity_data.items():
        for record_index, record in enumerate(records):
            # Validate required Oracle WMS fields
            if not record.get("OrganizationCode"):
                validation_errors.append(WmsValidationError(
                    entity_name=entity_name,
                    field_name="OrganizationCode",
                    error_message=f"Missing required OrganizationCode in record {record_index}"
                ))

            # Validate Oracle-specific business rules
            if entity_name == "INVENTORY" and not record.get("ItemNumber"):
                validation_errors.append(WmsValidationError(
                    entity_name=entity_name,
                    field_name="ItemNumber",
                    error_message=f"Missing required ItemNumber in inventory record {record_index}"
                ))

            # Validate Oracle date formats
            if "LastUpdateDate" in record:
                date_validation = _validate_oracle_date_format(record["LastUpdateDate"])
                if date_validation.is_failure:
                    validation_errors.append(WmsValidationError(
                        entity_name=entity_name,
                        field_name="LastUpdateDate",
                        error_message=f"Invalid Oracle date format: {date_validation.error}"
                    ))

    if validation_errors:
        error_summary = _format_validation_errors(validation_errors)
        return FlextResult[None].fail(f"Oracle WMS data validation failed: {error_summary}")

    return FlextResult[None].ok(entity_data)

def _format_validation_errors(errors: List[WmsValidationError]) -> str:
    """Format validation errors for reporting."""
    error_groups = {}
    for error in errors:
        entity_key = error.entity_name
        if entity_key not in error_groups:
            error_groups[entity_key] = []
        error_groups[entity_key].append(f"{error.field_name}: {error.error_message}")

    formatted_errors = []
    for entity_name, entity_errors in error_groups.items():
        formatted_errors.append(f"{entity_name}: {'; '.join(entity_errors)}")

    return "; ".join(formatted_errors)
```

---

## 🔧 **Configuration Patterns for Oracle WMS**

### **Oracle WMS Specific Configuration**

```python
from flext_core import FlextSettings
from typing import Optional, List
from enum import Enum

class OracleWmsAuthMethod(str, Enum):
    """Oracle WMS authentication methods."""
    BASIC = "basic"
    BEARER = "bearer"
    API_KEY = "api_key"
    OAUTH2 = "oauth2"

class OracleWmsEnvironment(str, Enum):
    """Oracle WMS environment types."""
    DEVELOPMENT = "dev"
    TEST = "test"
    STAGING = "stage"
    PRODUCTION = "prod"

class FlextOracleWmsAuthSettings(FlextSettings):
    """Oracle WMS authentication configuration."""
    method: OracleWmsAuthMethod = OracleWmsAuthMethod.BASIC
    username: Optional[str] = None
    password: Optional[str] = field(default=None, repr=False)
    bearer_token: Optional[str] = field(default=None, repr=False)
    api_key: Optional[str] = field(default=None, repr=False)
    oauth2_client_id: Optional[str] = None
    oauth2_client_secret: Optional[str] = field(default=None, repr=False)
    token_endpoint: Optional[str] = None

    class Config:
        env_prefix = "FLEXT_ORACLE_WMS_AUTH_"

class FlextOracleWmsPerformanceSettings(FlextSettings):
    """Oracle WMS performance configuration."""
    timeout_seconds: int = 30
    max_retries: int = 3
    retry_backoff_factor: float = 2.0
    connection_pool_size: int = 10
    max_connections_per_host: int = 5
    enable_http2: bool = True

    class Config:
        env_prefix = "FLEXT_ORACLE_WMS_PERF_"

class FlextOracleWmsCacheSettings(FlextSettings):
    """Oracle WMS caching configuration."""
    enabled: bool = True
    ttl_seconds: int = 300
    max_entries: int = 1000
    cache_type: str = "memory"  # memory, redis
    redis_url: Optional[str] = None

    class Config:
        env_prefix = "FLEXT_ORACLE_WMS_CACHE_"

class FlextOracleWmsClientConfig(FlextSettings):
    """Complete Oracle WMS client configuration."""

    # Connection settings
    base_url: str
    organization_code: str
    environment: OracleWmsEnvironment = OracleWmsEnvironment.DEVELOPMENT

    # Authentication
    auth: FlextOracleWmsAuthSettings = field(default_factory=FlextOracleWmsAuthSettings)

    # Performance
    performance: FlextOracleWmsPerformanceSettings = field(default_factory=FlextOracleWmsPerformanceSettings)

    # Caching
    cache: FlextOracleWmsCacheSettings = field(default_factory=FlextOracleWmsCacheSettings)

    # Oracle WMS specific settings
    api_version: str = "latest"
    supported_entities: List[str] = field(default_factory=lambda: [
        "INVENTORY", "INVENTORY_TRANSACTIONS", "SHIPMENTS",
        "ORDERS", "LOCATIONS", "ITEMS"
    ])

    # Debugging and monitoring
    enable_request_logging: bool = False
    enable_response_logging: bool = False
    enable_metrics: bool = True
    enable_tracing: bool = False

    class Config:
        env_prefix = "FLEXT_ORACLE_WMS_"
        env_nested_delimiter = "__"
        env_file = ".env"

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == OracleWmsEnvironment.PRODUCTION

    @property
    def full_auth_config(self) -> Dict[str, Any]:
        """Get complete authentication configuration."""
        return {
            "method": self.auth.method.value,
            "username": self.auth.username,
            "password": self.auth.password,
            "bearer_token": self.auth.bearer_token,
            "api_key": self.auth.api_key
        }

# Usage example
config = FlextOracleWmsClientConfig(
    base_url="https://your-wms.oraclecloud.com",
    organization_code="M1",
    environment=OracleWmsEnvironment.PRODUCTION
)

# Environment variables:
# FLEXT_ORACLE_WMS_BASE_URL=https://your-wms.oraclecloud.com
# FLEXT_ORACLE_WMS_ORGANIZATION_CODE=M1
# FLEXT_ORACLE_WMS_ENVIRONMENT=prod
# FLEXT_ORACLE_WMS_AUTH__METHOD=basic
# FLEXT_ORACLE_WMS_AUTH__USERNAME=wms_user
# FLEXT_ORACLE_WMS_AUTH__PASSWORD=secure_password
# FLEXT_ORACLE_WMS_PERF__TIMEOUT_SECONDS=60
# FLEXT_ORACLE_WMS_CACHE__ENABLED=true
```

---

## 🧪 **Testing Patterns for Oracle WMS**

### **Oracle WMS Test Organization**

```python
# Test structure for Oracle WMS
tests/
├── unit/                           # Unit tests (isolated, no external calls)
│   ├── domain/                     # Domain layer tests
│   │   ├── test_inventory_item.py  # Test InventoryItem entity
│   │   ├── test_shipment.py        # Test Shipment aggregate
│   │   └── test_value_objects.py   # Test value objects
│   ├── application/                # Application layer tests
│   │   ├── test_discover_entities_use_case.py
│   │   ├── test_query_inventory_use_case.py
│   │   └── test_wms_orchestrator.py
│   └── infrastructure/             # Infrastructure tests (mocked)
│       ├── test_wms_api_client.py
│       └── test_repository_impl.py
├── integration/                    # Integration tests (with external systems)
│   ├── test_oracle_wms_api.py     # Live Oracle WMS API tests
│   ├── test_database_integration.py
│   └── test_cache_integration.py
├── e2e/                           # End-to-end tests (complete workflows)
│   ├── test_inventory_sync_workflow.py
│   └── test_discovery_workflow.py
├── fixtures/                      # Test data and fixtures
│   ├── oracle_wms_responses/      # Sample Oracle WMS API responses
│   ├── test_configurations.py     # Test configurations
│   └── mock_data.py               # Mock domain data
└── conftest.py                    # Test configuration and fixtures
```

### **Domain Entity Testing**

```python
import pytest
from flext_oracle_wms.domain.entities import InventoryItem
from flext_oracle_wms.domain.value_objects import ItemNumber, Quantity

class TestInventoryItem:
    """Test Oracle WMS inventory item domain logic."""

    def test_inventory_item_creation(self):
        """Test inventory item creation with Oracle WMS patterns."""
        item_number = ItemNumber("ITEM-001")
        quantity = Quantity(100)
        location_code = LocationCode("LOC-A-01")

        inventory_item = InventoryItem(
            item_number=item_number,
            quantity=quantity,
            location=location_code,
            organization_code="M1"
        )

        assert inventory_item.item_number == item_number
        assert inventory_item.quantity == quantity
        assert inventory_item.available_quantity == quantity

    def test_quantity_adjustment_success(self):
        """Test successful quantity adjustment."""
        inventory_item = self._create_test_inventory_item()
        adjustment = QuantityAdjustment(delta=50, reason="Cycle count adjustment")

        result = inventory_item.adjust_quantity(adjustment)

        assert result.success
        assert inventory_item.quantity.value == 150
        assert len(inventory_item.domain_events) == 1
        assert inventory_item.domain_events[0].type == "InventoryAdjusted"

    def test_quantity_adjustment_insufficient_quantity(self):
        """Test quantity adjustment with insufficient quantity."""
        inventory_item = self._create_test_inventory_item()
        adjustment = QuantityAdjustment(delta=-150, reason="Damage adjustment")  # More than available

        result = inventory_item.adjust_quantity(adjustment)

        assert result.is_failure
        assert "Insufficient quantity" in result.error
        assert inventory_item.quantity.value == 100  # Unchanged
        assert len(inventory_item.domain_events) == 0

    def test_quantity_reservation(self):
        """Test quantity reservation for order fulfillment."""
        inventory_item = self._create_test_inventory_item()
        reservation = QuantityReservation(
            quantity=Quantity(30),
            order_id="ORDER-123",
            reason="Sales order reservation"
        )

        result = inventory_item.reserve_quantity(reservation)

        assert result.success
        assert inventory_item.reserved_quantity.value == 30
        assert inventory_item.available_quantity.value == 70
        assert len(inventory_item.domain_events) == 1

    def _create_test_inventory_item(self) -> InventoryItem:
        """Create test inventory item."""
        return InventoryItem(
            item_number=ItemNumber("TEST-ITEM-001"),
            quantity=Quantity(100),
            location=LocationCode("TEST-LOC-01"),
            organization_code="M1"
        )
```

### **Oracle WMS API Integration Testing**

```python
import pytest
from unittest.mock import AsyncMock, Mock
from flext_oracle_wms.infrastructure.api import OracleWmsApiClient
from flext_oracle_wms.infrastructure.config import FlextOracleWmsClientConfig

class TestOracleWmsApiClient:
    """Test Oracle WMS API client integration."""

    @pytest.fixture
    def mock_http_client(self):
        """Mock HTTP client for API testing."""
        mock_client = AsyncMock()
        return mock_client

    @pytest.fixture
    def api_client(self, mock_http_client):
        """Create API client with mocked HTTP client."""
        config = FlextOracleWmsClientConfig(
            base_url="https://test-wms.oraclecloud.com",
            organization_code="TEST",
            auth={"method": "basic", "username": "test", "password": "test"}
        )
        client = OracleWmsApiClient(config)
        client._http_client = mock_http_client
        return client

    @pytest.mark.asyncio
    async def test_query_inventory_success(self, api_client, mock_http_client):
        """Test successful inventory query."""
        # Mock Oracle WMS API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "ItemNumber": "ITEM-001",
                    "OrganizationCode": "TEST",
                    "Quantity": 100,
                    "Location": "LOC-A-01",
                    "LastUpdateDate": "2025-01-04T10:00:00.000Z"
                }
            ],
            "totalResults": 1,
            "limit": 25,
            "offset": 0
        }
        mock_http_client.get.return_value = mock_response

        result = await api_client.query_inventory_transactions(
            organization_code="TEST",
            date_from=datetime(2025, 1, 1),
            date_to=datetime(2025, 1, 4)
        )

        assert result.success
        assert len(result.data) == 1
        assert result.data[0]["ItemNumber"] == "ITEM-001"

        # Verify Oracle WMS specific API call
        mock_http_client.get.assert_called_once()
        call_args = mock_http_client.get.call_args
        assert "/inventoryTransactions" in call_args[0][0]
        assert call_args[1]["params"]["OrganizationCode"] == "TEST"
        assert "REST-Framework-Version" in call_args[1]["headers"]

    @pytest.mark.asyncio
    async def test_query_inventory_api_error(self, api_client, mock_http_client):
        """Test Oracle WMS API error handling."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_http_client.get.return_value = mock_response

        result = await api_client.query_inventory_transactions(
            organization_code="TEST",
            date_from=datetime(2025, 1, 1),
            date_to=datetime(2025, 1, 4)
        )

        assert result.is_failure
        assert "Oracle WMS API error: 500" in result.error

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_live_oracle_wms_discovery(self):
        """Test live Oracle WMS entity discovery (requires environment setup)."""
        # This test requires actual Oracle WMS credentials
        config = FlextOracleWmsClientConfig(
            base_url=os.getenv("ORACLE_WMS_BASE_URL"),
            organization_code=os.getenv("ORACLE_WMS_ORG_CODE"),
            auth={
                "method": "basic",
                "username": os.getenv("ORACLE_WMS_USERNAME"),
                "password": os.getenv("ORACLE_WMS_PASSWORD")
            }
        )

        if not all([config.base_url, config.organization_code]):
            pytest.skip("Oracle WMS credentials not configured")

        client = OracleWmsApiClient(config)
        result = await client.discover_entities()

        assert result.success
        assert len(result.data) > 0
        # Verify we get expected Oracle WMS entities
        entity_names = [entity["name"] for entity in result.data]
        assert "INVENTORY" in entity_names or "Items" in entity_names
```

### **End-to-End Workflow Testing**

```python
import pytest
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsClientConfig
from flext_core import FlextContainer

class TestOracleWmsWorkflows:
    """Test complete Oracle WMS workflows."""

    @pytest.fixture
    def test_client(self):
        """Create test client with mock configuration."""
        config = FlextOracleWmsClientConfig(
            base_url="https://mock-wms.oraclecloud.com",
            organization_code="TEST",
            auth={"method": "basic", "username": "test", "password": "test"}
        )
        return FlextOracleWmsClient(config)

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_complete_inventory_discovery_workflow(self, test_client):
        """Test complete inventory discovery and query workflow."""

        # Step 1: Discover entities
        entities_result = await test_client.discover_entities()
        assert entities_result.success

        inventory_entities = [
            entity for entity in entities_result.data
            if "inventory" in entity.name.lower()
        ]
        assert len(inventory_entities) > 0

        # Step 2: Query inventory data for each entity
        for entity in inventory_entities[:3]:  # Test first 3 entities
            data_result = await test_client.query_entity_data(
                entity_name=entity.name,
                filters={"OrganizationCode": "TEST"}
            )

            if data_result.success:
                assert isinstance(data_result.data, list)
                # Verify Oracle WMS data structure
                if data_result.data:
                    sample_record = data_result.data[0]
                    assert "OrganizationCode" in sample_record or "organizationCode" in sample_record

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_singer_catalog_generation_workflow(self, test_client):
        """Test Singer catalog generation workflow."""

        # Generate Singer catalog
        catalog_result = await generate_oracle_wms_catalog(
            client=test_client,
            organization_code="TEST"
        )

        assert catalog_result.success
        catalog = catalog_result.data

        # Verify Singer catalog structure
        assert hasattr(catalog, 'streams')
        assert len(catalog.streams) > 0

        # Verify Oracle WMS specific metadata
        for stream in catalog.streams:
            assert stream.tap_stream_id.startswith("TEST_")
            assert "oracle-wms-entity" in stream.metadata
            assert stream.metadata["organization-code"] == "TEST"
```

---

## 📏 **Code Quality Standards for Oracle WMS**

### **Oracle WMS Specific Type Annotations**

```python
# Oracle WMS specific type definitions
from typing import Dict, List, Optional, Union, Literal
from decimal import Decimal
from datetime import datetime

# Oracle WMS API response types
OracleWmsApiResponse = Dict[str, Any]
OracleWmsEntityData = List[Dict[str, Any]]
OracleWmsFilterParams = Dict[str, Union[str, int, float, bool, List[str]]]

# Oracle organization and location types
OrganizationCode = str  # 3-character Oracle org code
LocationCode = str      # Warehouse location identifier
SubinventoryCode = str  # Oracle subinventory code

# Oracle WMS business types
ItemNumber = str
LotNumber = Optional[str]
SerialNumber = Optional[str]
QuantityValue = Union[int, float, Decimal]

# Oracle WMS operation types
TransactionType = Literal[
    "ISSUE", "RECEIPT", "TRANSFER", "ADJUSTMENT",
    "CYCLE_COUNT", "PHYSICAL_INVENTORY"
]

TransactionStatus = Literal["PENDING", "PROCESSED", "ERROR", "CANCELLED"]

# Function with complete Oracle WMS type annotations
async def process_oracle_inventory_transaction(
    organization_code: OrganizationCode,
    item_number: ItemNumber,
    transaction_type: TransactionType,
    quantity: QuantityValue,
    location_code: LocationCode,
    subinventory_code: Optional[SubinventoryCode] = None,
    lot_number: Optional[LotNumber] = None,
    serial_numbers: Optional[List[SerialNumber]] = None,
    transaction_date: Optional[datetime] = None
) -> FlextResult[Dict[str, Any]]:
    """
    Process Oracle WMS inventory transaction with complete type safety.

    Args:
        organization_code: 3-character Oracle organization code
        item_number: Oracle item number identifier
        transaction_type: Type of inventory transaction
        quantity: Transaction quantity (positive for receipts, negative for issues)
        location_code: Warehouse location code
        subinventory_code: Oracle subinventory code (optional)
        lot_number: Lot number for lot-controlled items (optional)
        serial_numbers: Serial numbers for serial-controlled items (optional)
        transaction_date: Transaction timestamp (defaults to current time)

    Returns:
        FlextResult containing transaction confirmation or error details
    """
    # Implementation with full type safety
    pass
```

### **Oracle WMS Error Handling Standards**

```python
# Oracle WMS specific error handling patterns
from flext_core import FlextResult, FlextError
from enum import Enum

class OracleWmsErrorCode(str, Enum):
    """Oracle WMS specific error codes."""
    INVALID_ORGANIZATION = "ORACLE_WMS_INVALID_ORG"
    ITEM_NOT_FOUND = "ORACLE_WMS_ITEM_NOT_FOUND"
    INSUFFICIENT_QUANTITY = "ORACLE_WMS_INSUFFICIENT_QTY"
    LOCATION_NOT_FOUND = "ORACLE_WMS_LOCATION_NOT_FOUND"
    API_AUTHENTICATION_FAILED = "ORACLE_WMS_AUTH_FAILED"
    API_RATE_LIMIT_EXCEEDED = "ORACLE_WMS_RATE_LIMIT"
    INVALID_TRANSACTION_TYPE = "ORACLE_WMS_INVALID_TRANSACTION"
    ORACLE_BUSINESS_RULE_VIOLATION = "ORACLE_WMS_BUSINESS_RULE"

def handle_oracle_wms_error(
    error_code: OracleWmsErrorCode,
    error_message: str,
    context: Dict[str, Any]
) -> FlextResult[None]:
    """Standardized Oracle WMS error handling."""

    flext_error = FlextError(
        code=error_code.value,
        message=error_message,
        details={
            "oracle_wms_context": context,
            "error_category": "ORACLE_WMS_INTEGRATION",
            "timestamp": datetime.utcnow().isoformat(),
            "severity": _determine_error_severity(error_code)
        }
    )

    return FlextResult[None].fail(flext_error)

def _determine_error_severity(error_code: OracleWmsErrorCode) -> str:
    """Determine error severity for monitoring and alerting."""
    critical_errors = {
        OracleWmsErrorCode.API_AUTHENTICATION_FAILED,
        OracleWmsErrorCode.ORACLE_BUSINESS_RULE_VIOLATION
    }

    if error_code in critical_errors:
        return "CRITICAL"
    elif error_code == OracleWmsErrorCode.API_RATE_LIMIT_EXCEEDED:
        return "WARNING"
    else:
        return "ERROR"

# Usage in Oracle WMS operations
async def query_oracle_inventory(
    item_number: str,
    organization_code: str
) -> FlextResult[List[InventoryRecord]]:
    """Query Oracle inventory with proper error handling."""

    try:
        # Validate inputs
        if not organization_code or len(organization_code) != 3:
            return handle_oracle_wms_error(
                OracleWmsErrorCode.INVALID_ORGANIZATION,
                f"Invalid organization code: {organization_code}",
                {"item_number": item_number, "organization_code": organization_code}
            )

        # Call Oracle WMS API
        api_result = await oracle_api_client.query_inventory(item_number, organization_code)

        if api_result.status_code == 404:
            return handle_oracle_wms_error(
                OracleWmsErrorCode.ITEM_NOT_FOUND,
                f"Item {item_number} not found in organization {organization_code}",
                {"item_number": item_number, "organization_code": organization_code}
            )
        elif api_result.status_code == 401:
            return handle_oracle_wms_error(
                OracleWmsErrorCode.API_AUTHENTICATION_FAILED,
                "Oracle WMS API authentication failed",
                {"endpoint": "inventory_query", "status_code": 401}
            )
        elif api_result.status_code == 429:
            return handle_oracle_wms_error(
                OracleWmsErrorCode.API_RATE_LIMIT_EXCEEDED,
                "Oracle WMS API rate limit exceeded",
                {"retry_after": api_result.headers.get("Retry-After")}
            )

        # Process successful response
        inventory_records = _parse_oracle_inventory_response(api_result.data)
        return FlextResult[None].ok(inventory_records)

    except Exception as e:
        return handle_oracle_wms_error(
            OracleWmsErrorCode.ORACLE_BUSINESS_RULE_VIOLATION,
            f"Unexpected error in Oracle inventory query: {str(e)}",
            {"item_number": item_number, "organization_code": organization_code, "exception": str(e)}
        )
```

---

## 🌐 **FLEXT Ecosystem Integration Guidelines**

### **Cross-Project Oracle Integration**

```python
# Integration with other FLEXT Oracle projects
from flext_core import FlextResult, FlextContainer
from flext_db_oracle import OracleConnection, OracleRepository  # Reuse Oracle patterns
from flext_oracle_wms import FlextOracleWmsClient

class UnifiedOracleService:
    """Unified service integrating Oracle DB and Oracle WMS."""

    def __init__(
        self,
        oracle_db_connection: OracleConnection,
        oracle_wms_client: FlextOracleWmsClient,
        logger: FlextLogger
    ):
        self._db_connection = oracle_db_connection
        self._wms_client = oracle_wms_client
        self._logger = logger

    async def sync_inventory_db_to_wms(
        self,
        organization_code: str
    ) -> FlextResult[SyncResult]:
        """Synchronize inventory from Oracle DB to Oracle WMS."""

        # Query Oracle database using flext-db-oracle patterns
        db_query = """
        SELECT item_number, organization_code, quantity_on_hand, location_code
        FROM mtl_onhand_quantities_view
        WHERE organization_code = :org_code
        AND quantity_on_hand > 0
        """

        db_result = await self._db_connection.execute_query(
            query=db_query,
            parameters={"org_code": organization_code}
        )

        if db_result.is_failure:
            return FlextResult[None].fail(f"Database query failed: {db_result.error}")

        # Transform DB data for WMS
        wms_updates = []
        for db_record in db_result.data:
            wms_updates.append({
                "ItemNumber": db_record["item_number"],
                "OrganizationCode": db_record["organization_code"],
                "Quantity": db_record["quantity_on_hand"],
                "LocationCode": db_record["location_code"]
            })

        # Update Oracle WMS using WMS client
        wms_result = await self._wms_client.bulk_update_inventory(wms_updates)

        if wms_result.is_failure:
            return FlextResult[None].fail(f"WMS update failed: {wms_result.error}")

        sync_result = SyncResult(
            records_processed=len(wms_updates),
            success_count=wms_result.data.success_count,
            error_count=wms_result.data.error_count
        )

        return FlextResult[None].ok(sync_result)

# Container configuration for Oracle integration
def configure_oracle_container(container: FlextContainer) -> None:
    """Configure dependency injection for Oracle integration."""

    # Register flext-db-oracle services
    container.register_singleton(OracleConnection, lambda: create_oracle_db_connection())

    # Register flext-oracle-wms services
    container.register_singleton(FlextOracleWmsClient, lambda: create_oracle_wms_client())

    # Register unified service
    container.register(UnifiedOracleService, UnifiedOracleService)
```

### **Singer Ecosystem Integration**

```python
# Complete Singer integration with Oracle WMS
from singer import Catalog, Stream, write_record, write_schema, write_state
from flext_oracle_wms import FlextOracleWmsClient

class OracleWmsSingerTap:
    """Singer tap for Oracle WMS using flext-oracle-wms."""

    def __init__(self, config: Dict[str, Any]):
        self._config = config
        self._wms_client = FlextOracleWmsClient(
            FlextOracleWmsClientConfig(**config)
        )
        self._state = {}

    async def discover(self) -> Catalog:
        """Discover Oracle WMS entities and generate Singer catalog."""
        return await generate_oracle_wms_catalog(
            client=self._wms_client,
            organization_code=self._config["organization_code"]
        )

    async def sync(self, catalog: Catalog, state: Dict[str, Any]) -> None:
        """Sync Oracle WMS data using Singer protocol."""

        for stream in catalog.streams:
            if not stream.selected:
                continue

            entity_name = stream.metadata["oracle-wms-entity"]
            organization_code = stream.metadata["organization-code"]

            # Write Singer schema
            write_schema(stream.tap_stream_id, stream.schema.to_dict(), stream.key_properties)

            # Get incremental sync state
            last_sync_time = state.get(stream.tap_stream_id, {}).get("last_sync_time")

            # Query Oracle WMS data
            filters = {"OrganizationCode": organization_code}
            if last_sync_time:
                filters["LastUpdateDate"] = f">= '{last_sync_time}'"

            data_result = await self._wms_client.query_entity_data(
                entity_name=entity_name,
                filters=filters
            )

            if data_result.is_failure:
                raise Exception(f"Failed to sync {entity_name}: {data_result.error}")

            # Write Singer records
            latest_update_time = None
            for record in data_result.data:
                write_record(stream.tap_stream_id, record)

                # Track latest update time for incremental sync
                record_update_time = record.get("LastUpdateDate")
                if record_update_time:
                    if not latest_update_time or record_update_time > latest_update_time:
                        latest_update_time = record_update_time

            # Update state for incremental sync
            if latest_update_time:
                state[stream.tap_stream_id] = {"last_sync_time": latest_update_time}
                write_state(state)

# DBT integration for Oracle WMS
class OracleWmsDbtProject:
    """DBT project generator for Oracle WMS data."""

    @staticmethod
    def generate_inventory_model() -> str:
        """Generate DBT model for Oracle WMS inventory data."""
        return """
        {{ config(materialized='incremental', unique_key='inventory_id') }}

        with oracle_wms_inventory as (
            select
                item_number,
                organization_code,
                location_code,
                quantity_on_hand,
                reserved_quantity,
                available_quantity,
                last_update_date,
                md5(concat(item_number, organization_code, location_code)) as inventory_id
            from {{ source('oracle_wms', 'inventory') }}
            {% if is_incremental() %}
                where last_update_date > (select max(last_update_date) from {{ this }})
            {% endif %}
        ),

        inventory_with_calculations as (
            select
                *,
                case
                    when available_quantity > 0 then 'AVAILABLE'
                    when quantity_on_hand > 0 then 'RESERVED'
                    else 'OUT_OF_STOCK'
                end as inventory_status,
                current_timestamp as dbt_updated_at
            from oracle_wms_inventory
        )

        select * from inventory_with_calculations
        """
```

---

## 📋 **Module Creation Checklist for Oracle WMS**

### **Oracle WMS Module Standards**

- [ ] **Oracle WMS Naming**: Uses `FlextOracleWms` prefix for public API
- [ ] **Clean Architecture**: Proper layer placement (domain/application/infrastructure/presentation)
- [ ] **FLEXT Integration**: Uses FlextResult, FlextContainer, FlextLogger patterns
- [ ] **Oracle Specificity**: Handles Oracle WMS Cloud API patterns and business rules
- [ ] **Type Safety**: Complete type annotations with Oracle WMS specific types
- [ ] **Error Handling**: Uses OracleWmsErrorCode enum and structured error handling
- [ ] **Configuration**: Extends FlextSettings with Oracle WMS specific options
- [ ] **Testing**: 90%+ coverage with unit, integration, and Oracle WMS specific tests
- [ ] **Documentation**: Comprehensive docstrings with Oracle WMS examples
- [ ] **Singer Integration**: Compatible with Singer protocol and catalog generation

### **Oracle WMS Quality Gates**

- [ ] **FLEXT Validation**: `make validate` passes (lint + type + security + test)
- [ ] **Oracle WMS Tests**: All Oracle WMS specific test scenarios pass
- [ ] **API Integration**: Live Oracle WMS API integration tests pass (when configured)
- [ ] **Singer Compatibility**: Generated Singer catalog validates successfully
- [ ] **Performance**: Oracle WMS operations meet performance benchmarks
- [ ] **Security**: No Oracle credentials exposed in logs or error messages
- [ ] **Documentation**: Oracle WMS usage examples are tested and functional
- [ ] **Ecosystem Compatibility**: Integrates properly with flext-db-oracle and other Oracle projects

### **Oracle WMS Deployment Readiness**

- [ ] **Configuration Validation**: All Oracle WMS configuration options validated
- [ ] **Environment Testing**: Tested against development, staging, and production Oracle WMS environments
- [ ] **Error Scenarios**: All Oracle WMS error scenarios handled gracefully
- [ ] **Rate Limiting**: Oracle WMS API rate limiting handled appropriately
- [ ] **Monitoring**: Oracle WMS specific metrics and health checks implemented
- [ ] **Documentation**: Production deployment guide with Oracle WMS specific considerations

---

**Last Updated**: January 4, 2025  
**Target Audience**: FLEXT Oracle WMS developers and ecosystem contributors  
**Scope**: Python module organization for Oracle WMS Cloud integration  
**Version**: 0.9.0 → 1.0.0 development guidelines  
**Dependencies**: flext-core patterns, Clean Architecture, Oracle WMS Cloud APIs
