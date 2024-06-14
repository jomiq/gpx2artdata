#! /bin/bash

if [ "$1" != "" ]; then
  echo "no push, only build"
fi

scripts/build.sh gcloud.env

if [ -z "$(git status --untracked-files=no --porcelain)" ]; then 
  # Working directory must be clean. 
  # Untracked files are ok though.
  if [ "$1" == "" ]; then
    git push
    source gcloud.env
    gcloud auth configure-docker ${REGION}-docker.pkg.dev
    docker push $IMAGE_TAG
  fi
else 
  # Uncommitted changes in tracked files
    echo Aborting: we do not push with uncommitted changes in this house
fi
