#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1 import BaseModel


class PodCondition(BaseModel):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_podcondition
    """
    
    def __init__(self):
        super(PodCondition, self).__init__()

        self.type = None
        self.status = None
        self.last_probe_time = None
        self.last_transition_time = None
        self.reason = None
        self.message = None

    # ------------------------------------------------------------------------------------- serialize

    def json(self):
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
