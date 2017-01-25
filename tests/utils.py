#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import os
import socket
import re

from kubernetes.K8sConfig import K8sConfig
from kubernetes.K8sContainer import K8sContainer
from kubernetes.K8sCronJob import K8sCronJob
from kubernetes.K8sDaemonSet import K8sDaemonSet
from kubernetes.K8sDeployment import K8sDeployment
from kubernetes.K8sExceptions import NotFoundException
from kubernetes.K8sJob import K8sJob
from kubernetes.K8sObject import K8sObject
from kubernetes.K8sNamespace import K8sNamespace
from kubernetes.K8sPersistentVolume import K8sPersistentVolume
from kubernetes.K8sPersistentVolumeClaim import K8sPersistentVolumeClaim
from kubernetes.K8sPod import K8sPod
from kubernetes.K8sReplicaSet import K8sReplicaSet
from kubernetes.K8sReplicationController import K8sReplicationController
from kubernetes.K8sSecret import K8sSecret
from kubernetes.K8sService import K8sService
from kubernetes.K8sVolume import K8sVolume
from kubernetes.K8sVolumeMount import K8sVolumeMount
from kubernetes.K8sPetSet import K8sPetSet
from kubernetes.K8sServiceAccount import K8sServiceAccount

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


def create_namespace(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sNamespace(
        config=config,
        name=name
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


def create_petset(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sPetSet(
        config=config,
        name=name
    )
    return obj


def create_service_account(config=None, name=None):
    if config is None:
        config = create_config()
    obj = K8sServiceAccount(
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
        cleanup_namespaces()


def cleanup_namespaces():
    ref = create_namespace(name="throwaway")
    if is_reachable(ref.config.api_host):
        _list = ref.list()
        while len(_list) > 2:
            for p in _list:
                try:
                    if p['metadata']['name'] not in ['kube-system', 'default']:
                        ns = K8sNamespace(config=ref.config, name=p['metadata']['name']).get()
                        ns.delete()
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_pods():
    ref = create_pod(name="throwaway")
    if is_reachable(ref.config.api_host):
        _list = ref.list()
        while len(_list) > 0:
            for p in _list:
                try:
                    pod = K8sPod(config=ref.config, name=p['metadata']['name']).get()
                    pod.delete()
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_rc():
    ref = create_rc(name="throwaway")
    if is_reachable(ref.config.api_host):
        _list = ref.list()
        while len(_list) > 0:
            for rc in _list:
                try:
                    obj = K8sReplicationController(config=ref.config, name=rc['metadata']['name']).get()
                    obj.delete()
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_secrets():
    ref = create_secret(name="throwaway")
    if is_reachable(ref.config.api_host):
        try:
            _list = ref.list()
            while len(_list) > 0:
                for secret in _list:
                    try:
                        name = secret['metadata']['name']
                        obj = K8sSecret(config=ref.config, name=name).get()
                        if obj.type != 'kubernetes.io/service-account-token':
                            obj.delete()
                        if obj.type == 'kubernetes.io/service-account-token' and not re.search(r'default', name):
                            obj.delete()
                        if len(_list) == 1 and re.search(r'default', name):
                            raise StopIteration
                    except NotFoundException:
                        continue
                _list = ref.list()
        except StopIteration:
            pass


def cleanup_services():
    ref = create_service(name="throwaway")
    if is_reachable(ref.config.api_host):
        _list = ref.list()
        while len(_list) > 1:
            for service in _list:
                try:
                    obj = K8sService(config=ref.config, name=service['metadata']['name']).get()
                    if not _is_api_server(service):
                        obj.delete()
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_rs():
    ref = create_rs(name="throwaway")
    if is_reachable(ref.config.api_host):
        _list = ref.list()
        while len(_list) > 0:
            for rs in _list:
                try:
                    obj = K8sReplicaSet(config=ref.config, name=rs['metadata']['name']).get()
                    obj.delete()
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_deployments():
    ref = create_deployment(name="throwaway")
    if is_reachable(ref.config.api_host):
        _list = ref.list()
        while len(_list) > 0:
            for d in _list:
                try:
                    obj = K8sDeployment(config=ref.config, name=d['metadata']['name']).get()
                    obj.delete()
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_pv():
    ref = create_pv(name="throwaway", type="hostPath")
    if is_reachable(ref.config.api_host):
        _list = ref.list()
        while len(_list) > 0:
            for v in _list:
                try:
                    vol = K8sPersistentVolume(config=ref.config, name=v['metadata']['name'], type=ref.type).get()
                    vol.delete()
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_pvc():
    ref = create_pvc(name="throwaway")
    if is_reachable(ref.config.api_host):
        _list = ref.list()
        while len(_list) > 0:
            for c in _list:
                try:
                    claim = K8sPersistentVolumeClaim(config=ref.config, name=c['metadata']['name']).get()
                    claim.delete()
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_jobs():
    ref = create_job(name="throwaway")
    if is_reachable(ref.config.api_host):
        _list = ref.list()
        while len(_list) > 0:
            for j in _list:
                try:
                    job = K8sJob(config=ref.config, name=j['metadata']['name']).get()
                    job.delete()
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_cronjobs():
    ref = create_cronjob(name="throwaway")
    if is_reachable(ref.config.api_host):
        _list = ref.list()
        while len(_list) > 0:
            for j in _list:
                try:
                    job = K8sCronJob(config=ref.config, name=j['metadata']['name']).get()
                    job.delete()
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_ds():
    ref = create_daemonset(name="throwaway")
    if is_reachable(ref.config.api_host):
        _list = ref.list()
        while len(_list) > 0:
            for d in _list:
                try:
                    dset = K8sDaemonSet(config=ref.config, name=d['metadata']['name']).get()
                    dset.delete()
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_petset():
    ref = create_petset(name="throwaway")
    if is_reachable(ref.config.api_host):
        _list = ref.list()
        while len(_list) > 0:
            for p in _list:
                try:
                    petset = K8sPetSet(config=ref.config, name=p['metadata']['name']).get()
                    petset.delete()
                except NotFoundException:
                    continue
            _list = ref.list()


def cleanup_service_accounts():
    ref = create_service_account(name="throwaway")
    if is_reachable(ref.config.api_host):
        _list = ref.list()
        try:
            while len(_list) > 0:
                for p in _list:
                    try:
                        name = p['metadata']['name']
                        if name != 'default':
                            sa = K8sServiceAccount(config=ref.config, name=name).get()
                            sa.delete()
                        if len(_list) == 1 and name == 'default':
                            raise StopIteration
                    except NotFoundException:
                        continue
                _list = ref.list()
        except StopIteration:
            pass

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


# --------------------------------------------------------------------------------- cloud-native cassandra example

def cassandra_service():
    return {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "labels": {
                "name": "cassandra"
            },
            "name": "cassandra"
        },
        "spec": {
            "ports": [
                {
                    "port": 9042
                }
            ],
            "selector": {
                "name": "cassandra"
            }
        }
    }


def cassandra_rc():
    return {
        "apiVersion": "v1",
        "kind": "ReplicationController",
        "metadata": {
            "name": "cassandra"
        },
        "spec": {
            "replicas": 2,
            "template": {
                "metadata": {
                    "labels": {
                        "name": "cassandra"
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "command": [
                                "/run.sh"
                            ],
                            "resources": {
                                "limits": {
                                    "cpu": 0.5
                                }
                            },
                            "env": [
                                {
                                    "name": "MAX_HEAP_SIZE",
                                    "value": "512M"
                                },
                                {
                                    "name": "HEAP_NEWSIZE",
                                    "value": "100M"
                                },
                                {
                                    "name": "POD_NAMESPACE",
                                    "valueFrom": {
                                        "fieldRef": {
                                            "fieldPath": "metadata.namespace"
                                        }
                                    }
                                },
                                {
                                    "name": "POD_IP",
                                    "valueFrom": {
                                        "fieldRef": {
                                            "fieldPath": "status.podIP"
                                        }
                                    }
                                }
                            ],
                            "image": "gcr.io/google-samples/cassandra:v9",
                            "name": "cassandra",
                            "ports": [
                                {
                                    "containerPort": 7000,
                                    "name": "intra-node"
                                },
                                {
                                    "containerPort": 7001,
                                    "name": "tls-intra-node"
                                },
                                {
                                    "containerPort": 7199,
                                    "name": "jmx"
                                },
                                {
                                    "containerPort": 9042,
                                    "name": "cql"
                                }
                            ],
                            "volumeMounts": [
                                {
                                    "mountPath": "/cassandra_data",
                                    "name": "data"
                                }
                            ]
                        }
                    ],
                    "volumes": [
                        {
                            "name": "data",
                            "emptyDir": {}
                        }
                    ]
                }
            }
        }
    }


def cassandra_daemonset():
    return {
        "apiVersion": "extensions/v1beta1",
        "kind": "DaemonSet",
        "metadata": {
            "labels": {
                "name": "cassandra"
            },
            "name": "cassandra"
        },
        "spec": {
            "template": {
                "metadata": {
                    "labels": {
                        "name": "cassandra"
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "command": [
                                "/run.sh"
                            ],
                            "env": [
                                {
                                    "name": "MAX_HEAP_SIZE",
                                    "value": "512M"
                                },
                                {
                                    "name": "HEAP_NEWSIZE",
                                    "value": "100M"
                                },
                                {
                                    "name": "POD_NAMESPACE",
                                    "valueFrom": {
                                        "fieldRef": {
                                            "fieldPath": "metadata.namespace"
                                        }
                                    }
                                },
                                {
                                    "name": "POD_IP",
                                    "valueFrom": {
                                        "fieldRef": {
                                            "fieldPath": "status.podIP"
                                        }
                                    }
                                }
                            ],
                            "image": "gcr.io/google-samples/cassandra:v9",
                            "name": "cassandra",
                            "ports": [
                                {
                                    "containerPort": 7000,
                                    "name": "intra-node"
                                },
                                {
                                    "containerPort": 7001,
                                    "name": "tls-intra-node"
                                },
                                {
                                    "containerPort": 7199,
                                    "name": "jmx"
                                },
                                {
                                    "containerPort": 9042,
                                    "name": "cql"
                                }
                            ],
                            "resources": {
                                "requests": {
                                    "cpu": 0.5
                                }
                            },
                            "volumeMounts": [
                                {
                                    "mountPath": "/cassandra_data",
                                    "name": "data"
                                }
                            ]
                        }
                    ],
                    "volumes": [
                        {
                            "name": "data",
                            "emptyDir": {}
                        }
                    ]
                }
            }
        }
    }


# --------------------------------------------------------------------------------- fluentd

def fluentd_daemonset():
    return {
        "apiVersion": "extensions/v1beta1",
        "kind": "DaemonSet",
        "metadata": {
            "labels": {
                "k8s-app": "fluentd-logging",
                "version": "v1"
            },
            "name": "fluentd-elasticsearch-v1",
            "namespace": "default"
        },
        "spec": {
            "selector": {
                "matchLabels": {
                    "k8s-app": "fluentd-logging",
                    "version": "v1"
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "k8s-app": "fluentd-logging",
                        "version": "v1"
                    },
                    "name": "fluentd-elasticsearch-v1"
                },
                "spec": {
                    "containers": [
                        {
                            "image": "gcr.io/google_containers/fluentd-elasticsearch:1.17",
                            "name": "fluentd-elasticsearch",
                            "resources": {
                                "limits": {
                                    "memory": "200Mi"
                                },
                                "requests": {
                                    "cpu": "100m",
                                    "memory": "200Mi"
                                }
                            },
                            "volumeMounts": [
                                {
                                    "mountPath": "/var/log",
                                    "name": "varlog"
                                },
                                {
                                    "mountPath": "/var/lib/docker/containers",
                                    "name": "varlibdockercontainers",
                                    "readOnly": True
                                }
                            ]
                        }
                    ],
                    "terminationGracePeriodSeconds": 30,
                    "volumes": [
                        {
                            "hostPath": {
                                "path": "/var/log"
                            },
                            "name": "varlog"
                        },
                        {
                            "hostPath": {
                                "path": "/var/lib/docker/containers"
                            },
                            "name": "varlibdockercontainers"
                        }
                    ]
                }
            }
        }
    }


# --------------------------------------------------------------------------------- myweb

def myweb_container():
    return {
        "name": "myweb",
        "image": "nginx:1.10",
        "ports": [
            {
                "containerPort": 80,
                "name": "myweb",
                "protocol": "TCP"
            }
        ],
        "volumeMounts": [
            {
                "name": "dockercred",
                "mountPath": "/root/.dockercfg",
                "readOnly": True
            },
            {
                "name": "dockerbin",
                "mountPath": "/usr/bin/docker",
                "readOnly": True
            },
            {
                "name": "dockersock",
                "mountPath": "/var/run/docker.sock",
                "readOnly": True
            }
        ],
        "livenessProbe": {
            "tcpSocket": {
                "port": "myweb"
            },
            "initialDelaySeconds": 15,
            "timeoutSeconds": 1
        },
        "readinessProbe": {
            "httpGet": {
                "path": "/",
                "port": "myweb"
            }
        }
    }


def myweb_envs():
    return {
        "ENV": "sandbox",
        "DATADOG_PORT_8125_UDP_ADDR": "10.0.1.1",
        "A": {
            "valueFrom": {
                "fieldRef": {
                    "fieldPath": "status.podIP"
                }
            }
        },
        "DOCKER_HOST": "tcp://$(A):2375"
    }


# --------------------------------------------------------------------------------- petset

def nginx_service():
    return {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": "nginx",
            "labels": {
                "app": "nginx"
            }
        },
        "spec": {
            "ports": [
                {
                    "port": 80,
                    "name": "web"
                }
            ],
            "clusterIP": "None",
            "selector": {
                "app": "nginx"
            }
        }
    }

def nginx_petset():
    return {
        "apiVersion": "apps/v1alpha1",
        "kind": "PetSet",
        "metadata": {
            "name": "web"
        },
        "spec": {
            "replicas": 2,
            "serviceName": "nginx",
            "template": {
                "metadata": {
                    "annotations": {
                        "pod.alpha.kubernetes.io/initialized": "true"
                    },
                    "labels": {
                        "app": "nginx"
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "image": "gcr.io/google_containers/nginx-slim:0.8",
                            "name": "nginx",
                            "ports": [
                                {
                                    "containerPort": 80,
                                    "name": "web"
                                }
                            ],
                            "volumeMounts": [
                                {
                                    "mountPath": "/usr/share/nginx/html",
                                    "name": "www"
                                }
                            ]
                        }
                    ],
                    "terminationGracePeriodSeconds": 0
                }
            },
            "volumeClaimTemplates": [
                {
                    "metadata": {
                        "annotations": {
                            "volume.alpha.kubernetes.io/storage-class": "anything"
                        },
                        "name": "www"
                    },
                    "spec": {
                        "accessModes": [
                            "ReadWriteOnce"
                        ],
                        "resources": {
                            "requests": {
                                "storage": "1Gi"
                            }
                        }
                    }
                }
            ]
        }
    }