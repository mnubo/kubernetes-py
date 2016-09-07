#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
import utils
from kubernetes.K8sVolume import K8sVolume


class K8sVolumeTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        utils.cleanup_objects()

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        with self.assertRaises(SyntaxError):
            K8sVolume()

    def test_init_invalid_name(self):
        name = object()
        with self.assertRaises(SyntaxError):
            K8sVolume(name=name)

    def test_init_invalid_type(self):
        name = "yoname"
        type = object()
        with self.assertRaises(SyntaxError):
            K8sVolume(name=name, type=type)

    def test_init_invalid_mount_path(self):
        name = 'yoname'
        type = 'emptyDir'
        mount_path = object()
        with self.assertRaises(SyntaxError):
            K8sVolume(name=name, type=type, mount_path=mount_path)

    def test_init_windows_mount_path(self):
        name = 'yoname'
        type = 'emptyDir'
        mount_path = "C:\Program Files\Your Mom"
        vol = K8sVolume(name=name, type=type, mount_path=mount_path)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual('emptyDir', vol.type)

    def test_init(self):
        name = "yoname"
        mount_path = "/path/on/container"
        vol = K8sVolume(name=name, mount_path=mount_path)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual('emptyDir', vol.type)

    # --------------------------------------------------------------------------------- emptyDir

    def test_emptydir_init(self):
        name = "yoname"
        type = "emptyDir"
        mount_path = "/path/on/container"
        vol = K8sVolume(name=name, type=type, mount_path=mount_path)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual(type, vol.type)

    def test_emptydir_set_medium_invalid_type(self):
        name = "yoname"
        type = "hostPath"
        mount_path = "/path/on/container"
        vol = K8sVolume(name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_medium()

    def test_emptydir_set_medium_invalid(self):
        name = "yoname"
        type = "hostPath"
        medium = "yomedium"
        mount_path = "/path/on/container"
        vol = K8sVolume(name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_medium(medium)

    def test_emptydir_set_medium_none(self):
        name = "yoname"
        type = "emptyDir"
        mount_path = "/path/on/container"
        vol = K8sVolume(name=name, type=type, mount_path=mount_path)
        vol.set_medium()
        self.assertEqual('', vol.medium)

    def test_emptydir_set_medium_emptystring(self):
        name = "yoname"
        type = "emptyDir"
        mount_path = "/path/on/container"
        vol = K8sVolume(name=name, type=type, mount_path=mount_path)
        vol.set_medium('')
        self.assertEqual('', vol.medium)

    def test_emptydir_set_medium_memory(self):
        name = "yoname"
        type = "emptyDir"
        mount_path = "/path/on/container"
        medium = "Memory"
        vol = K8sVolume(name=name, type=type, mount_path=mount_path)
        vol.set_medium(medium)
        self.assertEqual(medium, vol.medium)

    # --------------------------------------------------------------------------------- hostPath

    def test_hostpath_init(self):
        name = "yoname"
        type = "hostPath"
        mount_path = "/path/on/container"
        vol = K8sVolume(name=name, type=type, mount_path=mount_path)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual(type, vol.type)

    def test_hostpath_set_path_invalid_type(self):
        name = "yoname"
        type = "emptyDir"
        mount_path = "/path/on/container"
        host_path = "/path/on/host"
        vol = K8sVolume(name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_host_path(host_path)

    def test_hostpath_set_path_none(self):
        name = "yoname"
        type = "hostPath"
        mount_path = "/path/on/container"
        vol = K8sVolume(name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_host_path()

    def test_hostpath_set_path(self):
        name = "yoname"
        type = "hostPath"
        host_path = "/path/on/host"
        mount_path = "/path/on/container"
        vol = K8sVolume(name=name, type=type, mount_path=mount_path)
        vol.set_host_path(host_path)
        self.assertEqual(host_path, vol.host_path)
