# from flext-oracle-wms_docs/security/sonarqube-triage.md:60
       95          return result
       96      return result
       97
       98
>>>    99  def query_entity_data(
      100      client: FlextOracleWmsClient, entity_name: str
      101  ) -> p.Result[Sequence[t.StrMapping]]:
      102      """Query data from a specific Oracle WMS entity.
      103
