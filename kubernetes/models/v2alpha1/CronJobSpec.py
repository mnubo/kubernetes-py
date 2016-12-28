#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v2alpha1.CronJobTemplate import CronJobTemplate
from kubernetes.utils import is_valid_string


class CronJobSpec(object):

    VALID_CONCURRENCY_POLICIES = ['Allow', 'Forbid', 'Replace']

    def __init__(self, model=None):
        super(CronJobSpec, self).__init__()

        self._schedule = "@hourly"
        self._job_template = CronJobTemplate()
        self._starting_deadline_seconds = None
        self._concurrency_policy = 'Allow'
        self._suspend = False

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'schedule' in model:
            self.schedule = model['schedule']
        if 'jobTemplate' in model:
            self.job_template = CronJobTemplate(model['jobTemplate'])
        if 'startingDeadlineSeconds' in model:
            self.starting_deadline_seconds = model['startingDeadlineSeconds']
        if 'concurrencyPolicy' in model:
            self.concurrency_policy = model['concurrencyPolicy']
        if 'suspend' in model:
            self.suspend = model['suspend']

    # ------------------------------------------------------------------------------------- schedule

    @property
    def schedule(self):
        return self._schedule

    @schedule.setter
    def schedule(self, s=None):
        if not is_valid_string(s):
            raise SyntaxError('CronJobSpec: schedule: [ {} ] is invalid.'.format(s))
        self._schedule = s

    # ------------------------------------------------------------------------------------- jobTemplate

    @property
    def job_template(self):
        return self._job_template

    @job_template.setter
    def job_template(self, jt=None):
        if not isinstance(jt, CronJobTemplate):
            raise SyntaxError('CronJobSpec: job_template: [ {} ] is invalid.'.format(jt))
        self._job_template = jt

    # ------------------------------------------------------------------------------------- startingDeadlineSeconds

    @property
    def starting_deadline_seconds(self):
        return self._starting_deadline_seconds

    @starting_deadline_seconds.setter
    def starting_deadline_seconds(self, sds=None):
        if not isinstance(sds, int) or not sds >= 0:
            raise SyntaxError('CronJobSpec: starting_deadline_seconds: [ {} ] is invalid.'.format(sds))
        self._starting_deadline_seconds = sds

    # ------------------------------------------------------------------------------------- concurrencyPolicy

    @property
    def concurrency_policy(self):
        return self._concurrency_policy

    @concurrency_policy.setter
    def concurrency_policy(self, cp=None):
        if cp not in self.VALID_CONCURRENCY_POLICIES:
            raise SyntaxError('CronJobSpec: concurrency_policy: [ {} ] is invalid.'.format(cp))
        self._concurrency_policy = cp

    # ------------------------------------------------------------------------------------- suspend

    @property
    def suspend(self):
        return self._suspend

    @suspend.setter
    def suspend(self, s=False):
        if not isinstance(s, bool):
            raise SyntaxError('CronJobSpec: suspend: [ {} ] is invalid.'.format(s))
        self._suspend = s

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.schedule is not None:
            data['schedule'] = self.schedule
        if self.job_template is not None:
            data['jobTemplate'] = self.job_template.serialize()
        if self.starting_deadline_seconds is not None:
            data['startingDeadlineSeconds'] = self.starting_deadline_seconds
        if self.concurrency_policy is not None:
            data['concurrencyPolicy'] = self.concurrency_policy
        if self.suspend is not None:
            data['suspend'] = self.suspend
        return data
