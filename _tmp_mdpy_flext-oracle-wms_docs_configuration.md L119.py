# from flext-oracle-wms/docs/configuration.md:119
from __future__ import annotations
from flext_oracle_wms import c

# Framework supports these methods (implementation required)
OracleWMSAuthMethod = c.OracleWms.OracleWMSAuthMethod
auth_methods = [
    OracleWMSAuthMethod.BASIC,  # Username/password
    OracleWMSAuthMethod.OAUTH2,  # Token-based (not implemented)
    OracleWMSAuthMethod.API_KEY,  # API key (not implemented)
]
