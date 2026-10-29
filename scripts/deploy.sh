#!/usr/bin/env bash
# deploy.sh <environment> <image@digest> -- lab stub: validates and prints the deploy
set -Eeuo pipefail
env=${1:?usage: deploy.sh <environment> <image@digest>}
image=${2:?usage: deploy.sh <environment> <image@digest>}

case $env in
  staging|production) ;;
  *) echo "unknown environment: $env" >&2; exit 2 ;;
esac
[[ $image == *@sha256:* ]] || { echo "refusing mutable tag, deploy by digest: $image" >&2; exit 2; }

echo "deploying $image to $env"
