#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from tests import _utils
from tests.BaseTest import BaseTest
from kubernetes_py.K8sReplicationController import K8sReplicationController
from kubernetes_py.K8sService import K8sService
from kubernetes_py.models.v1.ReplicationController import ReplicationController
from kubernetes_py.models.v1.Service import Service
from kubernetes_py.models.v1beta1.DaemonSet import DaemonSet


class StatefulSetCassandraTests(BaseTest):
    """
    https://github.com/kubernetes_py/kubernetes_py/tree/master/examples/storage/cassandra

    Currently incomplete.
    """

    def setUp(self):
        _utils.cleanup_services()
        _utils.cleanup_rc()
        _utils.cleanup_pods()

    def tearDown(self):
        _utils.cleanup_services()
        _utils.cleanup_rc()
        _utils.cleanup_pods()

    def test_cassandra_setup(self):
        svc = Service(_utils.cassandra_service())
        k8s_service = _utils.create_service(name="cassandra")
        k8s_service.model = svc

        rc = ReplicationController(_utils.cassandra_rc())
        k8s_rc = _utils.create_rc(name="cassandra")
        k8s_rc.model = rc

        ds = DaemonSet(_utils.cassandra_daemonset())
        k8s_ds = _utils.create_daemonset(name="cassandra")
        k8s_ds.model = ds

        if _utils.is_reachable(k8s_rc.config):
            k8s_service.create()
            k8s_rc.create()
            self.assertIsInstance(k8s_service, K8sService)
            self.assertIsInstance(k8s_rc, K8sReplicationController)
