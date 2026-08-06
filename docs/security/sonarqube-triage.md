# Triagem SonarCloud — flext-sh/flext-oracle-wms

Gerado do dump da plataforma SonarCloud (2026-08-06).

Bead de rastreio: `mro-2wjm.14`

## Resumo

**16 issues** — BLOCKER 2, CRITICAL 0, MAJOR 12, MINOR 2
Tipos: VULNERABILITY 4, BUG 0, CODE_SMELL 12

| regra | issues |
|---|---|
| `python:S108` | 6 |
| `python:S3516` | 2 |
| `githubactions:S8233` | 2 |
| `githubactions:S8264` | 1 |
| `text:S8565` | 1 |
| `python:S3358` | 1 |
| `python:S5778` | 1 |
| `python:S7504` | 1 |

## Issues

Coluna **Decisão**: `corrigir` / `falso-positivo` / `risco-aceito`.

| # | sev | tipo | regra | componente | linha | Decisão |
|---|---|---|---|---|---|---|
| 1 | BLOCKER | CODE_SMELL | `python:S3516` | `examples/01_basic_usage.py` | 75 | |
| 2 | BLOCKER | CODE_SMELL | `python:S3516` | `examples/01_basic_usage.py` | 99 | |
| 3 | MAJOR | VULNERABILITY | `githubactions:S8264` | `.github/workflows/docs.yml` | 18 | |
| 4 | MAJOR | VULNERABILITY | `githubactions:S8233` | `.github/workflows/docs.yml` | 19 | |
| 5 | MAJOR | VULNERABILITY | `githubactions:S8233` | `.github/workflows/docs.yml` | 20 | |
| 6 | MAJOR | CODE_SMELL | `python:S108` | `examples/02_configuration.py` | 215 | |
| 7 | MAJOR | CODE_SMELL | `python:S108` | `examples/02_configuration.py` | 217 | |
| 8 | MAJOR | CODE_SMELL | `python:S108` | `examples/02_configuration.py` | 222 | |
| 9 | MAJOR | CODE_SMELL | `python:S108` | `examples/02_configuration.py` | 232 | |
| 10 | MAJOR | CODE_SMELL | `python:S108` | `examples/02_configuration.py` | 247 | |
| 11 | MAJOR | CODE_SMELL | `python:S108` | `examples/03_complete_functionality_showcase.py` | 93 | |
| 12 | MAJOR | VULNERABILITY | `text:S8565` | `pyproject.toml` | - | |
| 13 | MAJOR | CODE_SMELL | `python:S3358` | `src/flext_oracle_wms/_utilities/filtering.py` | 205 | |
| 14 | MAJOR | CODE_SMELL | `python:S5778` | `tests/unit/test_helpers.py` | 126 | |
| 15 | MINOR | CODE_SMELL | `python:S7504` | `conftest.py` | 20 | |
| 16 | MINOR | CODE_SMELL | `python:S7500` | `src/flext_oracle_wms/_utilities/http_client.py` | 68 | |

## Como triar

1. **BLOCKER e CRITICAL primeiro**, e todo VULNERABILITY independente de severidade.
2. Classificar: **corrigir**, **falso-positivo** (marcar na plataforma SonarCloud com justificativa), **risco-aceito** (com prazo).
3. CODE_SMELL em volume alto sugere padrão — corrigir a causa raiz, não issue a issue.

Dados brutos: `~/sonarqube-violations/by-repo/flext-sh__flext-oracle-wms.json`

