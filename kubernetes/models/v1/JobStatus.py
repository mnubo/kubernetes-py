#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.JobCondition import JobCondition
from kubernetes.utils import is_valid_list, is_valid_string


class JobStatus(object):
    """
    http://kubernetes.io/docs/api-reference/batch/v1/definitions/#_v1_jobstatus
    """

    def __init__(self, model=None):
        super(JobStatus, self).__init__()

        self._conditions = []
        self._start_time = None
        self._completion_time = None
        self._active = None
        self._succeeded = None
        self._failed = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'conditions' in model:
            conds = []
            for c in model['conditions']:
                cond = JobCondition(c)
                conds.append(cond)
            self.conditions = conds
        if 'startTime' in model:
            self.start_time = model['startTime']
        if 'completionTime' in model:
            self.completion_time = model['completionTime']
        if 'active' in model:
            self.active = model['active']
        if 'succeeded' in model:
            self.succeeded = model['succeeded']
        if 'failed' in model:
            self.failed = model['failed']

    # --------------------------------------------------------------------------------- conditions

    @property
    def conditions(self):
        return self._conditions

    @conditions.setter
    def conditions(self, conds=None):
        if not is_valid_list(conds, JobCondition):
            raise SyntaxError('JobStatus: conditions: [ {} ] is invalid.'.format(conds))
        self._conditions = conds

    # --------------------------------------------------------------------------------- startTime

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, time=None):
        if not is_valid_string(time):
            raise SyntaxError('JobStatus: start_time: [ {} ] is invalid.'.format(time))
        self._start_time = time

    # --------------------------------------------------------------------------------- completionTime

    @property
    def completion_time(self):
        return self._completion_time

    @completion_time.setter
    def completion_time(self, time=None):
        if not is_valid_string(time):
            raise SyntaxError('JobStatus: completion_time: [ {} ] is invalid.'.format(time))
        self._completion_time = time

    # --------------------------------------------------------------------------------- active

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, a=None):
        if not isinstance(a, int):
            raise SyntaxError('JobStatus: active: [ {} ] is invalid.'.format(a))
        self._active = a

    # --------------------------------------------------------------------------------- succeeded

    @property
    def succeeded(self):
        return self._succeeded

    @succeeded.setter
    def succeeded(self, s=None):
        if not isinstance(s, int):
            raise SyntaxError('JobStatus: succeeded: [ {} ] is invalid.'.format(s))
        self._succeeded = s

    # --------------------------------------------------------------------------------- failed

    @property
    def failed(self):
        return self._failed

    @failed.setter
    def failed(self, f=None):
        if not isinstance(f, int):
            raise SyntaxError('JobStatus: failed: [ {} ] is invalid.'.format(f))
        self._succeeded = f

    # --------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.conditions is not None:
            data['conditions'] = [x.serialize() for x in self.conditions]
        if self.start_time is not None:
            data['startTime'] = self.start_time
        if self.completion_time is not None:
            data['completionTime'] = self.completion_time
        if self.active is not None:
            data['active'] = self.active
        if self.succeeded is not None:
            data['succeeded'] = self.succeeded
        if self.failed is not None:
            data['failed'] = self.failed
        return data
