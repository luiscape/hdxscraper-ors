#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import csv
import sys

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import json
import ckanapi
import requests
import scraperwiki

import hashlib as h
from random import random as r
from utilities.hdx_format import item
from utilities.fetch_arguments import FetchSystemArguments
from utilities.create_random_filename import CreateRandomFileName


def LoadLocalJson(json_path, verbose=False):
  '''Loading resources from a local json file.'''

  try:
    with open(json_path) as json_file:
      resources = json.load(json_file)

      #
      # Checking that the json provide contains at least
      # one resource.
      #
      if len(resources) < 1:
        print '%s Json looks odd! Please revise.' % item('prompt_error')

    return resources

  except Exception as e:
    print '%s Could not load local JSON: `%s`' % (item('prompt_error'), json_path)
    if verbose:
      print e
    return False


def DownloadResourceFromHDX(ckan_url, file_name, resource_id, api_key, verbose = True):
  '''Downloading a resource from CKAN based on its id. Resources need to be
     downloaded in order to be correctly parsed by the CreateDatastore function.'''


  print "%s Downloading resource file from HDX." % item('prompt_bullet')
  headers = { 'Authorization': api_key, 'user-agent': 'HDX-Script/v.0.1.0' }

  #
  # Querying.
  #
  url = ckan_url + '/api/action/resource_show?id=' + resource_id
  r = requests.get(url, headers=headers, auth=('dataproject', 'humdata'))
  doc = r.json()
  if doc['success'] is False:
    if verbose:
      print json.dumps(doc)
    print '%s Failed to read resource.' % item('prompt_error')
    return False

  else:
    resource_file_url = doc["result"]["url"]


  #
  # Downloading.
  #
  try:
    with open(file_name, 'wb') as handle:
      response = requests.get(resource_file_url, stream=True, headers=headers, auth=('dataproject', 'humdata'))

      if not response.ok:
        print '%s Error: attempt to download resource failed.' % item('prompt_error')
        return

      for block in response.iter_content(1024):
        if not block:
          break

        handle.write(block)

  except Exception as e:
    print '%s There was an error downlaoding the file.' % item('prompt_error')
    if verbose:
      print e
    return False



def DeleteDatastore(ckan_url, api_key, ckan_resource_id, verbose=False):
  '''Delete a CKAN DataStore.'''

  #
  # Configuring the remote CKAN instance.
  #
  ckan = ckanapi.RemoteCKAN(ckan_url, apikey=api_key)


  try:
    ckan.action.datastore_delete(resource_id=ckan_resource_id, force=True)

  #
  # If DataStore doesn't exist
  # print warning, but let it pass.
  #
  except Exception as e:
    if verbose:
        print e
    print '%s Old DataStore could not be deleted.' % item('prompt_warn')
    pass


def DefineSchema(file_name, verbose = False):
  '''Defining the schema to use. Does type-guessing.'''

  #
  # Reading downloaded CSV file.
  #
  try:
    reader = csv.DictReader(open(file_name))

  except Exception as e:
    print '%s There was an error reading resource.' % item('prompt_error')
    if verbose:
      print e

  #
  # Building the schema.
  #
  for row in reader:
    keys = row.keys()
    break
  schema = {'fields': []}
  for key in keys:
    schema['fields'].append( {'id': key.lower(), 'type': 'text'} )  # datastores need lower cases.

  return schema


def CreateDatastore(ckan_url, api_key, json_path, resource_id, file_name, resource, verbose=False):
  '''Creating a CKAN DataStore.'''

  #
  # Configuring the remote CKAN instance.
  #
  ckan = ckanapi.RemoteCKAN(ckan_url, apikey=api_key)

  if DeleteDatastore(
    ckan_url=ckan_url,
    api_key=api_key,
    ckan_resource_id=resource_id) is False:
    return False

  #
  # Creating a DataStore.
  #
  ckan.action.datastore_create(
    resource_id=resource_id,
    force=True,
    fields=resource['schema']['fields'],
    primary_key=resource['schema'].get('primary_key')
    )

  #
  # Reading CSV file and inserting data.
  #
  reader = csv.DictReader(open(file_name))
  rows = [ row for row in reader ]

  #
  # Hack for managing different encoding data.
  #
  if len(json_path) is 36:
    rows_decoded = []
    for row in rows:
      row_encoded = { key.lower():row[key].decode('utf-8') for key in row.keys() }
      rows_decoded.append(row_encoded)
  else:
    rows_decoded = []
    for row in rows:
      row_encoded = { key:row[key].decode('utf-8') for key in row.keys() }
      rows_decoded.append(row_encoded)

  #
  # Sending N records at a time.
  #
  offset = 0
  chunksize = 500  # N rows per POST request.
  while offset < len(rows_decoded):
    rowset = rows_decoded[offset:offset+chunksize]
    ckan.action.datastore_upsert(
      resource_id=resource_id,
      force=True,
      method='insert',
      records=rowset)
    offset += chunksize
    complete = str(float(offset)/len(rows_decoded) * 100)[:4] + '%'
    print '%s Update successful: %s completed' % (item('prompt_bullet'), complete)



def CreateDatastoresFromResourceID(resource_id, system_arguments=False):
  '''Create a datastore from a resource ID. Either collect system arguments
     if run from the command line or do type-guessing for the creation of schemas
     on the fly.'''

  #
  # Fetching arguments and configuring the script.
  #
  if system_arguments:
    p = FetchSystemArguments()

  #
  # Manual input of function parameters
  #
  else:
    p = {
      'json_path': resource_id,
      'prod_url': 'https://data.hdx.rwlabs.org/',
      'download_temp_path': os.path.join('tool', 'data', CreateRandomFileName(length=5, extension='.csv')),
      'api_key': LoadLocalJson(os.path.join(os.path.split(dir)[0], 'config', 'secrets.json'))['hdx_key']
    }

  api_key = p['api_key']
  ckan_url = p['prod_url']
  download_temp_path = p['download_temp_path']

  #
  # Loading resource information.
  #
  if len(p['json_path']) is 36:  # length of resource ID.
    resources = [ {'resource_id': p['json_path']} ]

    # Download file.
    DownloadResourceFromHDX(
        ckan_url=ckan_url,
        file_name=download_temp_path,
        resource_id=resources[0]['resource_id'],
        api_key=api_key
        )

    # Create schema.
    resources[0]['schema'] = DefineSchema(download_temp_path)
    resources[0]['indexes'] = []

    # Create datastore.
    CreateDatastore(
        ckan_url=ckan_url,
        api_key=api_key,
        json_path=p['json_path'],
        file_name=download_temp_path,
        resource_id=resource_id,
        resource=resources[0]
        )

    #
    # Delete temporary file.
    #
    print '%s Cleaning temp file.' % item('prompt_bullet')
    os.remove(download_temp_path)

  else:
    resources = LoadLocalJson(p['json_path'])

    #
    # Iterating over each resource provided.
    #
    for r in resources:
      resource_id = r['resource_id']
      print '%s Creating DataStore for resource id: %s' % (item('prompt_bullet'), resource_id)

      try:
        DownloadResourceFromHDX(
          ckan_url=ckan_url,
          file_name=download_temp_path,
          resource_id=resource_id,
          api_key=api_key
          )
        CreateDatastore(
          ckan_url=ckan_url,
          api_key=api_key,
          json_path=p['json_path'],
          file_name=download_temp_path,
          resource_id=resource_id,
          resource=r
          )



      except Exception as e:
        print '%s DataStore creation failed.' % item('prompt_error')
        if verbose:
          print e
        return False



if __name__ == '__main__':
  CreateDatastoresFromResourceID(resource_id='333333333333333333333333333333333333', system_arguments=False)
