#!/bin/sh

# Get the script path.
SCRIPT_PATH="$(
    cd "$(dirname "$0")" || return >/dev/null 2>&1
    pwd -P
)"

# Change to the directory of the script.
cd "$SCRIPT_PATH"

# Activate the virtual environment & start the server.
pipenv run gunicorn -b 0.0.0.0:8000 -w 3 src.api.wsgi:APP 2>errors.log

# here u can change the port for the project
# -w declares the number of additional worker
# 2> describes where the errors should be monitored
# with "--certfile=../Keys/server.crt --keyfile=../Keys/server.key" you can use the certificat for https
# "--log-level warning" to only get real errors and not the server start warning and similar 