#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import time
import uuid

from kubernetes_py.K8sConfigMap import K8sConfigMap
from kubernetes_py.models.v1.ConfigMap import ConfigMap
from tests import _constants
from tests import _utils
from tests.BaseTest import BaseTest


class K8sConfigMapTests(BaseTest):
    def setUp(self):
        _utils.cleanup_configmap()

    def tearDown(self):
        _utils.cleanup_configmap()

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sConfigMap()
            self.fail("Should not fail.")
        except SyntaxError:
            pass
        except IOError:
            pass
        except Exception as err:
            self.fail("Unhandled exception: [ {0} ]".format(err))

    def test_init_with_invalid_config(self):
        config = object()
        with self.assertRaises(SyntaxError):
            K8sConfigMap(config=config)

    def test_init_with_invalid_name(self):
        name = object()
        with self.assertRaises(SyntaxError):
            _utils.create_configmap(name=name)

    def test_init_with_name(self):
        name = "testcfgmap"
        rc = _utils.create_configmap(name=name)
        self.assertIsNotNone(rc)
        self.assertIsInstance(rc, K8sConfigMap)
        self.assertEqual(rc.name, name)

    # --------------------------------------------------------------------------------- api - create

    def test_api_create(self):
        name = "testcfgmap-{}".format(uuid.uuid4())
        config_map = ConfigMap(_constants.configmap())
        k8s_configmap = _utils.create_configmap(name=name)
        k8s_configmap.model = config_map
        if _utils.is_reachable(k8s_configmap.config):
            k8s_configmap.create()
            self.assertIsInstance(k8s_configmap, K8sConfigMap)

    # --------------------------------------------------------------------------------- api - list

    def test_list(self):
        name = "cfgmap-{}".format(uuid.uuid4())
        config_map = ConfigMap(_constants.configmap())

        k8s_configmap = _utils.create_configmap(name=name)
        k8s_configmap.model = config_map

        if _utils.is_reachable(k8s_configmap.config):
            k8s_configmap.create()
            all_configmaps = k8s_configmap.list()
            for c in all_configmaps:
                self.assertIsInstance(c, K8sConfigMap)

    # --------------------------------------------------------------------------------- object - data

    def test_data(self):
        cfg = _utils.create_config()
        k8s = K8sConfigMap(config=cfg, name="yo")
        fake_data = {"test_key": "test_value"}
        k8s.data = fake_data
        parsed_data = k8s.data
        self.assertIsInstance(parsed_data, dict)
        self.assertEqual(fake_data, parsed_data)

    def test_data_wrong_keys(self):
        cfg = _utils.create_config()
        k8s = K8sConfigMap(config=cfg, name="yo")
        fake_data = {"@": "test_value"}
        with self.assertRaises(SyntaxError):
            k8s.data = fake_data

        fake_data = {"abc@123": "test_value"}

        with self.assertRaises(SyntaxError):
            k8s.data = fake_data
