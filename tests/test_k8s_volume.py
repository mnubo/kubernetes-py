#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import uuid

from tests import utils
from tests.BaseTest import BaseTest
from kubernetes.K8sExceptions import TimedOutException
from kubernetes.K8sPod import K8sPod
from kubernetes.K8sReplicationController import K8sReplicationController
from kubernetes.K8sVolume import K8sVolume
from kubernetes.K8sVolumeMount import K8sVolumeMount
from kubernetes.models.v1.AWSElasticBlockStoreVolumeSource import AWSElasticBlockStoreVolumeSource
from kubernetes.models.v1.EmptyDirVolumeSource import EmptyDirVolumeSource
from kubernetes.models.v1.GCEPersistentDiskVolumeSource import GCEPersistentDiskVolumeSource
from kubernetes.models.v1.GitRepoVolumeSource import GitRepoVolumeSource
from kubernetes.models.v1.HostPathVolumeSource import HostPathVolumeSource
from kubernetes.models.v1.NFSVolumeSource import NFSVolumeSource
from kubernetes.models.v1.SecretVolumeSource import SecretVolumeSource


class K8sVolumeTest(BaseTest):

    def setUp(self):
        K8sPod.POD_READY_TIMEOUT_SECONDS = 20
        K8sReplicationController.SCALE_WAIT_TIMEOUT_SECONDS = 20
        utils.cleanup_rc()
        utils.cleanup_pods()
        utils.cleanup_secrets()

    def tearDown(self):
        utils.cleanup_rc()
        utils.cleanup_pods()
        utils.cleanup_secrets()

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

    # --------------------------------------------------------------------------------- emptyDir

    def test_init_empty_dir(self):
        name = "yoname"
        type = 'emptyDir'
        vol = K8sVolume(name=name, type=type)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual(type, vol.type)
        self.assertIsInstance(vol.source, EmptyDirVolumeSource)

    def test_emptydir_set_medium_invalid_type(self):
        name = "yoname"
        type = "hostPath"
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(NotImplementedError):
            vol.medium = None

    def test_emptydir_set_medium_invalid(self):
        name = "yoname"
        type = "emptyDir"
        medium = "yomedium"
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(SyntaxError):
            vol.medium = medium

    def test_emptydir_set_medium_none(self):
        name = "yoname"
        type = "emptyDir"
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(SyntaxError):
            vol.medium = None

    def test_emptydir_set_medium_emptystring(self):
        name = "yoname"
        type = "emptyDir"
        vol = K8sVolume(name=name, type=type)
        vol.medium = ''
        self.assertEqual('', vol.medium)

    def test_emptydir_set_medium_memory(self):
        name = "yoname"
        type = "emptyDir"
        medium = "Memory"
        vol = K8sVolume(name=name, type=type)
        vol.medium = medium
        self.assertEqual(medium, vol.medium)

    # --------------------------------------------------------------------------------- hostPath

    def test_init_host_path(self):
        name = "yoname"
        type = 'hostPath'
        vol = K8sVolume(name=name, type=type)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual('hostPath', vol.type)
        self.assertIsInstance(vol.source, HostPathVolumeSource)

    def test_hostpath_set_path_invalid_type(self):
        name = "yoname"
        type = "emptyDir"
        host_path = "/path/on/host"
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(NotImplementedError):
            vol.path = host_path

    def test_hostpath_set_path_none(self):
        name = "yoname"
        type = "hostPath"
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(SyntaxError):
            vol.path = None

    def test_hostpath_set_path(self):
        name = "yoname"
        type = "hostPath"
        host_path = "/path/on/host"
        vol = K8sVolume(name=name, type=type)
        vol.path = host_path
        self.assertEqual(host_path, vol.path)

    # --------------------------------------------------------------------------------- secret

    def test_init_secret(self):
        name = "yoname"
        type = "secret"
        vol = K8sVolume(name=name, type=type)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual(type, vol.type)
        self.assertIsInstance(vol.source, SecretVolumeSource)

    def test_secret_set_name_invalid_type(self):
        name = "yoname"
        type = "emptyDir"
        secret_name = "yosecret"
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(NotImplementedError):
            vol.secret_name = secret_name

    def test_secret_set_name_invalid_obj(self):
        name = "yoname"
        type = "secret"
        secret = object()
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(SyntaxError):
            vol.secret_name = secret

    def test_secret_set_name(self):
        name = "yoname"
        type = "secret"
        secret_name = "yosecret"
        vol = K8sVolume(name=name, type=type)
        vol.secret_name = secret_name
        self.assertEqual(vol.secret_name, secret_name)

    # --------------------------------------------------------------------------------- awsElasticBlockStore

    def test_aws_init(self):
        name = "yoname"
        type = "awsElasticBlockStore"
        vol = K8sVolume(name=name, type=type)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual(type, vol.type)
        self.assertIsInstance(vol.source, AWSElasticBlockStoreVolumeSource)

    def test_aws_set_volume_id_invalid_obj(self):
        name = "yoname"
        type = "awsElasticBlockStore"
        volume_id = object()
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(SyntaxError):
            vol.volume_id = volume_id

    def test_aws_set_volume_id_none(self):
        name = "yoname"
        type = "awsElasticBlockStore"
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(SyntaxError):
            vol.volume_id = None

    def test_aws_set_volume_id_invalid_type(self):
        name = "yoname"
        type = "emptyDir"
        volume_id = "vol-0a89c9040d544a371"
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(NotImplementedError):
            vol.volume_id = volume_id

    def test_aws_set_volume_id(self):
        name = "yoname"
        type = "awsElasticBlockStore"
        volume_id = "vol-0a89c9040d544a371"
        vol = K8sVolume(name=name, type=type)
        vol.volume_id = volume_id
        self.assertEqual(vol.volume_id, volume_id)

    # --------------------------------------------------------------------------------- gcePersistentDisk

    def test_gce_init(self):
        name = "yoname"
        type = "gcePersistentDisk"
        vol = K8sVolume(name=name, type=type)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual(type, vol.type)
        self.assertIsInstance(vol.source, GCEPersistentDiskVolumeSource)

    def test_gce_set_pd_name_none(self):
        name = "yoname"
        type = "gcePersistentDisk"
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(SyntaxError):
            vol.pd_name = None

    def test_gce_set_pd_name_invalid_obj(self):
        name = "yoname"
        type = "gcePersistentDisk"
        pd_name = object()
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(SyntaxError):
            vol.pd_name = pd_name

    def test_gce_set_pd_name_invalid_type(self):
        name = "yoname"
        type = "emptyDir"
        pd_name = "yopdname"
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(NotImplementedError):
            vol.pd_name = pd_name

    def test_gce_set_pd_name(self):
        name = "yoname"
        type = "gcePersistentDisk"
        pd_name = "vol-0a89c9040d544a371"
        vol = K8sVolume(name=name, type=type)
        vol.pd_name = pd_name
        self.assertEqual(vol.pd_name, pd_name)

    # --------------------------------------------------------------------------------- AWS & GCE - fs_type

    def test_aws_set_fs_type_none(self):
        name = "yoname"
        type = "awsElasticBlockStore"
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(SyntaxError):
            vol.fs_type = None

    def test_gce_set_fs_type_none(self):
        name = "yoname"
        type = "gcePersistentDisk"
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(SyntaxError):
            vol.fs_type = None

    def test_aws_fs_type_invalid_obj(self):
        name = "yoname"
        type = "awsElasticBlockStore"
        fs_type = object()
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(SyntaxError):
            vol.fs_type = fs_type

    def test_gce_fs_type_invalid_obj(self):
        name = "yoname"
        type = "gcePersistentDisk"
        fs_type = object()
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(SyntaxError):
            vol.fs_type = fs_type

    def test_fs_type_invalid_type(self):
        name = "yoname"
        type = "emptyDir"
        fs_type = object()
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(NotImplementedError):
            vol.fs_type = fs_type

    def test_aws_set_fs_type(self):
        name = "yoname"
        type = "awsElasticBlockStore"
        fs_type = "xfs"
        vol = K8sVolume(name=name, type=type)
        vol.fs_type = fs_type
        self.assertEqual(vol.fs_type, fs_type)

    def test_gce_set_fs_type(self):
        name = "yoname"
        type = "gcePersistentDisk"
        fs_type = "xfs"
        vol = K8sVolume(name=name, type=type)
        vol.fs_type = fs_type
        self.assertEqual(vol.fs_type, fs_type)

    # --------------------------------------------------------------------------------- nfs

    def test_nfs_init(self):
        name = "yoname"
        type = "nfs"
        vol = K8sVolume(name=name, type=type)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual(type, vol.type)
        self.assertIsInstance(vol.source, NFSVolumeSource)

    def test_nfs_set_server_none(self):
        name = "yoname"
        type = "nfs"
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(SyntaxError):
            vol.nfs_server = None

    def test_nfs_set_server_invalid(self):
        name = "yoname"
        type = "nfs"
        server = object()
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(SyntaxError):
            vol.nfs_server = server

    def test_nfs_set_server_invalid_type(self):
        name = "yoname"
        type = "emptyDir"
        server = "nfs.company.com"
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(NotImplementedError):
            vol.nfs_server = server

    def test_nfs_set_server(self):
        name = "yoname"
        type = "nfs"
        server = "nfs.company.com"
        vol = K8sVolume(name=name, type=type)
        vol.nfs_server = server
        self.assertEqual(vol.nfs_server, server)

    # --------------------------------------------------------------------------------- repository (gitRepo)

    def test_git_repo_init(self):
        name = "yoname"
        type = "gitRepo"
        vol = K8sVolume(name=name, type=type)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sVolume)
        self.assertEqual(type, vol.type)
        self.assertIsInstance(vol.source, GitRepoVolumeSource)

    def test_git_repo_set_repo_none(self):
        name = "yoname"
        type = "gitRepo"
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(SyntaxError):
            vol.git_repository = None

    def test_git_repo_set_repo_invalid(self):
        name = "yoname"
        type = "gitRepo"
        repo = object()
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(SyntaxError):
            vol.git_repository = repo

    def test_git_set_repo_invalid_type(self):
        name = "yoname"
        type = "emptyDir"
        repo = "git@somewhere:me/my-git-repository.git"
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(NotImplementedError):
            vol.git_repository = repo

    def test_git_set_repo(self):
        name = "yoname"
        type = "gitRepo"
        repo = "git@somewhere:me/my-git-repository.git"
        vol = K8sVolume(name=name, type=type)
        vol.git_repository = repo
        self.assertEqual(vol.git_repository, repo)

    # --------------------------------------------------------------------------------- revision (gitRepo)

    def test_git_set_revision_none(self):
        name = "yoname"
        type = "gitRepo"
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(SyntaxError):
            vol.git_revision = None

    def test_git_set_revision_invalid(self):
        name = "yoname"
        type = "gitRepo"
        rev = object()
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(SyntaxError):
            vol.git_revision = rev

    def test_git_set_revision_invalid_type(self):
        name = "yoname"
        type = "emptyDir"
        rev = "22f1d8406d464b0c0874075539c1f2e96c253775"
        vol = K8sVolume(name=name, type=type)
        with self.assertRaises(NotImplementedError):
            vol.git_revision = rev

    def test_git_set_revision(self):
        name = "yoname"
        type = "gitRepo"
        rev = "22f1d8406d464b0c0874075539c1f2e96c253775"
        vol = K8sVolume(name=name, type=type)
        vol.git_revision = rev
        self.assertEqual(vol.git_revision, rev)

    # --------------------------------------------------------------------------------- api - pod - emptydir

    def test_pod_emptydir(self):
        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container = utils.create_container(name=container_name, image=container_image)

        vol_name = "emptydir"
        vol_type = "emptyDir"
        volume = utils.create_volume(name=vol_name, type=vol_type)

        mount_name = vol_name
        mount_path = '/test-emptydir'
        mount = K8sVolumeMount(name=mount_name, mount_path=mount_path)
        container.add_volume_mount(mount)

        pod_name = "nginx"
        pod = utils.create_pod(name=pod_name)
        pod.add_volume(volume)
        pod.add_container(container)

        if utils.is_reachable(pod.config):
            pod.create()
            volnames = [x.name for x in pod.volumes]
            self.assertIn(vol_name, volnames)

    # --------------------------------------------------------------------------------- api - pod - hostpath

    def test_pod_hostpath(self):
        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container = utils.create_container(name=container_name, image=container_image)

        vol_name = "hostpath"
        vol_type = "hostPath"
        host_path = "/var/lib/docker"
        volume = utils.create_volume(name=vol_name, type=vol_type)
        volume.path = host_path

        mount_name = vol_name
        mount_path = '/test-hostpath'
        mount = K8sVolumeMount(name=mount_name, mount_path=mount_path)
        container.add_volume_mount(mount)

        pod_name = "nginx"
        pod = utils.create_pod(name=pod_name)
        pod.add_volume(volume)
        pod.add_container(container)

        if utils.is_reachable(pod.config):
            pod.create()
            volnames = [x.name for x in pod.volumes]
            self.assertIn(vol_name, volnames)

    # --------------------------------------------------------------------------------- api - pod - secret

    def test_pod_secret(self):
        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container = utils.create_container(name=container_name, image=container_image)

        secret_name = "yosecret"
        secret = utils.create_secret(name=secret_name)
        k = ".secret-file"
        v = "dmFsdWUtMg0KDQo="
        secret.data = {k: v}

        vol_name = "secret"
        vol_type = "secret"
        volume = utils.create_volume(name=vol_name, type=vol_type)
        volume.secret_name = secret_name

        mount_name = vol_name
        mount_path = '/test-secret'
        mount = K8sVolumeMount(name=mount_name, mount_path=mount_path)
        container.add_volume_mount(mount)

        pod_name = "nginx"
        pod = utils.create_pod(name=pod_name)
        pod.add_volume(volume)
        pod.add_container(container)

        if utils.is_reachable(pod.config):
            secret.create()
            pod.create()
            volnames = [x.name for x in pod.volumes]
            self.assertIn(vol_name, volnames)

    # --------------------------------------------------------------------------------- api - pod - aws ebs

    def test_pod_aws_ebs(self):
        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container = utils.create_container(name=container_name, image=container_image)

        volume_id = "vol-0e3056a2"
        vol_name = "ebs"
        vol_type = "awsElasticBlockStore"
        volume = utils.create_volume(name=vol_name, type=vol_type)
        volume.volume_id = volume_id

        mount_name = vol_name
        mount_path = '/test-aws'
        mount = K8sVolumeMount(name=mount_name, mount_path=mount_path)
        container.add_volume_mount(mount)

        pod_name = "nginx-{0}".format(str(uuid.uuid4()))
        pod = utils.create_pod(name=pod_name)
        pod.add_volume(volume)
        pod.add_container(container)

        if utils.is_reachable(pod.config):
            try:
                pod.create()
                volnames = [x.name for x in pod.volumes]
                self.assertIn(vol_name, volnames)
            except Exception as err:
                self.assertIsInstance(err, TimedOutException)

    # --------------------------------------------------------------------------------- api - pod - gce pd

    def test_pod_gce_pd(self):
        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container = utils.create_container(name=container_name, image=container_image)

        pd_name = "kubernetes-py-test-pd"
        vol_name = "persistent"
        vol_type = "gcePersistentDisk"
        volume = utils.create_volume(name=vol_name, type=vol_type)
        volume.pd_name = pd_name

        mount_name = vol_name
        mount_path = '/test-gce'
        mount = K8sVolumeMount(name=mount_name, mount_path=mount_path)
        container.add_volume_mount(mount)

        pod_name = "nginx-{0}".format(str(uuid.uuid4()))
        pod = utils.create_pod(name=pod_name)
        pod.add_volume(volume)
        pod.add_container(container)

        if utils.is_reachable(pod.config):
            try:
                pod.create()
                volnames = [x.name for x in pod.volumes]
                self.assertIn(vol_name, volnames)
            except Exception as err:
                self.assertIsInstance(err, TimedOutException)

    # --------------------------------------------------------------------------------- api - pod - nfs

    def test_pod_nfs(self):
        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container = utils.create_container(name=container_name, image=container_image)

        vol_name = "nfs"
        vol_type = "nfs"
        server = "howard.mtl.mnubo.com"
        nfs_path = "/fs1/test-nfs"
        volume = utils.create_volume(name=vol_name, type=vol_type)
        volume.nfs_server = server
        volume.nfs_path = nfs_path

        mount_name = vol_name
        mount_path = '/test-nfs'
        mount = K8sVolumeMount(name=mount_name, mount_path=mount_path)
        container.add_volume_mount(mount)

        pod_name = "nginx-{0}".format(str(uuid.uuid4()))
        pod = utils.create_pod(name=pod_name)
        pod.add_volume(volume)
        pod.add_container(container)

        if utils.is_reachable(pod.config):
            try:
                pod.create()
                volnames = [x.name for x in pod.volumes]
                self.assertIn(vol_name, volnames)
            except Exception as err:
                self.assertIsInstance(err, TimedOutException)

    # --------------------------------------------------------------------------------- api - pod - gitRepo

    def test_pod_git_repo(self):
        container_name = "nginx"
        container_image = "nginx:1.7.9"
        container = utils.create_container(name=container_name, image=container_image)

        vol_name = "git-repo"
        vol_type = "gitRepo"
        repo = "https://user:pass@somewhere/repo.git"
        revision = "e42d3dca1541ba085f34ce282feda1109a707c7b"
        volume = utils.create_volume(name=vol_name, type=vol_type)
        volume.git_repository = repo
        volume.git_revision = revision

        mount_name = vol_name
        mount_path = '/test-git'
        mount = K8sVolumeMount(name=mount_name, mount_path=mount_path)
        container.add_volume_mount(mount)

        pod_name = "nginx-{0}".format(str(uuid.uuid4()))
        pod = utils.create_pod(name=pod_name)
        pod.add_volume(volume)
        pod.add_container(container)

        if utils.is_reachable(pod.config):
            try:
                pod.create()
                volnames = [x.name for x in pod.volumes]
                self.assertIn(vol_name, volnames)
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
        volume = utils.create_volume(name=vol_name, type=vol_type)

        mount_name = vol_name
        mount_path = '/test-emptydir'
        mount = K8sVolumeMount(name=mount_name, mount_path=mount_path)
        container_nginx.add_volume_mount(mount)
        container_redis.add_volume_mount(mount)

        rc_name = "app"
        rc = utils.create_rc(name=rc_name)
        rc.add_volume(volume)
        rc.add_container(container_nginx)
        rc.add_container(container_redis)
        rc.desired_replicas = 1

        if utils.is_reachable(rc.config):
            rc.create()
            volnames = [x.name for x in rc.volumes]
            self.assertIn(vol_name, volnames)

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
        hostpath = "/var/lib/docker"
        volume = utils.create_volume(name=vol_name, type=vol_type)
        volume.path = hostpath

        mount_name = vol_name
        mount_path = '/test-hostpath'
        mount = K8sVolumeMount(name=mount_name, mount_path=mount_path)
        container_nginx.add_volume_mount(mount)
        container_redis.add_volume_mount(mount)

        rc_name = "app"
        rc = utils.create_rc(name=rc_name)
        rc.add_volume(volume)
        rc.add_container(container_nginx)
        rc.add_container(container_redis)
        rc.desired_replicas = 1

        if utils.is_reachable(rc.config):
            rc.create()
            volnames = [x.name for x in rc.volumes]
            self.assertIn(vol_name, volnames)

    def test_rc_hostpath_list(self):
        volumes = [
            {'hostPath': {'path': '/root/.dockercfg'}, 'name': 'dockercred'},
            {'hostPath': {'path': '/usr/bin/docker'}, 'name': 'dockerbin'},
            {'hostPath': {'path': '/var/run/docker.sock'}, 'name': 'dockersock'},
            {'hostPath': {'path': '/root/.docker'}, 'name': 'dockerconfig'}
        ]
        rc = utils.create_rc(name="admintool")

        for vol in volumes:
            keys = list(filter(lambda x: x != 'name', vol.keys()))
            v = K8sVolume(
                name=vol['name'],
                type=keys[0],
            )
            dico = vol[keys[0]]
            if dico is not None:
                v.path = dico['path']
            rc.add_volume(v)

        self.assertEqual(len(volumes), len(rc.volumes))
        for i in range(0, len(volumes)):
            self.assertEqual(volumes[i]['name'], rc.volumes[i].name)
            self.assertEqual(volumes[i]['hostPath']['path'], rc.volumes[i].hostPath.path)

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
        secret.data = {k: v}

        vol_name = "secret"
        vol_type = "secret"
        volume = utils.create_volume(name=vol_name, type=vol_type)
        volume.secret_name = secret_name

        mount_name = vol_name
        mount_path = '/test-secret'
        mount = K8sVolumeMount(name=mount_name, mount_path=mount_path)
        container_nginx.add_volume_mount(mount)
        container_redis.add_volume_mount(mount)

        rc_name = "app"
        rc = utils.create_rc(name=rc_name)
        rc.add_volume(volume)
        rc.add_container(container_nginx)
        rc.add_container(container_redis)
        rc.desired_replicas = 1

        if utils.is_reachable(rc.config):
            secret.create()
            rc.create()
            volnames = [x.name for x in rc.volumes]
            self.assertIn(vol_name, volnames)

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
        volume = utils.create_volume(name=vol_name, type=vol_type)
        volume.volume_id = volume_id

        mount_name = vol_name
        mount_path = '/test-aws'
        mount = K8sVolumeMount(name=mount_name, mount_path=mount_path)
        container_nginx.add_volume_mount(mount)
        container_redis.add_volume_mount(mount)

        rc_name = "nginx-{0}".format(str(uuid.uuid4()))
        rc = utils.create_rc(name=rc_name)
        rc.add_volume(volume)
        rc.add_container(container_nginx)
        rc.add_container(container_redis)
        rc.desired_replicas = 3

        if utils.is_reachable(rc.config):
            try:
                rc.create()
                volnames = [x.name for x in rc.volumes]
                self.assertIn(vol_name, volnames)
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

        pd_name = "mnubo-disk1"
        vol_name = "persistent"
        vol_type = "gcePersistentDisk"
        volume = utils.create_volume(name=vol_name, type=vol_type)
        volume.pd_name = pd_name
        volume.read_only = True  # HTTP 422: GCE PD can only be mounted on multiple machines if it is read-only

        mount_name = vol_name
        mount_path = '/test-gce'
        mount = K8sVolumeMount(name=mount_name, mount_path=mount_path)
        container_nginx.add_volume_mount(mount)
        container_redis.add_volume_mount(mount)

        rc_name = "nginx-{0}".format(str(uuid.uuid4()))
        rc = utils.create_rc(name=rc_name)
        rc.add_volume(volume)
        rc.add_container(container_nginx)
        rc.add_container(container_redis)
        rc.desired_replicas = 3

        if utils.is_reachable(rc.config):
            try:
                rc.create()
                volnames = [x.name for x in rc.volumes]
                self.assertIn(vol_name, volnames)
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
        server = "howard.mtl.mnubo.com"
        path = "/fs1/test-nfs"
        volume = utils.create_volume(name=vol_name, type=vol_type)
        volume.nfs_server = server
        volume.nfs_path = path

        mount_name = vol_name
        mount_path = '/test-nfs'
        mount = K8sVolumeMount(name=mount_name, mount_path=mount_path)
        container_nginx.add_volume_mount(mount)
        container_redis.add_volume_mount(mount)

        rc_name = "nginx-{0}".format(str(uuid.uuid4()))
        rc = utils.create_rc(name=rc_name)
        rc.add_volume(volume)
        rc.add_container(container_nginx)
        rc.add_container(container_redis)
        rc.desired_replicas = 3

        if utils.is_reachable(rc.config):
            try:
                rc.create()
                volnames = [x.name for x in rc.volumes]
                self.assertIn(vol_name, volnames)
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
        repo = "https://user:pass@somewhere/repo.git"
        revision = "e42d3dca1541ba085f34ce282feda1109a707c7b"
        volume = utils.create_volume(name=vol_name, type=vol_type)
        volume.git_repository = repo
        volume.git_revision = revision

        mount_name = vol_name
        mount_path = '/test-git'
        mount = K8sVolumeMount(name=mount_name, mount_path=mount_path)
        container_nginx.add_volume_mount(mount)
        container_redis.add_volume_mount(mount)

        rc_name = "nginx-{0}".format(str(uuid.uuid4()))
        rc = utils.create_rc(name=rc_name)
        rc.add_volume(volume)
        rc.add_container(container_nginx)
        rc.add_container(container_redis)
        rc.desired_replicas = 3

        if utils.is_reachable(rc.config):
            try:
                rc.create()
                volnames = [x.name for x in rc.volumes]
                self.assertIn(vol_name, volnames)
            except Exception as err:
                self.assertIsInstance(err, TimedOutException)
