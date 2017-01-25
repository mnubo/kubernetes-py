#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import json
import yaml

from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1.Namespace import Namespace


class K8sNamespace(K8sObject):

    def __init__(self, config=None, name=None):
        super(K8sNamespace, self).__init__(
            config=config,
            name=name,
            obj_type='Namespace'
        )

    # -------------------------------------------------------------------------------------  override

    def create(self):
        super(K8sNamespace, self).create()
        self.get()
        return self

    def update(self):
        super(K8sNamespace, self).update()
        self.get()
        return self

    # ------------------------------------------------------------------------------------- get

    def get(self):
        self.model = Namespace(self.get_model())
        return self

    def get_annotation(self, k=None):
        if k in self.model.metadata.annotations:
            return self.model.metadata.annotations[k]
        return None

    def get_label(self, k=None):
        if k in self.model.metadata.labels:
            return self.model.metadata.labels[k]
        return None

    # ------------------------------------------------------------------------------------- finalizers

    @property
    def finalizers(self):
        return self.model.spec.finalizers

    @finalizers.setter
    def finalizers(self, f=None):
        self.model.spec.finalizers = f

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
        namespace_list = []
        namespaces = K8sNamespace(config=config, name=name).list()
        for ns in namespaces:
            namespace_name = Namespace(ns).metadata.name
            if namespace_name == name:
                namespace_list.append(K8sNamespace(config=config, name=namespace_name).get())
        return namespace_list
