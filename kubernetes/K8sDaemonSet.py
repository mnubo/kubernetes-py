#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1beta1.DaemonSet import DaemonSet


class K8sDaemonSet(K8sObject):

    def __init__(self, config=None, name=None):

        super(K8sDaemonSet, self).__init__(
            config=config,
            name=name,
            obj_type='DaemonSet'
        )

    # -------------------------------------------------------------------------------------  override

    def create(self):
        super(K8sDaemonSet, self).create()
        self.get()
        return self

    def update(self):
        super(K8sDaemonSet, self).update()
        self.get()
        return self

    # -------------------------------------------------------------------------------------  get

    def get(self):
        self.model = DaemonSet(self.get_model())
        return self
