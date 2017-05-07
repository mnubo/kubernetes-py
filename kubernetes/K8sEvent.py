#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1.Event import Event


class K8sEvent(K8sObject):

    def __init__(self, config=None, name=None):
        super(K8sEvent, self).__init__(
            config=config,
            name=name,
            obj_type='Event'
        )

    def create(self):
        raise NotImplementedError("K8sEvent: cannot create events this way.")

    def update(self):
        raise NotImplementedError("K8sEvent: cannot update events this way.")

    def list(self, pattern=None):
        ls = super(K8sEvent, self).list()
        events = list(map(lambda x: Event(x), ls))
        if pattern is not None:
            events = list(filter(lambda x: pattern in x.name, events))
        k8s = []
        for x in events:
            j = K8sEvent(config=self.config, name=x.name)
            j.model = x
            k8s.append(j)
        return k8s

