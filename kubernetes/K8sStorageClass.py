#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1beta1.StorageClass import StorageClass


class K8sStorageClass(K8sObject):
    def __init__(self, config=None, name=None):

        super(K8sStorageClass, self).__init__(
            config=config,
            name=name,
            obj_type='StorageClass'
        )

    # -------------------------------------------------------------------------------------  override

    def get(self):
        self.model = StorageClass(self.get_model())
        return self

    def create(self):
        super(K8sStorageClass, self).create()
        self.get()
        return self

    def update(self):
        super(K8sStorageClass, self).update()
        self.get()
        return self

    def list(self, pattern=None):
        ls = super(K8sStorageClass, self).list()
        sclasses = list(map(lambda x: StorageClass(x), ls))
        if pattern is not None:
            sclasses = list(filter(lambda x: pattern in x.name, sclasses))
        k8s = []
        for x in sclasses:
            j = K8sStorageClass(config=self.config, name=x.name)
            j.model = x
            k8s.append(j)
        return k8s
