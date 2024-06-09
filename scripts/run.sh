#! /bin/bash
ENGINE=${1-"docker"}
$ENGINE run -p 8080:8080 gpx2artdata:latest