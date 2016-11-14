#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1beta1.ReplicaSet import ReplicaSet


class K8sReplicaSet(K8sObject):
    """
    http://kubernetes.io/docs/api-reference/extensions/v1beta1/definitions/#_v1beta1_replicaset
    """

    def __init__(self, config=None, name=None):
        super(K8sReplicaSet, self).__init__(config=config, obj_type='ReplicaSet', name=name)

    # -------------------------------------------------------------------------------------  get

    def get(self):
        self.model = ReplicaSet(model=self.get_model())
        return self
