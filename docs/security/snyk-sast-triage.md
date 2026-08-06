# Triagem Snyk Code (SAST) — flext-sh/flext-oracle-wms

Gerado do scan Snyk da org Datacosmos (dump 2026-08-06).

**12 achados** — critical 0, high 0, medium 3, low 9

| categoria | achados |
|---|---|
| Use of Hardcoded Passwords | 9 |
| Use of Hardcoded Credentials | 3 |

## Achados

Coluna **Decisão**: `corrigir` / `falso-positivo` / `risco-aceito`.

| # | sev | categoria | arquivo | linha | CWE | Decisão |
|---|---|---|---|---|---|---|
| 1 | medium | Use of Hardcoded Passwords | `examples/02_configuration.py` | 111 | - | |
| 2 | medium | Use of Hardcoded Passwords | `examples/02_singleton_config.py` | 73 | - | |
| 3 | medium | Use of Hardcoded Passwords | `examples/02_singleton_config.py` | 85 | - | |
| 4 | low | Use of Hardcoded Passwords | `tests/conftest.py` | 32 | - | |
| 5 | low | Use of Hardcoded Credentials | `tests/unit/test_authentication.py` | 155 | - | |
| 6 | low | Use of Hardcoded Credentials | `tests/unit/test_authentication.py` | 166 | - | |
| 7 | low | Use of Hardcoded Credentials | `tests/unit/test_authentication.py` | 176 | - | |
| 8 | low | Use of Hardcoded Passwords | `tests/unit/test_config.py` | 32 | - | |
| 9 | low | Use of Hardcoded Passwords | `tests/unit/test_config_module.py` | 53 | - | |
| 10 | low | Use of Hardcoded Passwords | `tests/unit/test_declarative.py` | 45 | - | |
| 11 | low | Use of Hardcoded Passwords | `tests/unit/test_unified_config.py` | 45 | - | |
| 12 | low | Use of Hardcoded Passwords | `tests/unit/test_wms_client.py` | 73 | - | |

## Como triar

1. Abrir `arquivo:linha` e seguir o fluxo de dados até o sink.
2. Classificar: **corrigir** (entrada externa alcança o sink sem sanitização), **falso-positivo** (credencial de fixture, path de constante — registrar em `.snyk` com justificativa), **risco-aceito** (com prazo de revisão).

Dados brutos: `~/snyk-violations/sast/flext-sh__flext-oracle-wms.sast.json`

