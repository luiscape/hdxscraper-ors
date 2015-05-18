#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import json
from utilities.hdx_format import item

def LoadConfig(j='prod.json', verbose=True):
  '''Load configuration parameters.'''
  
  data_dir = os.path.join(os.path.split(dir)[0], 'config')

  try:
    j = os.path.join(data_dir, j)
    with open(j) as json_file:    
      config = json.load(json_file)

  except Exception as e:
    print "%s Couldn't load configuration." % item('prompt_error')
    if verbose:
      print e
    return False

  return config

if __name__ == "__main__":
  LoadConfig()