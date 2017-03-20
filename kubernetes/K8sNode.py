#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1.Node import Node


class K8sNode(K8sObject):
    def __init__(self, config=None, name=None):
        super(K8sNode, self).__init__(
            config=config,
            name=name,
            obj_type='Node'
        )

    # -------------------------------------------------------------------------------------  override

    def create(self):
        super(K8sNode, self).create()
        self.get()
        return self

    def update(self):
        super(K8sNode, self).update()
        self.get()
        return self

    def list(self, pattern=None):
        ls = super(K8sNode, self).list()
        nodes = list(map(lambda x: Node(x), ls))
        if pattern is not None:
            nodes = list(filter(lambda x: pattern in x.name, nodes))
        k8s = []
        for x in nodes:
            j = K8sNode(config=self.config, name=x.name)
            j.model = x
            k8s.append(j)
        return k8s

    # ------------------------------------------------------------------------------------- get

    def get(self):
        self.model = Node(self.get_model())
        return self

    def get_annotation(self, k=None):
        if k in self.model.metadata.annotations:
            return self.model.metadata.annotations[k]
        return None

    def get_label(self, k=None):
        if k in self.model.metadata.labels:
            return self.model.metadata.labels[k]
        return None

    # ------------------------------------------------------------------------------------- pod_cidr

    @property
    def pod_cidr(self):
        return self.model.spec.pod_cidr

    @pod_cidr.setter
    def pod_cidr(self, v=None):
        self.model.spec.pod_cidr = v

    # ------------------------------------------------------------------------------------- external_id

    @property
    def external_id(self):
        return self.model.spec.external_id

    @external_id.setter
    def external_id(self, v=None):
        self.model.spec.external_id = v

    # ------------------------------------------------------------------------------------- provider_id

    @property
    def provider_id(self):
        return self.model.spec.provider_id

    @provider_id.setter
    def provider_id(self, v=None):
        self.model.spec.provider_id = v

    # ------------------------------------------------------------------------------------- unschedulable

    @property
    def unschedulable(self):
        return self.model.spec.unschedulable

    @unschedulable.setter
    def unschedulable(self, v=None):
        self.model.spec.unschedulable = v

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self.model.status

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self.model.metadata.name

    @name.setter
    def name(self, name=None):
        self.model.metadata.name = name

    # ------------------------------------------------------------------------------------- filter

    @staticmethod
    def get_by_name(config=None, name=None):
        nodes = K8sNode(config=config, name=name).list()
        filtered = list(filter(lambda x: x.name == name, nodes))
        if filtered:
            return filtered[0]
        return None
