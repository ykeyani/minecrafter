#!/usr/bin/env bash

echo "creating virtual environment"
python3 -m venv ./venv || { echo "failed to create virtual environment"; exit 1; }

echo "entering virtual environment"
source ./venv/bin/activate || { echo "failed to enter virtual environment"; exit 1; }

echo "updating virtual environment"
pip install -r requirements.txt || { echo "failed to update virtual environment"; exit 1; }

echo "create plugins directory"
mkdir -p ./plugins

echo "create backups directory"
mkdir -p ./backups

echo "setup complete"

