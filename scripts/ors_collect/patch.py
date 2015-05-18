#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import datetime
import scraperwiki

from config import config as Config
from utilities.hdx_format import item
from utilities.store_records import StoreRecords

def ConvertEpochDates(table_name, column_name, verbose=False):
  '''Convert timestamps from /Date(1420449209053)/ to 2015-01-05T09:13:29'''

  print '%s Cleaning epoch dates for table `%s` and field `%s`.' % (item('prompt_bullet').decode('utf-8'), table_name, column_name)
  
  #
  # Collect data from database.
  #
  sql = 'select * from %s' % table_name
  try:
    result_proxy = scraperwiki.sqlite.execute(sql)['data']
    data = []
    for row in result_proxy:
      data.append(dict(row.items()))

  except Exception as e:
    print '%s Could not collect data from database.' % item('prompt_error')
    return False
    if verbose:
      print e
  
  #
  # Converting dates.
  #
  for date in data:
    d = date[column_name]

    #
    # Seeing if the regex works.
    #
    if d != None:
      try:
        convent_date = int(d[d.find("(")+1:d.find(")")])

      except Exception as e:
        print '%s Regex did not quite work on table `%s`. Aborting.' % (item('prompt_warn'), table_name)
        if verbose:
          print e
        return False
    
    #
    # Making transformations.
    #
    epoch = convent_date / 1000
    dt = datetime.datetime.utcfromtimestamp(epoch)
    iso_format = dt.isoformat()
    if verbose:
      print '%s Date: %s' % (item('prompt_bullet'), iso_format)

    date[column_name] = iso_format

  #
  # Return data.
  #
  return data
  

def DeletePIIColumns(table_name, column_name, verbose=True):
  '''Deleting columns that contain personal identifiable information.'''

  print '%s Deleting PII column `%s` on table `%s`.' % (item('prompt_bullet').decode('utf-8'), column_name, table_name)
  
  #
  # Fetch keys from column in database.
  #
  try:
    c = scraperwiki.sqlite.execute('select * from {table_name} limit 1'.format(table_name=table_name))['keys']

  except Exception as e:
    print '%s Could not connect with database.' % item('prompt_error')
    if verbose:
      print e
    return False

  #
  # Copy data into backup table without
  # PII column, then copy it back.
  # From: http://stackoverflow.com/questions/10660435/pythonic-way-to-create-a-long-multi-line-string
  #
  columns = ','.join([t for t in c if t != column_name])
  sql_statements = [ #'BEGIN TRANSACTION;',
                    'CREATE TEMPORARY TABLE {table_name}_backup({columns});'.format(table_name=table_name, columns=columns),
                    'INSERT INTO {table_name}_backup SELECT {columns} FROM {table_name};'.format(table_name=table_name, columns=columns),
                    'DROP TABLE {table_name};'.format(table_name=table_name),
                    'CREATE TABLE {table_name}({columns});'.format(table_name=table_name, columns=columns),
                    'INSERT INTO {table_name} SELECT {columns} FROM {table_name}_backup;'.format(table_name=table_name, columns=columns),
                    'DROP TABLE {table_name}_backup;'.format(table_name=table_name, columns=columns)]
                    #'COMMIT;'.format(table_name=table_name, columns=columns)]

  try:
    for sql in sql_statements:
      scraperwiki.sqlite.execute(sql)

  except Exception as e:
    print '%s Could not delete column `%s` from table `%s`.' % (item('prompt_error'), column_name, table_name)
    if verbose:
      print e
    return False
   
  #
  # Close connection with database.
  #
  scraperwiki.sqlite._State.new_transaction()
  return True



def Main(verbose=True):
  '''Wrapper.'''
  
  #
  # Load endpoint info from config
  # and iterate over them.
  #
  endpoints = Config.LoadConfig()
  for endpoint in endpoints:

    #
    # Delete PII columns.
    #
    for field in endpoint['pii_columns']:
      DeletePIIColumns(table_name=endpoint['table_name'], column_name=field)

    # #
    # # Check the type of date conversion.
    # #
    # if endpoint['dates_formatting']['type'] == 'epoch':
    #   #
    #   # Iterate over every field.
    #   #
    #   for field in endpoint['dates_formatting']['fields']:
    #     data = ConvertEpochDates(endpoint['table_name'], column_name=field)
    #     #
    #     # Store data in database.
    #     #
    #     if data is not False:
    #       StoreRecords(data=data, table=endpoint['table_name'])



if __name__ == '__main__':
  Main()
