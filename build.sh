#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail

registry='quay.io'
organization='innovation-hub-bergisches-rheinland'
repository='sgm-kriging-models'
version='0.1.0'

workdir="$(
    cd "$(dirname "$0")"
    pwd
)"

docker build \
    --file "${workdir}/Dockerfile" \
    --tag "${repository}:${version}" \
    --build-arg 'R_VERSION=4.2.2' \
    --build-arg "PYTHON_VERSION=$(cat "${workdir}/.python-version")" \
    --build-arg 'POETRY_VERSION=1.3.2' \
    "${workdir}"
