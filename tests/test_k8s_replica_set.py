#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import uuid

from tests import _utils
from tests.BaseTest import BaseTest
from kubernetes_py.K8sExceptions import *


class K8sReplicaSetTests(BaseTest):
    def setUp(self):
        pass

    def tearDown(self):
        _utils.cleanup_objects()

    def test_delete_nonexistent(self):
        name = "yorc-{0}".format(str(uuid.uuid4()))
        dep = _utils.create_deployment(name=name)
        if _utils.is_reachable(dep.config):
            try:
                dep.delete()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_delete(self):
        name = "yoname"
        rs = _utils.create_rs(name=name)
        config = _utils.create_config()
        if _utils.is_reachable(config):
            _utils.cleanup_rs()
            result = rs.list()
            self.assertIsInstance(result, list)
            self.assertEqual(0, len(result))
