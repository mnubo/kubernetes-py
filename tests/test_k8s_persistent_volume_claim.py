#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
import uuid

from kubernetes.K8sExceptions import TimedOutException
from kubernetes.K8sPersistentVolume import K8sPersistentVolume
from kubernetes.K8sPersistentVolumeClaim import K8sPersistentVolumeClaim
from kubernetes.K8sPod import K8sPod
from kubernetes.models.v1.ResourceRequirements import ResourceRequirements
from tests import utils


class K8sPersistentVolumeClaimTest(unittest.TestCase):

    def setUp(self):
        K8sPod.POD_READY_TIMEOUT_SECONDS = 20
        utils.cleanup_pods()
        utils.cleanup_pvc()
        utils.cleanup_pv()

    def tearDown(self):
        utils.cleanup_pods()
        utils.cleanup_pvc()
        utils.cleanup_pv()

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        config = utils.create_config()
        with self.assertRaises(SyntaxError):
            K8sPersistentVolumeClaim(config=config)

    def test_init_invalid_name(self):
        name = object()
        config = utils.create_config()
        with self.assertRaises(SyntaxError):
            K8sPersistentVolumeClaim(config=config, name=name)

    def test_init(self):
        name = "yopvc123"
        claim = utils.create_pvc(name=name)
        self.assertIsInstance(claim, K8sPersistentVolumeClaim)
        self.assertEqual(claim.name, name)

    # --------------------------------------------------------------------------------- accessModes

    def test_access_modes_none(self):
        name = "yopvc-{}".format(str(uuid.uuid4()))
        claim = utils.create_pvc(name=name)
        with self.assertRaises(SyntaxError):
            claim.access_modes = None

    def test_access_modes_invalid(self):
        name = "yopvc-{}".format(str(uuid.uuid4()))
        claim = utils.create_pvc(name=name)
        with self.assertRaises(SyntaxError):
            claim.access_modes = object()
        modes = ['yomama']
        claim.access_modes = modes
        self.assertNotEqual(modes, claim.access_modes)

    def test_access_modes(self):
        name = "yopvc-{}".format(str(uuid.uuid4()))
        claim = utils.create_pvc(name=name)
        modes = ['ReadWriteMany']
        claim.access_modes = modes
        self.assertEqual(modes, claim.access_modes)

    # --------------------------------------------------------------------------------- resources

    def test_resources_none(self):
        name = "yopvc-{}".format(str(uuid.uuid4()))
        claim = utils.create_pvc(name=name)
        with self.assertRaises(SyntaxError):
            claim.resources = None

    def test_resources_invalid(self):
        name = "yopvc-{}".format(str(uuid.uuid4()))
        claim = utils.create_pvc(name=name)
        with self.assertRaises(SyntaxError):
            claim.resources = object()
        resources = {'cpu': '', 'memory': ''}
        claim.resources = resources
        self.assertNotEqual(resources, claim.resources)

    def test_resources(self):
        name = "yopvc-{}".format(str(uuid.uuid4()))
        claim = utils.create_pvc(name=name)
        resources = {'requests': {'storage': '100Gi'}}
        claim.resources = resources
        self.assertIsInstance(claim.resources, ResourceRequirements)
        self.assertEqual(resources, claim.resources.serialize())

    # --------------------------------------------------------------------------------- api - create

    def test_api_create_timeout(self):
        name = "yopvc-{}".format(str(uuid.uuid4()))
        claim = utils.create_pvc(name=name)
        if utils.is_reachable(claim.config.api_host):
            with self.assertRaises(TimedOutException):
                claim.create()

    def test_api_create_aws_ebs(self):
        pvname = "yopv"
        pvcname = "yopvc"
        volname = "yovolume"
        podname = "yopod"
        contname = "yocontainer"

        pvtype = "awsElasticBlockStore"
        pv = utils.create_pv(name=pvname, type=pvtype)
        pv.volume_id = "vol-0e3056a2"
        pv.fs_type = "xfs"

        pvc = utils.create_pvc(name=pvcname)

        vol = utils.create_volume(name=volname, type='persistentVolumeClaim')
        vol.claim_name = pvcname

        container = utils.create_container(name=contname, image="nginx:latest")
        volmount = utils.create_volume_mount(name=volname, mount_path='/test-persistent')
        container.add_volume_mount(volmount)

        pod = utils.create_pod(name=podname)
        pod.add_volume(vol)
        pod.add_container(container)

        if utils.is_reachable(pvc.config.api_host):
            try:
                pv.create()
                pvc.create()
                pod.create()
                self.assertIsInstance(pv, K8sPersistentVolume)
                self.assertIsInstance(pvc, K8sPersistentVolumeClaim)
            except Exception as err:
                self.assertIsInstance(err, TimedOutException)

    def test_api_create_gce_pd(self):
        pvname = "yopv"
        pvcname = "yopvc"
        volname = "yovolume"
        podname = "yopod"
        contname = "yocontainer"

        pvtype = "gcePersistentDisk"
        pv = utils.create_pv(name=pvname, type=pvtype)
        pv.pd_name = "mnubo-disk1"
        pv.fs_type = "xfs"

        pvc = utils.create_pvc(name=pvcname)

        vol = utils.create_volume(name=volname, type='persistentVolumeClaim')
        vol.claim_name = pvcname

        container = utils.create_container(name=contname, image="nginx:latest")
        volmount = utils.create_volume_mount(name=volname, mount_path='/test-persistent')
        container.add_volume_mount(volmount)

        pod = utils.create_pod(name=podname)
        pod.add_volume(vol)
        pod.add_container(container)

        if utils.is_reachable(pvc.config.api_host):
            try:
                pv.create()
                pvc.create()
                pod.create()
                self.assertIsInstance(pv, K8sPersistentVolume)
                self.assertIsInstance(pvc, K8sPersistentVolumeClaim)
            except Exception as err:
                self.assertIsInstance(err, TimedOutException)

    def test_api_create_nfs(self):
        pvname = "yopv"
        pvcname = "yopvc"
        volname = "yovolume"
        podname = "yopod"
        contname = "yocontainer"

        pvtype = "nfs"
        pv = utils.create_pv(name=pvname, type=pvtype)
        pv.nfs_server = "nfs.company.com"
        pv.nfs_path = "/fs1/test-nfs"

        pvc = utils.create_pvc(name=pvcname)

        vol = utils.create_volume(name=volname, type='persistentVolumeClaim')
        vol.claim_name = pvcname

        container = utils.create_container(name=contname, image="nginx:latest")
        volmount = utils.create_volume_mount(name=volname, mount_path='/test-persistent')
        container.add_volume_mount(volmount)

        pod = utils.create_pod(name=podname)
        pod.add_volume(vol)
        pod.add_container(container)

        if utils.is_reachable(pvc.config.api_host):
            try:
                pv.create()
                pvc.create()
                pod.create()
                self.assertIsInstance(pv, K8sPersistentVolume)
                self.assertIsInstance(pvc, K8sPersistentVolumeClaim)
            except Exception as err:
                self.assertIsInstance(err, TimedOutException)
