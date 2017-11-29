#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1.ConfigMap import ConfigMap


class K8sConfigMap(K8sObject):

    def __init__(self, config=None, name=None):

        _type = 'ConfigMap'

        super(K8sConfigMap, self).__init__(
            config=config,
            obj_type=_type,
            name=name
        )

    # -------------------------------------------------------------------------------------  override

    def create(self):
        super(K8sConfigMap, self).create()
        self.get()
        return self

    def update(self):
        super(K8sConfigMap, self).update()
        self.get()
        return self

    def list(self, pattern=None):
        ls = super(K8sConfigMap, self).list()
        cm = list(map(lambda x: ConfigMap(x), ls))
        if pattern is not None:
            cm = list(filter(lambda x: pattern in x.name, cm))
        k8s = []
        for x in cm:
            j = K8sConfigMap(config=self.config, name=x.name)
            j.model = x
            k8s.append(j)
        return k8s

    # -------------------------------------------------------------------------------------  get

    def get(self):
        self.model = ConfigMap(self.get_model())
        return self

    # -------------------------------------------------------------------------------------  add

    def add_data(self, k=None, v=None):
        if k is None or v is None:
            raise SyntaxError(
                'K8sConfigMap.add_data(): Key [ {0} ] or Value [ {1} ] is invalid.'.format(k, v))

        tmp_data = self.data
        if tmp_data is None:
            tmp_data = dict()
        if k in tmp_data.keys():
            tmp_data[k] = v
        else:
            tmp_data.update({k: v})
        self.data = tmp_data
        return self

    # -------------------------------------------------------------------------------------  data

    @property
    def data(self):
        return self.model.data

    @data.setter
    def data(self, v=None):
        self.model.data = v
