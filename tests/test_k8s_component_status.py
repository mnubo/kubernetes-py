#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import re
import uuid

from tests import utils
from tests.BaseTest import BaseTest
from kubernetes.K8sComponentStatus import K8sComponentStatus
from kubernetes.K8sConfig import K8sConfig
from kubernetes.K8sExceptions import *
from kubernetes.models.v1.ComponentCondition import ComponentCondition
from kubernetes.models.v1.ComponentStatus import ComponentStatus
from kubernetes.models.v1.ObjectMeta import ObjectMeta


class K8sComponentStatusTest(BaseTest):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sComponentStatus()
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
            K8sComponentStatus(config=config)

    def test_init_with_invalid_name(self):
        name = object()
        with self.assertRaises(SyntaxError):
            utils.create_component_status(name=name)

    def test_init_with_name(self):
        name = "yo-name"
        c = utils.create_component_status(name=name)
        self.assertIsNotNone(c)
        self.assertIsInstance(c, K8sComponentStatus)
        self.assertEqual('ComponentStatus', c.obj_type)
        self.assertEqual(c.name, name)
        self.assertIsInstance(c.config, K8sConfig)

    def test_init_with_name_and_config(self):
        nspace = "default"
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback, namespace=nspace)
        name = "yo-name"
        c = utils.create_component_status(config=config, name=name)
        self.assertIsNotNone(c)
        self.assertIsInstance(c, K8sComponentStatus)
        self.assertEqual(c.name, name)
        self.assertEqual('ComponentStatus', c.obj_type)
        self.assertIsInstance(c.config, K8sConfig)

    # --------------------------------------------------------------------------------- struct

    def test_struct_k8s_component_status(self):
        name = "yo-name"
        c = utils.create_component_status(name=name)
        self.assertIsInstance(c, K8sComponentStatus)
        self.assertIsInstance(c.base_url, str)
        self.assertIsInstance(c.config, K8sConfig)
        self.assertIsInstance(c.model, ComponentStatus)
        self.assertIsInstance(c.name, str)
        self.assertIsInstance(c.obj_type, str)

    def test_struct_component_status(self):
        c = ComponentStatus(model=utils.component_status_scheduler())
        self.assertIsInstance(c, ComponentStatus)
        self.assertIsInstance(c.metadata, ObjectMeta)
        self.assertIsInstance(c.conditions, list)
        for i in c.conditions:
            self.assertIsInstance(i, ComponentCondition)

    # --------------------------------------------------------------------------------- get

    def test_get_nonexistent(self):
        name = "yo-component"
        c = utils.create_component_status(name=name)
        if utils.is_reachable(c.config.api_host):
            with self.assertRaises(NotFoundException):
                c.get()

    def test_get(self):
        name = "scheduler"
        c = utils.create_component_status(name=name)
        if utils.is_reachable(c.config.api_host):
            from_get = c.get()
            self.assertIsInstance(from_get, K8sComponentStatus)
            self.assertEqual(c, from_get)

    # --------------------------------------------------------------------------------- api - list

    def test_list(self):
        name = "yo-{0}".format(str(uuid.uuid4().get_hex()[:16]))
        components = utils.create_component_status(name=name)
        if utils.is_reachable(components.config.api_host):
            _list = components.list()
            for x in _list:
                self.assertIsInstance(x, K8sComponentStatus)
            etcd_pattern = re.compile("etcd-")
            _filtered = filter(lambda x: etcd_pattern.match(x.name) is not None, _list)
            self.assertIsInstance(_filtered, list)
            self.assertGreaterEqual(len(_filtered), 1)
