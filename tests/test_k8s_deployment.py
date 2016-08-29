#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
import utils
import uuid
from kubernetes import K8sDeployment
from kubernetes.K8sExceptions import *


class K8sDeploymentTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sDeployment()
            self.fail("Should not fail.")
        except SyntaxError:
            pass
        except IOError:
            pass
        except Exception as err:
            self.fail("Unhandled exception: [ {0} ]".format(err.__class__.__name__))

    def test_init_with_invalid_config(self):
        config = object()
        try:
            K8sDeployment(config=config)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_invalid_name(self):
        name = object()
        try:
            utils.create_rc(name=name)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_name(self):
        name = "yomama"
        rc = utils.create_rc(name=name)
        self.assertIsNotNone(rc)
        self.assertIsInstance(rc, K8sDeployment)
        self.assertEqual(rc.name, name)

    # ------------------------------------------x--------------------------------------- api - create

    def test_create_no_args(self):
        name = "yodep-{0}".format(unicode(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        if utils.is_reachable(dep.config.api_host):
            try:
                dep.create()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, UnprocessableEntityException)

    def test_create_with_container_zero_replicas(self):
        name = "yodep-{0}".format(unicode(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        cont_name = "redis"
        cont_image = "redis:3.2.3"
        cont = utils.create_container(name=cont_name, image=cont_image)
        dep.add_container(container=cont)
        if utils.is_reachable(dep.config.api_host):
            d = dep.create()
            self.assertIsNotNone(d)
            self.assertIsInstance(d, K8sDeployment)
            self.assertEqual(d, dep)
            self.assertEqual(0, d.model.model['spec']['replicas'])


