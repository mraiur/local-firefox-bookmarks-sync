#!/bin/bash

cwd=$(pwd)

. $cwd/venv/bin/activate
py=$cwd/venv/bin/python3

export PYTHONPATH=${PYTHONPATH}

if [ "$1" == "" ]; then
  echo "serve - start server that displays bookmarks"
elif [ "$1" == "serve" ]; then
  $py src/serve.py $2
fi

