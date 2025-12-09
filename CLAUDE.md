# flext-oracle-wms - FLEXT Enterprise Integration

**Hierarchy**: PROJECT
**Parent**: [../CLAUDE.md](../CLAUDE.md) - Workspace standards
**Last Update**: 2025-12-07

---

## Project Overview

**FLEXT-Oracle-WMS** is the enterprise Oracle Warehouse Management System (WMS) integration foundation for the FLEXT ecosystem.

**Version**: 0.9.9 RC  
**Status**: Production-ready  
**Python**: 3.13+

---

## Essential Commands

```bash
# Setup and validation
make setup                    # Complete development environment setup
make validate                 # Complete validation (lint + type + security + test)
make check                    # Quick check (lint + type)

# Quality gates
make lint                     # Ruff linting
make type-check               # Pyrefly type checking
make security                 # Bandit security scan
make test                     # Run tests
```

---

## Key Patterns

### Oracle WMS Integration

```python
from flext_core import FlextResult
from flext_oracle_wms import FlextOracleWms

wms = FlextOracleWms()

# WMS operations
result = wms.execute_operation(operation_type="...", params={...})
if result.is_success:
    response = result.unwrap()
```

---

## Critical Development Rules

### ZERO TOLERANCE Policies

**ABSOLUTELY FORBIDDEN**:
- ❌ Exception-based error handling (use FlextResult)
- ❌ Type ignores or `Any` types
- ❌ Mockpatch in tests

**MANDATORY**:
- ✅ Use `FlextResult[T]` for all operations
- ✅ Complete type annotations
- ✅ Zero Ruff violations

---

**See Also**:
- [Workspace Standards](../CLAUDE.md)
- [flext-core Patterns](../flext-core/CLAUDE.md)
- [flext-db-oracle Patterns](../flext-db-oracle/CLAUDE.md)
- [flext-oracle-oic Patterns](../flext-oracle-oic/CLAUDE.md)
