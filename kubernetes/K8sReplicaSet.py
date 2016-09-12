#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sPodBasedObject import K8sPodBasedObject
from kubernetes.models.v1.ReplicaSet import ReplicaSet


class K8sReplicaSet(K8sPodBasedObject):
    """
    This module uses K8sReplicaSet for HTTP DELETE operations.

    From http://kubernetes.io/docs/user-guide/replicasets/:

    While Replica Sets can be used independently, today it’s mainly used by Deployments as
    a mechanism to orchestrate pod creation, deletion and updates. When you use Deployments
    you don’t have to worry about managing the Replica Sets that they create.
    Deployments own and manage their Replica Sets.

    A Replica Set ensures that a specified number of pod “replicas” are running at any given time.
    However, a Deployment is a higher-level concept that manages Replica Sets and provides declarative
    updates to pods along with a lot of other useful features. Therefore, we recommend using Deployments
    instead of directly using Replica Sets, unless you require custom update orchestration or don’t
    require updates at all.

    This actually means that you may never need to manipulate Replica Set objects: use directly a
    Deployment and define your application in the spec section.

    """

    def __init__(self, config=None, name=None):
        super(K8sReplicaSet, self).__init__(config=config, obj_type='ReplicaSet', name=name)
        self.model = ReplicaSet(name=name, namespace=self.config.namespace)

    # -------------------------------------------------------------------------------------  get

    def get(self):
        self.model = ReplicaSet(model=self.get_model())
        return self
