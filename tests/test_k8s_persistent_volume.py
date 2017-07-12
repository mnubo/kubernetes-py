#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sPersistentVolume import K8sPersistentVolume
from kubernetes.models.v1.AWSElasticBlockStoreVolumeSource import AWSElasticBlockStoreVolumeSource
from kubernetes.models.v1.GCEPersistentDiskVolumeSource import GCEPersistentDiskVolumeSource
from kubernetes.models.v1.HostPathVolumeSource import HostPathVolumeSource
from kubernetes.models.v1.NFSVolumeSource import NFSVolumeSource
from tests import _utils
from tests.BaseTest import BaseTest


class K8sPersistentVolumeTest(BaseTest):
    def setUp(self):
        _utils.cleanup_pv()

    def tearDown(self):
        _utils.cleanup_pv()

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        config = _utils.create_config()
        with self.assertRaises(SyntaxError):
            K8sPersistentVolume(config=config)

    def test_init_invalid_name(self):
        name = object()
        config = _utils.create_config()
        with self.assertRaises(SyntaxError):
            K8sPersistentVolume(config=config, name=name)

    def test_init_invalid_type(self):
        name = "yoname"
        _type = object()
        config = _utils.create_config()
        with self.assertRaises(SyntaxError):
            K8sPersistentVolume(config=config, name=name, type=_type)

    # --------------------------------------------------------------------------------- hostPath

    def test_init_host_path(self):
        name = "yoname"
        _type = 'hostPath'
        vol = _utils.create_pv(name=name, type=_type)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sPersistentVolume)
        self.assertEqual('hostPath', vol.type)
        self.assertIsInstance(vol.source, HostPathVolumeSource)

    def test_hostpath_set_path_invalid_type(self):
        name = "yoname"
        _type = "gcePersistentDisk"
        host_path = "/path/on/host"
        vol = _utils.create_pv(name=name, type=_type)
        with self.assertRaises(NotImplementedError):
            vol.path = host_path

    def test_hostpath_set_path_none(self):
        name = "yoname"
        _type = "hostPath"
        vol = _utils.create_pv(name=name, type=_type)
        with self.assertRaises(SyntaxError):
            vol.path = None

    def test_hostpath_set_path(self):
        name = "yoname"
        _type = "hostPath"
        host_path = "/path/on/host"
        vol = _utils.create_pv(name=name, type=_type)
        vol.path = host_path
        self.assertEqual(host_path, vol.path)

    # --------------------------------------------------------------------------------- api - hostpath

    def test_api_hostpath(self):
        name = "yoname"
        _type = "hostPath"
        host_path = "/path/on/host"
        vol = _utils.create_pv(name=name, type=_type)
        vol.path = host_path
        self.assertEqual(host_path, vol.path)

        if _utils.is_reachable(vol.config):
            vol.create()
            self.assertIsInstance(vol, K8sPersistentVolume)
            self.assertEqual(host_path, vol.path)

    # --------------------------------------------------------------------------------- gcePersistentDisk

    def test_gce_init(self):
        name = "yoname"
        _type = "gcePersistentDisk"
        vol = _utils.create_pv(name=name, type=_type)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sPersistentVolume)
        self.assertEqual(_type, vol.type)
        self.assertIsInstance(vol.source, GCEPersistentDiskVolumeSource)

    def test_gce_set_pd_name_none(self):
        name = "yoname"
        _type = "gcePersistentDisk"
        vol = _utils.create_pv(name=name, type=_type)
        with self.assertRaises(SyntaxError):
            vol.pd_name = None

    def test_gce_set_pd_name_invalid_obj(self):
        name = "yoname"
        _type = "gcePersistentDisk"
        pd_name = object()
        vol = _utils.create_pv(name=name, type=_type)
        with self.assertRaises(SyntaxError):
            vol.pd_name = pd_name

    def test_gce_set_pd_name_invalid_type(self):
        name = "yoname"
        _type = "hostPath"
        pd_name = "yopdname"
        vol = _utils.create_pv(name=name, type=_type)
        with self.assertRaises(NotImplementedError):
            vol.pd_name = pd_name

    def test_gce_set_pd_name(self):
        name = "yoname"
        _type = "gcePersistentDisk"
        pd_name = "vol-0a89c9040d544a371"
        vol = _utils.create_pv(name=name, type=_type)
        vol.pd_name = pd_name
        self.assertEqual(vol.pd_name, pd_name)

    # --------------------------------------------------------------------------------- GCE - fs_type

    def test_gce_set_fs_type_none(self):
        name = "yoname"
        _type = "gcePersistentDisk"
        vol = _utils.create_pv(name=name, type=_type)
        with self.assertRaises(SyntaxError):
            vol.fs_type = None

    def test_gce_fs_type_invalid_obj(self):
        name = "yoname"
        _type = "gcePersistentDisk"
        fs_type = object()
        vol = _utils.create_pv(name=name, type=_type)
        with self.assertRaises(SyntaxError):
            vol.fs_type = fs_type

    def test_fs_type_invalid_type(self):
        name = "yoname"
        _type = "hostPath"
        fs_type = object()
        vol = _utils.create_pv(name=name, type=_type)
        with self.assertRaises(NotImplementedError):
            vol.fs_type = fs_type

    def test_gce_set_fs_type(self):
        name = "yoname"
        _type = "gcePersistentDisk"
        fs_type = "xfs"
        vol = _utils.create_pv(name=name, type=_type)
        vol.fs_type = fs_type
        self.assertEqual(vol.fs_type, fs_type)

    # --------------------------------------------------------------------------------- api - gce pd

    def test_api_gce_pd(self):
        name = "yoname"
        _type = "gcePersistentDisk"
        pd_name = "mnubo-disk1"
        fs_type = 'xfs'
        vol = _utils.create_pv(name=name, type=_type)
        vol.pd_name = pd_name
        vol.fs_type = fs_type

        if _utils.is_reachable(vol.config):
            vol.create()
            self.assertIsInstance(vol, K8sPersistentVolume)
            self.assertEqual(vol.pd_name, pd_name)
            self.assertEqual(vol.fs_type, fs_type)

    # --------------------------------------------------------------------------------- awsElasticBlockStore

    def test_aws_init(self):
        name = "yoname"
        _type = "awsElasticBlockStore"
        vol = _utils.create_pv(name=name, type=_type)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sPersistentVolume)
        self.assertEqual(_type, vol.type)
        self.assertIsInstance(vol.source, AWSElasticBlockStoreVolumeSource)

    def test_aws_set_volume_id_invalid_obj(self):
        name = "yoname"
        _type = "awsElasticBlockStore"
        volume_id = object()
        vol = _utils.create_pv(name=name, type=_type)
        with self.assertRaises(SyntaxError):
            vol.volume_id = volume_id

    def test_aws_set_volume_id_none(self):
        name = "yoname"
        _type = "awsElasticBlockStore"
        vol = _utils.create_pv(name=name, type=_type)
        with self.assertRaises(SyntaxError):
            vol.volume_id = None

    def test_aws_set_volume_id_invalid_type(self):
        name = "yoname"
        _type = "hostPath"
        volume_id = "vol-0a89c9040d544a371"
        vol = _utils.create_pv(name=name, type=_type)
        with self.assertRaises(NotImplementedError):
            vol.volume_id = volume_id

    def test_aws_set_volume_id(self):
        name = "yoname"
        _type = "awsElasticBlockStore"
        volume_id = "vol-0a89c9040d544a371"
        vol = _utils.create_pv(name=name, type=_type)
        vol.volume_id = volume_id
        self.assertEqual(vol.volume_id, volume_id)

    # --------------------------------------------------------------------------------- AWS - fs_type

    def test_aws_set_fs_type_none(self):
        name = "yoname"
        _type = "awsElasticBlockStore"
        vol = _utils.create_pv(name=name, type=_type)
        with self.assertRaises(SyntaxError):
            vol.fs_type = None

    def test_aws_fs_type_invalid_obj(self):
        name = "yoname"
        _type = "awsElasticBlockStore"
        fs_type = object()
        vol = _utils.create_pv(name=name, type=_type)
        with self.assertRaises(SyntaxError):
            vol.fs_type = fs_type

    def test_aws_set_fs_type(self):
        name = "yoname"
        _type = "awsElasticBlockStore"
        fs_type = "xfs"
        vol = _utils.create_pv(name=name, type=_type)
        vol.fs_type = fs_type
        self.assertEqual(vol.fs_type, fs_type)

    # --------------------------------------------------------------------------------- api - aws ebs

    def test_api_aws_ebs(self):
        name = "yoname"
        _type = "awsElasticBlockStore"
        volume_id = "vol-0e3056a2"
        fs_type = 'xfs'
        vol = _utils.create_pv(name=name, type=_type)
        vol.volume_id = volume_id
        vol.fs_type = fs_type

        if _utils.is_reachable(vol.config):
            vol.create()
            self.assertIsInstance(vol, K8sPersistentVolume)
            self.assertEqual(vol.volume_id, volume_id)
            self.assertEqual(vol.fs_type, fs_type)

    # --------------------------------------------------------------------------------- nfs

    def test_nfs_init(self):
        name = "yoname"
        _type = "nfs"
        vol = _utils.create_pv(name=name, type=_type)
        self.assertIsNotNone(vol)
        self.assertIsInstance(vol, K8sPersistentVolume)
        self.assertEqual(_type, vol.type)
        self.assertIsInstance(vol.source, NFSVolumeSource)

    def test_nfs_set_server_none(self):
        name = "yoname"
        _type = "nfs"
        vol = _utils.create_pv(name=name, type=_type)
        with self.assertRaises(SyntaxError):
            vol.nfs_server = None

    def test_nfs_set_server_invalid(self):
        name = "yoname"
        _type = "nfs"
        server = object()
        vol = _utils.create_pv(name=name, type=_type)
        with self.assertRaises(SyntaxError):
            vol.nfs_server = server

    def test_nfs_set_server_invalid_type(self):
        name = "yoname"
        _type = "hostPath"
        server = "nfs.company.com"
        vol = _utils.create_pv(name=name, type=_type)
        with self.assertRaises(NotImplementedError):
            vol.nfs_server = server

    def test_nfs_set_server(self):
        name = "yoname"
        _type = "nfs"
        server = "nfs.company.com"
        vol = _utils.create_pv(name=name, type=_type)
        vol.nfs_server = server
        self.assertEqual(vol.nfs_server, server)

    # --------------------------------------------------------------------------------- api - nfs

    def test_api_nfs(self):
        name = "yoname"
        _type = "nfs"
        server = "nfs.company.com"
        path = "/some/path"
        vol = _utils.create_pv(name=name, type=_type)
        vol.nfs_server = server
        vol.nfs_path = path

        if _utils.is_reachable(vol.config):
            vol.create()
            self.assertIsInstance(vol, K8sPersistentVolume)
            self.assertEqual(vol.nfs_server, server)
            self.assertEqual(vol.nfs_path, path)

    # --------------------------------------------------------------------------------- api - list

    def test_list(self):
        name = "yoname"
        _type = "gcePersistentDisk"
        pd_name = "mnubo-disk1"
        fs_type = 'xfs'
        vol = _utils.create_pv(name=name, type=_type)
        vol.pd_name = pd_name
        vol.fs_type = fs_type

        if _utils.is_reachable(vol.config):
            vol.create()
            _list = vol.list()
            for x in _list:
                self.assertIsInstance(x, K8sPersistentVolume)
