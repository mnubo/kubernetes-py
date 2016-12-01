#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


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

    # --------------------------------------------------------------------------------- status

    # --------------------------------------------------------------------------------- lastProbeTime

    # --------------------------------------------------------------------------------- lastTransitionTime

    # --------------------------------------------------------------------------------- reason

    # --------------------------------------------------------------------------------- message

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
