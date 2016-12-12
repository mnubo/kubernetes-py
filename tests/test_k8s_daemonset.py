#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
import uuid

import utils
from kubernetes.models.v1beta1.DaemonSet import DaemonSet
from kubernetes.K8sDaemonSet import K8sDaemonSet


class K8sDaemonSetTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sDaemonSet()
            self.fail("Should not fail.")
        except SyntaxError:
            pass
        except IOError:
            pass
        except Exception as err:
            self.fail("Unhandled exception: [ {0} ]".format(err.__class__.__name__))

    def test_init_with_invalid_config(self):
        config = object()
        with self.assertRaises(SyntaxError):
            K8sDaemonSet(config=config)

    def test_init_with_invalid_name(self):
        name = object()
        with self.assertRaises(SyntaxError):
            utils.create_cronjob(name=name)

    def test_init_with_name(self):
        name = "yomama"
        rc = utils.create_daemonset(name=name)
        self.assertIsNotNone(rc)
        self.assertIsInstance(rc, K8sDaemonSet)
        self.assertEqual(rc.name, name)

    # --------------------------------------------------------------------------------- api - create

    def test_api_create(self):
        ds = DaemonSet(model=utils.fluentd_daemonset())
        k8s_ds = utils.create_daemonset(name=ds.name)
        k8s_ds.model = ds
        if utils.is_reachable(k8s_ds.config.api_host):
            k8s_ds.create()
            self.assertIsInstance(k8s_ds, K8sDaemonSet)
