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

    # --------------------------------------------------------------------------------- api - pod - emptydir

    def test_pod_emptydir(self):
        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container = utils.create_container(name=container_name, image=container_image)

        vol_name = "emptydir"
        vol_type = "emptyDir"
        vol_mount = "/test-emptydir"
        volume = utils.create_volume(name=vol_name, type=vol_type, mount_path=vol_mount)
        container.add_volume_mount(volume)

        pod_name = "nginx"
        pod = utils.create_pod(name=pod_name)
        pod.add_volume(volume)
        pod.add_container(container)

        if utils.is_reachable(pod.config.api_host):
            pod.create()
            vols = pod.model.model['spec']['volumes']
            volnames = [x['name'] for x in vols]
            self.assertIn(vol_name, volnames)
            vols = pod.model.pod_spec.model['volumes']
            volnames = [x['name'] for x in vols]
            self.assertIn(vol_name, volnames)
            self.assertEqual(1, len(pod.model.model['spec']['containers']))
            mounts = pod.model.model['spec']['containers'][0]['volumeMounts']
            mountnames = [x['name'] for x in mounts]
            self.assertIn(vol_name, mountnames)
            self.assertEqual(1, len(pod.model.pod_spec.model['containers']))
            mounts = pod.model.pod_spec.model['containers'][0]['volumeMounts']
            mountnames = [x['name'] for x in mounts]
            self.assertIn(vol_name, mountnames)

    # --------------------------------------------------------------------------------- api - pod - hostpath

    def test_pod_hostpath(self):
        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container = utils.create_container(name=container_name, image=container_image)

        vol_name = "hostpath"
        vol_type = "hostPath"
        vol_mount = "/test-hostpath"
        host_path = "/var/lib/docker"
        volume = utils.create_volume(name=vol_name, type=vol_type, mount_path=vol_mount)
        volume.set_host_path(host_path)
        container.add_volume_mount(volume)

        pod_name = "nginx"
        pod = utils.create_pod(name=pod_name)
        pod.add_volume(volume)
        pod.add_container(container)

        if utils.is_reachable(pod.config.api_host):
            pod.create()
            vols = pod.model.model['spec']['volumes']
            volnames = [x['name'] for x in vols]
            self.assertIn(vol_name, volnames)
            vols = pod.model.pod_spec.model['volumes']
            volnames = [x['name'] for x in vols]
            self.assertIn(vol_name, volnames)
            self.assertEqual(1, len(pod.model.model['spec']['containers']))
            mounts = pod.model.model['spec']['containers'][0]['volumeMounts']
            mountnames = [x['name'] for x in mounts]
            self.assertIn(vol_name, mountnames)
            self.assertEqual(1, len(pod.model.pod_spec.model['containers']))
            mounts = pod.model.pod_spec.model['containers'][0]['volumeMounts']
            mountnames = [x['name'] for x in mounts]
            self.assertIn(vol_name, mountnames)

    # --------------------------------------------------------------------------------- api - rc - emptydir

    def test_rc_emptydir(self):
        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container_nginx = utils.create_container(name=container_name, image=container_image)

        container_name = "redis"
        container_image = "redis:3.0.7"
        container_redis = utils.create_container(name=container_name, image=container_image)

        vol_name = "emptydir"
        vol_type = "emptyDir"
        vol_mount = "/test-emptydir"
        volume = utils.create_volume(name=vol_name, type=vol_type, mount_path=vol_mount)
        container_nginx.add_volume_mount(volume)
        container_redis.add_volume_mount(volume)

        rc_name = "app"
        rc = utils.create_rc(name=rc_name)
        rc.add_volume(volume)
        rc.add_container(container_nginx)
        rc.add_container(container_redis)
        rc.set_replicas(1)

        if utils.is_reachable(rc.config.api_host):
            rc.create()
            vols = rc.model.model['spec']['template']['spec']['volumes']
            volnames = [x['name'] for x in vols]
            self.assertIn(vol_name, volnames)
            vols = rc.model.pod_spec.model['volumes']
            volnames = [x['name'] for x in vols]
            self.assertIn(vol_name, volnames)
            self.assertEqual(2, len(rc.model.model['spec']['template']['spec']['containers']))
            mounts = rc.model.model['spec']['template']['spec']['containers'][0]['volumeMounts']
            mountnames = [x['name'] for x in mounts]
            self.assertIn(vol_name, mountnames)
            self.assertEqual(2, len(rc.model.pod_spec.model['containers']))
            mounts = rc.model.pod_spec.model['containers'][0]['volumeMounts']
            mountnames = [x['name'] for x in mounts]
            self.assertIn(vol_name, mountnames)

    # --------------------------------------------------------------------------------- api - rc - hostpath

    def test_rc_hostpath(self):
        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container_nginx = utils.create_container(name=container_name, image=container_image)

        container_name = "redis"
        container_image = "redis:3.0.7"
        container_redis = utils.create_container(name=container_name, image=container_image)

        vol_name = "hostpath"
        vol_type = "hostPath"
        vol_mount = "/test-hostpath"
        hostpath = "/var/lib/docker"
        volume = utils.create_volume(name=vol_name, type=vol_type, mount_path=vol_mount)
        volume.set_host_path(hostpath)
        container_nginx.add_volume_mount(volume)
        container_redis.add_volume_mount(volume)

        rc_name = "app"
        rc = utils.create_rc(name=rc_name)
        rc.add_volume(volume)
        rc.add_container(container_nginx)
        rc.add_container(container_redis)
        rc.set_replicas(1)

        if utils.is_reachable(rc.config.api_host):
            rc.create()
            vols = rc.model.model['spec']['template']['spec']['volumes']
            volnames = [x['name'] for x in vols]
            self.assertIn(vol_name, volnames)
            vols = rc.model.pod_spec.model['volumes']
            volnames = [x['name'] for x in vols]
            self.assertIn(vol_name, volnames)
            self.assertEqual(2, len(rc.model.model['spec']['template']['spec']['containers']))
            mounts = rc.model.model['spec']['template']['spec']['containers'][0]['volumeMounts']
            mountnames = [x['name'] for x in mounts]
            self.assertIn(vol_name, mountnames)
            self.assertEqual(2, len(rc.model.pod_spec.model['containers']))
            mounts = rc.model.pod_spec.model['containers'][0]['volumeMounts']
            mountnames = [x['name'] for x in mounts]
            self.assertIn(vol_name, mountnames)
