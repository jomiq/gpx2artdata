#! /bin/bash
echo
echo " ******* gpx2artdata quick start ******** "
echo " ***                                  *** "
echo " ***          dude, chill...          *** "
echo " ***                                  *** "
echo " ******* e l e k t r o s l ö j d ******** "
echo

ENGINE=${1-"docker"}
export ENGINE
if [ ! -f local.env ] 
then
    cp local.env.example local.env
fi

scripts/build.sh
scripts/run.sh