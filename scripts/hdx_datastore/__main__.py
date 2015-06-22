#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import scraperwiki

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

from utilities.hdx_format import item
from hdx_datastore.create import CreateDatastoresFromResourceID

def Main():
  '''Wrapper.'''

  resource_ids = [
    '68788137-84d6-4e9d-87f1-f23f71ec705f',
    '89a28fad-a862-4133-82cd-9ef5f1938f38',
    '891b778a-9657-4eda-91b9-de9b41240a90',
    'f28518b2-afed-47b2-a805-c36eb3b18dcf',
    'de3eb9fa-fea8-4dec-8119-1814552198b3',
    '61995548-93ab-4927-b760-faf5239d32a9',
    '735b3f3a-eef6-4eb4-8b43-9307bac3177c',
    '831ef44b-d7eb-4c03-b152-ce5dce174626',
    '860fd6e4-589b-49c0-b1cf-fb9c0528d391'
  ]

  i = 1
  for resource_id in resource_ids:
    print '%s Creating HDX DataStore %s / %s' % (item('prompt_bullet'), str(i), str(len(resource_ids)))
    CreateDatastoresFromResourceID(resource_id)
    print '%s Successfully created datastore for resource id %s' % (item('prompt_success'), resource_id)
    i += 1

if __name__ == '__main__':
  Main()
