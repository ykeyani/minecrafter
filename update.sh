#!/usr/bin/env bash

source ./venv/bin/activate || exit

ansible-playbook -i inventory.yml playbook.yml --tags "update"
