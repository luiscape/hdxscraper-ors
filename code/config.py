#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

def LoadConfig(j = os.path.join(dir, "config/config.json")):
  '''Load configuration parameters.'''
  try:
    j = os.path.join(dir, j)
    with open(j) as json_file:    
      config = json.load(json_file)

  except Exception as e:
    print "Couldn't load configuration."
    print e
    return

  return config

if __name__ == "__main__":
  LoadConfig()