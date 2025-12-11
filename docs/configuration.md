# Configuration Guide

**Settings and environment management for flext-oracle-wms**

**Version**: 0.9.9 RC | **Last Updated**: September 17, 2025 | **Status**: Test configuration only · 1.0.0 Release Preparation

---

## Configuration Overview

flext-oracle-wms provides test configuration framework requiring implementation for production Oracle WMS Cloud connectivity.

## Test Configuration

### FlextOracleWmsModuleSettings.for_testing()

Current implementation provides test configuration with fake URLs:

```python
from flext_oracle_wms import FlextOracleWmsModuleSettings

config = FlextOracleWmsModuleSettings.for_testing()
print(config.oracle_wms_base_url)  # "https://test.example.com"
print(config.oracle_wms_username)  # "test_user"
print(config.api_version)          # Current API version
print(config.oracle_wms_timeout)   # Default timeout
```

## Environment Variables

### Test Environment

```bash
# Current test configuration
export FLEXT_ORACLE_WMS_BASE_URL="https://test.example.com"
export FLEXT_ORACLE_WMS_USERNAME="test_user"
export FLEXT_ORACLE_WMS_PASSWORD="test_password"
export FLEXT_ORACLE_WMS_TIMEOUT="30"
export FLEXT_ORACLE_WMS_API_VERSION="v1"
```

### Required for Production (Not Implemented)

```bash
# Oracle WMS Cloud connection (requires implementation)
export FLEXT_ORACLE_WMS_BASE_URL="https://your-instance.oraclecloud.com"
export FLEXT_ORACLE_WMS_USERNAME="api_service_user"
export FLEXT_ORACLE_WMS_PASSWORD="secure_enterprise_password"

# Authentication method (requires implementation)
export FLEXT_ORACLE_WMS_AUTH_METHOD="oauth2"  # basic, oauth2, api_key

# Performance tuning (requires implementation)
export FLEXT_ORACLE_WMS_TIMEOUT="60"
export FLEXT_ORACLE_WMS_MAX_RETRIES="5"
export FLEXT_ORACLE_WMS_CACHE_TTL="3600"

# FLEXT integration (requires implementation)
export FLEXT_LOG_LEVEL="info"
export FLEXT_ENABLE_METRICS="true"
```

## Configuration Classes

### FlextOracleWmsClientSettings

Configuration for Oracle WMS client (framework structure):

```python
from flext_oracle_wms import FlextOracleWmsClientSettings

# Note: This is framework structure, not fully implemented
config = FlextOracleWmsClientSettings(
    base_url="https://test.example.com",  # Currently only test URLs
    username="test_user",
    password="test_password",
    timeout=30,
    # Additional configuration options
)
```

### Authentication Configuration (Framework)

Based on source code analysis, authentication framework exists but requires implementation:

```python
from flext_oracle_wms import OracleWMSAuthMethod

# Framework supports these methods (implementation required)
auth_methods = [
    OracleWMSAuthMethod.BASIC,    # Username/password
    OracleWMSAuthMethod.OAUTH2,   # Token-based (not implemented)
    OracleWMSAuthMethod.API_KEY,  # API key (not implemented)
]
```

## Configuration Validation

### Current Validation

The framework includes Pydantic-based configuration validation:

```python
# Configuration validation is implemented
config = FlextOracleWmsModuleSettings.for_testing()
# Pydantic automatically validates configuration structure
```

### Required Implementation

For production Oracle WMS Cloud integration:

1. **Real URL validation** - Replace test URLs with actual Oracle WMS Cloud endpoints
2. **Authentication validation** - Implement OAuth2 and API key authentication
3. **Connection testing** - Validate against real Oracle WMS instances
4. **SSL/TLS configuration** - Proper certificate handling
5. **Rate limiting** - Configure API call limits per Oracle WMS guidelines

## Oracle WMS Cloud Requirements

### API Version Support

Based on Oracle WMS best practices research:

- **LGF v10 APIs** - Modern endpoint support (not implemented)
- **Legacy APIs** - Backward compatibility (partial support)
- **Page size limits** - Up to 1250 records per request
- **Mandatory filters** - Required for data extraction

### Authentication Requirements

Oracle WMS Cloud authentication standards:

- **BasicAuth** - Username/password with `lgfapi_update_access` permission
- **OAuth2** - Token-based authentication (recommended for production)
- **Dedicated users** - Service accounts with appropriate permissions
- **Permission levels** - Read vs write access control

## Implementation Status

### Current Status

- ✅ **Test configuration** - Framework with fake URLs
- ✅ **Pydantic validation** - Configuration structure validation
- ✅ **Environment variable support** - Basic environment loading
- ❌ **Real Oracle WMS connectivity** - No actual connection validation
- ❌ **OAuth2 implementation** - Authentication framework only
- ❌ **Production configuration** - No real Oracle WMS Cloud settings

### Required Implementation

1. Replace test URLs with actual Oracle WMS Cloud endpoints
2. Implement OAuth2 authentication flow
3. Add SSL/TLS certificate validation
4. Configure rate limiting and retry policies
5. Validate against real Oracle WMS instances

---

**Last Updated**: September 17, 2025 | **Status**: Test configuration only, requires Oracle WMS Cloud implementation · 1.0.0 Release Preparation
