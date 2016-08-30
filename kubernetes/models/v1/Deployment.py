#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.PodBasedModel import PodBasedModel
from kubernetes.models.v1.PodSpec import PodSpec
from kubernetes.models.v1.ObjectMeta import ObjectMeta

API_VERSION = 'extensions/v1beta1'


class Deployment(PodBasedModel):

    def __init__(self, name=None, image=None, namespace='default', replicas=0, model=None):
        PodBasedModel.__init__(self)

        if name is None:
            raise SyntaxError('Deployment: name: [ {0} ] cannot be None.'.format(name))
        if not isinstance(name, str):
            raise SyntaxError('Deployment: name: [ {0} ] must be a string.'.format(name))

        if model is not None:
            self.model = model
            if 'metadata' in self.model:
                self.deployment_metadata = ObjectMeta(model=self.model['metadata'])
            if 'template' in self.model['spec']:
                self.pod_spec = PodSpec(model=self.model['spec']['template']['spec'])
                self.pod_metadata = ObjectMeta(model=self.model['spec']['template']['metadata'])

        else:
            self.model = dict(kind='Deployment', apiVersion=API_VERSION)
            self.deployment_metadata = ObjectMeta(name=name, namespace=namespace)
            self.pod_metadata = ObjectMeta(name=name, namespace=namespace)

            self.model['spec'] = {
                "replicas": replicas,
                "selector": {
                    "matchLabels": {
                        'name': name
                    }
                }
            }
            self.model['spec']['template'] = dict()

            if image is not None:
                self.pod_spec = PodSpec(name=name, image=image)
            else:
                self.pod_spec = PodSpec(name=name)

            self.pod_spec.set_restart_policy('Always')

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

    def set_selector(self, dico=None):
        if dico is None:
            raise SyntaxError('Deployment: dico: [ {0} ] cannot be None.'.format(dico))
        if not isinstance(dico, dict):
            raise SyntaxError('Deployment: dico: [ {0} ] must be a dict.'.format(dico))
        self.model['spec']['selector'] = dico
        return self

