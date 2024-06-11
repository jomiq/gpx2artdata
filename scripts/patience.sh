#! /bin/bash
ENGINE=${1-"docker"}
echo dude chill
cp .env.example .env 
mkdir data 
scripts/build.sh $ENGINE
scripts/run.sh $ENGINE