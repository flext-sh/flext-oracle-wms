# from flext-oracle-wms_docs/security/sonarqube-triage.md:40
       71      })
       72      _ = container.bind("FlextOracleWmsSettings", settings.model_dump(mode="python"))
       73
       74
>>>    75  def discover_wms_entities(client: FlextOracleWmsClient) -> p.Result[t.StrSequence]:
       76      """Discover available Oracle WMS entities.
       77
       78      Args:
       79        client: Configured Oracle WMS client
