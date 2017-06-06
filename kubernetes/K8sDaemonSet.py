#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1beta1.DaemonSet import DaemonSet
from kubernetes.models.v1beta1.LabelSelector import LabelSelector
from kubernetes.K8sContainer import K8sContainer
from kubernetes.K8sVolume import K8sVolume


class K8sDaemonSet(K8sObject):

    def __init__(self, config=None, name=None):

        super(K8sDaemonSet, self).__init__(
            config=config,
            name=name,
            obj_type='DaemonSet'
        )

        self.model.spec.template.metadata.labels = self.model.metadata.labels

        sel = LabelSelector()
        sel.match_labels = {'name': name}
        self.selector = sel

    # -------------------------------------------------------------------------------------  override

    def create(self):
        super(K8sDaemonSet, self).create()
        self.get()
        return self

    def update(self):
        super(K8sDaemonSet, self).update()
        self.get()
        return self

    def list(self, pattern=None):
        ls = super(K8sDaemonSet, self).list()
        daemons = list(map(lambda x: DaemonSet(x), ls))
        if pattern is not None:
            daemons = list(filter(lambda x: pattern in x.name, daemons))
        k8s = []
        for x in daemons:
            j = K8sDaemonSet(config=self.config, name=x.name)
            j.model = x
            k8s.append(j)
        return k8s

    # -------------------------------------------------------------------------------------  get

    def get(self):
        self.model = DaemonSet(self.get_model())
        return self

    # -------------------------------------------------------------------------------------  add

    def add_container(self, container=None):
        if not isinstance(container, K8sContainer):
            raise SyntaxError(
                'K8sDaemonSet.add_container() container: [ {0} ] is invalid.'.format(container))

        containers = self.model.spec.template.spec.containers
        if containers is None:
            containers = []
        filtered = list(filter(lambda x: x.name != container.name, containers))
        filtered.append(container.model)
        self.model.spec.template.spec.containers = filtered
        return self

    def add_image_pull_secrets(self, secrets=None):
        self.model.spec.template.spec.add_image_pull_secrets(secrets)
        return self

    def add_volume(self, volume=None):
        if not isinstance(volume, K8sVolume):
            raise SyntaxError(
                'K8sDaemonSet.add_volume() volume: [ {0} ] is invalid.'.format(volume))

        volumes = self.model.spec.template.spec.volumes
        if volume.model not in volumes:
            volumes.append(volume.model)
        self.model.spec.template.spec.volumes = volumes
        return self

    # -------------------------------------------------------------------------------------  selector

    @property
    def selector(self):
        return self.model.spec.selector

    @selector.setter
    def selector(self, selector=None):
        self.model.spec.selector = selector
