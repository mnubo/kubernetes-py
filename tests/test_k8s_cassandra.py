#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest

from kubernetes.models.v1.Service import Service
from kubernetes.models.v1.ReplicationController import ReplicationController
from kubernetes.models.v1beta1.DaemonSet import DaemonSet

import utils


class CloudNativeCassandraTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_cassandra_setup(self):
        svc = Service(model=utils.cassandra_service())
        k8s_service = utils.create_service(name="cassandra")
        k8s_service.model = svc

        rc = ReplicationController(model=utils.cassandra_rc())
        k8s_rc = utils.create_rc(name="cassandra")
        k8s_rc.model = rc

        ds = DaemonSet(model=utils.cassandra_daemonset())
        k8s_ds = utils.create_daemonset(name="cassandra")
        k8s_ds.model = ds

        if utils.is_reachable(k8s_rc.config.api_host):
           k8s_service.create()
           k8s_rc.create()
