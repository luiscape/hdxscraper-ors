#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import csv
import json
import requests
import scraperwiki
from config import config as Config
from utilities.hdx_format import item
from utilities.store_records import StoreRecords

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

def FetchData(endpoint):
  '''Fetch data from specific endpoint.'''
  u = endpoint["url"]
  r = requests.get(u)

  if r.status_code != 200:
    print "%s Query returned error code: %s" % (item('prompt_error'), r)
    return

  else: 
    json = r.json()

  return json


def ProcessRecords(data, endpoint):
  '''Process and store data in database.'''
  StoreRecords(data=data, table=endpoint["table_name"])


def Main():
  '''Wrapper.'''
  endpoints = Config.LoadConfig()
  for endpoint in endpoints:
    json = FetchData(endpoint)
    ProcessRecords(data=json, endpoint=endpoint)


if __name__ == '__main__':
  Main()