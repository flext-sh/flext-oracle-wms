# from flext-oracle-wms/docs/security/sonarqube-triage.md:160
      213      if warnings and isinstance(warnings, list):
      214          for _warning in warnings:
      215              pass
      216      if validation["valid"]:
>>>   217          pass
      218      else:
      219          errors = validation.get("errors", [])
      220          if errors and isinstance(errors, list):
      221              for _error in errors:
