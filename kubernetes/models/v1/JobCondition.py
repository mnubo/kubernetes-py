#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string


class JobCondition(object):
    """
    http://kubernetes.io/docs/api-reference/batch/v1/definitions/#_v1_jobcondition
    """

    def __init__(self, model=None):
        super(JobCondition, self).__init__()

        self._type = None
        self._status = None
        self._last_probe_time = None
        self._last_transition_time = None
        self._reason = None
        self._message = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'type' in model:
            self.type = model['type']
        if 'status' in model:
            self.status = model['status']
        if 'lastProbeTime' in model:
            self.last_probe_time = model['lastProbeTime']
        if 'lastTransitionTime' in model:
            self.last_transition_time = model['lastTransitionTime']
        if 'reason' in model:
            self.reason = model['reason']
        if 'message' in model:
            self.message = model['message']

    # --------------------------------------------------------------------------------- type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, t=None):
        if not is_valid_string(t):
            raise SyntaxError('JobCondition: type: [ {} ] is invalid.'.format(t))
        self._type = t

    # --------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, s=None):
        if not is_valid_string(s):
            raise SyntaxError('JobCondition: status: [ {} ] is invalid.'.format(s))
        self._status = s

    # --------------------------------------------------------------------------------- lastProbeTime

    @property
    def last_probe_time(self):
        return self._last_probe_time

    @last_probe_time.setter
    def last_probe_time(self, t=None):
        if not is_valid_string(t):
            raise SyntaxError('JobCondition: last_probe_time: [ {} ] is invalid.'.format(t))
        self._last_probe_time = t

    # --------------------------------------------------------------------------------- lastTransitionTime

    @property
    def last_transition_time(self):
        return self._last_transition_time

    @last_transition_time.setter
    def last_transition_time(self, t=None):
        if not is_valid_string(t):
            raise SyntaxError('JobCondition: last_transition_time: [ {} ] is invalid.'.format(t))
        self._last_transition_time = t

    # --------------------------------------------------------------------------------- reason

    @property
    def reason(self):
        return self._reason

    @reason.setter
    def reason(self, r=None):
        if not is_valid_string(r):
            raise SyntaxError('JobCondition: reason: [ {} ] is invalid.'.format(r))
        self._reason = r

    # --------------------------------------------------------------------------------- message

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, m=None):
        if not is_valid_string(m):
            raise SyntaxError('JobCondition: message: [ {} ] is invalid.'.format(m))
        self._message = m

    # --------------------------------------------------------------------------------- serialize

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
