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
from kubernetes.K8sCronJob import K8sCronJob
from kubernetes.K8sDaemonSet import K8sDaemonSet
from kubernetes.K8sDeployment import K8sDeployment
from kubernetes.K8sExceptions import NotFoundException
from kubernetes.K8sJob import K8sJob
from kubernetes.K8sObject import K8sObject
from kubernetes.K8sPersistentVolume import K8sPersistentVolume
from kubernetes.K8sPersistentVolumeClaim import K8sPersistentVolumeClaim
from kubernetes.K8sPod import K8sPod
from kubernetes.K8sReplicaSet import K8sReplicaSet
from kubernetes.K8sReplicationController import K8sReplicationController
from kubernetes.K8sSecret import K8sSecret
from kubernetes.K8sService import K8sService
from kubernetes.K8sVolume import K8sVolume
from kubernetes.K8sVolumeMount import K8sVolumeMount

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


def create_volume_mount(name=None, mount_path=None):
    obj = K8sVolumeMount(
        name=name,
        mount_path=mount_path,
    )
    return obj


def create_pv(config=None, name=None, type=None):
    if config is None:
        config = create_config()
    obj = K8sPersistentVolume(
        config=config,
        name=name,
        type=type,
    )
    return obj


def create_pvc(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sPersistentVolumeClaim(
        config=config,
        name=name
    )
    return obj


def create_job(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sJob(
        config=config,
        name=name
    )
    return obj


def create_cronjob(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sCronJob(
        config=config,
        name=name
    )
    return obj


def create_daemonset(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sDaemonSet(
        config=config,
        name=name
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
        cleanup_pv()
        cleanup_pvc()
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


def cleanup_pv():
    ref = create_pv(name="throwaway", type="hostPath")
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


def cleanup_pvc():
    ref = create_pvc(name="throwaway")
    if is_reachable(ref.config.api_host):
        claims = ref.list()
        while len(claims) > 0:
            for c in claims:
                try:
                    claim = K8sPersistentVolumeClaim(config=ref.config, name=c['metadata']['name']).get()
                    claim.delete()
                except NotFoundException:
                    continue
            claims = ref.list()


def cleanup_jobs():
    ref = create_job(name="throwaway")
    if is_reachable(ref.config.api_host):
        jobs = ref.list()
        while len(jobs) > 0:
            for j in jobs:
                try:
                    job = K8sJob(config=ref.config, name=j['metadata']['name']).get()
                    job.delete()
                except NotFoundException:
                    continue
            jobs = ref.list()


def cleanup_cronjobs():
    ref = create_cronjob(name="throwaway")
    if is_reachable(ref.config.api_host):
        jobs = ref.list()
        while len(jobs) > 0:
            for j in jobs:
                try:
                    job = K8sCronJob(config=ref.config, name=j['metadata']['name']).get()
                    job.delete()
                except NotFoundException:
                    continue
            jobs = ref.list()


# --------------------------------------------------------------------------------- front-end replication controller

def frontend():
    return {
        "kind": "ReplicationController",
        "apiVersion": "v1",
        "metadata": {
            "name": "frontend",
            "namespace": "default",
            "labels": {
                "name": "frontend",
                "rc_version": "780e750d-a0f7-491e-9038-1ee238c012fa"
            }
        },
        "spec": {
            "replicas": 2,
            "selector": {
                "name": "frontend",
                "rc_version": "780e750d-a0f7-491e-9038-1ee238c012fa"
            },
            "template": {
                "metadata": {
                    "labels": {
                        "name": "frontend",
                        "rc_version": "780e750d-a0f7-491e-9038-1ee238c012fa"
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": "frontend",
                            "image": "nginx:latest",
                            "ports": [
                                {
                                    "name": "feport",
                                    "containerPort": 80,
                                    "protocol": "TCP"
                                }
                            ],
                            "resources": {
                                "requests": {
                                    "cpu": "100m",
                                    "memory": "32M"
                                }
                            },
                            "livenessProbe": {
                                "tcpSocket": {
                                    "port": "feport"
                                },
                                "initialDelaySeconds": 15,
                                "timeoutSeconds": 1,
                                "periodSeconds": 10,
                                "successThreshold": 1,
                                "failureThreshold": 3
                            },
                            "readinessProbe": {
                                "httpGet": {
                                    "path": "/",
                                    "port": "feport",
                                    "scheme": "HTTP"
                                },
                                "timeoutSeconds": 1,
                                "periodSeconds": 10,
                                "successThreshold": 1,
                                "failureThreshold": 3
                            },
                            "terminationMessagePath": "/dev/termination-log",
                            "imagePullPolicy": "IfNotPresent"
                        },
                    ],
                    "restartPolicy": "Always",
                    "terminationGracePeriodSeconds": 30,
                    "dnsPolicy": "ClusterFirst",
                    "securityContext": {},
                }
            }
        }
    }


# --------------------------------------------------------------------------------- admintool replication controller

def admintool():
    return {
        'status': {
            'observedGeneration': 0,
            'readyReplicas': 0,
            'fullyLabeledReplicas': 0,
            'replicas': 0
        },
        'kind': 'ReplicationController',
        'spec': {
            'selector': {
                'name': 'admintool',
                'rc_version': '1926c7e1-74e5-4088-86d6-af7b21d38741'
            },
            'template': {
                'spec': {
                    'dnsPolicy': 'ClusterFirst',
                    'terminationGracePeriodSeconds': 30,
                    'restartPolicy': 'Always',

                    # docker in docker is evil
                    # 'volumes': [{
                    #     'hostPath': {
                    #         'path': '/root/.docker/config.json'
                    #     },
                    #     'name': 'dockercred'
                    # }, {
                    #     'hostPath': {
                    #         'path': '/usr/bin/docker'
                    #     },
                    #     'name': 'dockerbin'
                    # }, {
                    #     'hostPath': {
                    #         'path': '/var/run/docker.sock'
                    #     },
                    #     'name': 'dockersock'
                    # }, {
                    #     'hostPath': {
                    #         'path': '/root/.docker'
                    #     },
                    #     'name': 'dockerconfig'
                    # }],

                    'imagePullSecrets': [{'name': 'privateregistry'}],
                    'containers': [{
                        'livenessProbe': {
                            'initialDelaySeconds': 15,
                            'tcpSocket': {
                                'port': 'admintoolport'
                            },
                            'timeoutSeconds': 1
                        },
                        'name': 'admintool',
                        'image': 'nginx:latest',

                        # docker in docker is evil
                        # 'volumeMounts': [{
                        #     'mountPath': '/root/.dockercfg',
                        #     'name': 'dockercred',
                        #     'readOnly': True
                        # }, {
                        #     'mountPath': '/usr/bin/docker',
                        #     'name': 'dockerbin',
                        #     'readOnly': True
                        # }, {
                        #     'mountPath': '/var/run/docker.sock',
                        #     'name': 'dockersock',
                        #     'readOnly': True
                        # }, {
                        #     'mountPath': '/root/.docker',
                        #     'name': 'dockerconfig',
                        #     'readOnly': True
                        # }],

                        'env': [{
                            'name': 'docker_env',
                            'value': 'prod'
                        }, {
                            'name': 'DATADOG_PORT_8125_UDP_ADDR',
                            'value': '10.101.1.52'
                        }, {
                            'name': 'docker_repository',
                            'value': 'dockerep-1.mtl.mnubo.com:4329'
                        }, {
                            'name': 'ENV',
                            'value': 'prod'
                        }, {
                            'name': 'DOCKER_TAG',
                            'value': 'latest'
                        }],
                        'imagePullPolicy': 'IfNotPresent',
                        'readinessProbe': {
                            'httpGet': {
                                'path': '/',
                                'scheme': 'HTTP',
                                'port': 'admintoolport'
                            }
                        },
                        'ports': [{
                            'protocol': 'TCP',
                            'containerPort': 80,
                            'name': 'admintoolport',
                            'hostPort': 80
                        }],
                        'resources': {
                            'requests': {
                                'cpu': '100m',
                                'memory': '32M'
                            }
                        }
                    }]
                },
                'metadata': {
                    'labels': {
                        'name': 'admintool',
                        'rc_version': '1926c7e1-74e5-4088-86d6-af7b21d38741'
                    }
                }
            },
            'replicas': 1
        },
        'apiVersion': 'v1',
        'metadata': {
            'labels': {
                'name': 'admintool',
                'rc_version': '1926c7e1-74e5-4088-86d6-af7b21d38741'
            },
            'name': 'admintool'
        }
    }


# --------------------------------------------------------------------------------- jobs

def job():
    """
    http://kubernetes.io/docs/user-guide/jobs/#running-an-example-job
    """

    return {
        'apiVersion': 'batch/v1',
        'kind': 'Job',
        'metadata': {
            'name': 'pi'
        },
        'spec': {
            'template': {
                'metadata': {
                    'name': 'pi'
                },
                'spec': {
                    'containers': [
                        {
                            'name': 'pi',
                            'image': 'perl',
                            'command': ["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"]
                        }
                    ],
                    'restartPolicy': 'Never'
                }
            }
        }
    }


def scheduledjob():
    """
    http://kubernetes.io/docs/user-guide/cron-jobs/#creating-a-cron-job

    Note:: ScheduledJob resource was introduced in Kubernetes version 1.4,
    but starting from version 1.5 its current name is CronJob.
    """

    return {
        "apiVersion": "batch/v2alpha1",
        "kind": "ScheduledJob",
        "metadata": {
            "name": "hello"
        },
        "spec": {
            "schedule": "*/1 * * * *",
            "jobTemplate": {
                "spec": {
                    "template": {
                        "spec": {
                            "containers": [
                                {
                                    "name": "hello",
                                    "image": "busybox",
                                    "args": [
                                        "/bin/sh",
                                        "-c",
                                        "date; echo Hello from the Kubernetes cluster"
                                    ]
                                }
                            ],
                            "restartPolicy": "OnFailure"
                        }
                    }
                }
            }
        }
    }


def scheduledjob_90():
    """
    Job running for 90s scheduled every minute
    """

    return {
        "apiVersion": "batch/v2alpha1",
        "kind": "ScheduledJob",
        "metadata": {
            "name": "wait"
        },
        "spec": {
            "schedule": "*/1 * * * *",
            "jobTemplate": {
                "spec": {
                    "template": {
                        "spec": {
                            "containers": [
                                {
                                    "name": "wait",
                                    "image": "busybox",
                                    "args": [
                                        "/bin/sh",
                                        "-c",
                                        "date; echo Sleeping; sleep 90"
                                    ]
                                }
                            ],
                            "restartPolicy": "OnFailure"
                        }
                    }
                }
            }
        }
    }

def cronjob():
    """
    http://kubernetes.io/docs/user-guide/cron-jobs/#creating-a-cron-job

    Note:: ScheduledJob resource was introduced in Kubernetes version 1.4,
    but starting from version 1.5 its current name is CronJob.
    """

    return {
        "apiVersion": "batch/v2alpha1",
        "kind": "CronJob",
        "metadata": {
            "name": "hello"
        },
        "spec": {
            "schedule": "*/1 * * * *",
            "jobTemplate": {
                "spec": {
                    "template": {
                        "spec": {
                            "containers": [
                                {
                                    "name": "hello",
                                    "image": "busybox",
                                    "args": [
                                        "/bin/sh",
                                        "-c",
                                        "date; echo Hello from the Kubernetes cluster"
                                    ]
                                }
                            ],
                            "restartPolicy": "OnFailure"
                        }
                    }
                }
            }
        }
    }
