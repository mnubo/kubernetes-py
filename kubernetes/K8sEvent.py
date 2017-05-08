#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1.Event import Event
from dateutil.parser import parse


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

    def list(self, pattern=None, reverse=True):
        ls = super(K8sEvent, self).list()
        events = list(map(lambda x: Event(x), ls))
        if pattern is not None:
            events = list(filter(lambda x: pattern in x.name, events))
        k8s = []
        for x in events:
            j = K8sEvent(config=self.config, name=x.name)
            j.model = x
            k8s.append(j)
        k8s.sort(key=lambda x: x.last_timestamp, reverse=reverse)
        return k8s

    # ------------------------------------------------------------------------------------- warnings

    def warnings(self, pattern=None, reverse=True):
        ls = self.list(pattern, reverse)
        w = filter(lambda x: x.type == "Warning", ls)
        return w

    # ------------------------------------------------------------------------------------- type

    @property
    def type(self):
        return self.model.type

    @type.setter
    def type(self, t=None):
        raise NotImplementedError("K8sEvent: type is read-only.")

    # ------------------------------------------------------------------------------------- count

    @property
    def count(self):
        return self.model.count

    @count.setter
    def count(self, c=None):
        raise NotImplementedError("K8sEvent: count is read-only.")

    # ------------------------------------------------------------------------------------- source

    @property
    def source(self):
        return self.model.source

    @source.setter
    def source(self, s=None):
        raise NotImplementedError("K8sEvent: source is read-only.")

    # ------------------------------------------------------------------------------------- message

    @property
    def message(self):
        return self.model.message.strip()

    @message.setter
    def message(self, m=None):
        raise NotImplementedError("K8sEvent: message is read-only.")

    # ------------------------------------------------------------------------------------- reason

    @property
    def reason(self):
        return self.model.reason

    @reason.setter
    def reason(self, r=None):
        raise NotImplementedError("K8sEvent: reason is read-only.")

    # ------------------------------------------------------------------------------------- involvedObject

    @property
    def involved_object(self):
        return self.model.involved_object

    @involved_object.setter
    def involved_object(self, o=None):
        raise NotImplementedError("K8sEvent: involved_object is read-only.")

    # ------------------------------------------------------------------------------------- firstTimestamp

    @property
    def first_timestamp(self):
        dt = parse(self.model.first_timestamp)
        return dt

    @first_timestamp.setter
    def first_timestamp(self, t=None):
        raise NotImplementedError("K8sEvent: first_timestamp is read_only.")

    # ------------------------------------------------------------------------------------- lastTimestamp

    @property
    def last_timestamp(self):
        dt = parse(self.model.last_timestamp)
        return dt

    @last_timestamp.setter
    def last_timestamp(self, t=None):
        raise NotImplementedError("K8sEvent: last_timestamp is read-only.")
