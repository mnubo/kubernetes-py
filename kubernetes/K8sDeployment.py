#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sPodBasedObject import K8sPodBasedObject
from kubernetes.models.v1.Deployment import Deployment


class K8sDeployment(K8sPodBasedObject):

    def __init__(self, config=None, name=None, image=None, replicas=0):
        K8sPodBasedObject.__init__(self, config=config, obj_type='Deployment', name=name)
        self.model = Deployment(name=name, namespace=self.config.namespace)
        self.set_replicas(replicas)

    def set_replicas(self, replicas=None):
        self.model.set_replicas(replicas=replicas)
        return self

    # -------------------------------------------------------------------------------------  override

    def create(self):
        super(K8sDeployment, self).create()
        self.get()
        return self

    def update(self):
        super(K8sDeployment, self).update()
        self.get()
        return self

    # -------------------------------------------------------------------------------------  get

    def get(self):
        self.model = Deployment(model=self.get_model())
        return self

