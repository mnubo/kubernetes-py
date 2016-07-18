#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.PodBasedModel import PodBasedModel
from kubernetes.models.v1.PodSpec import PodSpec
from kubernetes.models.v1.ObjectMeta import ObjectMeta


class ReplicationController(PodBasedModel):
    def __init__(self, name=None, image=None, namespace='default', replicas=1, model=None):
        PodBasedModel.__init__(self)
        if model is not None:
            assert isinstance(model, dict)
            self.model = model
            if 'status' in self.model:
                self.model.pop('status', None)
            if 'metadata' in self.model:
                self.rc_metadata = ObjectMeta(model=self.model['metadata'])
            if 'template' in self.model['spec']:
                self.pod_spec = PodSpec(model=self.model['spec']['template']['spec'])
                self.pod_metadata = ObjectMeta(model=self.model['spec']['template']['metadata'])
        else:
            if name is None:
                raise SyntaxError('ReplicationController: name: [ {0} ] cannot be None.'.format(name))
            if not isinstance(name, str):
                raise SyntaxError('ReplicationController: name: [ {0} ] must be a string.'.format(name))

            self.model = dict(kind='ReplicationController', apiVersion='v1')
            self.rc_metadata = ObjectMeta(name=name, namespace=namespace)

            self.model['spec'] = {
                "replicas": replicas,
                "selector": dict(name=name)
            }

            self.model['spec']['template'] = dict()
            if image is not None:
                self.pod_spec = PodSpec(name=name, image=image)
            else:
                self.pod_spec = PodSpec(name=name)
            self.pod_spec.set_restart_policy('Always')
            self.pod_metadata = ObjectMeta(name=name, namespace=namespace)
            self._update_model()

    def _update_model(self):
        self.model['metadata'] = self.rc_metadata.get()
        if self.pod_metadata is not None:
            if 'template' not in self.model['spec']:
                self.model['spec']['template'] = dict()
            self.model['spec']['template']['metadata'] = self.pod_metadata.get()
        if self.pod_spec is not None:
            if 'template' not in self.model['spec']:
                self.model['spec']['template'] = dict()
            self.model['spec']['template']['spec'] = self.pod_spec.get()
        return self

    def add_label(self, k, v):
        assert isinstance(k, str)
        assert isinstance(v, str)
        self.rc_metadata.add_label(k=k, v=v)
        return self

    def add_annotation(self, k, v):
        assert isinstance(k, str)
        assert isinstance(v, str)
        self.rc_metadata.add_annotation(k=k, v=v)
        return self

    def del_annotation(self, k):
        assert isinstance(k, str)
        self.rc_metadata.del_annotation(k=k)
        return self

    def del_label(self, k):
        assert isinstance(k, str)
        self.rc_metadata.del_label(k=k)
        return self

    def get_annotation(self, k):
        assert isinstance(k, str)
        return self.rc_metadata.get_annotation(k=k)

    def get_annotations(self):
        return self.rc_metadata.get_annotations()

    def get_label(self, k):
        assert isinstance(k, str)
        return self.rc_metadata.get_label(k=k)

    def get_labels(self):
        return self.rc_metadata.get_labels()

    def get_name(self):
        return self.rc_metadata.get_name()

    def get_namespace(self):
        return self.rc_metadata.get_namespace()

    def get_replicas(self):
        my_replicas = self.model['spec']['replicas']
        return my_replicas

    def get_selector(self):
        return self.model['spec']['selector']

    def set_annotations(self, new_dict):
        assert isinstance(new_dict, dict)
        self.rc_metadata.set_annotations(dico=new_dict)
        return self

    def set_labels(self, new_dict):
        assert isinstance(new_dict, dict)
        self.rc_metadata.set_labels(dico=new_dict)
        return self

    def set_name(self, name):
        assert isinstance(name, str)
        self.rc_metadata.set_name(name=name)
        return self

    def set_namespace(self, name):
        assert isinstance(name, str)
        self.rc_metadata.set_namespace(name=name)
        self.pod_metadata.set_namespace(name=name)
        return self

    def set_replicas(self, replicas=None):
        if replicas is None or not isinstance(replicas, int):
            raise SyntaxError('ReplicationController: replicas should be a positive integer value')
        self.model['spec']['replicas'] = replicas
        return self

    def set_selector(self, selector=None):
        if selector is None or not isinstance(selector, dict):
            raise SyntaxError('ReplicationController: Selector should be a dict of key, value pairs.')
        self.model['spec']['selector'] = selector
        return self
