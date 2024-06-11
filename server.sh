#!/bin/sh
PORT=${PORT-8080}
export GPX2ARTDATA_PROD=PROD
uvicorn main:app --host 0.0.0.0 --port $PORT --proxy-headers