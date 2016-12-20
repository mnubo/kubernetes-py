#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1.ServiceAccount import ServiceAccount


class K8sServiceAccount(K8sObject):

    def __init__(self, config=None, name=None):
        super(K8sServiceAccount, self).__init__(
            config=config,
            name=name,
            obj_type='ServiceAccount'
        )

    # -------------------------------------------------------------------------------------  override

    def get(self):
        self.model = ServiceAccount(model=self.get_model())
        return self

    def create(self):
        super(K8sServiceAccount, self).create()
        self.get()
        return self

    def update(self):
        super(K8sServiceAccount, self).update()
        self.get()
        return self
