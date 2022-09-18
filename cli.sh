#!/bin/bash

cwd=$(pwd)

. $cwd/venv/bin/activate
py=$cwd/venv/bin/python3

export PYTHONPATH=${PYTHONPATH}

$py src/watch.py
