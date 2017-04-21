#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import time

from kubernetes.K8sHorizontalPodAutoscaler import K8sHorizontalPodAutoscaler
from kubernetes.models.v1.HorizontalPodAutoscaler import HorizontalPodAutoscaler
from kubernetes.models.v1.Service import Service
from kubernetes.models.v1beta1.Deployment import Deployment
from tests import utils
from tests.BaseTest import BaseTest


class K8sJobTests(BaseTest):

    def setUp(self):
        utils.cleanup_hpas()
        utils.cleanup_services()
        utils.cleanup_deployments()
        utils.cleanup_rs()
        utils.cleanup_pods()

    def tearDown(self):
        utils.cleanup_hpas()
        utils.cleanup_services()
        utils.cleanup_deployments()
        utils.cleanup_rs()
        utils.cleanup_pods()

    # ------------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sHorizontalPodAutoscaler()
            self.fail("Should not fail.")
        except SyntaxError:
            pass
        except IOError:
            pass
        except Exception as err:
            self.fail("Unhandled exception: [ {0} ]".format(err.__class__.__name__))

    # ------------------------------------------------------------------------------------- update

    def test_hpa_update(self):
        c_nginx = utils.create_container(name="yo", image="nginx:latest")

        deploy = utils.create_deployment(name="yo")
        deploy.add_container(c_nginx)
        deploy.desired_replicas = 3

        hpa = utils.create_hpa(name="yo")
        hpa.min_replicas = 1
        hpa.max_replicas = 10
        hpa.cpu_percent = 50
        hpa.scale_ref = ("Deployment", "yo")

        if utils.is_reachable(hpa.config):
            deploy.create()
            hpa.create()
            hpa.get()
            self.assertEqual(50, hpa.cpu_percent)
            hpa.cpu_percent = 70
            hpa.min_replicas = 3
            hpa.max_replicas = 5
            hpa.update()
            hpa.get()
            self.assertEqual(70, hpa.cpu_percent)
            self.assertEqual(3, hpa.min_replicas)
            self.assertEqual(5, hpa.max_replicas)

    # ------------------------------------------------------------------------------------- walkthrough

    def test_hpa_walkthrough(self):
        """
        https://kubernetes.io/docs/user-guide/horizontal-pod-autoscaling/walkthrough/
        https://github.com/kubernetes/community/blob/master/contributors/design-proposals/horizontal-pod-autoscaler.md
        """

        k8s_dep = utils.create_deployment(name="php-apache")
        k8s_dep.model = Deployment(utils.hpa_example_deployment())

        k8s_svc = utils.create_service(name="php-apache")
        k8s_svc.model = Service(utils.hpa_example_service())

        k8s_hpa = utils.create_hpa(name="php-apache")
        k8s_hpa.model = HorizontalPodAutoscaler(utils.hpa_example_autoscaler())

        if utils.is_reachable(k8s_hpa.config):
            # //--- Step One: Run & expose php-apache server
            k8s_dep.create()
            k8s_svc.create()
            # // --- Step Two: Create Horizontal Pod Autoscaler
            k8s_hpa.create()

        # // --- Step Three: Increase Load
        # $ kubectl run -i --tty load-generator --image=busybox /bin/sh
        # $ while true; do wget -q -O- http://php-apache.default.svc.cluster.local; done
        # watch 'kubectl config current-context; echo; kubectl get deployments; echo; kubectl get replicasets; echo; kubectl get pods; echo; kubectl top nodes; echo; kubectl top pods'

        time.sleep(10)  # wait for 10 secs; set a breakpoint if you need.
