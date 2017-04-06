#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1beta1.HorizontalPodAutoscaler import HorizontalPodAutoscaler


class K8sHorizontalPodAutoscaler(K8sObject):

    def __init__(self, config=None, name=None):

        super(K8sHorizontalPodAutoscaler, self).__init__(
            config=config,
            obj_type='HorizontalPodAutoscaler',
            name=name
        )

    # -------------------------------------------------------------------------------------  override

    def create(self):
        super(K8sHorizontalPodAutoscaler, self).create()
        self.get()
        return self

    def update(self):
        super(K8sHorizontalPodAutoscaler, self).update()
        self.get()
        return self

    def list(self, pattern=None):
        ls = super(K8sHorizontalPodAutoscaler, self).list()
        hpas = list(map(lambda x: HorizontalPodAutoscaler(x), ls))
        if pattern is not None:
            hpas = list(filter(lambda x: pattern in x.name, hpas))
        k8s = []
        for x in hpas:
            z = K8sHorizontalPodAutoscaler(config=self.config, name=x.name)
            z.model = x
            k8s.append(z)
        return k8s

    # ------------------------------------------------------------------------------------- get

    def get(self):
        self.model = HorizontalPodAutoscaler(self.get_model())
        return self
