#!/bin/bash

source venv/bin/activate
python tool/scripts/ors_collect/ > tool/http/log.txt
# python scripts/ors_collect/