# FLEXT-ORACLE-WMS CLAUDE.MD

**Enterprise Oracle Warehouse Management System (WMS) Integration Foundation for FLEXT Ecosystem**
**Version**: 0.9.0 | **Authority**: ORACLE WMS INTEGRATION AUTHORITY | **Updated**: 2025-01-08
**Status**: Production-ready Oracle WMS integration platform with zero errors across all quality gates

**Hierarchy**: This document provides project-specific standards based on workspace-level patterns defined in [../CLAUDE.md](../CLAUDE.md). For architectural principles, quality gates, and MCP server usage, reference the main workspace standards.

## 🔗 MCP SERVER INTEGRATION

| MCP Server | Purpose | Status |
|------------|---------|--------|
| **serena** | Oracle WMS codebase analysis and warehouse system integration patterns | **ACTIVE** |
| **sequential-thinking** | Oracle WMS architecture and enterprise warehouse problem solving | **ACTIVE** |
| **github** | Oracle WMS ecosystem integration and warehouse system PRs | **ACTIVE** |

**Usage**: `claude mcp list` for available servers, leverage for Oracle WMS-specific development patterns and warehouse system analysis.

## 🎯 FLEXT-ORACLE-WMS MISSION (ORACLE WMS INTEGRATION AUTHORITY)

**CRITICAL ROLE**: flext-oracle-wms is the enterprise-grade Oracle Warehouse Management System (WMS) integration and enterprise Oracle WMS foundation for the entire FLEXT ecosystem.

**ZERO TOLERANCE ENFORCEMENT (ORACLE WMS AUTHORITY)**:

### ⛔ ABSOLUTELY FORBIDDEN (IMMEDIATE TERMINATION POLICIES)

#### 1. **Oracle WMS Direct Integration Violations**

- **FORBIDDEN**: Direct `requests` or `httpx` imports for Oracle WMS operations
- **FORBIDDEN**: Custom Oracle WMS authentication implementations
- **FORBIDDEN**: Oracle WMS SQL queries outside flext-db-oracle patterns
- **FORBIDDEN**: WMS business logic mixed with infrastructure code
- **MANDATORY**: ALL Oracle WMS operations MUST use FlextOracleWmsClient

#### 2. **Oracle WMS Schema Violations**

- **FORBIDDEN**: Hardcoded Oracle WMS entity schemas
- **FORBIDDEN**: Manual WMS data transformations outside discovery patterns
- **FORBIDDEN**: WMS inventory/shipping logic in client layer
- **MANDATORY**: Use FlextOracleWmsEntityDiscovery for ALL schema operations

#### 3. **Enterprise Oracle WMS Security Violations**

- **FORBIDDEN**: Oracle WMS credentials in plain text or config files
- **FORBIDDEN**: Custom Oracle WMS SSL/TLS handling
- **FORBIDDEN**: WMS session management outside enterprise patterns
- **MANDATORY**: Use FlextOracleWmsAuthenticator with enterprise security

## 🏛️ ORACLE WMS INTEGRATION ARCHITECTURE (ENTERPRISE AUTHORITY)

### **Zero Tolerance Quality Requirements**

```bash
# MANDATORY before ANY Oracle WMS development
make validate              # Complete pipeline: 100% type safety + 90% coverage + zero security issues
make oracle-connect        # Verify Oracle WMS connectivity with enterprise credentials
make wms-schema            # Validate complete WMS schema compliance
make docker-validate       # Full Oracle WMS validation in production-like containers
```

### **Production Oracle WMS Configuration (MANDATORY)**

#### Enterprise Oracle WMS Client (FLEXT AUTHORITY)

```python
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsClientConfig

# MANDATORY: Use enterprise configuration patterns
config = FlextOracleWmsClientConfig(
    base_url="https://enterprise-wms.oraclecloud.com",  # Production Oracle WMS Cloud
    username=get_secure_credential("ORACLE_WMS_USER"),  # Enterprise credential management
    password=get_secure_credential("ORACLE_WMS_PASS"),  # Never plain text
    auth_method=OracleWMSAuthMethod.OAUTH2,            # Enterprise OAuth2 required
    timeout=WMSTimeout.PRODUCTION,                      # Production timeouts
    retry_attempts=WMSRetryAttempts.ENTERPRISE,        # Enterprise retry policy
    enable_ssl_verification=True,                       # MANDATORY for production
)

# MANDATORY: Enterprise client initialization
wms_client = FlextOracleWmsClient(config)
```

### **Oracle WMS Entity Discovery (PRODUCTION PATTERNS)**

#### Inventory Management (Clean Architecture)

```python
from flext_oracle_wms import (
    FlextOracleWmsEntityDiscovery,
    FlextOracleWmsDynamicSchemaProcessor,
    OracleWMSEntityType
)

# MANDATORY: Use discovery patterns for ALL WMS entities
discovery = FlextOracleWmsEntityDiscovery(wms_client)

# Production inventory discovery with enterprise patterns
inventory_result = await discovery.discover_entities(
    entity_type=OracleWMSEntityType.INVENTORY,
    include_schema=True,
    cache_duration=3600,  # Production caching
)

if inventory_result.success:
    # MANDATORY: Process via FlextResult patterns
    inventory_entities = inventory_result.value
    logger.info(f"Discovered {len(inventory_entities)} inventory entities")
```

### **Oracle WMS Business Operations (DOMAIN-DRIVEN DESIGN)**

#### Warehouse Operations (Enterprise Patterns)

```python
from flext_oracle_wms import (
    FlextOracleWmsOperations,
    FlextOracleWmsInventoryManager,
    FlextOracleWmsShipmentManager
)

# MANDATORY: Separate business logic from infrastructure
class EnterpriseWarehouseService:
    def __init__(self, wms_client: FlextOracleWmsClient):
        self.wms_client = wms_client
        self.inventory_mgr = FlextOracleWmsInventoryManager(wms_client)
        self.shipment_mgr = FlextOracleWmsShipmentManager(wms_client)

    async def process_inbound_shipment(self, shipment_id: str) -> FlextResult[bool]:
        # Enterprise WMS inbound processing with Clean Architecture
        return await self.shipment_mgr.process_inbound(shipment_id)

    async def execute_picking_wave(self, wave_id: str) -> FlextResult[PickingResult]:
        # Enterprise WMS picking operations with domain modeling
        return await self.inventory_mgr.execute_picking_wave(wave_id)
```

## 🔒 ENTERPRISE ORACLE WMS SECURITY (ZERO TOLERANCE)

### **Oracle WMS Authentication (PRODUCTION REQUIREMENTS)**

#### OAuth2/Enterprise SSO Integration

```python
from flext_oracle_wms import FlextOracleWmsAuthenticator, OracleWMSAuthMethod

# MANDATORY: Enterprise authentication patterns
auth_config = FlextOracleWmsAuthConfig(
    auth_method=OracleWMSAuthMethod.OAUTH2,
    oauth2_client_id=get_secure_credential("WMS_OAUTH2_CLIENT"),
    oauth2_client_secret=get_secure_credential("WMS_OAUTH2_SECRET"),
    oauth2_scope="wms:read wms:write wms:REDACTED_LDAP_BIND_PASSWORD",
    token_refresh_threshold=300,  # Auto-refresh 5 minutes before expiry
)

authenticator = FlextOracleWmsAuthenticator(auth_config)
```

### **Oracle WMS Data Security (ENTERPRISE COMPLIANCE)**

- **GDPR Compliance**: All WMS personal data handling via FlextOracleWmsDataProtection
- **Audit Logging**: Complete WMS operation audit via FlextObservability patterns
- **Encryption**: All WMS data encrypted in transit and at rest
- **Access Control**: Role-based WMS access via FlextOracleWmsAccessManager

## 🔧 ORACLE WMS DEVELOPMENT COMMANDS (ENTERPRISE WORKFLOWS)

### **Mandatory Quality Gates (ZERO ERRORS TOLERANCE)**

```bash
# MANDATORY: Complete Oracle WMS validation pipeline
make validate                    # 100% type safety + 90% coverage + zero security vulnerabilities
make oracle-connect             # Enterprise Oracle WMS connectivity verification
make wms-schema                 # Complete WMS schema validation and compliance
make wms-inventory              # Production inventory operation validation
make wms-shipping               # Enterprise shipping workflow validation
make docker-validate            # Full containerized Oracle WMS validation
```

### **Oracle WMS Quality Standards (PRODUCTION REQUIREMENTS)**

```bash
# Type Safety (ZERO TOLERANCE)
make type-check                 # MyPy strict mode: zero errors across all WMS modules
make lint                       # Ruff comprehensive linting: enterprise code standards
make security                   # Bandit + pip-audit: zero security vulnerabilities

# Oracle WMS Testing (ENTERPRISE COVERAGE)
make test                       # 90% minimum coverage with real Oracle WMS integration
make test-integration           # Full Oracle WMS API integration testing
make test-wms                   # WMS-specific business logic validation
make test-oracle                # Oracle database connectivity and schema testing
```

### **Oracle WMS Docker Operations (MAXIMUM CONTAINER USAGE)**

```bash
# Enterprise Docker Workflows
make docker-build               # Build production Oracle WMS containers
make docker-up                  # Start enterprise Oracle WMS environment
make docker-examples            # Run complete Oracle WMS examples in containers
make docker-test                # Full test suite with containerized Oracle WMS
make docker-full-validation     # Complete enterprise validation workflow

# Direct Docker Scripts
./docker-run.sh examples        # Execute Oracle WMS examples directly
./docker-run.sh test            # Run comprehensive test suite
./docker-run.sh all             # Complete validation pipeline
./docker-run.sh clean           # Clean all Oracle WMS Docker resources
```

### **Oracle WMS Development Workflow (CLEAN ARCHITECTURE)**

```bash
# Environment Setup
make setup                      # Complete Oracle WMS development environment
make install                    # Install all enterprise dependencies
make deps-update                # Update Oracle WMS dependencies securely

# Oracle WMS Operations
make wms-test                   # Test Oracle WMS connectivity and authentication
make oracle-schema              # Validate Oracle database schema compliance
make diagnose                   # Complete Oracle WMS diagnostics and health check
```

## 🏗️ ENTERPRISE ORACLE WMS ARCHITECTURE (CLEAN ARCHITECTURE + DDD)

### **Oracle WMS Integration Layers (PRODUCTION SEPARATION)**

#### 1. **Domain Layer (WMS Business Logic)**

```python
# src/flext_oracle_wms/domain/
from flext_oracle_wms.wms_models import (
    FlextOracleWmsEntity,           # WMS domain entities
    FlextOracleWmsInventoryItem,    # Inventory domain model
    FlextOracleWmsShipment,         # Shipping domain model
    FlextOracleWmsPick,             # Picking domain model
)
```

#### 2. **Application Layer (WMS Use Cases)**

```python
# src/flext_oracle_wms/wms_operations.py
from flext_oracle_wms.wms_operations import (
    FlextOracleWmsInventoryManager,  # Inventory operations
    FlextOracleWmsShipmentManager,   # Shipping operations
    FlextOracleWmsPickingManager,    # Picking operations
)
```

#### 3. **Infrastructure Layer (Oracle WMS Client)**

```python
# src/flext_oracle_wms/wms_client.py
from flext_oracle_wms.wms_client import (
    FlextOracleWmsClient,           # Main Oracle WMS client
    FlextOracleWmsAuthenticator,    # Enterprise authentication
)
```

#### 4. **Interface Layer (API & Discovery)**

```python
# src/flext_oracle_wms/wms_api.py + wms_discovery.py
from flext_oracle_wms import (
    FLEXT_ORACLE_WMS_APIS,          # Oracle WMS API catalog
    FlextOracleWmsEntityDiscovery,  # Entity discovery service
)
```

### **Oracle WMS Configuration Architecture (ENTERPRISE PATTERNS)**

```python
# MANDATORY: Enterprise configuration structure
src/flext_oracle_wms/wms_config.py:
- FlextOracleWmsClientConfig      # Main client configuration
- FlextOracleWmsModuleConfig      # Module-level configuration
- WMSAPIVersion                   # API version management
- WMSRetryAttempts               # Enterprise retry policies
```

### **Oracle WMS Exception Architecture (COMPREHENSIVE ERROR HANDLING)**

```python
# Complete Oracle WMS error hierarchy
src/flext_oracle_wms/wms_exceptions.py:
- FlextOracleWmsError                    # Base WMS error
- FlextOracleWmsConnectionError          # Connection failures
- FlextOracleWmsAuthenticationError      # Auth failures
- FlextOracleWmsInventoryError           # Inventory operation errors
- FlextOracleWmsShipmentError           # Shipping operation errors
- FlextOracleWmsPickingError            # Picking operation errors
```

## 📦 FLEXT ECOSYSTEM INTEGRATION (MANDATORY DEPENDENCIES)

### **FLEXT Foundation Dependencies (ENTERPRISE INTEGRATION)**

```python
# MANDATORY: Core FLEXT patterns
from flext_core import (
    FlextResult,              # Railway-oriented programming (ALL operations)
    FlextLogger,              # Enterprise logging patterns
    FlextContainer,           # Dependency injection container
    FlextConfig,             # Configuration management
)

# MANDATORY: Enterprise API patterns
from flext_api import (
    FlextApiClient,          # Base API client patterns
    FlextApiAuth,            # Enterprise authentication
    FlextApiRetry,           # Retry policies
)

# MANDATORY: Observability integration
from flext_observability import (
    FlextMetrics,            # Oracle WMS metrics collection
    FlextTracing,            # Distributed tracing
    FlextAlerting,           # Oracle WMS alerts
)

# MANDATORY: Database integration
from flext_db_oracle import (
    FlextOracleConnection,   # Oracle database connectivity
    FlextOracleSchema,       # Schema management
    FlextOracleTypes,        # Oracle type handling
)
```

### **Oracle WMS Import Standards (ZERO TOLERANCE ENFORCEMENT)**

#### ✅ **MANDATORY: Always Use These Patterns**

```python
# CORRECT: Root-level imports ONLY
from flext_oracle_wms import FlextOracleWmsClient
from flext_oracle_wms import FlextOracleWmsEntityDiscovery
from flext_oracle_wms import OracleWMSEntityType

# CORRECT: flext-core integration
from flext_core import FlextResult, get_logger
result: FlextResult[List[WMSEntity]] = await client.discover_entities()
```

#### ❌ **ABSOLUTELY FORBIDDEN: These Import Patterns**

```python
# FORBIDDEN: Internal module imports
from flext_oracle_wms.wms_client import FlextOracleWmsClient  # ❌ VIOLATION
from flext_oracle_wms.internal.auth import WMSAuth            # ❌ VIOLATION

# FORBIDDEN: Direct Oracle WMS integrations
import requests                                               # ❌ VIOLATION
import httpx                                                 # ❌ VIOLATION
import oracledb                                              # ❌ VIOLATION (use flext-db-oracle)

# FORBIDDEN: Custom WMS implementations
class MyWMSClient: pass                                      # ❌ VIOLATION (use FlextOracleWmsClient)
```

## 🔍 ORACLE WMS QUALITY REQUIREMENTS (ENTERPRISE STANDARDS)

### **Type Safety (100% COMPLIANCE MANDATORY)**

```python
# MANDATORY: All Oracle WMS operations must be typed
async def get_inventory_data(
    self,
    entity_name: str,
    filters: Optional[Dict[str, object]] = None,
) -> FlextResult[List[FlextOracleWmsEntity]]:
    """Get inventory data with complete type safety."""

# MANDATORY: Use FlextResult for ALL operations
result = await wms_client.get_inventory_data("inventory_items")
if result.success:
    entities: List[FlextOracleWmsEntity] = result.value
else:
    logger.error(f"Inventory fetch failed: {result.error}")
```

### **Error Handling (COMPREHENSIVE COVERAGE)**

```python
# MANDATORY: Use Oracle WMS exception hierarchy
from flext_oracle_wms.wms_exceptions import (
    FlextOracleWmsError,
    FlextOracleWmsConnectionError,
    FlextOracleWmsAuthenticationError,
    FlextOracleWmsInventoryError,
)

try:
    result = await wms_client.process_inventory_update(data)
    if result.is_failure:
        # Handle business logic errors via FlextResult
        logger.error(f"Inventory update failed: {result.error}")
except FlextOracleWmsInventoryError as e:
    # Handle Oracle WMS inventory-specific errors
    await handle_inventory_error(e)
except FlextOracleWmsConnectionError as e:
    # Handle Oracle WMS connectivity issues
    await handle_connection_error(e)
```

## 🚀 ORACLE WMS DEVELOPMENT PATTERNS (CLEAN ARCHITECTURE ENFORCEMENT)

### **Domain-Driven Oracle WMS Design (MANDATORY PATTERNS)**

#### Enterprise WMS Service Layer

```python
# MANDATORY: Clean Architecture separation
from flext_oracle_wms import (
    FlextOracleWmsClient,
    FlextOracleWmsEntityDiscovery,
    FlextOracleWmsInventoryManager,
    FlextOracleWmsShipmentManager,
)
from flext_core import FlextResult, get_logger

class EnterpriseWarehouseOrchestrator:
    """Domain service orchestrating Oracle WMS operations."""

    def __init__(self, wms_client: FlextOracleWmsClient):
        self.wms_client = wms_client
        self.inventory_mgr = FlextOracleWmsInventoryManager(wms_client)
        self.shipment_mgr = FlextOracleWmsShipmentManager(wms_client)
        self.logger = get_logger(__name__)

    async def orchestrate_order_fulfillment(
        self,
        order_id: str
    ) -> FlextResult[OrderFulfillmentResult]:
        """Orchestrate complete order fulfillment in Oracle WMS."""
        # Step 1: Validate inventory availability
        inventory_check = await self.inventory_mgr.check_availability(order_id)
        if inventory_check.is_failure:
            return FlextResult.fail(f"Inventory check failed: {inventory_check.error}")

        # Step 2: Create picking wave
        picking_wave = await self.inventory_mgr.create_picking_wave(order_id)
        if picking_wave.is_failure:
            return FlextResult.fail(f"Picking wave creation failed: {picking_wave.error}")

        # Step 3: Execute shipment processing
        shipment = await self.shipment_mgr.process_outbound_shipment(order_id)
        return shipment
```

#### Oracle WMS Configuration Patterns (ENTERPRISE SECURITY)

```python
# MANDATORY: Enterprise configuration with secrets management
from flext_oracle_wms import FlextOracleWmsClientConfig
from flext_core import FlextSecretManager

class OracleWMSConfigurationService:
    """Enterprise Oracle WMS configuration management."""

    @classmethod
    async def create_production_config(cls) -> FlextOracleWmsClientConfig:
        """Create production Oracle WMS configuration."""
        secret_manager = FlextSecretManager()

        return FlextOracleWmsClientConfig(
            # Production Oracle WMS Cloud endpoint
            base_url=await secret_manager.get_secret("ORACLE_WMS_PRODUCTION_URL"),

            # Enterprise authentication
            username=await secret_manager.get_secret("ORACLE_WMS_SERVICE_USER"),
            password=await secret_manager.get_secret("ORACLE_WMS_SERVICE_PASS"),

            # Production settings
            auth_method=OracleWMSAuthMethod.OAUTH2,
            timeout=300,  # 5 minutes for production operations
            retry_attempts=5,  # Enterprise retry policy
            enable_ssl_verification=True,
            connection_pool_size=20,

            # Enterprise monitoring
            enable_metrics=True,
            enable_tracing=True,
            enable_audit_logging=True,
        )
```

### **Oracle WMS Testing Patterns (ENTERPRISE VALIDATION)**

#### Integration Testing with Real Oracle WMS

```python
# MANDATORY: Real Oracle WMS integration testing
import pytest
from flext_oracle_wms import FlextOracleWmsClient
from flext_core import FlextResult

@pytest.mark.integration
@pytest.mark.wms
@pytest.mark.oracle
async def test_oracle_wms_inventory_integration():
    """Test real Oracle WMS inventory operations."""
    # Use test Oracle WMS instance
    config = await OracleWMSConfigurationService.create_test_config()
    wms_client = FlextOracleWmsClient(config)

    # Test inventory discovery
    discovery_result = await wms_client.discover_entities(
        entity_type=OracleWMSEntityType.INVENTORY
    )
    assert discovery_result.success
    assert len(discovery_result.value) > 0

    # Test inventory operations
    inventory_data = await wms_client.get_inventory_data("test_entity")
    assert inventory_data.success
```

#### Docker-based Oracle WMS Testing

```python
# MANDATORY: Containerized testing with real Oracle WMS
@pytest.mark.docker
@pytest.mark.e2e
async def test_oracle_wms_complete_workflow_in_docker():
    """Test complete Oracle WMS workflow in Docker containers."""
    # Docker will provide real Oracle WMS instance
    async with OracleWMSDockerEnvironment() as wms_env:
        wms_client = await wms_env.get_authenticated_client()

        # Execute complete business workflow
        orchestrator = EnterpriseWarehouseOrchestrator(wms_client)
        fulfillment_result = await orchestrator.orchestrate_order_fulfillment("TEST_ORDER_001")

        assert fulfillment_result.success
        assert fulfillment_result.value.status == "FULFILLED"
```

## 🎯 ORACLE WMS CRITICAL SUCCESS METRICS (ENTERPRISE KPIS)

### **Production Readiness Requirements (ZERO TOLERANCE)**

- **Type Safety**: 100% MyPy compliance across all Oracle WMS modules
- **Test Coverage**: 90% minimum with real Oracle WMS integration tests
- **Security Compliance**: Zero security vulnerabilities in Oracle WMS operations
- **Performance**: Oracle WMS operations complete within enterprise SLAs
- **Availability**: Oracle WMS integration maintains 99.9% uptime
- **Error Handling**: 100% of Oracle WMS errors handled via FlextResult patterns

### **Oracle WMS Integration Health Metrics**

```bash
# MANDATORY: Health monitoring commands
make oracle-connect           # Oracle WMS connectivity health
make wms-schema              # Schema compliance validation
make wms-inventory           # Inventory operations health
make wms-shipping            # Shipping workflows health
make docker-validate         # Complete containerized validation
```

## ⚡ PERFORMANCE OPTIMIZATION (ENTERPRISE ORACLE WMS)

### **Oracle WMS Connection Optimization**

- **Connection Pooling**: Enterprise connection pool management
- **Caching Strategy**: Intelligent Oracle WMS entity caching
- **Retry Logic**: Exponential backoff with jitter for Oracle WMS operations
- **Batch Operations**: Optimized batch processing for Oracle WMS data
- **Monitoring**: Real-time Oracle WMS performance metrics via FlextObservability

## 📋 ORACLE WMS ENTERPRISE INTEGRATION CHECKLIST

### **Pre-Development Validation (MANDATORY)**

```bash
# REQUIRED: Execute BEFORE any Oracle WMS development
□ make validate                    # Zero errors across all quality gates
□ make oracle-connect             # Verify Oracle WMS connectivity
□ make wms-schema                 # Validate schema compliance
□ make docker-validate            # Container-based validation
□ make security                   # Zero security vulnerabilities
```

### **Development Standards Compliance**

```bash
# REQUIRED: During development
□ 100% type safety (MyPy strict mode)
□ 90% minimum test coverage with real Oracle WMS
□ All Oracle WMS operations via FlextResult patterns
□ Zero custom Oracle WMS implementations
□ Enterprise authentication patterns only
□ Complete Docker integration testing
```

### **Production Deployment Readiness**

```bash
# REQUIRED: Before production
□ Enterprise Oracle WMS configuration validated
□ OAuth2/SSO authentication verified
□ Performance benchmarks met
□ Security audit completed
□ Monitoring and alerting configured
□ Disaster recovery tested
```

---

**FLEXT-ORACLE-WMS AUTHORITY**: This document establishes flext-oracle-wms as the definitive Oracle Warehouse Management System integration foundation for the entire FLEXT ecosystem.

**ZERO TOLERANCE ENFORCEMENT**: object deviation from these patterns requires explicit approval from FLEXT architecture authority.

**ENTERPRISE GRADE**: Production-ready Oracle WMS integration with comprehensive enterprise features, security, and monitoring.

**CLEAN ARCHITECTURE**: Strict separation of Oracle WMS business logic, application services, and infrastructure concerns.

**FLEXT ECOSYSTEM INTEGRATION**: Complete integration with flext-core, flext-api, flext-db-oracle, and flext-observability patterns.

---

## 🔗 RELATED FLEXT ECOSYSTEM PROJECTS

### **Core Dependencies (MANDATORY)**

- **flext-core**: Foundation patterns, FlextResult, logging, DI container
- **flext-api**: Enterprise API client patterns and authentication
- **flext-db-oracle**: Oracle database connectivity and schema management
- **flext-observability**: Monitoring, tracing, and alerting

### **Singer Integration Projects**

- **flext-tap-oracle-wms**: Oracle WMS data extraction via Singer
- **flext-target-oracle-wms**: Oracle WMS data loading via Singer
- **flext-dbt-oracle-wms**: Oracle WMS data transformations via dbt

### **Enterprise Platform Integration**

- **flext-auth**: Enterprise authentication and authorization
- **flext-config**: Centralized configuration management
- **flext-quality**: Quality gates and validation framework

---

**FINAL AUTHORITY**: flext-oracle-wms is the single source of truth for all Oracle Warehouse Management System integration operations within the FLEXT ecosystem. No custom Oracle WMS implementations are permitted.
