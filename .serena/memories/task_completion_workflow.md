# Task Completion Workflow

## Mandatory Quality Gates (Execute After Every Change)

```bash
# 1. ALWAYS run complete validation
make validate

# 2. Alternative: Quick check for minor changes
make check
```

## Required Standards Before Completion

- **Zero Errors**: All quality gates must pass
- **Type Safety**: 100% MyPy compliance
- **Test Coverage**: 90% minimum coverage
- **Security**: Zero security vulnerabilities
- **Linting**: Clean ruff checks

## Pre-Commit Requirements

```bash
# These run automatically with pre-commit hooks:
- ruff check
- ruff format
- mypy
- bandit (security)
```

## When Making Code Changes

1. **Make changes**
2. **Format code**: `make format`
3. **Fix linting**: `make fix`
4. **Validate types**: `make type-check`
5. **Run tests**: `make test`
6. **Full validation**: `make validate`

## Docker Validation (For Major Changes)

```bash
make docker-full-validation  # Complete containerized testing
```

## Failure Recovery

- **Test failures**: Fix failing tests before proceeding
- **Type errors**: Address all MyPy errors
- **Linting issues**: Use `make fix` for auto-fixable issues
- **Coverage below 90%**: Add tests for uncovered code

## FLEXT Compliance Checks

- Verify no direct httpx imports (should use flext-api)
- Check for unified class architecture (single class per module)
- Ensure FlextResult patterns for error handling
- Validate proper flext-core integration

## Documentation Updates

- Update docstrings for modified APIs
- Ensure examples remain functional
- Check that README reflects actual capabilities
