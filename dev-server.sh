#!/bin/bash
# Starts FASTAPI server locally with uvicorn
GPX2ARTDATA_PROD=${1-"False"}
source local.env
export BUILD_VERSION="local"
cat local.env
echo && echo
fastapi dev --port 8080