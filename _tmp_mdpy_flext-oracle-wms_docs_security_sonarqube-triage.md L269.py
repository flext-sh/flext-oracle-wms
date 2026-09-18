# from flext-oracle-wms/docs/security/sonarqube-triage.md:269
      201
      202                  def key_func(record: t.OracleWms.FilterRecord) -> str:
      203                      value = self._get_nested_value(record, sort_field)
      204                      return str(
>>>   205                          value if value is not None else "" if ascending else "zzz"
      206                      )
      207
      208                  return r[Sequence[t.OracleWms.FilterRecord]].ok(
      209                      sorted(records, key=key_func, reverse=not ascending)
