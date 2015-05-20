#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import random as r
import hashlib as h

from utilities.hdx_format import item

def CreateRandomFileName(length, extension):
  '''Create a random, hash-based file name.'''
  
  #
  # Sanity check.
  #
  if type(length) != int:
    print '%s Provide an integer for the length parameter. %s provided.' % (item('prompt_error'), type(length))
    return False

  if type(extension) != str:
    print '%s Provide an string for the extension parameter. %s provided' % (item('prompt_error'), type(extension))
    return False

  #
  # Creating an unique file name.
  #
  file_name = h.sha1(str(r.random())).hexdigest()[0:length] + extension
  return file_name



if __name__ == '__main__':
  print CreateRandomFileName(length=5, extension='.csv')