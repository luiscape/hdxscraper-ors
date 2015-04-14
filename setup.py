#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import scraperwiki

dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(dir, 'code'))

import config as Config
from hdx_format import item


def CreateTables():
  '''Creating the tables of the new database.'''

  endpoints = Config.LoadConfig()

  sql_statements = {}
  for endpoint in endpoints:
    table_name = endpoint["table_name"]
    statement = " TEXT, ".join(endpoint['table_schema'])
    statement = 'CREATE TABLE IF NOT EXISTS %s(%s TEXT)' % (table_name, statement)
    sql_statements[table_name] = statement

  for table in sql_statements:
    try:
      query = scraperwiki.sqlite.execute(sql_statements[table])
      print "%s table `%s` created." % (item('prompt_bullet'), str(table))

    except Exception as e:
      print e
      return False


  print "%s Database created successfully." % item('prompt_success')
  return True


if __name__ == '__main__':
  CreateTables()