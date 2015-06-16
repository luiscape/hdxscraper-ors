#!/bin/bash

source venv/bin/activate
python tool/scripts/ors_collect/
python tool/scripts/hdx_datastore/
