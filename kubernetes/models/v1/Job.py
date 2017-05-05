#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.unversioned.BaseModel import BaseModel
from kubernetes.models.v1.JobSpec import JobSpec
from kubernetes.models.v1.JobStatus import JobStatus
from kubernetes.models.v1.ObjectMeta import ObjectMeta


class Job(BaseModel):
    """
    http://kubernetes.io/docs/api-reference/batch/v1/definitions/#_v1_job
    """

    def __init__(self, model=None):
        super(Job, self).__init__()

        self.kind = 'Job'
        self.api_version = 'batch/v1'

        self.spec = JobSpec()
        self.status = JobStatus()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        super(Job, self).build_with_model(model)

        if 'spec' in model:
            self.spec = JobSpec(model['spec'])
        if 'status' in model:
            self.status = JobStatus(model['status'])

    # --------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, s=None):
        if not isinstance(s, JobSpec):
            raise SyntaxError('Job: spec: [ {} ] is invalid.'.format(s))
        self._spec = s

    # --------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, s=None):
        if not isinstance(s, JobStatus):
            raise SyntaxError('Job: status: [ {} ] is invalid.'.format(s))
        self._status = s

    # --------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(Job, self).serialize()

        if self.spec is not None:
            data['spec'] = self.spec.serialize()
        if self.status is not None:
            data['status'] = self.status.serialize()
        return data
