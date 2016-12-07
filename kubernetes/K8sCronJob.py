#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject
from kubernetes.models.v2alpha1.CronJob import CronJob


class K8sCronJob(K8sObject):

    def __init__(self, config=None, name=None):
        super(K8sCronJob, self).__init__(
            config=config,
            obj_type='CronJob',
            name=name
        )

    # -------------------------------------------------------------------------------------  override

    def create(self):
        super(K8sCronJob, self).create()
        self.get()
        return self

    def update(self):
        super(K8sCronJob, self).update()
        self.get()
        return self

    # -------------------------------------------------------------------------------------  get

    def get(self):
        self.model = CronJob(model=self.get_model())
        return self

    # -------------------------------------------------------------------------------------  schedule

    @property
    def schedule(self):
        return self.model.spec.schedule

    @schedule.setter
    def schedule(self, s=None):
        self.model.spec.schedule = s

    # -------------------------------------------------------------------------------------  startingDeadlineSeconds

    @property
    def starting_deadline_seconds(self):
        return self.model.spec.starting_deadline_seconds

    @starting_deadline_seconds.setter
    def starting_deadline_seconds(self, s=None):
        self.model.spec.starting_deadline_seconds = s

    # -------------------------------------------------------------------------------------  concurrencyPolicy

    @property
    def concurrency_policy(self):
        return self.model.spec.concurrency_policy

    @concurrency_policy.setter
    def concurrency_policy(self, cp=None):
        self.model.spec.concurrency_policy = cp

    # -------------------------------------------------------------------------------------  suspend

    @property
    def suspend(self):
        return self.model.spec.suspend

    @suspend.setter
    def suspend(self, s=None):
        self.model.spec.suspend = s

    # -------------------------------------------------------------------------------------  parallelism

    @property
    def parallelism(self):
        return self.model.spec.job_template.spec.parallelism

    @parallelism.setter
    def parallelism(self, jp=None):
        self.model.spec.job_template.spec.parallelism = jp

    # -------------------------------------------------------------------------------------  completions

    @property
    def completions(self):
        return self.model.spec.job_template.spec.completions

    @completions.setter
    def completions(self, c=None):
        self.model.spec.job_template.spec.completions = c
