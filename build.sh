#!/bin/bash

tag=${tag:-dev}

docker build --progress=plain -t hub.cerit.io/scipion-portal/portal:$tag . && \
docker push hub.cerit.io/scipion-portal/portal:$tag
