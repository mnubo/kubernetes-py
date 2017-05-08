#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sContainer import K8sContainer
from kubernetes.K8sObject import K8sObject
from kubernetes.K8sVolume import K8sVolume
from kubernetes.models.v2alpha1.CronJob import CronJob
from kubernetes.utils import is_valid_list, is_reachable


class K8sCronJob(K8sObject):
    def __init__(self, config=None, name=None):

        temp = K8sObject(config=config, obj_type='Pod', name='temp')
        _type = 'CronJob'

        if config and is_reachable(config):
            v = temp.server_version()
            if int(v['major']) == 1 and int(v['minor']) == 4:
                _type = 'ScheduledJob'

        super(K8sCronJob, self).__init__(
            config=config,
            obj_type=_type,
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

    def list(self, pattern=None):
        ls = super(K8sCronJob, self).list()
        jobs = list(map(lambda x: CronJob(x), ls))
        if pattern is not None:
            jobs = list(filter(lambda x: pattern in x.name, jobs))
        k8s = []
        for x in jobs:
            j = K8sCronJob(config=self.config, name=x.name)
            j.model = x
            k8s.append(j)
        return k8s

    # -------------------------------------------------------------------------------------  get

    def get(self):
        self.model = CronJob(self.get_model())
        return self

    # -------------------------------------------------------------------------------------  add

    def add_container(self, container=None):
        if not isinstance(container, K8sContainer):
            raise SyntaxError(
                'K8sCronJob.add_container() container: [ {0} ] is invalid.'.format(container))
        containers = self.model.spec.job_template.spec.template.spec.containers
        if containers is None:
            containers = []
        filtered = list(filter(lambda x: x.name != container.name, containers))
        filtered.append(container.model)
        self.model.spec.job_template.spec.template.spec.containers = filtered
        return self

    def add_image_pull_secrets(self, secrets=None):
        self.model.spec.add_image_pull_secrets(secrets)
        return self

    def add_volume(self, volume=None):
        if not isinstance(volume, K8sVolume):
            raise SyntaxError('K8sCronJob.add_volume() volume: [ {0} ] is invalid.'.format(volume))
        volumes = self.model.spec.job_template.spec.template.spec.volumes
        if volume.model not in volumes:
            volumes.append(volume.model)
        self.model.spec.job_template.spec.template.spec.volumes = volumes
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
        found = list(filter(lambda x: x.name == name, self.containers))
        if found:
            new = list(filter(lambda x: x.name != name, self.containers))
            found[0].image = image
            new.append(found[0])
            self.containers = new

    # -------------------------------------------------------------------------------------  restartPolicy

    @property
    def restart_policy(self):
        return self.model.spec.job_template.spec.template.spec.restart_policy

    @restart_policy.setter
    def restart_policy(self, p=None):
        self.model.spec.job_template.spec.template.spec.restart_policy = p

    # -------------------------------------------------------------------------------------  lastScheduleTime

    @property
    def last_schedule_time(self):
        return self.model.status.last_schedule_time

    @last_schedule_time.setter
    def last_schedule_time(self, t=None):
        raise NotImplementedError('K8sCronJob: last_schedule_time: this property is read-only.')
