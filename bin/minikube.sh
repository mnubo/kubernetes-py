#!/usr/bin/env bash

OS="`uname`"
case $OS in
  'Linux')
    curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.7.0/minikube-linux-amd64
    ;;
  'Darwin')
    curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.7.0/minikube-darwin-amd64
    ;;
esac

chmod +x minikube
