# Project Purpose and Tech Stack

## Project Purpose

flext-oracle-wms is an Oracle Warehouse Management System (WMS) integration framework for the FLEXT data integration ecosystem. Version 0.9.0 is described as a "framework with implementation gaps" requiring substantial implementation work to achieve Oracle WMS Cloud integration.

## Status

- Framework structure exists but with limited proven functionality
- Tests use fake URLs (test.example.com) and expect network failures
- Contains mock implementations but lacks real Oracle WMS connectivity
- Currently has 99 classes across 6,974 lines of code with significant scaffolding

## Tech Stack

- **Python**: 3.13+ (strict version requirement)
- **Framework**: FLEXT ecosystem (flext-core, flext-api, flext-observability)
- **Type Safety**: Pydantic v2, MyPy strict mode, full type annotations
- **HTTP Client**: httpx (violates FLEXT compliance - should use flext-api)
- **Testing**: pytest with 90% coverage target
- **Package Management**: Poetry
- **Quality Tools**: Ruff (linting), MyPy (types), Bandit (security)
- **Documentation**: MkDocs
- **Containerization**: Docker with docker-compose

## Dependencies

- pydantic (>=2.11.7)
- httpx (>=0.28.1) - FLEXT violation
- pydantic-settings (>=2.10.1)
- Python-dotenv (>=1.1.1)
- flext-core (local workspace dependency)
- flext-api, flext-observability (local workspace dependencies)

## Architecture

- 18 Python modules in src/flext_oracle_wms/
- 99 classes total (violates FLEXT unified class requirement)
- 22 Oracle WMS API endpoints defined
- Comprehensive exception hierarchy (16 exception classes)
- Mock server implementation for testing
