#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import os
import socket

from kubernetes.K8sConfig import K8sConfig
from kubernetes.K8sContainer import K8sContainer
from kubernetes.K8sDeployment import K8sDeployment
from kubernetes.K8sExceptions import NotFoundException
from kubernetes.K8sObject import K8sObject
from kubernetes.K8sPersistentVolume import K8sPersistentVolume
from kubernetes.K8sPod import K8sPod
from kubernetes.K8sReplicaSet import K8sReplicaSet
from kubernetes.K8sReplicationController import K8sReplicationController
from kubernetes.K8sSecret import K8sSecret
from kubernetes.K8sService import K8sService
from kubernetes.K8sVolume import K8sVolume

kubeconfig_fallback = '{0}/.kube/config'.format(os.path.abspath(os.path.dirname(os.path.realpath(__file__))))


# --------------------------------------------------------------------------------- reachability


def is_reachable(api_host):
    port = None
    s = None
    try:
        scheme, host, port = api_host.replace("//", "").split(':')
    except ValueError:  # no port specified
        scheme, host = api_host.replace("//", "").split(":")
    try:
        if port is not None:
            s = socket.create_connection((host, port), timeout=0.5)
        else:
            if scheme == 'http':
                port = 80
            elif scheme == 'https':
                port = 443
            s = socket.create_connection((host, port), timeout=0.5)
        if s is not None:
            s.close()
        return True
    except Exception as err:
        return False


# --------------------------------------------------------------------------------- detecting api server


def _is_api_server(service=None):
    if not isinstance(service, dict):
        return False
    if 'metadata' not in service:
        return False
    if 'labels' not in service['metadata']:
        return False
    if 'component' not in service['metadata']['labels']:
        return False
    if 'provider' not in service['metadata']['labels']:
        return False
    if 'apiserver' != service['metadata']['labels']['component']:
        return False
    if 'kubernetes' != service['metadata']['labels']['provider']:
        return False
    return True


# --------------------------------------------------------------------------------- create


def create_container(model=None, name=None, image="redis"):
    if model is None:
        obj = K8sContainer(
            name=name,
            image=image
        )
    else:
        obj = K8sContainer(model=model)
    return obj


def create_config():
    try:
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
    except Exception:
        config = K8sConfig()
    return config


def create_deployment(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sDeployment(
        config=config,
        name=name
    )
    return obj


def create_object(config=None, name=None, obj_type=None):
    if config is None:
        config = create_config()
    obj = K8sObject(
        config=config,
        name=name,
        obj_type=obj_type
    )
    return obj


def create_pod(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sPod(
        config=config,
        name=name
    )
    return obj


def create_rc(config=None, name=None, replicas=0):
    if config is None:
        config = create_config()
    obj = K8sReplicationController(
        config=config,
        name=name,
        replicas=replicas
    )
    return obj


def create_rs(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sReplicaSet(
        config=config,
        name=name,
    )
    return obj


def create_secret(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sSecret(
        config=config,
        name=name
    )
    return obj


def create_service(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sService(
        config=config,
        name=name
    )
    return obj


def create_volume(name=None, type=None):
    obj = K8sVolume(
        name=name,
        type=type,
    )
    return obj


def create_persistent_volume(config=None, name=None, type=None):
    if config is None:
        config = create_config()
    obj = K8sPersistentVolume(
        config=config,
        name=name,
        type=type,
    )
    return obj


# --------------------------------------------------------------------------------- delete


def cleanup_objects():
    config = K8sConfig(kubeconfig=kubeconfig_fallback)
    if is_reachable(config.api_host):
        cleanup_rc()
        cleanup_deployments()
        cleanup_rs()
        cleanup_pods()
        cleanup_secrets()
        cleanup_services()


def cleanup_pods():
    ref = create_pod(name="throwaway")
    if is_reachable(ref.config.api_host):
        pods = ref.list()
        while len(pods) > 0:
            for p in pods:
                try:
                    pod = K8sPod(config=ref.config, name=p['metadata']['name']).get()
                    pod.delete()
                except NotFoundException:
                    continue
            pods = ref.list()


def cleanup_rc():
    ref = create_rc(name="throwaway")
    if is_reachable(ref.config.api_host):
        rcs = ref.list()
        while len(rcs) > 0:
            for rc in rcs:
                try:
                    obj = K8sReplicationController(config=ref.config, name=rc['metadata']['name']).get()
                    obj.delete()
                except NotFoundException:
                    continue
            rcs = ref.list()


def cleanup_secrets():
    ref = create_secret(name="throwaway")
    if is_reachable(ref.config.api_host):
        secrets = ref.list()
        while len(secrets) > 1:
            for secret in secrets:
                try:
                    obj = K8sSecret(config=ref.config, name=secret['metadata']['name']).get()
                    if 'service-account-token' != obj.type:
                        obj.delete()
                except NotFoundException:
                    continue
            secrets = ref.list()


def cleanup_services():
    ref = create_service(name="throwaway")
    if is_reachable(ref.config.api_host):
        services = ref.list()
        while len(services) > 1:
            for service in services:
                try:
                    obj = K8sService(config=ref.config, name=service['metadata']['name']).get()
                    if not _is_api_server(service):
                        obj.delete()
                except NotFoundException:
                    continue
            services = ref.list()


def cleanup_rs():
    ref = create_rs(name="throwaway")
    if is_reachable(ref.config.api_host):
        rs_list = ref.list()
        while len(rs_list) > 0:
            for rs in rs_list:
                try:
                    obj = K8sReplicaSet(config=ref.config, name=rs['metadata']['name']).get()
                    obj.delete()
                except NotFoundException:
                    continue
            rs_list = ref.list()


def cleanup_deployments():
    ref = create_deployment(name="throwaway")
    if is_reachable(ref.config.api_host):
        deps = ref.list()
        while len(deps) > 0:
            for d in deps:
                try:
                    obj = K8sDeployment(config=ref.config, name=d['metadata']['name']).get()
                    obj.delete()
                except NotFoundException:
                    continue
            deps = ref.list()


def cleanup_persistent_volumes():
    ref = create_persistent_volume(name="throwaway", type="hostPath")
    if is_reachable(ref.config.api_host):
        vols = ref.list()
        while len(vols) > 0:
            for v in vols:
                try:
                    vol = K8sPersistentVolume(config=ref.config, name=v['metadata']['name'], type=ref.type).get()
                    vol.delete()
                except NotFoundException:
                    continue
            vols = ref.list()
