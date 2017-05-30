#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sExceptions import NotFoundException
from kubernetes.K8sObject import K8sObject
from kubernetes.K8sPod import K8sPod
from kubernetes.models.v1beta1.ReplicaSet import ReplicaSet


class K8sReplicaSet(K8sObject):
    """
    http://kubernetes.io/docs/api-reference/extensions/v1beta1/definitions/#_v1beta1_replicaset
    """

    REVISION_ANNOTATION = 'deployment.kubernetes.io/revision'
    REVISION_HISTORY_ANNOTATION = 'deployment.kubernetes.io/revision-history'

    def __init__(self, config=None, name=None):

        super(K8sReplicaSet, self).__init__(
            config=config,
            obj_type='ReplicaSet',
            name=name
        )

    # -------------------------------------------------------------------------------------  override

    def get(self):
        self.model = ReplicaSet(self.get_model())
        return self

    def list(self, pattern=None, reverse=True):
        ls = super(K8sReplicaSet, self).list()
        rsets = list(map(lambda x: ReplicaSet(x), ls))
        if pattern is not None:
            rsets = list(filter(lambda x: pattern in x.name, rsets))
        k8s = []
        for x in rsets:
            j = K8sReplicaSet(config=self.config, name=x.name)
            j.model = x
            k8s.append(j)
        k8s.sort(key=lambda x: x.creation_timestamp, reverse=reverse)
        return k8s

    def delete(self, cascade=False):
        super(K8sReplicaSet, self).delete(cascade)
        if cascade:
            pods = K8sPod(config=self.config, name="yo").list(pattern=self.name)
            for pod in pods:
                try:
                    pod.delete(cascade)
                except NotFoundException:
                    pass
        return self

    # -------------------------------------------------------------------------------------  revision

    @property
    def revision(self):
        if self.REVISION_ANNOTATION in self.model.metadata.annotations:
            return self.model.metadata.annotations[self.REVISION_ANNOTATION]
        return None

    @revision.setter
    def revision(self, r=None):
        raise NotImplementedError(
            'K8sReplicaSet: revision is read-only.')

    # -------------------------------------------------------------------------------------  revision history

    @property
    def revision_history(self):
        if self.REVISION_HISTORY_ANNOTATION in self.model.metadata.annotations:
            comma_string = self.model.metadata.annotations[self.REVISION_HISTORY_ANNOTATION]
            version_array = comma_string.split(",")
            return map(lambda x: int(x), version_array)
        return None

    @revision_history.setter
    def revision_history(self, r=None):
        raise NotImplementedError(
            'K8sReplicaSet: revision_history is read-only.')
