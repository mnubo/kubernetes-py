#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import time
from kubernetes.K8sPodBasedObject import K8sPodBasedObject
from kubernetes.models.v1.Pod import Pod
from kubernetes.models.v1.PodStatus import PodStatus
from kubernetes.K8sExceptions import NotFoundException, TimedOutException
from kubernetes import K8sConfig

POD_READY_TIMEOUT_SECONDS = 60


class K8sPod(K8sPodBasedObject):

    def __init__(self, config=None, name=None):
        super(K8sPod, self).__init__(config=config, obj_type='Pod', name=name)

        self.model = Pod(name=name, namespace=self.config.namespace)
        if self.config.pull_secret is not None:
            self.model.add_image_pull_secrets(name=self.config.pull_secret)

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
        self.model.add_pod_annotation(k=k, v=v)
        return self

    def add_label(self, k=None, v=None):
        self.model.add_pod_label(k=k, v=v)
        return self

    # ------------------------------------------------------------------------------------- delete

    def del_annotation(self, k=None):
        self.model.del_pod_annotation(k=k)
        return self

    def del_label(self, k=None):
        self.model.del_pod_label(k=k)
        return self

    # ------------------------------------------------------------------------------------- get

    def get(self):
        self.model = Pod(model=self.get_model())
        return self

    def get_annotation(self, k=None):
        return self.model.get_pod_annotation(k=k)

    def get_annotations(self):
        return self.model.get_pod_annotations()

    def get_label(self, k=None):
        return self.model.get_pod_label(k=k)

    def get_labels(self):
        return self.model.get_pod_labels()

    def get_namespace(self):
        return self.model.get_pod_namespace()

    def get_status(self):
        self.get()
        return self.model.get_pod_status()

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
