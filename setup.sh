#!/bin/bash

printf "Installing Python's virtual environment and security add-on.\n"
virtualenv venv
source venv/bin/activate

pip install -r requirements.txt
pip install requests[security]

printf "Setting-up database."
python setup.py

printf "Installing crontab.\n"
crontab -l | { cat; echo "@daily bash tool/run.sh"; } | crontab -