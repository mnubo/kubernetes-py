#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import uuid

from tests import utils
from tests.BaseTest import BaseTest
from kubernetes.K8sExceptions import *


class K8sReplicaSetTests(BaseTest):
    def setUp(self):
        pass

    def tearDown(self):
        utils.cleanup_objects()

    def test_delete_nonexistent(self):
        name = "yorc-{0}".format(str(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        if utils.is_reachable(dep.config):
            try:
                dep.delete()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_delete(self):
        name = "yoname"
        rs = utils.create_rs(name=name)
        config = utils.create_config()
        if utils.is_reachable(config):
            utils.cleanup_rs()
            result = rs.list()
            self.assertIsInstance(result, list)
            self.assertEqual(0, len(result))
