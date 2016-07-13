#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
from kubernetes import K8sPodBasedObject


class K8sPodBasedObjectTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # ------------------------------------------------------------------------------------- instantiation

    def test_instantiate_no_args(self):
        try:
            K8sPodBasedObject()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_instantiate_object_type_pod(self):
        ot = "Pod"
        name = "yomama"
        obj = K8sPodBasedObject(name=name, obj_type=ot)
        self.assertIsInstance(obj, K8sPodBasedObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    def test_instantiate_object_type_rc(self):
        ot = "ReplicationController"
        name = "yomama"
        obj = K8sPodBasedObject(name=name, obj_type=ot)
        self.assertIsInstance(obj, K8sPodBasedObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)


