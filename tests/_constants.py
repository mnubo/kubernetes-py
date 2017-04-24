#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


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


# --------------------------------------------------------------------------------- component_status

def component_status_scheduler():
    return {
        "metadata": {
            "name": "scheduler",
            "selfLink": "/api/v1/componentstatuses/scheduler",
            "creationTimestamp": None
        },
        "conditions": [
            {
                "type": "Healthy",
                "status": "True",
                "message": "ok",
            }
        ]
    }


# --------------------------------------------------------------------------------- horizontal pod autoscaler


def hpa_example_service():
    return {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": "php-apache",
            "namespace": "default",
        },
        "spec": {
            "clusterIP": "10.3.255.25",
            "ports": [
                {
                    "port": 80,
                    "protocol": "TCP",
                    "targetPort": 80
                }
            ],
            "selector": {
                "run": "php-apache"
            },
            "sessionAffinity": "None",
            "type": "ClusterIP"
        },
        "status": {
            "loadBalancer": {}
        }
    }


def hpa_example_deployment():
    return {
        "apiVersion": "extensions/v1beta1",
        "kind": "Deployment",
        "metadata": {
            "annotations": {
                "deployment.kubernetes.io/revision": "1"
            },
            "labels": {
                "run": "php-apache"
            },
            "name": "php-apache",
            "namespace": "default",
        },
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "run": "php-apache"
                }
            },
            "strategy": {
                "rollingUpdate": {
                    "maxSurge": 1,
                    "maxUnavailable": 1
                },
                "type": "RollingUpdate"
            },
            "template": {
                "metadata": {
                    "labels": {
                        "run": "php-apache"
                    }
                },
                "spec": {
                    "containers": [{
                        "image": "gcr.io/google_containers/hpa-example",
                        "imagePullPolicy": "Always",
                        "name": "php-apache",
                        "ports": [{
                            "containerPort": 80,
                            "protocol": "TCP"
                        }],
                        "resources": {
                            "requests": {
                                "cpu": "200m"
                            },
                        },
                    }],
                    "dnsPolicy": "ClusterFirst",
                    "restartPolicy": "Always",
                    "securityContext": {},
                    "terminationGracePeriodSeconds": 30
                }
            }
        },
    }


def hpa_example_autoscaler():
    return {
        "apiVersion": "autoscaling/v1",
        "kind": "HorizontalPodAutoscaler",
        "metadata": {
            "name": "php-apache",
            "namespace": "default",
        },
        "spec": {
            "maxReplicas": 10,
            "minReplicas": 1,
            "scaleTargetRef": {
                "apiVersion": "extensions/v1beta1",
                "kind": "Deployment",
                "name": "php-apache"
            },
            "targetCPUUtilizationPercentage": 50
        },
    }
