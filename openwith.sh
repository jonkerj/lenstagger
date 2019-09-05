#!/bin/bash

SCRIPTPATH=$( cd "$(dirname "$0")" ; pwd -P )

${SCRIPTPATH}/venv/bin/python ${SCRIPTPATH}/openwith.py "${@}"
