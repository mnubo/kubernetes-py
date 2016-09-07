#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
import utils
from kubernetes.K8sContainer import K8sContainer
from kubernetes.K8sVolume import K8sVolume
from kubernetes.models.v1 import Container


class K8sContainerTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        utils.cleanup_objects()

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
        image = "redis"
        try:
            K8sContainer(image=image)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_name_and_image(self):
        name = "yomama"
        image = "redis"
        c = K8sContainer(name=name, image=image)
        self.assertIsNotNone(c)
        self.assertIsInstance(c, K8sContainer)
        self.assertEqual(c.model.get_name(), name)
        self.assertEqual(c.model.get_image(), image)

    # ------------------------------------------------------------------------------------- struct

    def test_struct_k8scontainer(self):
        name = "yomama"
        image = "redis"
        c = K8sContainer(name=name, image=image)
        self.assertIsNotNone(c)
        self.assertIsInstance(c, K8sContainer)
        self.assertIsNotNone(c.model)
        self.assertIsInstance(c.model, Container)

    def test_struct_container(self):
        name = "yomama"
        image = "redis"
        c = K8sContainer(name=name, image=image)
        self.assertIsInstance(c.model, Container)
        self.assertIsNone(c.model.liveness_probe)
        self.assertIsNone(c.model.readiness_probe)
        self.assertIsNotNone(c.model.model)

    def test_struct_container_model(self):
        name = "yomama"
        image = "redis"
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

    # ------------------------------------------------------------------------------------- add volume mount

    def test_add_volume_mount_no_args(self):
        name = "yomama"
        image = "redis"
        c = K8sContainer(name=name, image=image)
        with self.assertRaises(SyntaxError):
            c.add_volume_mount()

    def test_add_volume_mount_invalid_volume(self):
        name = "yomama"
        image = "redis"
        volume = object()
        c = K8sContainer(name=name, image=image)
        with self.assertRaises(SyntaxError):
            c.add_volume_mount(volume)

    def test_add_volume_emptydir(self):
        name = "redis"
        image = "redis:3.0.7"
        c = K8sContainer(name=name, image=image)
        volname = "vol1"
        voltype = "emptyDir"
        volmount = "/path/on/container"
        vol = K8sVolume(name=volname, type=voltype, mount_path=volmount)
        c.add_volume_mount(vol)
        self.assertIn('volumeMounts', c.model.model)
        self.assertIsInstance(c.model.model['volumeMounts'], list)
        self.assertEqual(1, len(c.model.model['volumeMounts']))
        self.assertIsInstance(c.model.model['volumeMounts'][0], dict)
        for i in ['mountPath', 'name', 'readOnly']:
            self.assertIn(i, c.model.model['volumeMounts'][0])
        self.assertEqual(volname, c.model.model['volumeMounts'][0]['name'])
        self.assertEqual(volmount, c.model.model['volumeMounts'][0]['mountPath'])

    def test_add_volume_hostpath(self):
        name = "redis"
        image = "redis:3.0.7"
        c = K8sContainer(name=name, image=image)
        volname = "vol1"
        voltype = "hostPath"
        volmount = "/path/on/container"
        volhostpath = "/path/on/host"
        vol = K8sVolume(name=volname, type=voltype, mount_path=volmount)
        vol.set_host_path(volhostpath)
        c.add_volume_mount(vol)
        self.assertIn('volumeMounts', c.model.model)
        self.assertIsInstance(c.model.model['volumeMounts'], list)
        self.assertEqual(1, len(c.model.model['volumeMounts']))
        self.assertIsInstance(c.model.model['volumeMounts'][0], dict)
        for i in ['mountPath', 'name', 'readOnly']:
            self.assertIn(i, c.model.model['volumeMounts'][0])
        self.assertEqual(volname, c.model.model['volumeMounts'][0]['name'])
        self.assertEqual(volmount, c.model.model['volumeMounts'][0]['mountPath'])
