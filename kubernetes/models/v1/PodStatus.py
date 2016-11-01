#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1 import (
    BaseModel,
    ContainerStatus,
    PodCondition
)
from kubernetes.utils import is_valid_list


class PodStatus(BaseModel):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_podstatus
    """

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
        if not is_valid_list(conditions, PodCondition):
            raise SyntaxError('PodStatus: conditions: [ {0} ] is invalid.'.format(conditions))
        self._conditions = conditions

    # ------------------------------------------------------------------------------------- container status

    @property
    def container_statuses(self):
        return self._container_statuses

    @container_statuses.setter
    def container_statuses(self, statuses=None):
        if not is_valid_list(statuses, ContainerStatus):
            raise SyntaxError('PodStatus: container_statuses: [ {0} ] is invalid.'.format(statuses))
        self._container_statuses = statuses

    # ------------------------------------------------------------------------------------- serialize

    def json(self):
        data = {}
        if self.phase is not None:
            data['phase'] = self.phase
        if self.conditions:
            data['conditions'] = [x.json() for x in self.conditions]
        if self.message is not None:
            data['message'] = self.message
        if self.reason is not None:
            data['reason'] = self.reason
        if self.host_ip is not None:
            data['hostIP'] = self.host_ip
        if self.pod_ip is not None:
            data['podIP'] = self.pod_ip
        if self.start_time is not None:
            data['startTime'] = self.start_time
        if self.container_statuses:
            data['containerStatuses'] = [x.json() for x in self.container_statuses]
        return data