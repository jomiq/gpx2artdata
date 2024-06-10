#! /bin/bash
# So I actually wanna use podman but I've yet to figure out how to install it in WSL
ENGINE=${1-"docker"}
BUILD_VERSION="${BUILD_VERSION:-local}"
$ENGINE build --pull --rm --no-cache --build-arg build_version=${BUILD_VERSION} -f "Containerfile"  . -t "gpx2artdata:latest"