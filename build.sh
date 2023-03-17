#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail

workdir="$(
    cd "$(dirname "$0")"
    pwd
)"

# registry='quay.io'
# organization='innovation-hub-bergisches-rheinland'
repository='sgm-kriging-models'
version='0.1.1'

r_version='4.2.2'
python_version="$(cat "${workdir}/.python-version")"
poetry_version='1.4.0'

docker build \
    --target 'test' \
    --file "${workdir}/Dockerfile" \
    --tag "${repository}:test" \
    --build-arg "R_VERSION=${r_version}" \
    --build-arg "PYTHON_VERSION=${python_version}" \
    --build-arg "POETRY_VERSION=${poetry_version}" \
    "${workdir}"

docker build \
    --file "${workdir}/Dockerfile" \
    --tag "${repository}:${version}" \
    --build-arg "R_VERSION=${r_version}" \
    --build-arg "PYTHON_VERSION=${python_version}" \
    --build-arg "POETRY_VERSION=${poetry_version}" \
    "${workdir}"
