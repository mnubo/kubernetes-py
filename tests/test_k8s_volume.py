#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
import utils
import uuid
from kubernetes.K8sVolume import K8sVolume
from kubernetes.K8sExceptions import TimedOutException


class K8sVolumeTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        utils.cleanup_objects()

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        config = utils.create_config()
        with self.assertRaises(SyntaxError):
            K8sVolume(config=config)

    def test_init_invalid_name(self):
        name = object()
        config = utils.create_config()
        with self.assertRaises(SyntaxError):
            K8sVolume(config=config, name=name)

    def test_init_invalid_type(self):
        name = "yoname"
        type = object()
        config = utils.create_config()
        with self.assertRaises(SyntaxError):
            K8sVolume(config=config, name=name, type=type)

    def test_init_invalid_mount_path(self):
        name = 'yoname'
        type = 'emptyDir'
        mount_path = object()
        config = utils.create_config()
        with self.assertRaises(SyntaxError):
            K8sVolume(config=config, name=name, type=type, mount_path=mount_path)

    def test_init_windows_mount_path(self):
        name = 'yoname'
        type = 'emptyDir'
        mount_path = "C:\Program Files\Your Mom"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual('emptyDir', vol.type)

    def test_init(self):
        name = "yoname"
        type = 'hostPath'
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual('hostPath', vol.type)

    # --------------------------------------------------------------------------------- emptyDir

    def test_emptydir_init(self):
        name = "yoname"
        type = "emptyDir"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual(type, vol.type)

    def test_emptydir_set_medium_invalid_type(self):
        name = "yoname"
        type = "hostPath"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_medium()

    def test_emptydir_set_medium_invalid(self):
        name = "yoname"
        type = "hostPath"
        medium = "yomedium"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_medium(medium)

    def test_emptydir_set_medium_none(self):
        name = "yoname"
        type = "emptyDir"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        vol.set_medium()
        self.assertEqual('', vol.model.medium)

    def test_emptydir_set_medium_emptystring(self):
        name = "yoname"
        type = "emptyDir"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        vol.set_medium('')
        self.assertEqual('', vol.model.medium)

    def test_emptydir_set_medium_memory(self):
        name = "yoname"
        type = "emptyDir"
        mount_path = "/path/on/container"
        medium = "Memory"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        vol.set_medium(medium)
        self.assertEqual(medium, vol.model.medium)

    # --------------------------------------------------------------------------------- hostPath

    def test_hostpath_init(self):
        name = "yoname"
        type = "hostPath"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual(type, vol.type)

    def test_hostpath_set_path_invalid_type(self):
        name = "yoname"
        type = "emptyDir"
        mount_path = "/path/on/container"
        host_path = "/path/on/host"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_path(host_path)

    def test_hostpath_set_path_none(self):
        name = "yoname"
        type = "hostPath"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_path()

    def test_hostpath_set_path(self):
        name = "yoname"
        type = "hostPath"
        host_path = "/path/on/host"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        vol.set_path(host_path)
        self.assertEqual(host_path, vol.model.path)

    # --------------------------------------------------------------------------------- secret

    def test_secret_init(self):
        name = "yoname"
        type = "secret"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual(type, vol.type)

    def test_secret_set_name_invalid_obj(self):
        name = "yoname"
        type = "secret"
        mount_path = "/path/on/container"
        secret = object()
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_secret_name(secret)

    def test_secret_set_name_invalid_type(self):
        name = "yoname"
        type = "emptyDir"
        mount_path = "/path/on/container"
        secret_name = "yosecret"
        secret = utils.create_secret(name=secret_name)
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_secret_name(secret)

    def test_secret_set_name(self):
        name = "yoname"
        type = "secret"
        mount_path = "/path/on/container"
        secret_name = "yosecret"
        secret = utils.create_secret(name=secret_name)
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        vol.set_secret_name(secret)
        self.assertEqual(vol.model.secret_name, secret_name)

    # --------------------------------------------------------------------------------- awsElasticBlockStore

    def test_aws_init(self):
        name = "yoname"
        type = "awsElasticBlockStore"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual(type, vol.type)

    def test_aws_set_volume_id_none(self):
        name = "yoname"
        type = "awsElasticBlockStore"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_volume_id()

    def test_aws_set_volume_id_invalid_obj(self):
        name = "yoname"
        type = "awsElasticBlockStore"
        mount_path = "/path/on/container"
        volume_id = object()
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_volume_id(volume_id)

    def test_aws_set_volume_id_invalid_type(self):
        name = "yoname"
        type = "emptyDir"
        mount_path = "/path/on/container"
        volume_id = "vol-0a89c9040d544a371"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_volume_id(volume_id)

    def test_aws_set_volume_id(self):
        name = "yoname"
        type = "awsElasticBlockStore"
        mount_path = "/path/on/container"
        volume_id = "vol-0a89c9040d544a371"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        vol.set_volume_id(volume_id)
        self.assertEqual(vol.model.aws_volume_id, volume_id)

    # --------------------------------------------------------------------------------- gcePersistentDisk

    def test_gce_init(self):
        name = "yoname"
        type = "gcePersistentDisk"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual(type, vol.type)

    def test_gce_set_pd_name_none(self):
        name = "yoname"
        type = "gcePersistentDisk"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_pd_name()

    def test_gce_set_pd_name_invalid_obj(self):
        name = "yoname"
        type = "gcePersistentDisk"
        mount_path = "/path/on/container"
        pd_name = object()
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_volume_id(pd_name)

    def test_gce_set_pd_name_invalid_type(self):
        name = "yoname"
        type = "emptyDir"
        mount_path = "/path/on/container"
        pd_name = "yopdname"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_volume_id(pd_name)

    def test_gce_set_pd_name(self):
        name = "yoname"
        type = "awsElasticBlockStore"
        mount_path = "/path/on/container"
        volume_id = "vol-0a89c9040d544a371"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        vol.set_volume_id(volume_id)
        self.assertEqual(vol.model.aws_volume_id, volume_id)

    # --------------------------------------------------------------------------------- aws & gce - fs_type

    def test_aws_set_fs_type_none(self):
        name = "yoname"
        type = "awsElasticBlockStore"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_fs_type()

    def test_gce_set_fs_type_none(self):
        name = "yoname"
        type = "gcePersistentDisk"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_fs_type()

    def test_aws_fs_type_invalid_obj(self):
        name = "yoname"
        type = "awsElasticBlockStore"
        mount_path = "/path/on/container"
        fs_type = object()
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_fs_type(fs_type)

    def test_gce_fs_type_invalid_obj(self):
        name = "yoname"
        type = "gcePersistentDisk"
        mount_path = "/path/on/container"
        fs_type = object()
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_fs_type(fs_type)

    def test_fs_type_invalid_type(self):
        name = "yoname"
        type = "emptyDir"
        mount_path = "/path/on/container"
        fs_type = object()
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_fs_type(fs_type)

    def test_aws_set_fs_type(self):
        name = "yoname"
        type = "awsElasticBlockStore"
        mount_path = "/path/on/container"
        fs_type = "xfs"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        vol.set_fs_type(fs_type)
        self.assertEqual(vol.model.fs_type, fs_type)

    def test_gce_set_fs_type(self):
        name = "yoname"
        type = "gcePersistentDisk"
        mount_path = "/path/on/container"
        fs_type = "xfs"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        vol.set_fs_type(fs_type)
        self.assertEqual(vol.model.fs_type, fs_type)

    # --------------------------------------------------------------------------------- nfs

    def test_nfs_init(self):
        name = "yoname"
        type = "nfs"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual(type, vol.type)

    def test_nfs_set_server_none(self):
        name = "yoname"
        type = "nfs"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_server()

    def test_nfs_set_server_invalid(self):
        name = "yoname"
        type = "nfs"
        mount_path = "/path/on/container"
        server = object()
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_server(server)

    def test_nfs_set_server_invalid_type(self):
        name = "yoname"
        type = "emptyDir"
        mount_path = "/path/on/container"
        server = "nfs.company.com"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_server(server)

    def test_nfs_set_server(self):
        name = "yoname"
        type = "nfs"
        mount_path = "/path/on/container"
        server = "nfs.company.com"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        vol.set_server(server)
        self.assertEqual(vol.model.server, server)

    # --------------------------------------------------------------------------------- gitRepo

    def test_git_repo_init(self):
        name = "yoname"
        type = "gitRepo"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual(type, vol.type)

    def test_git_repo_set_repo_none(self):
        name = "yoname"
        type = "gitRepo"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_git_repository()

    def test_git_repo_set_repo_invalid(self):
        name = "yoname"
        type = "gitRepo"
        mount_path = "/path/on/container"
        repo = object()
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_git_repository(repo=repo)

    def test_nfs_set_repo_invalid_type(self):
        name = "yoname"
        type = "emptyDir"
        mount_path = "/path/on/container"
        repo = "git@somewhere:me/my-git-repository.git"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_git_repository(repo)

    def test_git_repo_set_revision_none(self):
        name = "yoname"
        type = "gitRepo"
        mount_path = "/path/on/container"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_git_revision()

    def test_git_repo_set_revision_invalid(self):
        name = "yoname"
        type = "gitRepo"
        mount_path = "/path/on/container"
        rev = object()
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_git_revision(revision=rev)

    def test_nfs_set_revision_invalid_type(self):
        name = "yoname"
        type = "emptyDir"
        mount_path = "/path/on/container"
        rev = "22f1d8406d464b0c0874075539c1f2e96c253775"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        with self.assertRaises(SyntaxError):
            vol.set_git_revision(rev)

    def test_git_repo_set_repository(self):
        name = "yoname"
        type = "gitRepo"
        mount_path = "/path/on/container"
        repo = "git@somewhere:me/my-git-repository.git"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        vol.set_git_repository(repo)
        self.assertEqual(vol.model.git_repo, repo)

    def test_git_repo_set_revision(self):
        name = "yoname"
        type = "gitRepo"
        mount_path = "/path/on/container"
        rev = "22f1d8406d464b0c0874075539c1f2e96c253775"
        config = utils.create_config()
        vol = K8sVolume(config=config, name=name, type=type, mount_path=mount_path)
        vol.set_git_revision(rev)
        self.assertEqual(vol.model.git_revision, rev)

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
        volume.set_path(host_path)
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

    # --------------------------------------------------------------------------------- api - pod - secret

    def test_pod_secret(self):
        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container = utils.create_container(name=container_name, image=container_image)

        secret_name = "yosecret"
        secret = utils.create_secret(name=secret_name)
        k = ".secret-file"
        v = "dmFsdWUtMg0KDQo="
        secret.set_data(k, v)

        vol_name = "secret"
        vol_type = "secret"
        vol_mount = "/test-secret"
        volume = utils.create_volume(name=vol_name, type=vol_type, mount_path=vol_mount)
        volume.set_secret_name(secret)
        container.add_volume_mount(volume)

        pod_name = "nginx"
        pod = utils.create_pod(name=pod_name)
        pod.add_volume(volume)
        pod.add_container(container)

        if utils.is_reachable(pod.config.api_host):
            secret.create()
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

    # --------------------------------------------------------------------------------- api - pod - aws ebs

    def test_pod_aws_ebs(self):
        # http://kubernetes.io/docs/user-guide/volumes/#awselasticblockstore
        # - the nodes on which pods are running must be AWS EC2 instances
        # - those instances need to be in the same region and availability-zone as the EBS volume
        # - EBS only supports a single EC2 instance mounting a volume

        # Pod creation will timeout waiting for readiness if not on AWS; unschedulable.

        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container = utils.create_container(name=container_name, image=container_image)

        volume_id = "vol-0e3056a2"
        vol_name = "ebs"
        vol_type = "awsElasticBlockStore"
        vol_mount = "/test-aws-ebs"
        volume = utils.create_volume(name=vol_name, type=vol_type, mount_path=vol_mount)
        volume.set_volume_id(volume_id)
        container.add_volume_mount(volume)

        pod_name = "nginx-{0}".format(str(uuid.uuid4()))
        pod = utils.create_pod(name=pod_name)
        pod.add_volume(volume)
        pod.add_container(container)

        if utils.is_reachable(pod.config.api_host):
            try:
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

            except Exception as err:
                self.assertIsInstance(err, TimedOutException)

    # --------------------------------------------------------------------------------- api - pod - gce pd

    def test_pod_gce_pd(self):
        # http://kubernetes.io/docs/user-guide/volumes/#gcepersistentdisk
        # - the nodes on which pods are running must be GCE VMs
        # - those VMs need to be in the same GCE project and zone as the PD

        # Pod creation will timeout waiting for readiness if not on GCE; unschedulable.

        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container = utils.create_container(name=container_name, image=container_image)

        pd_name = "kubernetes-py-test-pd"
        vol_name = "persistent"
        vol_type = "gcePersistentDisk"
        vol_mount = "/test-gce-pd"
        volume = utils.create_volume(name=vol_name, type=vol_type, mount_path=vol_mount)
        volume.set_pd_name(pd_name)
        container.add_volume_mount(volume)

        pod_name = "nginx-{0}".format(str(uuid.uuid4()))
        pod = utils.create_pod(name=pod_name)
        pod.add_volume(volume)
        pod.add_container(container)

        if utils.is_reachable(pod.config.api_host):
            try:
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

            except Exception as err:
                self.assertIsInstance(err, TimedOutException)

    # --------------------------------------------------------------------------------- api - pod - nfs

    def test_pod_nfs(self):
        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container = utils.create_container(name=container_name, image=container_image)

        vol_name = "nfs"
        vol_type = "nfs"
        vol_mount = "/test-nfs"
        server = "howard.mtl.mnubo.com"
        path = "/fs1/test-nfs"
        volume = utils.create_volume(name=vol_name, type=vol_type, mount_path=vol_mount)
        volume.set_server(server)
        volume.set_path(path)
        container.add_volume_mount(volume)

        pod_name = "nginx-{0}".format(str(uuid.uuid4()))
        pod = utils.create_pod(name=pod_name)
        pod.add_volume(volume)
        pod.add_container(container)

        if utils.is_reachable(pod.config.api_host):
            try:
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

            except Exception as err:
                self.assertIsInstance(err, TimedOutException)

    # --------------------------------------------------------------------------------- api - pod - gitRepo

    def test_pod_git_repo(self):
        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container = utils.create_container(name=container_name, image=container_image)

        vol_name = "git-repo"
        vol_type = "gitRepo"
        vol_mount = "/test-git-repo"
        repo = "https://user:pass@git-lab1.mtl.mnubo.com/ops/traffic-analyzer.git"
        revision = "e42d3dca1541ba085f34ce282feda1109a707c7b"
        volume = utils.create_volume(name=vol_name, type=vol_type, mount_path=vol_mount)
        volume.set_git_repository(repo)
        volume.set_git_revision(revision)
        container.add_volume_mount(volume)

        pod_name = "nginx-{0}".format(str(uuid.uuid4()))
        pod = utils.create_pod(name=pod_name)
        pod.add_volume(volume)
        pod.add_container(container)

        if utils.is_reachable(pod.config.api_host):
            try:
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

            except Exception as err:
                self.assertIsInstance(err, TimedOutException)

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
        volume.set_path(hostpath)
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

    # --------------------------------------------------------------------------------- api - rc - secret

    def test_rc_secret(self):
        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container_nginx = utils.create_container(name=container_name, image=container_image)

        container_name = "redis"
        container_image = "redis:3.0.7"
        container_redis = utils.create_container(name=container_name, image=container_image)

        secret_name = "yosecret"
        secret = utils.create_secret(name=secret_name)
        k = ".secret-file"
        v = "dmFsdWUtMg0KDQo="
        secret.set_data(k, v)

        vol_name = "secret"
        vol_type = "secret"
        vol_mount = "/test-secret"
        volume = utils.create_volume(name=vol_name, type=vol_type, mount_path=vol_mount)
        volume.set_secret_name(secret)
        container_nginx.add_volume_mount(volume)
        container_redis.add_volume_mount(volume)

        rc_name = "app"
        rc = utils.create_rc(name=rc_name)
        rc.add_volume(volume)
        rc.add_container(container_nginx)
        rc.add_container(container_redis)
        rc.set_replicas(1)

        if utils.is_reachable(rc.config.api_host):
            secret.create()
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

    # --------------------------------------------------------------------------------- api - rc - aws ebs

    def test_rc_aws_ebs(self):
        # http://kubernetes.io/docs/user-guide/volumes/#awselasticblockstore
        # - the nodes on which pods are running must be AWS EC2 instances
        # - those instances need to be in the same region and availability-zone as the EBS volume
        # - EBS only supports a single EC2 instance mounting a volume

        # Pod creation will timeout waiting for readiness if not on AWS; unschedulable.

        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container_nginx = utils.create_container(name=container_name, image=container_image)

        container_name = "redis"
        container_image = "redis:3.0.7"
        container_redis = utils.create_container(name=container_name, image=container_image)

        volume_id = "vol-0e3056a2"
        vol_name = "ebs"
        vol_type = "awsElasticBlockStore"
        vol_mount = "/test-aws-ebs"
        volume = utils.create_volume(name=vol_name, type=vol_type, mount_path=vol_mount)
        volume.set_volume_id(volume_id)
        container_nginx.add_volume_mount(volume)
        container_redis.add_volume_mount(volume)

        rc_name = "nginx-{0}".format(str(uuid.uuid4()))
        rc = utils.create_rc(name=rc_name)
        rc.add_volume(volume)
        rc.add_container(container_nginx)
        rc.add_container(container_redis)
        rc.set_replicas(3)

        if utils.is_reachable(rc.config.api_host):
            try:
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

            except Exception as err:
                self.assertIsInstance(err, TimedOutException)

    # --------------------------------------------------------------------------------- api - rc - gce pd

    def test_rc_gce_pd(self):
        # http://kubernetes.io/docs/user-guide/volumes/#gcepersistentdisk
        # - the nodes on which pods are running must be GCE VMs
        # - those VMs need to be in the same GCE project and zone as the PD

        # Pod creation will timeout waiting for readiness if not on GCE; unschedulable.

        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container_nginx = utils.create_container(name=container_name, image=container_image)

        container_name = "redis"
        container_image = "redis:3.0.7"
        container_redis = utils.create_container(name=container_name, image=container_image)

        pd_name = "kubernetes-py-test-pd"
        vol_name = "persistent"
        vol_type = "gcePersistentDisk"
        vol_mount = "/test-gce-pd"
        volume = utils.create_volume(name=vol_name, type=vol_type, mount_path=vol_mount, read_only=True)
        volume.set_pd_name(pd_name)
        container_nginx.add_volume_mount(volume)
        container_redis.add_volume_mount(volume)

        rc_name = "nginx-{0}".format(str(uuid.uuid4()))
        rc = utils.create_rc(name=rc_name)
        rc.add_volume(volume)
        rc.add_container(container_nginx)
        rc.add_container(container_redis)
        rc.set_replicas(3)

        if utils.is_reachable(rc.config.api_host):
            try:
                rc.create()

                vols = rc.model.model['spec']['volumes']
                volnames = [x['name'] for x in vols]
                self.assertIn(vol_name, volnames)

                vols = rc.model.pod_spec.model['volumes']
                volnames = [x['name'] for x in vols]
                self.assertIn(vol_name, volnames)
                self.assertEqual(1, len(rc.model.model['spec']['containers']))

                mounts = rc.model.model['spec']['containers'][0]['volumeMounts']
                mountnames = [x['name'] for x in mounts]
                self.assertIn(vol_name, mountnames)
                self.assertEqual(1, len(rc.model.pod_spec.model['containers']))

                mounts = rc.model.pod_spec.model['containers'][0]['volumeMounts']
                mountnames = [x['name'] for x in mounts]
                self.assertIn(vol_name, mountnames)

            except Exception as err:
                self.assertIsInstance(err, TimedOutException)

    # --------------------------------------------------------------------------------- api - rc - nfs

    def test_rc_nfs(self):
        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container_nginx = utils.create_container(name=container_name, image=container_image)

        container_name = "redis"
        container_image = "redis:3.0.7"
        container_redis = utils.create_container(name=container_name, image=container_image)

        vol_name = "nfs"
        vol_type = "nfs"
        vol_mount = "/test-nfs"
        server = "howard.mtl.mnubo.com"
        path = "/fs1/test-nfs"
        volume = utils.create_volume(name=vol_name, type=vol_type, mount_path=vol_mount)
        volume.set_server(server)
        volume.set_path(path)
        container_nginx.add_volume_mount(volume)
        container_redis.add_volume_mount(volume)

        rc_name = "nginx-{0}".format(str(uuid.uuid4()))
        rc = utils.create_rc(name=rc_name)
        rc.add_volume(volume)
        rc.add_container(container_nginx)
        rc.add_container(container_redis)
        rc.set_replicas(3)

        if utils.is_reachable(rc.config.api_host):
            try:
                rc.create()

                vols = rc.model.model['spec']['volumes']
                volnames = [x['name'] for x in vols]
                self.assertIn(vol_name, volnames)

                vols = rc.model.pod_spec.model['volumes']
                volnames = [x['name'] for x in vols]
                self.assertIn(vol_name, volnames)
                self.assertEqual(1, len(rc.model.model['spec']['containers']))

                mounts = rc.model.model['spec']['containers'][0]['volumeMounts']
                mountnames = [x['name'] for x in mounts]
                self.assertIn(vol_name, mountnames)
                self.assertEqual(1, len(rc.model.pod_spec.model['containers']))

                mounts = rc.model.pod_spec.model['containers'][0]['volumeMounts']
                mountnames = [x['name'] for x in mounts]
                self.assertIn(vol_name, mountnames)

            except Exception as err:
                self.assertIsInstance(err, TimedOutException)

    # --------------------------------------------------------------------------------- api - rc - gitRepo

    def test_rc_git_repo(self):
        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container_nginx = utils.create_container(name=container_name, image=container_image)

        container_name = "redis"
        container_image = "redis:3.0.7"
        container_redis = utils.create_container(name=container_name, image=container_image)

        vol_name = "git-repo"
        vol_type = "gitRepo"
        vol_mount = "/test-git-repo"
        repo = "https://user:pass@git-lab1.mtl.mnubo.com/ops/traffic-analyzer.git"
        revision = "e42d3dca1541ba085f34ce282feda1109a707c7b"
        volume = utils.create_volume(name=vol_name, type=vol_type, mount_path=vol_mount)
        volume.set_git_repository(repo)
        volume.set_git_revision(revision)
        container_nginx.add_volume_mount(volume)
        container_redis.add_volume_mount(volume)

        rc_name = "nginx-{0}".format(str(uuid.uuid4()))
        rc = utils.create_rc(name=rc_name)
        rc.add_volume(volume)
        rc.add_container(container_nginx)
        rc.add_container(container_redis)
        rc.set_replicas(3)

        if utils.is_reachable(rc.config.api_host):
            try:
                rc.create()

                vols = rc.model.model['spec']['volumes']
                volnames = [x['name'] for x in vols]
                self.assertIn(vol_name, volnames)

                vols = rc.model.pod_spec.model['volumes']
                volnames = [x['name'] for x in vols]
                self.assertIn(vol_name, volnames)
                self.assertEqual(1, len(rc.model.model['spec']['containers']))

                mounts = rc.model.model['spec']['containers'][0]['volumeMounts']
                mountnames = [x['name'] for x in mounts]
                self.assertIn(vol_name, mountnames)
                self.assertEqual(1, len(rc.model.pod_spec.model['containers']))

                mounts = rc.model.pod_spec.model['containers'][0]['volumeMounts']
                mountnames = [x['name'] for x in mounts]
                self.assertIn(vol_name, mountnames)

            except Exception as err:
                self.assertIsInstance(err, TimedOutException)