#!/bin/bash
# Starts FASTAPI server locally with uvicorn
source local.env
cat local.env

if [ "$PRODUCTION" == "" ]; then
    PRODUCTION=${1-"false"}
    BUILD_VERSION="${BUILD_VERSION-'none'}-dev"
else
    BUILD_VERSION=${BUILD_VERSION-"none"}
fi

export PRODUCTION
export BUILD_VERSION

echo && echo
fastapi dev --port 8080