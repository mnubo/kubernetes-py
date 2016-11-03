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
from kubernetes.K8sExceptions import NotFoundException, TimedOutException
from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1.Pod import Pod
from kubernetes.models.v1.PodSpec import PodSpec
from kubernetes.models.v1.PodStatus import PodStatus

POD_READY_TIMEOUT_SECONDS = 60


class K8sPod(K8sObject):
    def __init__(self, config=None, name=None):
        super(K8sPod, self).__init__(config=config, obj_type='Pod', name=name)

        self.model = Pod()

        self.model.metadata = ObjectMeta()
        self.model.metadata.name = name
        self.model.metadata.namespace = config.namespace

        self.model.spec = PodSpec()
        self.model.status = PodStatus()

        if self.config.pull_secret is not None:
            self.add_image_pull_secret(self.config.pull_secret)

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
        data = {k: v}
        annotations = self.model.metadata.annotations
        if annotations is None:
            annotations = []
        if data not in annotations:
            annotations.append(data)
            self.model.metadata.annotations = annotations
        return self

    def add_container(self, container=None):
        containers = self.model.spec.containers
        if container not in containers:
            containers.append(container)
            self.model.spec.continers = containers
        return self

    def add_label(self, k=None, v=None):
        data = {k: v}
        labels = self.model.metadata.labels
        if labels is None:
            labels = []
        if data not in labels:
            labels.append(data)
            self.model.metadata.labels = labels
        return self

    def add_image_pull_secret(self, name=None):
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
        new = filter(lambda x: k not in x, orig)
        if orig != new:
            self.model.metadata.annotations = new
        return self

    def del_label(self, k=None):
        orig = self.model.metadata.labels
        new = filter(lambda x: k not in x, orig)
        if orig != new:
            self.model.metadata.labels = new
        return self

    def del_node_name(self):
        self.model.spec.node_name = None
        return self

    # ------------------------------------------------------------------------------------- get

    def get(self):
        self.model = Pod(model=self.get_model())
        return self

    def get_annotation(self, k=None):
        ann = filter(lambda x: k in x, self.model.metadata.annotations)
        return ann

    def get_annotations(self):
        return self.model.metadata.annotations

    def get_label(self, k=None):
        label = filter(lambda x: k in x, self.model.metadata.labels)
        if label:
            return label[0][k]
        return None

    def get_labels(self):
        return self.model.metadata.labels

    def get_namespace(self):
        return self.model.get_pod_namespace()

    def get_status(self):
        self.get()
        return self.model.get_pod_status()

    def get_pod_containers(self):
        return self.model.get_pod_containers()

    def get_pod_node_name(self):
        return self.model.get_pod_node_name()

    def get_pod_node_selector(self):
        return self.model.get_pod_node_selector()

    def get_pod_restart_policy(self):
        return self.model.get_pod_restart_policy()

    def get_service_account(self):
        return self.model.get_service_account()

    def get_termination_grace_period(self):
        return self.model.get_termination_grace_period()

    # ------------------------------------------------------------------------------------- polling readiness

    def is_ready(self):
        status = self.get_status()
        if status is not None and isinstance(status, PodStatus):
            pod_phase = status.get_pod_phase()
            conditions = status.get_pod_conditions()
            conditions_ok = 0
            for cond in conditions:
                if cond.get('status', 'False') == 'True':
                    conditions_ok += 1
            if pod_phase == 'Running' and len(conditions) == conditions_ok:
                return True
        return False

    # ------------------------------------------------------------------------------------- set

    def set_annotations(self, annotations=None):
        self.model.set_pod_annotations(annotations)
        return self

    def set_labels(self, labels=None):
        self.model.set_pod_labels(labels)
        return self

    def set_namespace(self, namespace=None):
        self.model.set_pod_namespace(namespace)
        return self

    def set_active_deadline(self, seconds=None):
        self.model.set_active_deadline(seconds=seconds)
        return self

    def set_container_image(self, name, image=None):
        self.model.set_pod_image(name=name, image=image)
        return self

    def set_dns_policy(self, policy=None):
        self.model.set_dns_policy(policy=policy)
        return self

    def set_pod_generate_name(self, mode=None, name=None):
        self.model.set_pod_generate_name(mode=mode, name=name)
        return self

    def set_pod_node_name(self, name=None):
        self.model.set_pod_node_name(name=name)
        return self

    def set_pod_node_selector(self, selector=None):
        self.model.set_pod_node_selector(selector=selector)
        return self

    def set_pod_restart_policy(self, policy=None):
        self.model.set_pod_restart_policy(policy=policy)
        return self

    def set_service_account(self, name=None):
        self.model.set_service_account(name=name)
        return self

    def set_termination_grace_period(self, seconds=None):
        self.model.set_termination_grace_period(seconds=seconds)
        return self

    # ------------------------------------------------------------------------------------- filtering

    @staticmethod
    def get_by_name(config=None, name=None):
        if name is None:
            raise SyntaxError('K8sPod: name: [ {0} ] cannot be None.'.format(name))
        if not isinstance(name, str):
            raise SyntaxError('K8sPod: name: [ {0} ] must be a string.'.format(name))
        if config is None:
            config = K8sConfig()

        pod_list = list()
        data = {'labelSelector': 'name={0}'.format(name)}
        pods = K8sPod(config=config, name=name).get_with_params(data=data)

        for pod in pods:
            try:
                pod_name = Pod(model=pod).get_pod_name()
                pod_list.append(K8sPod(config=config, name=pod_name).get())
            except NotFoundException:
                pass

        return pod_list

    @staticmethod
    def get_by_labels(config=None, labels=None):
        if labels is None:
            raise SyntaxError('K8sPod: labels: [ {0} ] cannot be None.'.format(labels))
        if not isinstance(labels, dict):
            raise SyntaxError('K8sPod: labels: [ {0} ] must be a dict.'.format(labels))
        if config is None:
            config = K8sConfig()

        pod_list = list()
        my_labels = ",".join(['%s=%s' % (key, value) for (key, value) in labels.items()])
        data = dict(labelSelector="{labels}".format(labels=my_labels))
        pods = K8sPod(config=config, name=labels.get('name')).get_with_params(data=data)

        for pod in pods:
            try:
                pod_name = Pod(model=pod).get_pod_name()
                pod_list.append(K8sPod(config=config, name=pod_name).get())
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
