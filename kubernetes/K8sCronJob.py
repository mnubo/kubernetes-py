#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject
from kubernetes.K8sContainer import K8sContainer
from kubernetes.models.v2alpha1.CronJob import CronJob
from kubernetes.utils import is_valid_list


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

    # -------------------------------------------------------------------------------------  add

    def add_container(self, container=None):
        if not isinstance(container, K8sContainer):
            raise SyntaxError(
                'K8sCronJob.add_container() container: [ {0} ] is invalid.'.format(container))
        containers = self.model.spec.job_template.spec.template.spec.containers
        if containers is None:
            containers = []
        filtered = filter(lambda x: x.name != container.name, containers)
        filtered.append(container.model)
        self.model.spec.job_template.spec.template.spec.containers = filtered
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

    # -------------------------------------------------------------------------------------  containers

    @property
    def containers(self):
        objs = []
        for c in self.model.spec.job_template.spec.template.spec.containers:
            k8scontainer = K8sContainer(name=c.name, image=c.image)
            k8scontainer.model = c
            objs.append(k8scontainer)
        return objs

    @containers.setter
    def containers(self, containers=None):
        if not is_valid_list(containers, K8sContainer):
            raise SyntaxError('K8sCronJob: containers: [ {} ] is invalid.'.format(containers))
        models = []
        for obj in containers:
            models.append(obj.model)
        self.model.spec.job_template.spec.template.spec.containers = models

    # -------------------------------------------------------------------------------------  container_image

    @property
    def container_image(self):
        data = {}
        for c in self.containers:
            data[c.name] = c.image
        return data

    @container_image.setter
    def container_image(self, tup=None):
        if not isinstance(tup, tuple):
            raise SyntaxError('K8sCronJob.container_image() must be a tuple of the form (name, image)')
        name, image = tup
        found = filter(lambda x: x.name == name, self.containers)
        if found:
            new = filter(lambda x: x.name != name, self.containers)
            found[0].image = image
            new.append(found[0])
            self.containers = new