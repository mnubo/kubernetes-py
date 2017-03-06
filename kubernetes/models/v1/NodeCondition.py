#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#
from kubernetes.utils import filter_model, is_valid_date_time


class NodeCondition(object):
    """
    https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_nodecondition
    """

    def __init__(self, model=None):
        super(NodeCondition, self).__init__()

        self._condition_type = None
        self._status = None
        self._last_heartbeat_time = None
        self._last_transition_time = None
        self._reason = None
        self._message = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'type' in model:
            self.condition_type = model['type']
        if 'status' in model:
            self.status = model['status']
        if 'lastHeartbeatTime' in model:
            self.last_heartbeat_time = model['lastHeartbeatTime']
        if 'lastTransitionTime' in model:
            self.last_transition_time = model['lastTransitionTime']
        if 'reason' in model:
            self.reason = model['reason']
        if 'message' in model:
            self.message = model['message']

    # ------------------------------------------------------------------------------------- type

    @property
    def condition_type(self):
        return self._condition_type

    @condition_type.setter
    def condition_type(self, v):
        if not isinstance(v, str):
            raise SyntaxError('NodeCondition: condition_type: [ {0} ] is invalid.'.format(v))
        self._condition_type = v

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, v):
        if not isinstance(v, str):
            raise SyntaxError('NodeCondition: status: [ {0} ] is invalid.'.format(v))
        self._status = v

    # ------------------------------------------------------------------------------------- last_heartbeat_time

    @property
    def last_heartbeat_time(self):
        return self._last_heartbeat_time

    @last_heartbeat_time.setter
    def last_heartbeat_time(self, v):
        if not isinstance(v, str) or not is_valid_date_time(v):
            raise SyntaxError('NodeCondition: last_heartbeat_time: [ {0} ] is invalid.'.format(v))
        self._last_heartbeat_time = v

    # ------------------------------------------------------------------------------------- last_transition_time

    @property
    def last_transition_time(self):
        return self._last_transition_time

    @last_transition_time.setter
    def last_transition_time(self, v):
        if not isinstance(v, str) or not is_valid_date_time(v):
            raise SyntaxError('NodeCondition: last_transition_time: [ {0} ] is invalid.'.format(v))
        self._last_transition_time = v

    # ------------------------------------------------------------------------------------- last_transition_time

    @property
    def reason(self):
        return self._reason

    @reason.setter
    def reason(self, v):
        if not isinstance(v, str):
            raise SyntaxError('NodeCondition: reason: [ {0} ] is invalid.'.format(v))
        self._reason = v

    # ------------------------------------------------------------------------------------- message

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, v):
        if not isinstance(v, str):
            raise SyntaxError('NodeCondition: message: [ {0} ] is invalid.'.format(v))
        self._message = v

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.condition_type:
            data['type'] = self.condition_type
        if self.status:
            data['status'] = self.status
        if self.last_heartbeat_time:
            data['lastHeartbeatTime'] = self.last_heartbeat_time
        if self.last_transition_time:
            data['lastTransitionTime'] = self.last_transition_time
        if self.reason:
            data['reason'] = self.reason
        if self.message:
            data['message'] = self.message
        return data
