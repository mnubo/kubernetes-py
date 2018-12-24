#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes_py.K8sDaemonSet import K8sDaemonSet
from kubernetes_py.models.v1beta1.DaemonSet import DaemonSet
from tests import _constants
from tests import _utils
from tests.BaseTest import BaseTest


class K8sDaemonSetTests(BaseTest):
    def setUp(self):
        _utils.cleanup_ds()
        _utils.cleanup_rs()
        _utils.cleanup_pods()

    def tearDown(self):
        _utils.cleanup_ds()
        _utils.cleanup_rs()
        _utils.cleanup_pods()

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
            _utils.create_cronjob(name=name)

    def test_init_with_name(self):
        name = "yomama"
        rc = _utils.create_daemonset(name=name)
        self.assertIsNotNone(rc)
        self.assertIsInstance(rc, K8sDaemonSet)
        self.assertEqual(rc.name, name)

    # --------------------------------------------------------------------------------- api - create

    def test_api_create(self):
        ds = DaemonSet(_constants.fluentd_daemonset())
        k8s_ds = _utils.create_daemonset(name=ds.name)
        k8s_ds.model = ds
        if _utils.is_reachable(k8s_ds.config):
            k8s_ds.create()
            self.assertIsInstance(k8s_ds, K8sDaemonSet)

    # --------------------------------------------------------------------------------- api - list

    def test_list(self):
        ds = DaemonSet(_constants.fluentd_daemonset())
        k8s_ds = _utils.create_daemonset(name=ds.name)
        k8s_ds.model = ds

        if _utils.is_reachable(k8s_ds.config):
            k8s_ds.create()
            _list = k8s_ds.list()
            for x in _list:
                self.assertIsInstance(x, K8sDaemonSet)

    # --------------------------------------------------------------------------------- test add selector

    def test_create_without_selector(self):
        k8s_container = _utils.create_container(name="nginx", image="nginx:latest")
        k8s_ds = _utils.create_daemonset(name="yo")
        k8s_ds.add_container(k8s_container)
        if _utils.is_reachable(k8s_ds.config):
            k8s_ds.create()
            self.assertIsInstance(k8s_ds, K8sDaemonSet)
            self.assertEqual(k8s_ds.name, "yo")
