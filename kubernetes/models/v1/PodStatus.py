#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.ContainerStatus import ContainerStatus
from kubernetes.models.v1.PodCondition import PodCondition
from kubernetes.utils import is_valid_list, is_valid_string, filter_model


class PodStatus(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_podstatus
    """

    def __init__(self, model=None):
        super(PodStatus, self).__init__()

        self._conditions = []
        self._container_statuses = []
        self._phase = None
        self._message = None
        self._reason = None
        self._host_ip = None
        self._pod_ip = None
        self._start_time = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'conditions' in model:
            conditions = []
            for c in model['conditions']:
                condition = PodCondition(c)
                conditions.append(condition)
            self.conditions = conditions
        if 'containerStatuses' in model:
            statuses = []
            for s in model['containerStatuses']:
                status = ContainerStatus(s)
                statuses.append(status)
            self.container_statuses = statuses
        if 'phase' in model:
            self.phase = model['phase']
        if 'message' in model:
            self.message = model['message']
        if 'reason' in model:
            self.reason = model['reason']
        if 'hostIP' in model:
            self.host_ip = model['hostIP']
        if 'podIP' in model:
            self.host_ip = model['podIP']
        if 'startTime' in model:
            self.start_time = model['startTime']

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

    # ------------------------------------------------------------------------------------- phase

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, phase=None):
        if not is_valid_string(phase):
            raise SyntaxError('PodStatus: container_statuses: [ {0} ] is invalid.'.format(phase))
        self._phase = phase

    # ------------------------------------------------------------------------------------- phase

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message=None):
        if not is_valid_string(message):
            raise SyntaxError('PodStatus: message: [ {0} ] is invalid.'.format(message))
        self._message = message

    # ------------------------------------------------------------------------------------- reason

    @property
    def reason(self):
        return self._reason

    @reason.setter
    def reason(self, reason=None):
        if not is_valid_string(reason):
            raise SyntaxError('PodStatus: reason: [ {0} ] is invalid.'.format(reason))
        self._reason = reason

    # ------------------------------------------------------------------------------------- hostIP

    @property
    def host_ip(self):
        return self._host_ip

    @host_ip.setter
    def host_ip(self, ip=None):
        if not is_valid_string(ip):
            raise SyntaxError('PodStatus: host_ip: [ {0} ] is invalid.'.format(ip))
        self._host_ip = ip

    # ------------------------------------------------------------------------------------- podIP

    @property
    def pod_ip(self):
        return self._pod_ip

    @pod_ip.setter
    def pod_ip(self, ip=None):
        if not is_valid_string(ip):
            raise SyntaxError('PodStatus: pod_ip: [ {0} ] is invalid.'.format(ip))
        self._pod_ip = ip

    # ------------------------------------------------------------------------------------- start time

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, time=None):
        if not is_valid_string(time):
            raise SyntaxError('PodStatus: start_time: [ {0} ] is invalid.'.format(time))
        self._start_time = time

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.phase is not None:
            data['phase'] = self.phase
        if self.conditions:
            data['conditions'] = [x.serialize() for x in self.conditions]
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
            data['containerStatuses'] = [x.serialize() for x in self.container_statuses]
        return data
