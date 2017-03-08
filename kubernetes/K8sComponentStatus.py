#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1.ComponentStatus import ComponentStatus


class K8sComponentStatus(K8sObject):
    def __init__(self, config=None, name=None):
        super(K8sComponentStatus, self).__init__(
            config=config,
            name=name,
            obj_type='ComponentStatus'
        )

    # -------------------------------------------------------------------------------------  override

    def create(self):
        return self

    def update(self):
        return self

    def delete(self, orphan=False):
        return self

    # ------------------------------------------------------------------------------------- get

    def get(self):
        self.model = ComponentStatus(self.get_model())
        return self

    # ------------------------------------------------------------------------------------- conditions

    @property
    def conditions(self):
        return self.model.conditions

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
        component_list = []
        components = K8sComponentStatus(config=config, name=name).list()
        for c in components:
            component_name = ComponentStatus(c).metadata.name
            if component_name == name:
                component_list.append(K8sComponentStatus(config=config, name=component_name).get())
        return component_list
