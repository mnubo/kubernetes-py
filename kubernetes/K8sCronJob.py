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
