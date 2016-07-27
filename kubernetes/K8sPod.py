#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sPodBasedObject import K8sPodBasedObject
from kubernetes.models.v1.Pod import Pod
from kubernetes.models.v1.PodStatus import PodStatus
from kubernetes.K8sExceptions import NotFoundException


class K8sPod(K8sPodBasedObject):

    def __init__(self, config=None, name=None):
        K8sPodBasedObject.__init__(self, config=config, obj_type='Pod', name=name)
        self.model = Pod(name=name, namespace=self.config.namespace)

        if self.config.pull_secret is not None:
            self.model.add_image_pull_secrets(name=self.config.pull_secret)

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
        return self.model.get_pod_status()

    # ------------------------------------------------------------------------------------- polling readiness

    def is_ready(self):
        ready = False
        status = self.get_status()
        if status is not None:
            assert isinstance(status, PodStatus)
            pod_phase = status.get_pod_phase()
            conditions = status.get_pod_conditions()
            conditions_ok = 0
            for cond in conditions:
                assert isinstance(cond, dict)
                cond_type = cond.get('type', '')
                cond_status = cond.get('status', 'False')
                if cond_status == 'True' and cond_type == 'Ready':
                    conditions_ok += 1
            if pod_phase == 'Running' and len(conditions) == conditions_ok:
                ready = True
        return ready

    # ------------------------------------------------------------------------------------- set

    def set_annotations(self, dico=None):
        self.model.set_pod_annotations(new_dict=dico)
        return self

    def set_labels(self, dico=None):
        self.model.set_pod_labels(dico=dico)
        return self

    def set_namespace(self, name=None):
        self.model.set_pod_namespace(name=name)
        return self

    # ------------------------------------------------------------------------------------- filtering

    @staticmethod
    def get_by_name(config=None, name=None):
        if name is None:
            raise SyntaxError('K8sPod: name: [ {0} ] cannot be None.'.format(name))
        if not isinstance(name, str):
            raise SyntaxError('K8sPod: name: [ {0} ] must be a string.'.format(name))

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
