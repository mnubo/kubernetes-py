#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import time
import json
import yaml

from kubernetes import K8sConfig
from kubernetes.K8sContainer import K8sContainer
from kubernetes.K8sExceptions import NotFoundException, TimedOutException
from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1.Pod import Pod
from kubernetes.models.v1.PodSpec import PodSpec
from kubernetes.models.v1.PodStatus import PodStatus
from kubernetes.utils import is_valid_dict, is_valid_string

POD_READY_TIMEOUT_SECONDS = 60


class K8sPod(K8sObject):
    def __init__(self, config=None, name=None):
        super(K8sPod, self).__init__(config=config, obj_type='Pod', name=name)

        self.model = Pod()

        self.model.metadata = ObjectMeta()
        self.model.metadata.name = name
        self.model.metadata.labels['name'] = name
        self.model.metadata.namespace = config.namespace

        self.model.spec = PodSpec()
        self.model.status = PodStatus()

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

    def _wait_for_readiness(self):
        start_time = time.time()
        while not self.is_ready():
            time.sleep(0.2)
            elapsed_time = time.time() - start_time
            if elapsed_time >= POD_READY_TIMEOUT_SECONDS:
                raise TimedOutException("Timed out on Pod readiness: [ {0} ]".format(self.name))

    # -------------------------------------------------------------------------------------  add

    def add_annotation(self, k=None, v=None):
        if not is_valid_string(k) or not is_valid_string(v):
            raise SyntaxError('K8sPod.add_annotation(): annotation: [ {0}: {1} ] is invalid'.format(k, v))
        annotations = self.model.metadata.annotations
        if annotations is None:
            annotations = {}
        if k not in annotations:
            annotations.update({k: v})
        else:
            annotations[k] = v
        self.model.metadata.annotations = annotations
        return self

    def add_container(self, container=None):
        if not isinstance(container, K8sContainer):
            raise SyntaxError('K8sPod.add_container() container: [ {0} ] is invalid.'.format(container))
        containers = self.model.spec.containers
        if container not in containers:
            containers.append(container.model)
            self.model.spec.containers = containers
        return self

    def add_label(self, k=None, v=None):
        if not is_valid_string(k) or not is_valid_string(v):
            raise SyntaxError('K8sPod.add_label(): label: [ {0}: {1} ] is invalid'.format(k, v))
        labels = self.model.metadata.labels
        if labels is None:
            labels = {}
        if k not in labels:
            labels[k] = v
        else:
            labels.update({k: v})
        self.model.metadata.labels = labels
        return self

    def add_image_pull_secrets(self, name=None):
        secrets = self.model.spec.image_pull_secrets
        if secrets is None:
            secrets = []
        if name not in secrets:
            secrets.append(name)
            self.model.spec.image_pull_secrets = secrets
        return self

    def add_volume(self, volume=None):
        volumes = self.model.spec.volumes
        if volume not in volumes:
            volumes.append(volume)
            self.model.spec.volumes = volumes
        return self

    # ------------------------------------------------------------------------------------- delete

    def del_annotation(self, k=None):
        orig = self.model.metadata.annotations
        if k in orig:
            orig.pop(k)
            self.model.metadata.annotations = orig
        return self

    def del_label(self, k=None):
        orig = self.model.metadata.labels
        if k in orig:
            orig.pop(k)
            self.model.metadata.labels = orig
        return self

    def del_node_name(self):
        self.model.spec.node_name = None
        return self

    # ------------------------------------------------------------------------------------- get

    def get(self):
        self.model = Pod(model=self.get_model())
        return self

    def get_annotation(self, k=None):
        if k in self.model.metadata.annotations:
            return self.model.metadata.annotations[k]
        return None

    def get_label(self, k=None):
        if k in self.model.metadata.labels:
            return self.model.metadata.labels[k]
        return None

    # ------------------------------------------------------------------------------------- polling readiness

    def is_ready(self):
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

    # ------------------------------------------------------------------------------------- annotations

    @property
    def annotations(self):
        return self.model.metadata.annotations

    @annotations.setter
    def annotations(self, anns=None):
        self.model.metadata.annotations = anns

    # ------------------------------------------------------------------------------------- containers

    @property
    def containers(self):
        _list = []
        for c in self.model.spec.containers:
            k8scontainer = K8sContainer(model=c)
            _list.append(k8scontainer)
        return _list

    @containers.setter
    def containers(self, containers=None):
        self.model.spec.containers = containers

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

    # ------------------------------------------------------------------------------------- labels

    @property
    def labels(self):
        return self.model.metadata.labels

    @labels.setter
    def labels(self, labels=None):
        self.model.metadata.labels = labels

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

    # ------------------------------------------------------------------------------------- filtering

    @staticmethod
    def get_by_name(config=None, name=None):
        if config is None:
            config = K8sConfig()
        if not is_valid_string(name):
            raise SyntaxError('K8sPod.get_by_name(): name: [ {0} ] is invalid.'.format(name))

        pod_list = []
        data = {'labelSelector': 'name={0}'.format(name)}
        pods = K8sPod(config=config, name=name).get_with_params(data=data)

        for pod in pods:
            try:
                p = Pod(model=pod)
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
            raise SyntaxError('K8sPod.get_by_labels(): labels: [ {} ] is invalid.'.format(labels))

        pod_list = []
        selector = ",".join(['%s=%s' % (key, value) for (key, value) in labels.items()])
        data = {'labelSelector': selector}
        p = K8sPod(config=config, name=labels['name'])
        pods = p.get_with_params(data=data)

        for pod in pods:
            try:
                p = Pod(model=pod)
                k8s_pod = K8sPod(config=config, name=p.metadata.name).get()
                pod_list.append(k8s_pod)
            except NotFoundException:
                pass

        return pod_list

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        return self.model.serialize()

    def as_json(self):
        data = self.serialize()
        j = json.dumps(data, indent=4)
        return j

    def as_yaml(self):
        data = self.serialize()
        y = yaml.dump(data, default_flow_style=False)
        return y
