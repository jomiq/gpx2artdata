#!/bin/sh
PORT=${PORT-8080}
export GPX2ARTDATA_PROD=PROD
uvicorn main:app --port $PORT --proxy-headers