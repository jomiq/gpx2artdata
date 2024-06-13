#!/bin/bash
# Starts FASTAPI server locally with uvicorn
source local.env
export BUILD_VERSION="local"
cat local.env
echo && echo
fastapi dev --port 8080