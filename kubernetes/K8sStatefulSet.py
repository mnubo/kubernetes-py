#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1beta1.StatefulSet import StatefulSet


class K8sStatefulSet(K8sObject):
    """
    https://kubernetes.io/docs/api-reference/apps/v1beta1/definitions/#_v1beta1_statefulset
    """

    def __init__(self, config=None, name=None):
        super(K8sStatefulSet, self).__init__(
            config=config,
            name=name,
            obj_type='StatefulSet'
        )

    # -------------------------------------------------------------------------------------  override

    def get(self):
        self.model = StatefulSet(self.get_model())
        return self

    def create(self):
        super(K8sStatefulSet, self).create()
        self.get()
        return self

    def update(self):
        super(K8sStatefulSet, self).update()
        self.get()
        return self

    def list(self, pattern=None):
        ls = super(K8sStatefulSet, self).list()
        ssets = list(map(lambda x: StatefulSet(x), ls))
        if pattern is not None:
            ssets = list(filter(lambda x: pattern in x.name, ssets))
        k8s = []
        for x in ssets:
            j = K8sStatefulSet(config=self.config, name=x.name)
            j.model = x
            k8s.append(j)
        return k8s
