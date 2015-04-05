#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import json
import requests
import scraperwiki
# import config as Config
from hdx_format import item
from termcolor import colored as color
from store_records import StoreRecords

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

def FetchData():
  u = 'http://ors.ocharowca.info/anonymous/alldatafeed.ashx?format=json'
  r = requests.get(u)

  if r.status_code != 200:
    print "%s Query returned error code: %s" % (item('prompt_error'), r)
    return

  else: 
    json = r.json()

  return json

def ProcessRecords(data):

  for row in data:
    record = [{ key:row[key] if isinstance(row[key], dict) is False else row[key].values()[0] for key in row.keys() }]
    StoreRecords(record, "ors_all_data")


def Main():
  json = FetchData()
  ProcessRecords(data=json)

if __name__ == '__main__':
  Main()