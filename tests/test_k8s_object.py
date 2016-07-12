#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
from kubernetes import K8sObject


class K8sObjectTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_instantiate_no_args(self):
        try:
            K8sObject()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_instantiate_invalid_object_type(self):
        ot = 666
        try:
            K8sObject(obj_type=ot)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_instantiate_unknown_object_type(self):
        ot = "yomama"
        try:
            K8sObject(obj_type=ot)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_instantiate_object_type_pod(self):
        ot = "Pod"
        name = "yomama"
        obj = K8sObject(name=name, obj_type=ot)
        self.assertIsInstance(obj, K8sObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    def test_instantiate_object_type_rc(self):
        ot = "ReplicationController"
        name = "yomama"
        obj = K8sObject(name=name, obj_type=ot)
        self.assertIsInstance(obj, K8sObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    def test_instantiate_object_type_secret(self):
        ot = "Secret"
        name = "yomama"
        obj = K8sObject(name=name, obj_type=ot)
        self.assertIsInstance(obj, K8sObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    def test_instantiate_object_type_service(self):
        ot = "Service"
        name = "yomama"
        obj = K8sObject(name=name, obj_type=ot)
        self.assertIsInstance(obj, K8sObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)
