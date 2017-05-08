#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v2alpha1.CronJob import CronJob


class ScheduledJob(CronJob):
    """
    Making ScheduledJobs a subclass of CronJobs. 
    
    ScheduledJobs exist only in Kubernetes 1.4.x.
    CronJobs exist from Kubernetes 1.5.x onwards.
    """

    def __init__(self, model=None):
        super(ScheduledJob, self).__init__(model=model)
        self.kind = "ScheduledJob"
