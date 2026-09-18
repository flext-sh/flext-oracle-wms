# from flext-oracle-wms/docs/security/sonarqube-triage.md:331
       64                  match value:
       65                      case str() as s:
       66                          str_value = s
       67                      case list() as list_value:
>>>    68                          str_value = ",".join(item for item in list_value)
       69                      case _:
       70                          str_value = str(value)
       71                  normalized[key] = str_value
       72              return normalized
