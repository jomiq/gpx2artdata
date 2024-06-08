#! /bin/bash
# install into new venv 
rm -rf .venv
python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -e .[dev]
pre-commit install