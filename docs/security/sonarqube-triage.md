# Triagem SonarCloud — flext-sh/flext-oracle-wms

Gerado do dump da plataforma SonarCloud (2026-08-06).

Bead: `mro-2wjm.14`

## Resumo

**16 issues** — BLOCKER 2, CRITICAL 0, MAJOR 12, MINOR 2
Tipos: VULNERABILITY 4, BUG 0, CODE_SMELL 12 · **Debt total: 74min**

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
| `python:S7500` | 1 |

## Como usar

Cada issue traz a **mensagem do SonarQube** (descreve o problema e o impacto), o **código real** (linha `>>>`), o tipo e o effort estimado.
**Decisão**: `corrigir` / `falso-positivo` (marcar na plataforma com justificativa) / `risco-aceito`. Ordem: BLOCKER → CRITICAL → VULNERABILITY → MAJOR. CODE_SMELL em volume pede correção de padrão.

## Issues

### 1 · 🔴 BLOCKER · CODE_SMELL · `python:S3516`
**Local**: `examples/01_basic_usage.py:75` · **Effort**: 2min

> Refactor this method to not always return the same value.

```python
       71      })
       72      _ = container.bind("FlextOracleWmsSettings", settings.model_dump(mode="python"))
       73  
       74  
>>>    75  def discover_wms_entities(client: FlextOracleWmsClient) -> p.Result[t.StrSequence]:
       76      """Discover available Oracle WMS entities.
       77  
       78      Args:
       79        client: Configured Oracle WMS client
```

**Decisão**: pendente

### 2 · 🔴 BLOCKER · CODE_SMELL · `python:S3516`
**Local**: `examples/01_basic_usage.py:99` · **Effort**: 2min

> Refactor this method to not always return the same value.

```python
       95          return result
       96      return result
       97  
       98  
>>>    99  def query_entity_data(
      100      client: FlextOracleWmsClient, entity_name: str
      101  ) -> p.Result[Sequence[t.StrMapping]]:
      102      """Query data from a specific Oracle WMS entity.
      103  
```

**Decisão**: pendente

### 3 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8264`
**Local**: `.github/workflows/docs.yml:18` · **Effort**: 5min

> Move this read permission from workflow level to job level.

```yaml
       14        - ".github/workflows/docs.yml"
       15    workflow_dispatch:
       16  
       17  permissions:
>>>    18    contents: read
       19    pages: write
       20    id-token: write
       21  
       22  concurrency:
```

**Decisão**: pendente

### 4 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8233`
**Local**: `.github/workflows/docs.yml:19` · **Effort**: 5min

> Move this write permission from workflow level to job level.

```yaml
       15    workflow_dispatch:
       16  
       17  permissions:
       18    contents: read
>>>    19    pages: write
       20    id-token: write
       21  
       22  concurrency:
       23    group: pages
```

**Decisão**: pendente

### 5 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8233`
**Local**: `.github/workflows/docs.yml:20` · **Effort**: 5min

> Move this write permission from workflow level to job level.

```yaml
       16  
       17  permissions:
       18    contents: read
       19    pages: write
>>>    20    id-token: write
       21  
       22  concurrency:
       23    group: pages
       24    cancel-in-progress: false
```

**Decisão**: pendente

### 6 · 🟡 MAJOR · CODE_SMELL · `python:S108`
**Local**: `examples/02_configuration.py:215` · **Effort**: 5min

> Either remove or fill this block of code.

```python
      211      validation = validate_configuration(env_config)
      212      warnings = validation.get("warnings", [])
      213      if warnings and isinstance(warnings, list):
      214          for _warning in warnings:
>>>   215              pass
      216      if validation["valid"]:
      217          pass
      218      else:
      219          errors = validation.get("errors", [])
```

**Decisão**: pendente

### 7 · 🟡 MAJOR · CODE_SMELL · `python:S108`
**Local**: `examples/02_configuration.py:217` · **Effort**: 5min

> Either remove or fill this block of code.

```python
      213      if warnings and isinstance(warnings, list):
      214          for _warning in warnings:
      215              pass
      216      if validation["valid"]:
>>>   217          pass
      218      else:
      219          errors = validation.get("errors", [])
      220          if errors and isinstance(errors, list):
      221              for _error in errors:
```

**Decisão**: pendente

### 8 · 🟡 MAJOR · CODE_SMELL · `python:S108`
**Local**: `examples/02_configuration.py:222` · **Effort**: 5min

> Either remove or fill this block of code.

```python
      218      else:
      219          errors = validation.get("errors", [])
      220          if errors and isinstance(errors, list):
      221              for _error in errors:
>>>   222                  pass
      223  
      224  
      225  def _demonstrate_demo_configuration() -> None:
      226      """Demonstrate demo configuration validation."""
```

**Decisão**: pendente

### 9 · 🟡 MAJOR · CODE_SMELL · `python:S108`
**Local**: `examples/02_configuration.py:232` · **Effort**: 5min

> Either remove or fill this block of code.

```python
      228      validation = validate_configuration(demo_config)
      229      warnings = validation.get("warnings", [])
      230      if warnings and isinstance(warnings, (list, tuple)):
      231          for _warning in warnings:
>>>   232              pass
      233  
      234  
      235  def demonstrate_configuration_patterns() -> None:
      236      """Demonstrate working Oracle WMS configuration patterns."""
```

**Decisão**: pendente

### 10 · 🟡 MAJOR · CODE_SMELL · `python:S108`
**Local**: `examples/02_configuration.py:247` · **Effort**: 5min

> Either remove or fill this block of code.

```python
      243      except Exception as exc:
      244          logger.warning("Configuration validation failed: %s", exc)
      245      env_configs = get_environment_configs()
      246      for _config in env_configs.values():
>>>   247          pass
      248  
      249  
      250  def main() -> None:
      251      """Demonstrate Oracle WMS configuration patterns."""
```

**Decisão**: pendente

### 11 · 🟡 MAJOR · CODE_SMELL · `python:S108`
**Local**: `examples/03_complete_functionality_showcase.py:93` · **Effort**: 5min

> Either remove or fill this block of code.

```python
       89      """Feature 1: Client Configuration and Initialization."""
       90      client = FlextOracleWmsClient(settings)
       91      start_result = client.start()
       92      if start_result.success:
>>>    93          pass
       94      else:
       95          msg = f"Failed to start client: {start_result.error}"
       96          raise FlextOracleWmsErrors.Error(msg)
       97      return client
```

**Decisão**: pendente

### 12 · 🟡 MAJOR · VULNERABILITY · `text:S8565`
**Local**: `pyproject.toml:-` · **Effort**: 5min

> Dependency versions are not predictable if the lock file (uv.lock, poetry.lock, pdm.lock or pylock.toml) is missing.


**Decisão**: pendente

### 13 · 🟡 MAJOR · CODE_SMELL · `python:S3358`
**Local**: `src/flext_oracle_wms/_utilities/filtering.py:205` · **Effort**: 5min

> Extract this nested conditional expression into an independent statement.

```python
      201  
      202                  def key_func(record: t.OracleWms.FilterRecord) -> str:
      203                      value = self._get_nested_value(record, sort_field)
      204                      return str(
>>>   205                          value if value is not None else "" if ascending else "zzz"
      206                      )
      207  
      208                  return r[Sequence[t.OracleWms.FilterRecord]].ok(
      209                      sorted(records, key=key_func, reverse=not ascending)
```

**Decisão**: pendente

### 14 · 🟡 MAJOR · CODE_SMELL · `python:S5778`
**Local**: `tests/unit/test_helpers.py:126` · **Effort**: 5min

> Refactor this exception test to have only one invocation possibly throwing an exception.

```python
      122              u.Filter.create_filter(max_conditions=max_conditions)
      123  
      124      def test_constructor_rejects_filters_exceeding_condition_limit(self) -> None:
      125          """Building an engine with too many conditions raises a validation error."""
>>>   126          with pytest.raises(FlextOracleWmsErrors.ValidationError):
      127              u.Filter(
      128                  filters={
      129                      "id": m.OracleWms.FlextOracleWmsOperatorFilter(
      130                          operator=c.OracleWms.WmsFilterOperator.IN, value=[1, 2, 3]
```

**Decisão**: pendente

### 15 · ⚪ MINOR · CODE_SMELL · `python:S7504`
**Local**: `conftest.py:20` · **Effort**: 5min

> Remove this unnecessary `list()` call on an already iterable object.

```python
       16      if (
       17          existing_package is None
       18          or Path(getattr(existing_package, "__file__", "")).resolve() != init_file
       19      ):
>>>    20          for module_name in list(sys.modules):
       21              if module_name == package_name or module_name.startswith(
       22                  f"{package_name}."
       23              ):
       24                  sys.modules.pop(module_name, None)
```

**Decisão**: pendente

### 16 · ⚪ MINOR · CODE_SMELL · `python:S7500`
**Local**: `src/flext_oracle_wms/_utilities/http_client.py:68` · **Effort**: 5min

> Replace this comprehension with passing the iterable to the collection constructor call

```python
       64                  match value:
       65                      case str() as s:
       66                          str_value = s
       67                      case list() as list_value:
>>>    68                          str_value = ",".join(item for item in list_value)
       69                      case _:
       70                          str_value = str(value)
       71                  normalized[key] = str_value
       72              return normalized
```

**Decisão**: pendente
