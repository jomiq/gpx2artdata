#! /bin/bash
echo dude chill
cp .env.example .env 
mkdir data 
scripts/build.sh 
scripts/run.sh