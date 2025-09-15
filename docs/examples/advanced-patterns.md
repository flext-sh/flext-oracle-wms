# Advanced Usage Patterns

**Advanced patterns and implementations for flext-oracle-wms**

**Version**: 0.9.0 | **Last Updated**: September 17, 2025 | **Status**: Framework patterns requiring implementation

---

## Advanced Configuration Patterns

### Environment-Specific Configuration

Framework structure for different environments:

```python
from flext_oracle_wms import FlextOracleWmsModuleConfig
import os

def get_environment_config():
    """Load configuration based on environment."""
    env = os.getenv("FLEXT_ENV", "test")

    if env == "test":
        # Current working configuration
        return FlextOracleWmsModuleConfig.for_testing()

    elif env == "production":
        # Requires implementation
        return FlextOracleWmsModuleConfig(
            oracle_wms_base_url=os.getenv("ORACLE_WMS_PROD_URL"),
            oracle_wms_username=os.getenv("ORACLE_WMS_PROD_USER"),
            # OAuth2 implementation required
        )

    else:
        raise ValueError(f"Unknown environment: {env}")
```

### Advanced Error Handling Patterns

```python
from flext_oracle_wms.wms_exceptions import (
    FlextOracleWmsError,
    FlextOracleWmsConnectionError,
    FlextOracleWmsAuthenticationError,
    FlextOracleWmsApiError
)
from flext_core import FlextResult
import logging

class OracleWmsErrorHandler:
    """Advanced error handling for Oracle WMS operations."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def handle_operation_result(self, result: FlextResult) -> bool:
        """Handle operation results with advanced error analysis."""
        if result.is_success:
            self.logger.info("Operation completed successfully")
            return True

        # Analyze error types
        error = result.error
        if error and "connection" in error.lower():
            self.logger.warning("Connection issue detected")
            return self._handle_connection_error(error)

        elif error and "authentication" in error.lower():
            self.logger.error("Authentication failure")
            return self._handle_auth_error(error)

        else:
            self.logger.error(f"Unknown error: {error}")
            return False

    def _handle_connection_error(self, error: str) -> bool:
        """Handle connection-specific errors."""
        # With test config, connection errors are expected
        if "test.example.com" in error:
            self.logger.info("Expected connection error with test configuration")
            return True

        # For real Oracle WMS, implement retry logic
        self.logger.warning("Real connection error - retry logic needed")
        return False

    def _handle_auth_error(self, error: str) -> bool:
        """Handle authentication-specific errors."""
        # Requires OAuth2 implementation
        self.logger.error("Authentication error - OAuth2 implementation required")
        return False
```

## Entity Discovery Patterns

### Advanced Entity Processing

```python
import asyncio
from typing import List, Dict, Any
from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsModuleConfig
from flext_core import FlextResult

class EntityDiscoveryManager:
    """Advanced entity discovery and processing."""

    def __init__(self, config: FlextOracleWmsModuleConfig):
        self.config = config
        self.client = FlextOracleWmsClient(config)

    async def discover_and_process_entities(self) -> Dict[str, Any]:
        """Discover entities and process metadata."""
        results = {
            "discovered_count": 0,
            "processed_entities": [],
            "errors": []
        }

        try:
            # Discovery operation (will fail with test config)
            discovery_result = self.client.discover_entities()

            if discovery_result.is_success:
                entities = discovery_result.value
                results["discovered_count"] = len(entities)

                # Process each entity
                for entity in entities:
                    try:
                        processed = await self._process_entity(entity)
                        results["processed_entities"].append(processed)
                    except Exception as e:
                        results["errors"].append(f"Entity processing error: {e}")

            else:
                # Expected with test configuration
                results["errors"].append(f"Discovery failed: {discovery_result.error}")

        except Exception as e:
            results["errors"].append(f"Discovery exception: {e}")

        return results

    async def _process_entity(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Process individual entity with metadata."""
        return {
            "name": entity.get("name", "unknown"),
            "type": entity.get("type", "unknown"),
            "metadata": {
                "processed_at": "2025-09-17",
                "framework_version": "0.9.0"
            }
        }
```

## Batch Processing Patterns

### Batch Operation Framework

```python
from typing import List, Callable, TypeVar, Generic
from dataclasses import dataclass
import asyncio

T = TypeVar('T')
R = TypeVar('R')

@dataclass
class BatchOperation(Generic[T, R]):
    """Framework for batch operations."""
    items: List[T]
    operation: Callable[[T], R]
    batch_size: int = 10
    max_concurrent: int = 3

class BatchProcessor:
    """Advanced batch processing for Oracle WMS operations."""

    def __init__(self, client: FlextOracleWmsClient):
        self.client = client

    async def process_batch(self, operation: BatchOperation) -> List[R]:
        """Process items in batches with concurrency control."""
        results = []

        # Split into batches
        batches = [
            operation.items[i:i + operation.batch_size]
            for i in range(0, len(operation.items), operation.batch_size)
        ]

        # Process batches with concurrency control
        semaphore = asyncio.Semaphore(operation.max_concurrent)

        async def process_batch_chunk(batch: List[T]) -> List[R]:
            async with semaphore:
                batch_results = []
                for item in batch:
                    try:
                        result = operation.operation(item)
                        batch_results.append(result)
                    except Exception as e:
                        # Handle individual item failures
                        batch_results.append(f"Error: {e}")
                return batch_results

        # Execute all batches
        batch_tasks = [process_batch_chunk(batch) for batch in batches]
        batch_results = await asyncio.gather(*batch_tasks)

        # Flatten results
        for batch_result in batch_results:
            results.extend(batch_result)

        return results

# Example usage:
async def demonstrate_batch_processing():
    """Demonstrate batch processing patterns."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)
    processor = BatchProcessor(client)

    # Define batch operation
    items = ["item1", "item2", "item3", "item4", "item5"]

    def process_item(item: str) -> str:
        # Simulate processing (with test config, actual operations will fail)
        return f"processed_{item}"

    batch_op = BatchOperation(
        items=items,
        operation=process_item,
        batch_size=2,
        max_concurrent=2
    )

    results = await processor.process_batch(batch_op)
    print(f"Batch processing results: {results}")
```

## Caching Patterns

### Entity Metadata Caching

```python
from typing import Dict, Any, Optional
import time
from dataclasses import dataclass

@dataclass
class CacheEntry:
    """Cache entry with TTL."""
    data: Any
    timestamp: float
    ttl: float

    @property
    def is_expired(self) -> bool:
        return time.time() - self.timestamp > self.ttl

class EntityCache:
    """Advanced caching for Oracle WMS entities."""

    def __init__(self, default_ttl: float = 3600):  # 1 hour default
        self.cache: Dict[str, CacheEntry] = {}
        self.default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        """Get cached entry if not expired."""
        if key in self.cache:
            entry = self.cache[key]
            if not entry.is_expired:
                return entry.data
            else:
                del self.cache[key]
        return None

    def set(self, key: str, data: Any, ttl: Optional[float] = None) -> None:
        """Set cache entry with TTL."""
        ttl = ttl or self.default_ttl
        self.cache[key] = CacheEntry(data, time.time(), ttl)

    def clear_expired(self) -> int:
        """Clear expired entries and return count."""
        expired_keys = [
            key for key, entry in self.cache.items()
            if entry.is_expired
        ]

        for key in expired_keys:
            del self.cache[key]

        return len(expired_keys)

class CachedOracleWmsClient:
    """Oracle WMS client with advanced caching."""

    def __init__(self, config: FlextOracleWmsModuleConfig):
        self.client = FlextOracleWmsClient(config)
        self.cache = EntityCache()

    async def get_cached_entities(self) -> FlextResult[List[Dict[str, Any]]]:
        """Get entities with caching."""
        cache_key = "entities_list"

        # Try cache first
        cached_entities = self.cache.get(cache_key)
        if cached_entities is not None:
            return FlextResult.ok(cached_entities)

        # Cache miss - fetch from Oracle WMS
        result = self.client.discover_entities()

        if result.is_success:
            # Cache successful results
            self.cache.set(cache_key, result.value, ttl=1800)  # 30 minutes

        return result
```

## Monitoring and Observability

### Advanced Logging Patterns

```python
import logging
from typing import Dict, Any
from functools import wraps
import time

class OracleWmsLogger:
    """Advanced logging for Oracle WMS operations."""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.operation_metrics: Dict[str, Dict[str, Any]] = {}

    def log_operation_start(self, operation: str, context: Dict[str, Any]) -> str:
        """Log operation start with context."""
        operation_id = f"{operation}_{int(time.time())}"

        self.logger.info(
            f"Starting operation: {operation}",
            extra={"operation_id": operation_id, "context": context}
        )

        self.operation_metrics[operation_id] = {
            "operation": operation,
            "start_time": time.time(),
            "context": context
        }

        return operation_id

    def log_operation_end(self, operation_id: str, success: bool, result: Any = None) -> None:
        """Log operation completion with metrics."""
        if operation_id in self.operation_metrics:
            metrics = self.operation_metrics[operation_id]
            duration = time.time() - metrics["start_time"]

            self.logger.info(
                f"Operation completed: {metrics['operation']}",
                extra={
                    "operation_id": operation_id,
                    "success": success,
                    "duration_seconds": duration,
                    "result_summary": str(result)[:100] if result else None
                }
            )

            del self.operation_metrics[operation_id]

def log_oracle_wms_operation(operation_name: str):
    """Decorator for logging Oracle WMS operations."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            logger = OracleWmsLogger(func.__module__)

            context = {
                "function": func.__name__,
                "args_count": len(args),
                "kwargs": list(kwargs.keys())
            }

            operation_id = logger.log_operation_start(operation_name, context)

            try:
                result = await func(*args, **kwargs)
                logger.log_operation_end(operation_id, True, result)
                return result
            except Exception as e:
                logger.log_operation_end(operation_id, False, str(e))
                raise

        return wrapper
    return decorator

# Example usage:
@log_oracle_wms_operation("entity_discovery")
async def discover_entities_with_logging():
    """Entity discovery with comprehensive logging."""
    config = FlextOracleWmsModuleConfig.for_testing()
    client = FlextOracleWmsClient(config)

    return client.discover_entities()
```

## Implementation Status

### Advanced Patterns Available

- ✅ **Error handling patterns** - Exception hierarchy with context
- ✅ **Caching framework** - TTL-based caching structure
- ✅ **Batch processing** - Async batch operation framework
- ✅ **Logging patterns** - Structured logging with metrics

### Advanced Patterns Requiring Implementation

- ❌ **Real Oracle WMS connectivity** - All patterns use test configuration
- ❌ **OAuth2 authentication flow** - Advanced auth patterns need implementation
- ❌ **LGF v10 API patterns** - Modern Oracle WMS API integration
- ❌ **Production monitoring** - Real observability integration

---

**Last Updated**: September 17, 2025 | **Status**: Framework patterns requiring Oracle WMS Cloud implementation