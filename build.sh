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

poetry export --without-hashes -f 'requirements.txt' >"${workdir}/requirements/requirements.txt"

docker build \
    --file "${workdir}/Dockerfile" \
    --tag "${repository}:${version}" \
    "${workdir}"

rm --force "${workdir}/requirements/requirements.txt"