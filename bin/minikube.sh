#!/usr/bin/env bash

# see https://github.com/kubernetes/minikube/releases

MINIKUBE_VERSION="0.17.1"

OS="$(uname)"
case ${OS} in
  'Linux')
    curl -Lo minikube "https://storage.googleapis.com/minikube/releases/v${MINIKUBE_VERSION}/minikube-linux-amd64"
    ;;
  'Darwin')
    curl -Lo minikube "https://storage.googleapis.com/minikube/releases/v${MINIKUBE_VERSION}/minikube-darwin-amd64"
    ;;
esac

chmod +x minikube
