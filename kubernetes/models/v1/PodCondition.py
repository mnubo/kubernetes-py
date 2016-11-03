#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, filter_model


class PodCondition(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_podcondition
    """
    
    def __init__(self, model=None):
        super(PodCondition, self).__init__()

        self._last_probe_time = None
        self._last_transition_time = None
        self._message = None
        self._reason = None
        self._status = None
        self._type = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'lastProbeTime' in model:
            self.last_probe_time = model['lastProbeTime']
        if 'lastTransitionTime' in model:
            self.last_transition_time = model['lastTransitionTime']
        if 'message' in model:
            self.message = model['message']
        if 'reason' in model:
            self.reason = model['reason']
        if 'status' in model:
            self.status = model['status']
        if 'type' in model:
            self.type = model['type']

    # ------------------------------------------------------------------------------------- last probe time

    @property
    def last_probe_time(self):
        return self._last_probe_time

    @last_probe_time.setter
    def last_probe_time(self, time=None):
        if not is_valid_string(time):
            raise SyntaxError('PodCondition: last_probe_time: [ {0} ] is invalid.'.format(time))
        self._last_probe_time = time

    # ------------------------------------------------------------------------------------- last transition time

    @property
    def last_transition_time(self):
        return self._last_transition_time

    @last_transition_time.setter
    def last_transition_time(self, time=None):
        if not is_valid_string(time):
            raise SyntaxError('PodCondition: last_transition_time: [ {0} ] is invalid.'.format(time))
        self._last_transition_time = time

    # ------------------------------------------------------------------------------------- message

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, msg=None):
        if not is_valid_string(msg):
            raise SyntaxError('PodCondition: message: [ {0} ] is invalid.'.format(msg))
        self._message = msg

    # ------------------------------------------------------------------------------------- reason

    @property
    def reason(self):
        return self._reason

    @reason.setter
    def reason(self, r=None):
        if not is_valid_string(r):
            raise SyntaxError('PodCondition: reasons: [ {0} ] is invalid.'.format(r))
        self._reason = r

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status=None):
        if not is_valid_string(status):
            raise SyntaxError('PodCondition: status: [ {0} ] is invalid.'.format(status))
        self._status = status

    # ------------------------------------------------------------------------------------- type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, t=None):
        if not is_valid_string(t):
            raise SyntaxError('PodCondition: status: [ {0} ] is invalid.'.format(t))
        self._type = t

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.type is not None:
            data['type'] = self.type
        if self.status is not None:
            data['status'] = self.status
        if self.last_probe_time is not None:
            data['lastProbeTime'] = self.last_probe_time
        if self.last_transition_time is not None:
            data['lastTransitionTime'] = self.last_transition_time
        if self.reason is not None:
            data['reason'] = self.reason
        if self.message is not None:
            data['message'] = self.message
        return data
