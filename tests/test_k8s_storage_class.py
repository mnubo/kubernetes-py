#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from tests import _utils
from tests.BaseTest import BaseTest
from kubernetes_py.K8sStorageClass import K8sStorageClass
from kubernetes_py.models.v1beta1.StorageClass import StorageClass


class K8sStorageClassTests(BaseTest):
    def setUp(self):
        _utils.cleanup_storage_class()

    def tearDown(self):
        _utils.cleanup_storage_class()

    def test_gce_pd(self):
        json = {
            "kind": "StorageClass",
            "apiVersion": "storage.k8s.io/v1beta1",
            "metadata": {"name": "slow"},
            "provisioner": "kubernetes.io/gce-pd",
            "parameters": {"type": "pd-standard",},
        }

        sc = StorageClass(json)
        k8s_sc = _utils.create_storage_class(name="sc")
        k8s_sc.model = sc

        if _utils.is_reachable(k8s_sc.config):
            k8s_sc.create()
            from_get = k8s_sc.get()
            self.assertIsInstance(from_get, K8sStorageClass)
