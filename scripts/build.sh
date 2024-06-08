#! /bin/bash
# So I actually wanna use podman but I've yet to figure out how to install it in WSL
ENGINE=${1-"docker"}
$ENGINE build --pull --rm --no-cache -f "Containerfile" . -t "gpx2artdata:latest"