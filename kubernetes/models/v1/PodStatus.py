#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.BaseModel import BaseModel
from kubernetes.models.v1.ContainerStatus import ContainerStatus


class PodStatus(BaseModel):

    def __init__(self, model=None):
        BaseModel.__init__(self)

        self._conditions = []
        self._container_statuses = []

        self.phase = None
        self.message = None
        self.reason = None
        self.host_ip = None
        self.pod_ip = None
        self.start_time = None

    # ------------------------------------------------------------------------------------- add

    def add_container_status(self, status=None):
        if not isinstance(status, ContainerStatus):
            raise SyntaxError('PodStatus: status: [ {0} ] is invalid.'.format(status))
        self._container_statuses.append(status)

    # ------------------------------------------------------------------------------------- conditions

    @property
    def conditions(self):
        return self._conditions

    @conditions.setter
    def conditions(self, conditions=None):
        msg = 'PodStatus: conditions: [ {0} ] is invalid.'.format(conditions)
        if not isinstance(conditions, list):
            raise SyntaxError(msg)
        self._conditions = conditions

    # ------------------------------------------------------------------------------------- container status

    @property
    def container_statuses(self):
        return self._container_statuses

    @container_statuses.setter
    def container_statuses(self, statuses=None):
        msg = 'PodStatus: statuses: [ {0} ] is invalid.'.format(statuses)
        if not isinstance(statuses, list):
            raise SyntaxError(msg)
        for x in statuses:
            if not isinstance(x, ContainerStatus):
                raise SyntaxError(msg)
        self._container_statuses = statuses
