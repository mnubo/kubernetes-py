#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import time

import requests

from tests import utils
from tests.BaseTest import BaseTest
from kubernetes.K8sService import K8sService


class K8sUpgradeTest(BaseTest):
    def setUp(self):
        pass

    def tearDown(self):
        utils.cleanup_rc()
        utils.cleanup_pods()
        utils.cleanup_services()

    def test_myweb_start(self):

        # create a myweb service
        svc = utils.create_service(name="myweb")
        self.assertIsInstance(svc, K8sService)
        svc.selector = {'name': 'myweb'}
        svc.type = 'NodePort'
        svc.add_port(
            name="tcp31030",
            port=31030,
            target_port="tcp31030",
            protocol="tcp",
            node_port=8030
        )

        # create a myweb replication controller
        container = utils.create_container(name="myweb", image="nginx:latest")
        container.add_port(
            container_port=80,
            host_port=31030,
            name="tcp31030",
            protocol="tcp"
        )
        rc = utils.create_rc(name="myweb", replicas=2)
        rc.add_container(container)

        # create the API resources
        if utils.is_reachable(rc.config.api_host):
            svc.create()
            rc.create()
            pass

    def test_request_nodes(self):
        r = None
        while True:
            try:
                r = requests.get(url="http://dcm001-yonkers:8030")
                self.assertEqual(200, r.status_code)
                r = requests.get(url="http://dcs001-yonkers:8030")
                self.assertEqual(200, r.status_code)
                r = requests.get(url="http://dcs002-yonkers:8030")
                self.assertEqual(200, r.status_code)
                print("200 OK")
                time.sleep(0.5)
            except AssertionError:
                print("ERROR! {}".format(r))
