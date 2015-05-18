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
    scraperwiki.sqlite.commit()
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
    if d is not None:
      try:
        convent_date = int(d[d.find("(")+1:d.find(")")])

      except Exception as e:
        print '%s Regex did not quite work on table `%s`. Aborting.' % (item('prompt_warn'), table_name)
        if verbose: 
          print e
        return False
    
    else:
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
  

def Main():
  '''Wrapper.'''
  
  #
  # Load endpoint info from config
  # and iterate over them.
  #
  endpoints = Config.LoadConfig()
  for endpoint in endpoints:
    #
    # Check the type of conversion.
    #
    if endpoint['dates_formatting']['type'] == 'epoch':
      #
      # Iterate over every field.
      #
      for field in endpoint['dates_formatting']['fields']:
        data = ConvertEpochDates(endpoint['table_name'], column_name=field)
        #
        # Store data in database.
        #
        if data is not False:
          StoreRecords(data=data, table=endpoint['table_name'])

    else:
      print '%s Not epoch.' % item('prompt_warn')

if __name__ == '__main__':
  Main()
