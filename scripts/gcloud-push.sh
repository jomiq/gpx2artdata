#! /bin/bash
if [ -z "$(git status --untracked-files=no --porcelain)" ]; then 
  # Working directory clean excluding untracked files
    git push
    BUILD_VERSION=$(git rev-parse --short HEAD)
    source gcloud.env
    gcloud auth configure-docker ${REGION}-docker.pkg.dev

    docker build --build-arg build_version=${BUILD_VERSION} --build-arg website_url=${WEBSITE_URL} -t $IMAGE_TAG -f Containerfile --platform linux/x86_64 .
    docker push $IMAGE_TAG
else 
  # Uncommitted changes in tracked files
    echo Aborting: we do not push uncommitted changes in this house
fi
