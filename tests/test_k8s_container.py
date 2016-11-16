#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import json
import unittest

import yaml

from kubernetes.K8sContainer import K8sContainer
from kubernetes.K8sVolumeMount import K8sVolumeMount
from kubernetes.models.v1 import Container


class K8sContainerTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        # utils.cleanup_objects()
        pass

    # ------------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        with self.assertRaises(SyntaxError):
            K8sContainer()

    def test_init_name_only(self):
        name = "yomama"
        with self.assertRaises(SyntaxError):
            K8sContainer(name=name)

    def test_init_image_only(self):
        image = "redis"
        with self.assertRaises(SyntaxError):
            K8sContainer(image=image)

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
        j = c.serialize()
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
        with self.assertRaises(SyntaxError):
            mount = K8sVolumeMount(name=vname, mount_path=vmount)
            c = K8sContainer(name=name, image=image)
            c.add_volume_mount(mount)

    def test_add_volume_mount(self):
        name = "redis"
        image = "redis:3.0.7"
        c = K8sContainer(name=name, image=image)
        volname = "vol1"
        volpath = "/path/on/container"
        mount = K8sVolumeMount(name=volname, mount_path=volpath)
        c.add_volume_mount(mount)
        self.assertEqual(1, len(c.volume_mounts))
        self.assertIn(mount.model, c.volume_mounts)

    # ------------------------------------------------------------------------------------- serialize

    def test_serialize(self):
        name = "redis"
        image = "redis:3.0.7"
        c = K8sContainer(name=name, image=image)
        volname = "vol1"
        volpath = "/path/on/container"
        mount = K8sVolumeMount(name=volname, mount_path=volpath)
        c.add_volume_mount(mount)
        data = c.serialize()
        self.assertIsInstance(data, dict)

    def test_as_json(self):
        name = "redis"
        image = "redis:3.0.7"
        c = K8sContainer(name=name, image=image)
        volname = "vol1"
        volpath = "/path/on/container"
        mount = K8sVolumeMount(name=volname, mount_path=volpath)
        c.add_volume_mount(mount)
        j = c.as_json()
        self.assertIsInstance(j, str)
        d = json.loads(j)
        self.assertIsInstance(d, dict)

    def test_as_yaml(self):
        name = "redis"
        image = "redis:3.0.7"
        c = K8sContainer(name=name, image=image)
        volname = "vol1"
        volpath = "/path/on/container"
        mount = K8sVolumeMount(name=volname, mount_path=volpath)
        c.add_volume_mount(mount)
        y = c.as_yaml()
        self.assertIsInstance(y, str)
        d = yaml.load(y)
        self.assertIsInstance(d, dict)
