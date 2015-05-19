#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

from utilities.hdx_format import item

def FetchSystemArguments():
  '''Fetching arguments from the command line interface.'''
  
  try:
    arguments = {
      'api_key': sys.argv[1],
      'json_path': sys.argv[2],
      'download_temp_path': sys.argv[3],
      'stag_url': 'https://test-data.hdx.rwlabs.org',
      'prod_url': 'https://data.hdx.rwlabs.org'
    }

  except IndexError:
    print '%s Not all arguments provided.' % item('prompt_error')
    return False
  
  #
  # Checking that all arguments have been provided.
  # 
  for argument in arguments:

    if argument is None:
      print 'Argument %s is empty. That argument is necessary.' % argument.keys()
      return False

  return arguments


def Main():
  '''Wrapper.'''
  
  arguments = FetchSystemArguments()
  if arguments is not False:
    return arguments


if __name__ == '__main__':
  Main()