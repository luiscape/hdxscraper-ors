#!/bin/bash

printf "Installing Python's virtual environment and security add-on.\n"
virtualenv venv
source venv/bin/activate

cd tool

pip install -r requirements.txt
pip install[security]

printf "Setting-up database.\n"
python scripts/setup/

# printf "Installing crontab.\n"
# crontab -l | { cat; echo "@daily bash tool/run.sh"; } | crontab -
