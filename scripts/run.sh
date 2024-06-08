#! /bin/bash
ENGINE=${1-"docker"}
$ENGINE run -p 8000:8000 gpx2artdata:latest