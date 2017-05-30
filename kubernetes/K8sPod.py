#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import time

from kubernetes import K8sConfig
from kubernetes.K8sContainer import K8sContainer
from kubernetes.K8sExceptions import NotFoundException, TimedOutException
from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1.Pod import Pod
from kubernetes.models.v1.PodStatus import PodStatus
from kubernetes.models.v1.Probe import Probe
from kubernetes.utils import is_valid_dict, is_valid_string, is_valid_list


class K8sPod(K8sObject):

    POD_READY_TIMEOUT_SECONDS = 120

    def __init__(self, config=None, name=None):
        super(K8sPod, self).__init__(
            config=config,
            obj_type='Pod',
            name=name
        )
        if self.config.pull_secret is not None:
            self.add_image_pull_secrets(self.config.pull_secret)

    # -------------------------------------------------------------------------------------  override

    def create(self):
        super(K8sPod, self).create()
        self.get()
        self._wait_for_readiness()
        return self

    def update(self):
        super(K8sPod, self).update()
        self.get()
        self._wait_for_readiness()
        return self

    def list(self, pattern=None):
        ls = super(K8sPod, self).list()
        pods = list(map(lambda x: Pod(x), ls))
        if pattern is not None:
            pods = list(filter(lambda x: pattern in x.name, pods))
        k8s = []
        for x in pods:
            p = K8sPod(config=self.config, name=x.name)
            p.model = x
            k8s.append(p)
        return k8s

    # -------------------------------------------------------------------------------------  wait

    def _wait_for_readiness(self):
        start_time = time.time()
        while not self.is_ready():
            time.sleep(0.2)
            elapsed_time = time.time() - start_time
            if elapsed_time >= self.POD_READY_TIMEOUT_SECONDS:
                raise TimedOutException(
                    "Timed out on Pod readiness: [ {0} ]".format(self.name))

    # -------------------------------------------------------------------------------------  add

    def add_container(self, container=None):
        if not isinstance(container, K8sContainer):
            raise SyntaxError(
                'K8sPod.add_container() container: [ {0} ] is invalid.'.format(container))

        containers = self.model.spec.containers
        if container not in containers:
            containers.append(container.model)
            self.model.spec.containers = containers
        return self

    def add_image_pull_secrets(self, secrets=None):
        self.model.spec.add_image_pull_secrets(secrets)
        return self

    def add_volume(self, volume=None):
        volumes = self.model.spec.volumes
        if volume not in volumes:
            volumes.append(volume.model)
        self.model.spec.volumes = volumes
        return self

    # ------------------------------------------------------------------------------------- delete

    def del_node_name(self):
        self.model.spec.node_name = None
        return self

    # ------------------------------------------------------------------------------------- get

    def get(self):
        self.model = Pod(self.get_model())
        return self

    # ------------------------------------------------------------------------------------- polling readiness

    def is_ready(self):
        self.get()
        if self.status is not None and isinstance(self.status, PodStatus):
            pod_phase = self.status.phase
            conditions = self.status.conditions
            conditions_ok = 0
            for cond in conditions:
                if cond.status == 'True':
                    conditions_ok += 1
            if pod_phase == 'Running' and len(conditions) == conditions_ok:
                return True
        return False

    # ------------------------------------------------------------------------------------- set

    def set_container_image(self, name=None, image=None):
        containers = []
        for c in self.model.spec.containers:
            if c.name == name:
                c.image = image
            containers.append(c)
        self.model.spec.containers = containers
        return self

    # ------------------------------------------------------------------------------------- activeDeadline

    @property
    def active_deadline(self):
        return self.model.spec.active_deadline_seconds

    @active_deadline.setter
    def active_deadline(self, secs=None):
        self.model.spec.active_deadline_seconds = secs

    # ------------------------------------------------------------------------------------- containers

    @property
    def containers(self):
        _list = []
        for c in self.model.spec.containers:
            k8scontainer = K8sContainer(name=c.name, image=c.image)
            k8scontainer.model = c
            _list.append(k8scontainer)
        return _list

    @containers.setter
    def containers(self, containers=None):
        if not is_valid_list(containers, K8sContainer):
            self.model.spec.containers = [x.model for x in containers]

    # ------------------------------------------------------------------------------------- dnsPolicy

    @property
    def dns_policy(self):
        return self.model.spec.dns_policy

    @dns_policy.setter
    def dns_policy(self, policy=None):
        self.model.spec.dns_policy = policy

    # ------------------------------------------------------------------------------------- generateName

    @property
    def generate_name(self):
        return self.model.metadata.generate_name

    @generate_name.setter
    def generate_name(self, name=None):
        self.model.metadata.generate_name = name

    # ------------------------------------------------------------------------------------- namespace

    @property
    def namespace(self):
        return self.model.metadata.namespace

    @namespace.setter
    def namespace(self, nspace=None):
        self.model.metadata.namespace = nspace

    # ------------------------------------------------------------------------------------- nodeName

    @property
    def node_name(self):
        return self.model.spec.node_name

    @node_name.setter
    def node_name(self, name=None):
        self.model.spec.node_name = name

    # ------------------------------------------------------------------------------------- nodeSelector

    @property
    def node_selector(self):
        return self.model.spec.node_selector

    @node_selector.setter
    def node_selector(self, selector=None):
        self.model.spec.node_selector = selector

    # -------------------------------------------------------------------------------------  livenessProbes

    @property
    def liveness_probes(self):
        data = {}
        containers = self.model.spec.containers
        for c in containers:
            if c.liveness_probe is not None:
                data[c.name] = c.liveness_probe
        return data

    @liveness_probes.setter
    def liveness_probes(self, tup=None):
        if not isinstance(tup, tuple):
            raise SyntaxError(
                'K8sPod: liveness_probes: [ {} ] is invalid.'.format(tup))

        c_name, probe = tup
        container_names = [c.name for c in self.model.spec.containers]
        if c_name not in container_names:
            raise SyntaxError(
                'K8sPod: liveness_probes: container [ {} ] not found.'.format(c_name))
        if not isinstance(probe, Probe):
            raise SyntaxError(
                'K8sPod: liveness_probe: probe: [ {} ] is invalid.'.format(probe))

        containers = []
        for c in self.model.spec.containers:
            if c.name == c_name:
                c.liveness_probe = probe
            containers.append(c)
        self.model.spec.template.spec.containers = containers

    # -------------------------------------------------------------------------------------  readinessProbes

    @property
    def readiness_probes(self):
        data = {}
        containers = self.model.spec.containers
        for c in containers:
            if c.readiness_probe is not None:
                data[c.name] = c.readiness_probe
        return data

    @readiness_probes.setter
    def readiness_probes(self, tup=None):
        if not isinstance(tup, tuple):
            raise SyntaxError(
                'K8sPod: readiness_probes: [ {} ] is invalid.'.format(tup))

        c_name, probe = tup
        container_names = [c.name for c in self.model.spec.template.spec.containers]
        if c_name not in container_names:
            raise SyntaxError(
                'K8sPod: readiness_probes: container [ {} ] not found.'.format(c_name))
        if not isinstance(probe, Probe):
            raise SyntaxError(
                'K8sPod: readiness_probes: probe: [ {} ] is invalid.'.format(probe))

        containers = []
        for c in self.model.spec.template.spec.containers:
            if c.name == c_name:
                c.readiness_probe = probe
            containers.append(c)
        self.model.spec.template.spec.containers = containers

    # ------------------------------------------------------------------------------------- restartPolicy

    @property
    def restart_policy(self):
        return self.model.spec.restart_policy

    @restart_policy.setter
    def restart_policy(self, policy=None):
        self.model.spec.restart_policy = policy

    # ------------------------------------------------------------------------------------- serviceAccountName

    @property
    def service_account_name(self):
        return self.model.spec.service_account_name

    @service_account_name.setter
    def service_account_name(self, name=None):
        self.model.spec.service_account_name = name

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        self.get()
        return self.model.status

    @status.setter
    def status(self, status=None):
        self.model.status = status

    # ------------------------------------------------------------------------------------- terminationGracePeriod

    @property
    def termination_grace_period(self):
        return self.model.spec.termination_grace_period_seconds

    @termination_grace_period.setter
    def termination_grace_period(self, secs=None):
        self.model.spec.termination_grace_period_seconds = secs

    # ------------------------------------------------------------------------------------- volumes

    @property
    def volumes(self):
        return self.model.spec.volumes

    @volumes.setter
    def volumes(self, v=None):
        self.model.spec.volumes = v

    # -------------------------------------------------------------------------------------  start time

    @property
    def start_time(self):
        return self.model.status.start_time

    @start_time.setter
    def start_time(self, t=None):
        raise NotImplementedError()

    # -------------------------------------------------------------------------------------  phase

    @property
    def phase(self):
        return self.model.status.phase

    @phase.setter
    def phase(self, p=None):
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------- filtering

    @staticmethod
    def get_by_name(config=None, name=None):
        if config is None:
            config = K8sConfig()
        if not is_valid_string(name):
            raise SyntaxError(
                'K8sPod.get_by_name(): name: [ {0} ] is invalid.'.format(name))

        pod_list = []
        data = {'labelSelector': 'name={0}'.format(name)}
        pods = K8sPod(config=config, name=name).get_with_params(data=data)

        for pod in pods:
            try:
                p = Pod(pod)
                k8s_pod = K8sPod(config=config, name=p.metadata.name).get()
                pod_list.append(k8s_pod)
            except NotFoundException:
                pass

        return pod_list

    @staticmethod
    def get_by_labels(config=None, labels=None):
        if config is None:
            config = K8sConfig()
        if not is_valid_dict(labels):
            raise SyntaxError(
                'K8sPod.get_by_labels(): labels: [ {} ] is invalid.'.format(labels))

        pod_list = []
        selector = ",".join(['%s=%s' % (key, value) for (key, value) in labels.items()])
        data = {'labelSelector': selector}
        p = K8sPod(config=config, name=labels['name'])
        pods = p.get_with_params(data=data)

        for pod in pods:
            try:
                p = Pod(pod)
                k8s_pod = K8sPod(config=config, name=p.metadata.name).get()
                pod_list.append(k8s_pod)
            except NotFoundException:
                pass

        return pod_list
