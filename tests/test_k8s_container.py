#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
import utils
from kubernetes.K8sContainer import K8sContainer
from kubernetes.models.v1 import Container
from kubernetes.models.v1.VolumeMount import VolumeMount


class K8sContainerTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        # utils.cleanup_objects()
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
        self.assertEqual(c.model.name, name)
        self.assertEqual(c.model.image, image)

    # ------------------------------------------------------------------------------------- struct

    def test_struct_k8scontainer(self):
        name = "yomama"
        image = "redis:latest"
        c = K8sContainer(name=name, image=image)
        self.assertIsNotNone(c)
        self.assertIsInstance(c, K8sContainer)
        self.assertIsNotNone(c.model)
        self.assertIsInstance(c.model, Container)

    def test_struct_json(self):
        name = "yomama"
        image = "redis:latest"
        c = K8sContainer(name=name, image=image)
        j = c.json()
        self.assertIsInstance(j, dict)
        for i in ['image', 'imagePullPolicy', 'name']:
            self.assertIn(i, j)

    # ------------------------------------------------------------------------------------- add volume mount

    def test_add_volume_mount_no_args(self):
        name = "yomama"
        image = "redis"
        c = K8sContainer(name=name, image=image)
        with self.assertRaises(SyntaxError):
            c.add_volume_mount()

    def test_add_volume_mount_invalid_args(self):
        name = "yomama"
        image = "redis"
        vname = object()
        vmount = object()
        c = K8sContainer(name=name, image=image)
        with self.assertRaises(SyntaxError):
            c.add_volume_mount(name=vname)
        with self.assertRaises(SyntaxError):
            c.add_volume_mount(name=name, mount_path=vmount)

    def test_add_volume_mount(self):
        name = "redis"
        image = "redis:3.0.7"
        c = K8sContainer(name=name, image=image)

        volname = "vol1"
        volmount = "/path/on/container"
        c.add_volume_mount(name=volname, mount_path=volmount)
        self.assertTrue(hasattr(c.model, 'volume_mounts'))
        self.assertIsInstance(c.model.volume_mounts, list)
        self.assertEqual(1, len(c.model.volume_mounts))

        mount = c.model.volume_mounts[0]
        self.assertIsInstance(mount, VolumeMount)
        self.assertEqual(volname, mount.name)
        self.assertEqual(volmount, mount.mount_path)
