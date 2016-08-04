#!/usr/bin/env bash

# see https://github.com/kubernetes/minikube/releases

OS="`uname`"
case ${OS} in
  'Linux')
    curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.7.1/minikube-linux-amd64
    ;;
  'Darwin')
    curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.7.1/minikube-darwin-amd64
    ;;
esac

chmod +x minikube
