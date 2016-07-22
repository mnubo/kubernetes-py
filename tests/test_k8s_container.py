#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
from kubernetes import K8sContainer
from kubernetes.models.v1 import Container


class K8sContainerTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # ------------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sContainer()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_name_only(self):
        name = "yomama"
        try:
            K8sContainer(name=name)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_image_only(self):
        image = "busybox"
        try:
            K8sContainer(image=image)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_name_and_image(self):
        name = "yomama"
        image = "busybox"
        c = K8sContainer(name=name, image=image)
        self.assertIsNotNone(c)
        self.assertIsInstance(c, K8sContainer)
        self.assertEqual(c.model.get_name(), name)
        self.assertEqual(c.model.get_image(), image)

    # ------------------------------------------------------------------------------------- struct

    def test_struct_k8scontainer(self):
        name = "yomama"
        image = "busybox"
        c = K8sContainer(name=name, image=image)
        self.assertIsNotNone(c)
        self.assertIsInstance(c, K8sContainer)
        self.assertIsNotNone(c.model)
        self.assertIsInstance(c.model, Container)

    def test_struct_container(self):
        name = "yomama"
        image = "busybox"
        c = K8sContainer(name=name, image=image)
        self.assertIsInstance(c.model, Container)
        self.assertIsNone(c.model.liveness_probe)
        self.assertIsNone(c.model.readiness_probe)
        self.assertIsNotNone(c.model.model)

    def test_struct_container_model(self):
        name = "yomama"
        image = "busybox"
        c = K8sContainer(name=name, image=image)
        model = c.model.model
        self.assertIsInstance(model, dict)
        self.assertEqual(7, len(model))
        self.assertIn('hostNetwork', model)
        self.assertIsInstance(model['hostNetwork'], bool)
        self.assertIn('image', model)
        self.assertIsInstance(model['image'], str)
        self.assertIn('imagePullPolicy', model)
        self.assertIsInstance(model['imagePullPolicy'], str)
        self.assertIn('name', model)
        self.assertIsInstance(model['name'], str)
        self.assertEqual(model['name'], name)
        self.assertIn('privileged', model)
        self.assertIsInstance(model['privileged'], bool)
        self.assertIn('resources', model)
        self.assertIsInstance(model['resources'], dict)
        self.assertEqual(1, len(model['resources']))
        self.assertIn('requests', model['resources'])
        self.assertIsInstance(model['resources']['requests'], dict)
        self.assertEqual(2, len(model['resources']['requests']))
        self.assertIn('cpu', model['resources']['requests'])
        self.assertIsInstance(model['resources']['requests']['cpu'], str)
        self.assertIn('memory', model['resources']['requests'])
        self.assertIsInstance(model['resources']['requests']['memory'], str)
        self.assertIn('terminationMessagePath', model)
