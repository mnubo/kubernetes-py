#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
from kubernetes import K8sPodBasedObject, K8sConfig, K8sContainer
from kubernetes.models.v1 import Pod, ReplicationController, ObjectMeta, PodSpec


class K8sPodBasedObjectTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # ------------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sPodBasedObject()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_object_type_pod(self):
        ot = "Pod"
        name = "yomama"
        obj = K8sPodBasedObject(name=name, obj_type=ot)
        self.assertIsNotNone(obj)
        self.assertIsInstance(obj, K8sPodBasedObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    def test_init_object_type_rc(self):
        ot = "ReplicationController"
        name = "yomama"
        obj = K8sPodBasedObject(name=name, obj_type=ot)
        self.assertIsNotNone(obj)
        self.assertIsInstance(obj, K8sPodBasedObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    # ------------------------------------------------------------------------------------- pod - init

    def test_init_with_model_pod(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)
        self.assertIsInstance(obj.model.model, dict)
        self.assertIsInstance(obj.model.pod_metadata, ObjectMeta)
        self.assertIsInstance(obj.model.pod_spec, PodSpec)
        self.assertIsNone(obj.model.pod_status)

    # ------------------------------------------------------------------------------------- pod - structure

    def test_struct_with_model_pod_check_podmeta(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        obj.model = Pod(name=name)
        meta = obj.model.pod_metadata
        self.assertIsNotNone(meta)
        self.assertIsInstance(meta, ObjectMeta)
        self.assertIsInstance(meta.model, dict)
        self.assertEqual(len(meta.model), 3)
        self.assertIn('labels', meta.model)
        self.assertIsInstance(meta.model['labels'], dict)
        self.assertIn('name', meta.model['labels'])
        self.assertEqual(meta.model['labels']['name'], name)
        self.assertIn('name', meta.model)
        self.assertIsInstance(meta.model['name'], str)
        self.assertEqual(meta.model['name'], name)
        self.assertIn('namespace', meta.model)
        self.assertIsInstance(meta.model['namespace'], str)

    def test_struct_with_model_pod_check_podspec(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        obj.model = Pod(name=name)
        spec = obj.model.pod_spec
        self.assertIsNotNone(spec)
        self.assertIsInstance(spec, PodSpec)
        self.assertIsInstance(spec.containers, list)
        self.assertEqual(0, len(spec.containers))
        self.assertIsInstance(spec.model, dict)
        self.assertEqual(len(spec.model), 4)
        self.assertIn('containers', spec.model)
        self.assertIsInstance(spec.model['containers'], list)
        self.assertIn('dnsPolicy', spec.model)
        self.assertIsInstance(spec.model['dnsPolicy'], str)
        self.assertIn('restartPolicy', spec.model)
        self.assertIsInstance(spec.model['restartPolicy'], str)
        self.assertIn('volumes', spec.model)
        self.assertIsInstance(spec.model['volumes'], list)

    # ------------------------------------------------------------------------------------- rc - init

    def test_init_with_model_rc(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='ReplicationController', name=name)
        self.assertIsNotNone(obj)
        obj.model = ReplicationController(name=name)
        self.assertIsInstance(obj.model, ReplicationController)
        self.assertIsInstance(obj.model.model, dict)
        self.assertIsInstance(obj.model.pod_metadata, ObjectMeta)
        self.assertIsInstance(obj.model.pod_spec, PodSpec)
        self.assertIsNone(obj.model.pod_status)
        self.assertIsInstance(obj.model.rc_metadata, ObjectMeta)

    # ------------------------------------------------------------------------------------- rc - structure

    def test_struct_with_model_rc_check_podmeta(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='ReplicationController', name=name)
        self.assertIsNotNone(obj)
        obj.model = ReplicationController(name=name)
        meta = obj.model.pod_metadata
        self.assertIsNotNone(meta)
        self.assertIsInstance(meta, ObjectMeta)
        self.assertIsInstance(meta.model, dict)
        self.assertEqual(len(meta.model), 3)
        self.assertIn('labels', meta.model)
        self.assertIsInstance(meta.model['labels'], dict)
        self.assertIn('name', meta.model['labels'])
        self.assertEqual(meta.model['labels']['name'], name)
        self.assertIn('name', meta.model)
        self.assertIsInstance(meta.model['name'], str)
        self.assertEqual(meta.model['name'], name)
        self.assertIn('namespace', meta.model)
        self.assertIsInstance(meta.model['namespace'], str)

    def test_struct_with_model_rc_check_podspec(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='ReplicationController', name=name)
        self.assertIsNotNone(obj)
        obj.model = ReplicationController(name=name)
        spec = obj.model.pod_spec
        self.assertIsNotNone(spec)
        self.assertIsInstance(spec, PodSpec)
        self.assertIsInstance(spec.containers, list)
        self.assertEqual(0, len(spec.containers))
        self.assertIsInstance(spec.model, dict)
        self.assertEqual(len(spec.model), 4)
        self.assertIn('containers', spec.model)
        self.assertIsInstance(spec.model['containers'], list)
        self.assertIn('dnsPolicy', spec.model)
        self.assertIsInstance(spec.model['dnsPolicy'], str)
        self.assertIn('restartPolicy', spec.model)
        self.assertIsInstance(spec.model['restartPolicy'], str)
        self.assertIn('volumes', spec.model)
        self.assertIsInstance(spec.model['volumes'], list)

    def test_struct_with_model_rc_check_rcmeta(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='ReplicationController', name=name)
        self.assertIsNotNone(obj)
        obj.model = ReplicationController(name=name)
        meta = obj.model.rc_metadata
        self.assertIsNotNone(meta)
        self.assertIsInstance(meta, ObjectMeta)
        self.assertIsInstance(meta.model, dict)
        self.assertEqual(len(meta.model), 3)
        self.assertIn('labels', meta.model)
        self.assertIsInstance(meta.model['labels'], dict)
        self.assertIn('name', meta.model['labels'])
        self.assertEqual(meta.model['labels']['name'], name)
        self.assertIn('name', meta.model)
        self.assertIsInstance(meta.model['name'], str)
        self.assertEqual(meta.model['name'], name)
        self.assertIn('namespace', meta.model)
        self.assertIsInstance(meta.model['namespace'], str)

    # ------------------------------------------------------------------------------------- pod - add

    def test_pod_add_container_invalid(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        c = object()
        try:
            obj.add_container(c)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, AssertionError)

    def test_pod_add_container(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        podspec = obj.model.model['spec']
        self.assertEqual(0, len(podspec['containers']))

        podspec = obj.model.pod_spec
        self.assertEqual(0, len(podspec.containers))
        self.assertEqual(0, len(podspec.model['containers']))

        name = "yomama"
        image = "busybox"
        c = K8sContainer(name=name, image=image)
        obj.add_container(c)

        podspec = obj.model.model['spec']
        self.assertEqual(1, len(podspec['containers']))

        podspec = obj.model.pod_spec
        self.assertEqual(1, len(podspec.containers))
        self.assertEqual(1, len(podspec.model['containers']))
