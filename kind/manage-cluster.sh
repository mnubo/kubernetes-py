#!/usr/bin/env bash

# Get the current path
pushd . > /dev/null
SCRIPT_PATH="${BASH_SOURCE[0]}"
while([ -h "${SCRIPT_PATH}" ]); do
  cd "$(dirname "${SCRIPT_PATH}")"
  SCRIPT_PATH="$(readlink "$(basename "${SCRIPT_PATH}")")"
done
cd "$(dirname "${SCRIPT_PATH}")" > /dev/null
SCRIPT_PATH=$(pwd)
popd  > /dev/null

# Set some variables
CLUSTER_NAME=${CLUSTER_NAME:-kind}
CLUSTER_VERSION=${CLUSTER_VERSION:-"1.14"}
CONFIG_FILE=${SCRIPT_PATH}/config-${CLUSTER_VERSION}.yaml
KUBECONFIG_FILE=${SCRIPT_PATH}/kubeconfig.yaml

set -e
while getopts "cd" opts; do 
  case "${opts}" in
    c)
      ACTION="create"
      shift
      ;;
    d)
      ACTION="delete"
      shift
      ;;
    *)
      echo "Unknown option ${opts}"
      exit 1
      ;;
  esac
done

if [ -z "${ACTION}" ]; then
  echo "Please create (-c) or delete (-d)."
  exit 1
fi

set -e

case "${ACTION}" in
  create)
    if [ -r "${CONFIG_FILE}" ]; then
      kind create cluster --config "${CONFIG_FILE}" --name "${CLUSTER_NAME}" --kubeconfig "${KUBECONFIG_FILE}" --wait 10m
    else
      echo "Non-existant config file: ${CONFIG_FILE}"
      echo "Check your Kubernetes cluster version (${CLUSTER_VERSION})"
      exit 1
    fi
    ;;
  delete)
    kind delete cluster --name "${CLUSTER_NAME}" --kubeconfig "${KUBECONFIG_FILE}"
    ;;
esac

exit 0
