#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import utils
from BaseTest import BaseTest
from kubernetes.K8sStorageClass import K8sStorageClass
from kubernetes.models.v1beta1.StorageClass import StorageClass


class K8sStorageClassTests(BaseTest):

    def setUp(self):
        utils.cleanup_storage_class()

    def tearDown(self):
        utils.cleanup_storage_class()

    def test_gce_pd(self):
        json = {
            "kind": "StorageClass",
            "apiVersion": "storage.k8s.io/v1beta1",
            "metadata": {
                "name": "slow"
            },
            "provisioner": "kubernetes.io/gce-pd",
            "parameters": {
                "type": "pd-standard",
            }
        }

        sc = StorageClass(json)
        k8s_sc = utils.create_storage_class(name='sc')
        k8s_sc.model = sc

        if utils.is_reachable(k8s_sc.config.api_host):
            k8s_sc.create()
            from_get = k8s_sc.get()
            self.assertIsInstance(from_get, K8sStorageClass)
