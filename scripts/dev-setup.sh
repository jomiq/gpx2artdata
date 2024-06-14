#! /bin/bash

echo
echo " ********* gpx2artdata dev setup ******** "
echo " ***                                  *** "
echo " ***          dude, chill...          *** "
echo " ***                                  *** "
echo " ******* e l e k t r o s l ö j d ******** "
echo

if [ ! -f local.env ] 
then
    echo " *** no local environment found. creating local.env *** "
    cp local.env.example local.env
else
    echo "local.env found."
fi

# install into new venv
[ -d .venv ] && echo " *** virtual environment found, torching it. *** " && rm -r .venv

echo " *** creating venv *** "
python -m venv .venv

echo " *** installing [dev] group *** "
source .venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]

echo " *** installing pre-commit hooks *** "
pre-commit install

echo
echo " ***************  done!  **************** "
echo " ***                                  *** "
echo " ***  run source .venv/bin/activate   *** "
echo " ***   and let the good times roll    *** "
echo " ***                                  *** "
echo " ******* e l e k t r o s l ö j d ******** "
echo