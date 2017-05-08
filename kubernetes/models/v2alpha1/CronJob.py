#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.unversioned.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v2alpha1.CronJobSpec import CronJobSpec
from kubernetes.models.v2alpha1.CronJobStatus import CronJobStatus


class CronJob(BaseModel):
    """
    http://kubernetes.io/docs/user-guide/cron-jobs/#creating-a-cron-job
    """

    def __init__(self, model=None):
        super(CronJob, self).__init__()

        self.kind = "CronJob"
        self.api_version = "batch/v2alpha1"

        self.spec = CronJobSpec()
        self.status = CronJobStatus()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        super(CronJob, self).build_with_model(model)

        if 'spec' in model:
            self.spec = CronJobSpec(model['spec'])
        if 'status' in model:
            self.status = CronJobStatus(model['status'])

    # ------------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec=None):
        if not isinstance(spec, CronJobSpec):
            raise SyntaxError('CronJob: spec: [ {} ] is invalid.'.format(spec))
        self._spec = spec

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status=None):
        if not isinstance(status, CronJobStatus):
            raise SyntaxError('CronJob: status: [ {} ] is invalid.'.format(status))
        self._status = status

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(CronJob, self).serialize()

        if self.spec is not None:
            data['spec'] = self.spec.serialize()
        if self.status is not None:
            data['status'] = self.status.serialize()
        return data
