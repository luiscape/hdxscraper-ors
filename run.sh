#!/bin/bash

# for now, this:
rm scraperwiki.sqlite

source venv/bin/activate
python tool/code/scraper.py

