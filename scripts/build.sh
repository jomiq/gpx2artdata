#! /bin/bash
ENV_FILE=${1-"local.env"}

echo "*** ENVIRONMENT: $ENV_FILE ***"
cat $ENV_FILE
echo && echo

source $ENV_FILE
ENGINE=${ENGINE-"docker"}
PRODUCTION=${PRODUCTION-1}

BUILD_VERSION="$(git describe --exact-match --tags HEAD)"

if [ "$BUILD_VERSION" == "" ]; then
  BUILD_VERSION="$(git branch --show-current)-$(git rev-parse --short HEAD)" 
  if [ "$(git status --untracked-files=no --porcelain)" ]; then 
    BUILD_VERSION="$BUILD_VERSION-custom"
  fi
else
  echo "*** RELEASE BUILD ***"
fi

echo "*** $ENGINE: building $BUILD_VERSION ***"
$ENGINE build --pull --rm --progress=plain --build-arg production=${PRODUCTION} --build-arg build_version=${BUILD_VERSION} --build-arg website_hostname=${WEBSITE_HOSTNAME} --build-arg static_url=${STATIC_URL} -t $IMAGE_TAG -f Containerfile --platform linux/x86_64 .