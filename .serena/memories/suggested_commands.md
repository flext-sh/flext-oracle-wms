# Essential Development Commands

## Quality Gates (Most Important)

```bash
make validate           # Complete validation pipeline (lint + type + security + test)
make check             # Quick health check (lint + type-check)
make test              # Run tests with 90% coverage requirement
```

## Individual Quality Checks

```bash
make lint              # Ruff linting
make type-check        # MyPy strict mode type checking
make security          # Bandit + pip-audit security scan
make format            # Auto-format code with ruff
make fix               # Auto-fix linting issues
```

## Testing Commands

```bash
make test-unit         # Unit tests only
make test-integration  # Integration tests
make test-wms          # WMS-specific tests
make test-oracle       # Oracle database tests
make test-fast         # Tests without coverage
make coverage-html     # Generate HTML coverage report
```

## Oracle WMS Operations (May Not Work - Test URLs)

```bash
make wms-test          # Test WMS connectivity (uses test.example.com)
make wms-schema        # Validate WMS schema
make oracle-connect    # Test Oracle connection
```

## Development Setup

```bash
make install           # Install dependencies
make install-dev       # Install dev dependencies
make setup             # Complete project setup with pre-commit
```

## Docker Operations (Comprehensive)

```bash
make docker-build          # Build Docker images
make docker-validate       # Complete Docker validation
make docker-test           # Run tests in Docker
make docker-examples       # Run examples in Docker
make docker-full-validation # Complete Docker workflow
```

## Utilities

```bash
make build             # Build package
make clean             # Clean build artifacts
make diagnose          # Project diagnostics
make doctor            # Health check with diagnostics
```

## Shortcuts

```bash
make v    # validate
make t    # test
make l    # lint
make f    # format
make tc   # type-check
```
