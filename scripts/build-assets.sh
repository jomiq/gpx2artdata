#! /bin/bash

rm -rf build static/media/

python scripts/make_vids.py

cp -r build/media/ static/