#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import utils
from BaseTest import BaseTest
from kubernetes.K8sService import K8sService
from kubernetes.K8sStatefulSet import K8sStatefulSet
from kubernetes.models.v1.Service import Service
from kubernetes.models.v1beta1.StatefulSet import StatefulSet


class StatefulSetNginxTests(BaseTest):
    """
    https://kubernetes.io/docs/tutorials/stateful-application/basic-stateful-set/
    """

    def setUp(self):
        utils.cleanup_stateful_sets()
        utils.cleanup_services()

    def tearDown(self):
        utils.cleanup_stateful_sets()
        utils.cleanup_services()

    def test_stateful_nginx(self):
        svc = Service(headless_service())
        sset = StatefulSet(stateful_set())
        k8s_svc = K8sService(name='headless')
        k8s_sset = K8sStatefulSet(name='sset')
        k8s_svc.model = svc
        k8s_sset.model = sset
        if utils.is_reachable(k8s_svc.config.api_host):
            k8s_svc.create()
            k8s_sset.create()


def headless_service():
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


def stateful_set():
    return {
        "kind": "StatefulSet",
        "metadata": {
            "name": "web"
        },
        "spec": {
            "replicas": 2,
            "serviceName": "nginx",
            "template": {
                "metadata": {
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
                    ]
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
