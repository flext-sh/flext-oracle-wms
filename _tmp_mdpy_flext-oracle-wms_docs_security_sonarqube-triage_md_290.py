# from flext-oracle-wms_docs/security/sonarqube-triage.md:290
      122              u.Filter.create_filter(max_conditions=max_conditions)
      123
      124      def test_constructor_rejects_filters_exceeding_condition_limit(self) -> None:
      125          """Building an engine with too many conditions raises a validation error."""
>>>   126          with pytest.raises(FlextOracleWmsErrors.ValidationError):
      127              u.Filter(
      128                  filters={
      129                      "id": m.OracleWms.FlextOracleWmsOperatorFilter(
      130                          operator=c.OracleWms.WmsFilterOperator.IN, value=[1, 2, 3]
