#!/bin/bash
set -eu -o pipefail

push()
{
    export DOCKER_BUILDKIT=1
    export COMPOSE_DOCKER_CLI_BUILD=1
    docker tag app:latest ${REGISTRY}:${BRANCH_NAME}
    docker tag app:latest ${REGISTRY}:latest
    docker tag app:latest ${REGISTRY}:${GITHUB_JOB}
    docker push ${REGISTRY}:${GITHUB_JOB}
    echo "::set-output name=image_id::${REGISTRY}:${GITHUB_JOB}"
}

"$@"
