#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import scraperwiki
import config as Config
from hdx_format import item

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

def StoreRecords(data, table, verbose = False):
  '''Store records in a ScraperWiki database.'''

  schemas = Config.LoadConfig(os.path.join(dir, "config/config.json"))
  table_names = []
  for schema in schemas:
    table_names.append(schema["table_name"])

  if table not in table_names:
    print "%s select one of the following tables: %s." % (item('prompt_error'), ", ".join(table_names))
    return False

  try:
    tables = scraperwiki.sqlite.show_tables()

    if table in tables.keys():
      old_records = scraperwiki.sqlite.execute("SELECT count(*) from %s" % table)["data"][0][0]
      delete_statement = "DELETE FROM %s" % table
      scraperwiki.sqlite.execute(delete_statement)
      print " Cleaning %s records from database table: %s" % (old_records, table)

      scraperwiki.sqlite.save(schema, data, table_name=table)
      print " Storing record %s in database." % len(data)


  # Before storing check that the record exists in database.
  except Exception as e:
    print "%s Failed to store record in database." % item('prompt_error')
    print e



if __name__ == '__main__':
  records = [{ "x": "x", "y": "y", "z": "5" }, { "x": "x", "y": "y", "z": "5" }]
  StoreRecords(data = records, table = "ors_frw", verbose = True)