# Development Standards

**Version 0.9.0 | September 17, 2025 | Status: Framework standards for implementation**

## Standards Documentation

### Python Development
- **[Python Module Organization](python-module-organization.md)** - Module structure and organization standards

## Current Standards Status

Based on source code analysis, the library requires adherence to FLEXT standards:

### Code Quality Requirements
- **Type Safety** - MyPy strict compliance (implemented)
- **Error Handling** - FlextResult patterns (implemented)
- **Unified Classes** - Single class per module with nested helpers (required)
- **FLEXT Integration** - flext-api, flext-auth compliance (required)

### Quality Validation
```bash
make validate           # Complete validation pipeline
make lint              # Code quality checks
make type-check        # Type safety verification
```

### Critical Standards Issues
1. **Multiple classes per module** - violates FLEXT unified pattern
2. **httpx direct usage** - violates flext-api requirement
3. **Custom authentication** - should use flext-auth patterns

### Required Implementation Work
- Consolidate to unified class architecture
- Migrate to flext-api HTTP client patterns
- Integrate with flext-auth for authentication
- Validate real Oracle WMS connectivity

---

**Last Updated**: September 17, 2025 | **Status**: Framework requiring FLEXT compliance implementation