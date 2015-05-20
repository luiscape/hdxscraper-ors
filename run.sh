#!/bin/bash

source venv/bin/activate
python tool/scripts/ors_collect/ #> tool/http/log.txt
python tool/scripts/hdx_datastore/ #> tool/http/datastore_log.txt