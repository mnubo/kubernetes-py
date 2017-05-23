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
from kubernetes.K8sExceptions import TimedOutException


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
    SCALE_WAIT_TIMEOUT_SECONDS = 120

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

    def list(self, pattern=None):
        ls = super(K8sJob, self).list()
        jobs = list(map(lambda x: Job(x), ls))
        if pattern is not None:
            jobs = list(filter(lambda x: pattern in x.name, jobs))
        k8s = []
        for x in jobs:
            j = K8sJob(config=self.config, name=x.name)
            j.model = x
            k8s.append(j)
        return k8s

    # ------------------------------------------------------------------------------------- get

    def get(self):
        self.model = Job(self.get_model())
        return self

    # ------------------------------------------------------------------------------------- scale

    def scale(self, p=None):
        self.parallelism = p
        self.update()
        self._wait_for_desired_parallelism(p)

    # ------------------------------------------------------------------------------------- wait

    def _wait_for_desired_parallelism(self, p=None):
        start_time = time.time()
        while self.parallelism != p:
            time.sleep(0.5)
            self.get()
            self._check_timeout(start_time, p)

    def _check_timeout(self, start_time=None, p=None):
        elapsed_time = time.time() - start_time
        if elapsed_time >= self.SCALE_WAIT_TIMEOUT_SECONDS:  # timeout
            raise TimedOutException(
                "Timed out scaling job: [ {0} ] to parallelism: [ {1} ]".format(self.name, p))

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

    # -------------------------------------------------------------------------------------  dnsPolicy

    @property
    def dns_policy(self):
        return self.model.spec.template.spec.dns_policy

    @dns_policy.setter
    def dns_policy(self, policy=None):
        if policy not in self.model.spec.template.spec.VALID_DNS_POLICIES:
            raise SyntaxError('K8sJob: dns_policy: [ {} ] is invalid.'.format(policy))
        self.model.spec.template.spec.dns_policy = policy

    # -------------------------------------------------------------------------------------  start time

    @property
    def start_time(self):
        return self.model.status.start_time

    @start_time.setter
    def start_time(self, t=None):
        raise NotImplementedError()

    # -------------------------------------------------------------------------------------  completion time

    @property
    def completion_time(self):
        return self.model.status.completion_time

    @completion_time.setter
    def completion_time(self, t=None):
        raise NotImplementedError()

    # -------------------------------------------------------------------------------------  failed

    @property
    def failed(self):
        return self.model.status.failed

    @failed.setter
    def failed(self, t=None):
        raise NotImplementedError()

    # -------------------------------------------------------------------------------------  succeeded

    @property
    def succeeded(self):
        return self.model.status.succeeded

    @succeeded.setter
    def succeeded(self, t=None):
        raise NotImplementedError()
