# Code Style and Conventions

## Type Safety (Strict Enforcement)

- **MyPy**: Strict mode enabled with comprehensive checks
- **Type Annotations**: Required for all functions and methods
- **Pydantic Models**: Used for all data structures
- **No object Types**: Explicit typing required, object types discouraged
- **Generic Types**: Used extensively (e.g., FlextResult[T])

## Code Structure Patterns

- **FLEXT Compliance**: Should use flext-core patterns (FlextResult, FlextLogger)
- **Single Responsibility**: Classes should have focused purposes
- **Error Handling**: All operations return FlextResult[T] for type-safe error handling
- **Configuration**: Pydantic-based config classes with validation

## Current Violations (Need Fixing)

- **Multiple Classes per Module**: 99 classes total (violates FLEXT unified class requirement)
- **HTTP Client**: Uses httpx directly (should use flext-api)
- **Helper Functions**: Some loose functions exist (should be nested in classes)

## Naming Conventions

- **Classes**: PascalCase with Flext prefix (FlextOracleWmsClient)
- **Functions**: snake_case
- **Constants**: UPPER_CASE with module prefix
- **Files**: snake_case.py
- **Modules**: Package structure: src/flext_oracle_wms/

## Documentation Style

- **Docstrings**: Required for all public APIs
- **Type Hints**: Comprehensive type annotations
- **Examples**: Practical usage examples in docstrings
- **Comments**: Minimal inline comments, prefer descriptive names

## Quality Standards

- **Ruff**: Linting with strict rules
- **Black**: Code formatting (though using ruff format)
- **Coverage**: 90% minimum test coverage target
- **Security**: Bandit security scanning required

## Import Organization

- **Root Level Only**: Import from package root (from flext_oracle_wms import ...)
- **No Internal Imports**: Avoid deep module imports
- **FLEXT Dependencies**: Import from flext-core, flext-api properly
