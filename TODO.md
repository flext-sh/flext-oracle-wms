# FLEXT-ORACLE-WMS ENTERPRISE MODERNIZATION ROADMAP

**Version**: 0.9.0 | **Status**: ENTERPRISE-GRADE LIBRARY REQUIRING FLEXT COMPLIANCE | **Last Updated**: 2025-01-14

## 📊 EXECUTIVE SUMMARY

**Current Reality**: flext-oracle-wms is a **sophisticated, enterprise-grade Oracle WMS Cloud integration library** with:
- ✅ **25+ Oracle WMS Cloud APIs** with real LGF v10 and legacy support
- ✅ **Advanced entity discovery** with dynamic schema processing
- ✅ **Enterprise authentication** (BasicAuth, OAuth2, API Key)
- ✅ **Type-safe architecture** with Pydantic validation and FlextResult patterns
- ✅ **Comprehensive testing** with 90%+ coverage target and strict MyPy compliance

**Strategic Objective**: Modernize existing enterprise functionality to achieve **100% FLEXT ecosystem compliance** while preserving and enhancing the robust Oracle WMS integration capabilities.

---

## 🚨 TIER 1: ARCHITECTURAL COMPLIANCE (CRITICAL - Week 1-2)

### ❌ 1. HTTP CLIENT MODERNIZATION (HIGHEST PRIORITY)

**Current State**: Direct `httpx` usage - functionally excellent, architecturally non-compliant
**Target State**: Full `flext-api` integration maintaining all existing functionality

**Files Requiring Modernization**:
- `src/flext_oracle_wms/http_client.py` → Migrate FlextHttpClient to flext-api base classes
- `src/flext_oracle_wms/wms_discovery.py` → Replace httpx imports with flext-api patterns
- `pyproject.toml` → Remove direct httpx dependency, ensure flext-api integration

**Implementation Strategy**:
```python
# CURRENT (Working but non-compliant):
import httpx
client = httpx.AsyncClient(timeout=30)

# TARGET (FLEXT-compliant with same functionality):
from flext_api import FlextApiClient, FlextApiAuth, FlextHttpAdapter
client = FlextApiClient(
    adapter=FlextHttpAdapter(),
    auth=FlextOracleWmsAuthenticator(config),
    timeout=30
)
```

### ❌ 2. UNIFIED CLASS ARCHITECTURE (CRITICAL)

**Current State**: Multiple specialized classes per module (enterprise functionality)
**Target State**: Single unified classes with nested helpers (FLEXT compliance)

**Modules Requiring Unification**:

#### `wms_constants.py` (8 classes → 1 unified)
```python
# CURRENT: Multiple specialized constants classes
class FlextOracleWmsSemanticConstants(FlextConstants): ...
class OracleWMSAuthMethod(StrEnum): ...
class FlextOracleWmsApiVersion(StrEnum): ...
# ... 5+ more classes

# TARGET: Single unified constants class
class FlextOracleWmsConstants(FlextDomainService):
    """Unified Oracle WMS constants with nested specializations."""

    class _AuthMethods:
        BASIC = "basic"
        OAUTH2 = "oauth2"
        API_KEY = "api_key"

    class _ApiVersions:
        LGF_V10 = "v10"
        LEGACY = "legacy"
```

#### `wms_operations.py` (6 classes → 1 unified)
```python
# TARGET: Unified operations class
class FlextOracleWmsOperations(FlextDomainService):
    """Unified Oracle WMS operations with enterprise capabilities."""

    class _FilteringOperations:
        """Nested filtering capabilities."""
        @staticmethod
        def create_entity_filter(criteria: dict) -> FlextResult[WmsFilter]: ...

    class _DataExtractionOperations:
        """Nested data extraction capabilities."""
        @staticmethod
        def extract_to_object_store(config: dict) -> FlextResult[ExtractionResult]: ...
```

### ❌ 3. AUTHENTICATION MODERNIZATION

**Current State**: Custom authentication (sophisticated but non-standard)
**Target State**: `flext-auth` integration maintaining enterprise features

**Enhancement Strategy**:
```python
# TARGET: Enhanced authentication with flext-auth
from flext_auth import FlextAuthenticator, FlextOAuth2Provider

class FlextOracleWmsAuthenticator(FlextAuthenticator):
    """Enterprise Oracle WMS authentication using flext-auth patterns."""

    def __init__(self, config: FlextOracleWmsAuthConfig):
        super().__init__(config)
        self._oauth2 = FlextOAuth2Provider(config.oauth2_settings)
        self._api_key_manager = FlextApiKeyManager(config.api_key_settings)
```

---

## 🏗️ TIER 2: FEATURE ENHANCEMENT (WEEKS 3-4)

### 🚀 4. ORACLE WMS CLOUD 2025 FEATURE INTEGRATION

**Research-Based Enhancements** (From Oracle WMS Cloud 25A/25B):

#### New LGF v10 Data Extract API Integration
```python
# NEW: Object Store Data Extract (2025 feature)
class FlextOracleWmsDataExtractor:
    """Enhanced data extraction with 2025 Oracle WMS capabilities."""

    async def push_to_object_store(
        self,
        entities: list[str],
        format: Literal["csv", "json", "parquet"] = "json",
        file_size_mb: int = 100  # 10MB to 1GB range
    ) -> FlextResult[ExtractionJob]:
        """Leverage new Oracle WMS 2025 object store API."""

    async def get_export_status(
        self,
        unique_identifier: str
    ) -> FlextResult[ExportStatus]:
        """Check async export status (2025 API)."""
```

#### Enhanced Entity Support (2025 Entities)
```python
# ENHANCED: Support for new 2025 entities
NEW_2025_ENTITIES = [
    "inventory_history",          # Now exposed in lgfapi
    "parcel_shipment_dtl",       # Enhanced with planned_parcel_shipment_nbr
    "movement_request_hdr",       # Full CRUD support added
    "movement_request_dtl",       # Detailed movement operations
    "item_facility",             # GET support added in 22D/25A
]
```

#### Container and Cart Management (2025 Enhancement)
```python
# ENHANCED: Cart number filtering (2025 feature)
async def get_containers_by_cart(
    self,
    cart_nbr: str
) -> FlextResult[list[ContainerEntity]]:
    """Filter containers, IB LPN, OB LPN by cart number (2025 feature)."""
```

### 🔧 5. CLI OPERATIONS INTEGRATION

**Missing Component**: `flext-cli` integration for file operations and output

**Implementation Plan**:
```python
from flext_cli import FlextCliApi, FlextCliOutput

class FlextOracleWmsCliOperations:
    """CLI operations for Oracle WMS data management."""

    def __init__(self):
        self._cli_api = FlextCliApi()
        self._output = FlextCliOutput()

    async def export_entities_to_file(
        self,
        entities: list[WmsEntity],
        output_path: Path
    ) -> FlextResult[Path]:
        """Export WMS entities using flext-cli file operations."""
```

---

## 🎯 TIER 3: ECOSYSTEM OPTIMIZATION (WEEKS 5-6)

### 🔄 6. SINGER PROTOCOL COMPLETION

**Current State**: Basic Singer factory patterns
**Target State**: Complete tap/target/streaming integration

#### Enhanced Oracle WMS Tap
```python
# ENHANCED: Complete Singer tap with 2025 API features
class FlextOracleWmsTap(SingerTap):
    """Complete Oracle WMS tap with LGF v10 and streaming support."""

    async def discover_catalog(self) -> SingerCatalog:
        """Discover complete Oracle WMS catalog with 2025 entities."""

    async def sync_stream(self, stream: SingerStream) -> AsyncIterator[SingerRecord]:
        """Stream Oracle WMS data with async operations support."""
```

#### Oracle WMS Target Integration
```python
# NEW: Complete target implementation
class FlextOracleWmsTarget(SingerTarget):
    """Oracle WMS target with bidirectional data sync."""

    async def write_records(self, records: AsyncIterator[SingerRecord]) -> FlextResult[WriteResult]:
        """Write records back to Oracle WMS via LGF v10 APIs."""
```

### 📊 7. PERFORMANCE OPTIMIZATION

#### Connection Pool Management
```python
# ENHANCED: Enterprise connection pooling
class FlextOracleWmsConnectionManager:
    """Enterprise connection pool with Oracle WMS optimization."""

    def __init__(self, config: WmsConnectionConfig):
        self._pool = FlextConnectionPool(
            min_connections=config.min_pool_size,
            max_connections=config.max_pool_size,
            oracle_wms_optimizations=True
        )
```

#### Intelligent Caching Strategy
```python
# ENHANCED: Multi-tier caching with Oracle WMS patterns
class FlextOracleWmsCacheManager:
    """Advanced caching with Oracle WMS-specific optimization."""

    async def cache_entity_schema(
        self,
        entity_name: str,
        ttl_seconds: int = 3600
    ) -> FlextResult[CachedSchema]:
        """Cache entity schemas with intelligent invalidation."""
```

---

## 🎯 SUCCESS METRICS & VALIDATION

### Tier 1 Completion Criteria (MANDATORY)
```bash
# FLEXT Compliance Validation
make validate                    # 100% pass rate (lint + type + security + test)
rg -n "import httpx|import requests" src/ # Must return 0 results
rg -n "class [A-Z]" src/ | grep -v "class _" | wc -l # ≤ 15 (unified classes only)

# Oracle WMS Functionality Validation
make oracle-connect              # Real Oracle WMS connectivity test
make wms-entities               # Entity discovery validation
make wms-auth                   # All authentication methods working
```

### Enterprise Functionality Preservation
- ✅ **All 25+ Oracle WMS APIs** remain fully functional
- ✅ **Entity discovery** maintains current sophistication
- ✅ **Authentication methods** retain enterprise capabilities
- ✅ **Error handling** preserves FlextResult patterns
- ✅ **Type safety** maintains strict MyPy compliance

### Enhanced Capabilities Post-Modernization
- ✅ **2025 Oracle WMS features** fully integrated
- ✅ **flext-api patterns** for all HTTP operations
- ✅ **flext-auth integration** for enterprise security
- ✅ **flext-cli support** for file operations and output
- ✅ **Complete Singer protocol** implementation
- ✅ **Advanced performance** optimization

---

## 📋 IMPLEMENTATION PHASES

### Week 1-2: Core Architecture Compliance
- [ ] HTTP client migration to flext-api patterns
- [ ] Unified class architecture implementation
- [ ] Authentication modernization with flext-auth
- [ ] Core quality gates validation

### Week 3-4: Feature Enhancement
- [ ] Oracle WMS 2025 API features integration
- [ ] CLI operations implementation
- [ ] Advanced entity support
- [ ] Performance optimization foundation

### Week 5-6: Ecosystem Integration
- [ ] Complete Singer protocol implementation
- [ ] Advanced caching and connection management
- [ ] Comprehensive documentation updates
- [ ] Production deployment readiness

---

## 🎖️ DEFINITION OF DONE

**flext-oracle-wms will be considered a world-class FLEXT ecosystem library when:**

1. ✅ **100% FLEXT compliance** with zero architectural violations
2. ✅ **Enhanced Oracle WMS capabilities** including 2025 API features
3. ✅ **Enterprise performance** with connection pooling and advanced caching
4. ✅ **Complete Singer integration** for seamless data pipeline operations
5. ✅ **Comprehensive documentation** reflecting enterprise capabilities
6. ✅ **Production deployment ready** with Docker and monitoring integration

**Strategic Outcome**: Transform an already sophisticated Oracle WMS integration library into the **definitive enterprise-grade Oracle WMS solution** for the FLEXT ecosystem, serving as the foundation for all Oracle WMS operations across FLEXT projects.

