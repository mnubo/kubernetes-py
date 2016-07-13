#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
import json
from kubernetes import K8sObject, K8sConfig


class K8sObjectTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # ------------------------------------------------------------------------------------- instantiation

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

    # ------------------------------------------------------------------------------------- conversions

    def test_object_as_dict(self):
        ot = "Service"
        name = "yomama"
        obj = K8sObject(name=name, obj_type=ot)
        dico = obj.as_dict()
        self.assertIsInstance(dico, dict)

    def test_object_as_json(self):
        ot = "Service"
        name = "yomama"
        obj = K8sObject(name=name, obj_type=ot)
        s = obj.as_json()
        self.assertIsInstance(s, str)
        valid = json.loads(s)
        self.assertIsInstance(valid, dict)

    # ------------------------------------------------------------------------------------- set

    def test_object_set_name(self):
        ot = "Pod"
        name1 = "yomama"
        obj = K8sObject(name=name1, obj_type=ot)
        self.assertEqual(name1, obj.name)
        name2 = "sofat"
        obj.set_name(name2)
        self.assertNotEqual(obj.name, name1)
        self.assertEqual(obj.name, name2)

