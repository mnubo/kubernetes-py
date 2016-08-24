#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.PodBasedModel import PodBasedModel
from kubernetes.models.v1.PodSpec import PodSpec
from kubernetes.models.v1.ObjectMeta import ObjectMeta


class Deployment(PodBasedModel):

    def __init__(self, name=None, image=None, namespace='default', replicas=1, model=None):
        PodBasedModel.__init__(self)

        if name is None:
            raise SyntaxError('Deployment: name: [ {0} ] cannot be None.'.format(name))
        if not isinstance(name, str):
            raise SyntaxError('Deployment: name: [ {0} ] must be a string.'.format(name))

        self.model = dict(kind='Deployment', apiVersion='v1')
        self.deployment_metadata = ObjectMeta(name=name, namespace=namespace)

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
        self.model['metadata'] = self.deployment_metadata.get()
        if self.pod_metadata is not None:
            if 'template' not in self.model['spec']:
                self.model['spec']['template'] = dict()
            self.model['spec']['template']['metadata'] = self.pod_metadata.get()
        if self.pod_spec is not None:
            if 'template' not in self.model['spec']:
                self.model['spec']['template'] = dict()
            self.model['spec']['template']['spec'] = self.pod_spec.get()
        return self

    def set_replicas(self, replicas=None):
        if replicas is None:
            raise SyntaxError('Deployment: replicas: [ {0} ] cannot be None.'.format(replicas))
        if not isinstance(replicas, int) or replicas < 0:
            raise SyntaxError('Deployment: replicas: [ {0} ] must be a positive integer.'.format(replicas))
        self.model['spec']['replicas'] = replicas
        return self

