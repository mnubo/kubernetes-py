#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import os
import re
import socket

from kubernetes_py.utils import HttpRequest
from kubernetes_py.K8sComponentStatus import K8sComponentStatus
from kubernetes_py.K8sConfig import K8sConfig
from kubernetes_py.K8sContainer import K8sContainer
from kubernetes_py.K8sCronJob import K8sCronJob
from kubernetes_py.K8sDaemonSet import K8sDaemonSet
from kubernetes_py.K8sDeployment import K8sDeployment
from kubernetes_py.K8sEvent import K8sEvent
from kubernetes_py.K8sExceptions import NotFoundException
from kubernetes_py.K8sExceptions import VersionMismatchException
from kubernetes_py.K8sHorizontalPodAutoscaler import K8sHorizontalPodAutoscaler
from kubernetes_py.K8sJob import K8sJob
from kubernetes_py.K8sNamespace import K8sNamespace
from kubernetes_py.K8sNode import K8sNode
from kubernetes_py.K8sObject import K8sObject
from kubernetes_py.K8sPersistentVolume import K8sPersistentVolume
from kubernetes_py.K8sPersistentVolumeClaim import K8sPersistentVolumeClaim
from kubernetes_py.K8sPetSet import K8sPetSet
from kubernetes_py.K8sPod import K8sPod
from kubernetes_py.K8sReplicaSet import K8sReplicaSet
from kubernetes_py.K8sReplicationController import K8sReplicationController
from kubernetes_py.K8sSecret import K8sSecret
from kubernetes_py.K8sService import K8sService
from kubernetes_py.K8sServiceAccount import K8sServiceAccount
from kubernetes_py.K8sStatefulSet import K8sStatefulSet
from kubernetes_py.K8sStorageClass import K8sStorageClass
from kubernetes_py.K8sVolume import K8sVolume
from kubernetes_py.K8sVolumeMount import K8sVolumeMount
from kubernetes_py.K8sConfigMap import K8sConfigMap


kubeconfig_fallback = "{0}/../kind/kubeconfig.yaml".format(os.path.abspath(os.path.dirname(os.path.realpath(__file__))))


# --------------------------------------------------------------------------------- reachability


def is_reachable(cfg=None):
    try:
        trimmed = re.sub(r"https?://", "", cfg.api_host)
        sock = socket.socket()
        sock.settimeout(0.5)
        if ":" in trimmed:
            host, port = trimmed.split(":")
            address = (host, int(port)) if port is not None else (host, 80)
        else:
            host = trimmed
            address = (host, 80)
        sock.connect(address)
        sock.close()
        req = HttpRequest(
            host=cfg.api_host,
            method="GET",
            auth=cfg.auth,
            cert=cfg.cert,
            ca_cert=cfg.ca_cert,
            ca_cert_data=cfg.ca_cert_data,
            token=cfg.token,
        )
        r = req.send()
        return r["success"]

    except socket.timeout:
        return False

    except Exception as err:
        print(err)
        return False


def assert_server_version(api_host=None, major=None, minor=None, type="exact"):
    try:
        if not api_host:
            return False
        if is_reachable(api_host):
            cfg = K8sConfig(api_host=api_host)
            obj = K8sObject(config=cfg, obj_type="Pod", name="temp")
            v = obj.server_version()
            if type == "exact":
                if int(v["major"]) != major or int(v["minor"]) != minor:
                    msg = "Desired: [ {}.{} ]. Observed: [ {}.{} ].".format(major, minor, v["major"], v["minor"])
                    raise VersionMismatchException(msg)
            return True
        return False

    except VersionMismatchException:
        return False


# --------------------------------------------------------------------------------- detecting api server


def _is_api_server(service=None):
    if not isinstance(service, dict):
        return False
    if "metadata" not in service:
        return False
    if "labels" not in service["metadata"]:
        return False
    if "component" not in service["metadata"]["labels"]:
        return False
    if "provider" not in service["metadata"]["labels"]:
        return False
    if "apiserver" != service["metadata"]["labels"]["component"]:
        return False
    if "kubernetes_py" != service["metadata"]["labels"]["provider"]:
        return False
    return True


# --------------------------------------------------------------------------------- create
def create_component_status(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sComponentStatus(config=config, name=name)
    return obj


def create_container(name=None, image="redis"):
    return K8sContainer(name=name, image=image)


def create_config():
    try:
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
    except Exception:
        config = K8sConfig()
    return config


def create_deployment(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sDeployment(config=config, name=name)
    return obj


def create_object(config=None, name=None, obj_type=None):
    if config is None:
        config = create_config()
    obj = K8sObject(config=config, name=name, obj_type=obj_type)
    return obj


def create_namespace(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sNamespace(config=config, name=name)
    return obj


def create_node(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sNode(config=config, name=name)
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


def create_rs(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sReplicaSet(config=config, name=name,)
    return obj


def create_secret(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sSecret(config=config, name=name)
    return obj


def create_service(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sService(config=config, name=name)
    return obj


def create_volume(name=None, type=None):
    obj = K8sVolume(name=name, type=type,)
    return obj


def create_volume_mount(name=None, mount_path=None):
    obj = K8sVolumeMount(name=name, mount_path=mount_path,)
    return obj


def create_pv(config=None, name=None, type=None):
    if config is None:
        config = create_config()
    obj = K8sPersistentVolume(config=config, name=name, type=type,)
    return obj


def create_pvc(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sPersistentVolumeClaim(config=config, name=name)
    return obj


def create_job(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sJob(config=config, name=name)
    return obj


def create_cronjob(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sCronJob(config=config, name=name)
    return obj


def create_daemonset(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sDaemonSet(config=config, name=name)
    return obj


def create_petset(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sPetSet(config=config, name=name)
    return obj


def create_service_account(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sServiceAccount(config=config, name=name)
    return obj


def create_stateful_set(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sStatefulSet(config=config, name=name)
    return obj


def create_storage_class(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sStorageClass(config=config, name=name)
    return obj


def create_hpa(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sHorizontalPodAutoscaler(config=config, name=name)
    return obj


def create_event(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sEvent(config=config, name=name)
    return obj


def create_configmap(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sConfigMap(config=config, name=name)
    return obj


# --------------------------------------------------------------------------------- delete


def cleanup_objects():
    config = K8sConfig(kubeconfig=kubeconfig_fallback)
    if is_reachable(config):
        cleanup_rc()
        cleanup_deployments()
        cleanup_rs()
        cleanup_pods()
        cleanup_pv()
        cleanup_pvc()
        cleanup_secrets()
        cleanup_services()
        cleanup_namespaces()
        cleanup_nodes()


def cleanup_namespaces():
    ref = create_namespace(name="yo")
    if is_reachable(ref.config):
        _list = ref.list()
        while len(_list) > 3:
            for ns in _list:
                try:
                    if ns.name not in ["kube-system", "default", "kube-public"]:
                        ns.delete(cascade=True)
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_nodes():
    ref = create_node(name="yo")
    if is_reachable(ref.config):
        _list = ref.list(pattern="yo")
        for n in _list:
            n.delete()


def cleanup_pods():
    ref = create_pod(name="yo")
    if is_reachable(ref.config):
        _list = ref.list()
        while len(_list) > 0:
            for p in _list:
                try:
                    p.delete(cascade=True)
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_rc():
    ref = create_rc(name="yo")
    if is_reachable(ref.config):
        _list = ref.list()
        while len(_list) > 0:
            for rc in _list:
                try:
                    rc.delete(cascade=True)
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_secrets():
    ref = create_secret(name="yo")
    if is_reachable(ref.config):
        try:
            _list = ref.list()
            while len(_list) > 0:
                for s in _list:
                    try:
                        if s.type != "kubernetes.io/service-account-token":
                            s.delete(cascade=True)
                        if s.type == "kubernetes.io/service-account-token" and not re.search(r"default", s.name):
                            s.delete(cascade=True)
                        if len(_list) == 1 and re.search(r"default", s.name):
                            raise StopIteration
                    except NotFoundException:
                        continue
                _list = ref.list()
        except StopIteration:
            pass


def cleanup_services():
    ref = create_service(name="yo")
    if is_reachable(ref.config):
        _list = ref.list()
        while len(_list) > 1:
            for svc in _list:
                try:
                    if not _is_api_server(svc):
                        svc.delete(cascade=True)
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_rs():
    ref = create_rs(name="yo")
    if is_reachable(ref.config):
        _list = ref.list()
        while len(_list) > 0:
            for rs in _list:
                try:
                    rs.delete(cascade=True)
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_deployments():
    ref = create_deployment(name="yo")
    if is_reachable(ref.config):
        _list = ref.list()
        while len(_list) > 0:
            for d in _list:
                try:
                    d.delete(cascade=True)
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_pv():
    ref = create_pv(name="yo", type="hostPath")
    if is_reachable(ref.config):
        _list = ref.list()
        while len(_list) > 0:
            for v in _list:
                try:
                    v.delete(cascade=True)
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_pvc():
    ref = create_pvc(name="yo")
    if is_reachable(ref.config):
        _list = ref.list()
        while len(_list) > 0:
            for c in _list:
                try:
                    c.delete(cascade=True)
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_jobs():
    ref = create_job(name="yo")
    if is_reachable(ref.config):
        _list = ref.list()
        while len(_list) > 0:
            for j in _list:
                try:
                    j.delete(cascade=True)
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_cronjobs():
    ref = create_cronjob(name="yo")
    if is_reachable(ref.config):
        _list = ref.list()
        while len(_list) > 0:
            for job in _list:
                try:
                    job.delete(cascade=True)
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_ds():
    ref = create_daemonset(name="yo")
    if is_reachable(ref.config):
        _list = ref.list()
        while len(_list) > 0:
            for d in _list:
                try:
                    d.delete(cascade=True)
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_petsets():
    ref = create_petset(name="yo")
    if is_reachable(ref.config):
        _list = ref.list()
        while len(_list) > 0:
            for p in _list:
                try:
                    petset = K8sPetSet(config=ref.config, name=p["metadata"]["name"]).get()
                    petset.delete(cascade=True)
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_stateful_sets():
    ref = create_stateful_set(name="yo")
    if is_reachable(ref.config):
        _list = ref.list()
        while len(_list) > 0:
            for p in _list:
                try:
                    sset = K8sStatefulSet(config=ref.config, name=p["metadata"]["name"]).get()
                    sset.delete(cascade=True)
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_service_accounts():
    ref = create_service_account(name="yo")
    if is_reachable(ref.config):
        _list = ref.list()
        try:
            while len(_list) > 0:
                for p in _list:
                    try:
                        name = p.name
                        if name != "default":
                            p.delete(cascade=True)
                        if len(_list) == 1 and name == "default":
                            raise StopIteration
                    except NotFoundException:
                        continue
                _list = ref.list()
        except StopIteration:
            pass


def cleanup_storage_class():
    ref = create_storage_class(name="yo")
    if is_reachable(ref.config):
        _list = ref.list()
        while len(_list) > 0:
            for p in _list:
                try:
                    p.delete(cascade=True)
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_hpas():
    ref = create_hpa(name="yo")
    if is_reachable(ref.config):
        _list = ref.list()
        while len(_list) > 0:
            for p in _list:
                try:
                    p.delete(cascade=True)
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_configmap():
    ref = create_configmap(name="yo")
    if is_reachable(ref.config):
        _list = ref.list(pattern="testcfgmap")
        while len(_list) > 0:
            for p in _list:
                try:
                    p.delete(cascade=True)
                except NotFoundException:
                    continue
            _list = ref.list()
