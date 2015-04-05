#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import scraperwiki
from hdx_format import item

def StoreRecords(data, table, verbose = False):
  '''Store records in a ScraperWiki database.'''

  # Available schemas.
  schemas = {
    'ors_all_data': ["LocationPCode", "Indicator", "BeneficiariesWomen", "ProjectContactPhone", "ProjectCode", "Accumulative", "Admin1", "Objective", "Admin2", "ProjectEndDate", "ReportingYearMonth", "ProjectContactEmail", "GenderMarker", "ProjectContactName", "BeneficiariesOthers", "OPSProjectStatus", "FundingStatus", "Country", "BeneficiaryTotalNumber", "RunningSum", "Activity", "Organization", "BeneficiariesChildren", "AnnualTarget", "Achieved", "ProjectStartDate", "MONTH", "Cluster", "Year"]
  }

  try:
    schema = schemas[table]

  except Exception as e:

    if verbose is True:
      print e
      return False

    else: 
      print "%s select one of the following tables: %s." % (item('prompt_error'), ", ".join(schemas.keys()))
      return False

  try:
    for record in data:
      scraperwiki.sqlite.save(schema, record, table_name=table)

  except Exception as e:
    print "%s Failed to store record in database." % item('prompt_error')
    print e