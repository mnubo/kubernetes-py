#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import os
import socket
import time
from kubernetes import K8sConfig, K8sObject, K8sContainer, K8sPod, K8sReplicationController, K8sSecret
from kubernetes.K8sExceptions import NotFoundException

kubeconfig_fallback = '{0}/.kube/config'.format(os.path.abspath(os.path.dirname(os.path.realpath(__file__))))


def is_reachable(api_host):
    scheme, host, port = api_host.replace("//", "").split(':')
    try:
        s = socket.create_connection((host, port), timeout=1)
        s.close()
        return True
    except Exception as err:
        return False


def create_container(model=None, name=None, image="redis"):
    if model is None:
        obj = K8sContainer(name=name, image=image)
    else:
        obj = K8sContainer(model=model)
    return obj


def create_config():
    try:
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
    except Exception:
        config = K8sConfig()
    return config


def create_object(config=None, name=None, obj_type=None):
    if config is None:
        config = create_config()
    obj = K8sObject(config=config, name=name, obj_type=obj_type)
    return obj


def create_pod(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sPod(config=config, name=name)
    return obj


def create_rc(config=None, name=None, replicas=0):
    if config is None:
        config = create_config()
    obj = K8sReplicationController(config=config, name=name, replicas=replicas)
    return obj


def create_secret(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sSecret(config=config, name=name)
    return obj


def cleanup_objects():
    config = K8sConfig(kubeconfig=kubeconfig_fallback)
    if is_reachable(config.api_host):
        cleanup_pods()
        cleanup_rcs()


def cleanup_pods():
    pod = create_pod(name="throwaway")
    if is_reachable(pod.config.api_host):
        pods = pod.list()
        for p in pods:
            _list = K8sPod.get_by_name(name=p['metadata']['name'])
            try:
                [x.delete() for x in _list]
            except NotFoundException:
                continue
        time.sleep(2)  # let the pods die


def cleanup_rcs():
    rc = create_rc(name="throwaway")
    if is_reachable(rc.config.api_host):
        rcs = rc.list()
        for rc in rcs:
            _list = K8sReplicationController.get_by_name(name=rc['metadata']['name'])
            try:
                [x.delete() for x in _list]
            except NotFoundException:
                continue
        time.sleep(2)  # let the replication controllers die
