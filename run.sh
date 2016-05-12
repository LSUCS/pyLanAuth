#!/bin/bash
source env/bin/activate
export PYTHONPATH=$PWD
python3 $PWD/lanauth/__main__.py -c prod.conf
