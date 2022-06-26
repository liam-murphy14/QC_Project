#!/bin/bash

# check number of args
if [[ $# < 1 ]]; then
    echo "no project name given, exiting."
    echo
    echo "run with -h for help."
    exit 1
elif [[ $# > 1 ]]; then
    echo "too many arguments, exiting."
    echo 
    echo "run with -h for help."
    exit 1
fi 

# check for valid project
if [[ ! -d "container/$1" ]]; then
    echo "bad project name, exiting."
    exit 1
fi
echo "good project name"
exit 0


# activate venv
# MUST run from QC_Projects directory
source venv/bin/activate
cd container
