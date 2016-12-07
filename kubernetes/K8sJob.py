#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import time

from kubernetes.K8sContainer import K8sContainer
from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1.Job import Job


class K8sJob(K8sObject):
    """
    See http://kubernetes.io/docs/user-guide/jobs/#parallel-jobs for the three main types of Jobs.
    Also see http://kubernetes.io/docs/user-guide/jobs/#job-patterns for common use-cases.

    - For a Non-parallel job, you can leave both .completions and .parallelism unset.
      When both are unset, both are defaulted to 1.

    - For a Fixed Completion Count job, you should set .completions to the number of completions needed.
      You can set .parallelism, or leave it unset and it will default to 1.

    - For a Work Queue Job, you must leave .completions unset, and set .parallelism to a non-negative integer.

    """

    VALID_RESTART_POLICIES = ['OnFailure', 'Never']

    def __init__(self, config=None, name=None):

        super(K8sJob, self).__init__(
            config=config,
            obj_type='Job',
            name=name
        )

        self.restart_policy = 'OnFailure'

    # -------------------------------------------------------------------------------------  override

    def create(self):
        super(K8sJob, self).create()
        self.get()
        return self

    def update(self):
        super(K8sJob, self).update()
        self.get()
        return self

    # ------------------------------------------------------------------------------------- get

    def get(self):
        self.model = Job(model=self.get_model())
        return self

    # ------------------------------------------------------------------------------------- scale

    def scale(self, replicas=None):
        self.parallelism = replicas
        self.update()
        self._wait_for_desired_parallelism(replicas)

    def _wait_for_desired_parallelism(self, p=None):
        self.get()
        while self.parallelism != p:
            self.get()
            time.sleep(0.2)

    # ------------------------------------------------------------------------------------- parallelism

    @property
    def parallelism(self):
        return self.model.spec.parallelism

    @parallelism.setter
    def parallelism(self, p=None):
        self.model.spec.parallelism = p

    # ------------------------------------------------------------------------------------- completions

    @property
    def completions(self):
        return self.model.spec.completions

    @completions.setter
    def completions(self, c=None):
        self.model.spec.completions = c

    # ------------------------------------------------------------------------------------- activeDeadlineSeconds

    @property
    def active_deadline_seconds(self):
        return self.model.spec.active_deadline_seconds

    @active_deadline_seconds.setter
    def active_deadline_seconds(self, s=None):
        self.model.spec.active_deadline_seconds = s

    # ------------------------------------------------------------------------------------- containers

    @property
    def containers(self):
        _list = []
        for c in self.model.spec.template.spec.containers:
            k8scontainer = K8sContainer(name=c.name, image=c.image)
            k8scontainer.model = c
            _list.append(k8scontainer)
        return _list

    @containers.setter
    def containers(self, containers=None):
        self.model.spec.template.spec.containers = [x.model for x in containers]

    # -------------------------------------------------------------------------------------  volumes

    @property
    def volumes(self):
        return self.model.spec.template.spec.volumes

    @volumes.setter
    def volumes(self, v=None):
        self.model.spec.template.spec.volumes = v

    # -------------------------------------------------------------------------------------  restartPolicy

    @property
    def restart_policy(self):
        return self.model.spec.template.spec.restart_policy

    @restart_policy.setter
    def restart_policy(self, policy=None):
        if policy not in self.VALID_RESTART_POLICIES:
            raise SyntaxError('K8sJob: restart_policy: [ {} ] is invalid.'.format(policy))
        self.model.spec.template.spec.restart_policy = policy
