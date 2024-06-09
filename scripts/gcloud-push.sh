#! /bin/bash
source gcloud.env
gcloud auth configure-docker ${REGION}-docker.pkg.dev

docker build -t $IMAGE_TAG -f Containerfile --platform linux/x86_64 .
docker push $IMAGE_TAG