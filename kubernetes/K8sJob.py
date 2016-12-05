#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.Job import Job
from kubernetes.K8sObject import K8sObject


class K8sJob(K8sObject):

    def __init__(self, config=None, name=None):

        super(K8sJob, self).__init__(
            config=config,
            obj_type='Job',
            name=name
        )

    def get(self):
        self.model = Job(model=self.get_model())
        return self
