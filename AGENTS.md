# AGENTS.md — flext-oracle-wms

> **Parent workspace law** lives in [`../AGENTS.md`](../AGENTS.md) — read it first.
> Universal engineering core: `~/.agents/UNIVERSAL_CORE.md`. Composition: global skills + parent/root `AGENTS.md` + this scope delta. Do not re-embed universal law.
>
> **Standalone / independent mode:** when `../AGENTS.md` does not resolve, pin the parent raw `AGENTS.md` URL to the same branch/release as this package (never `main`).

<!-- AIHUB-AGENTS-SCOPE-LOCAL-BEGIN -->
**Package:** `flext_oracle_wms` · deps: `flext-api`, `flext-cli`, `flext-core`

## Overview

Enterprise Oracle WMS (Warehouse Management System) REST client library. Base for `flext-tap-oracle-wms`, `flext-target-oracle-wms`, `flext-dbt-oracle-wms`.

## Structure

```text
src/flext_oracle_wms/
├── api.py                    # FlextOracleWmsApi facade: execute / api_endpoints / create_*_client
├── errors.py
├── _utilities/
│   ├── client.py            # WMS client (held as _client)
│   └── http_client.py       # HTTP transport
├── constants.py typings.py protocols.py models.py utilities.py   # AUTO-GENERATED facets
└── _models/ _protocols/
```

## Code Map

| Symbol | Kind | Location | Role |
|--------|------|----------|------|
| `FlextOracleWmsApi` | class | `api.py` | facade: `execute`, `api_endpoints`, `create_flext_http_client`, `create_oracle_wms_client` |
| WMS client | class | `_utilities/client.py` | REST client (`_client`) |

## Conventions (specific to this package)

- Client creation resolves base URL, timeout, headers, and SSL verification **from settings** — never embed transport defaults inline.
- Requests/responses are typed `m.*` models.

## Anti-Patterns / Gotchas

- Go through `FlextOracleWmsApi`; the client is a private `_client`, not a public surface.

## Commands

```bash
make check PROJECT=flext-oracle-wms
make test  PROJECT=flext-oracle-wms
```
<!-- AIHUB-AGENTS-SCOPE-LOCAL-END -->
