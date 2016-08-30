#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.PodBasedModel import PodBasedModel


class ReplicaSet(PodBasedModel):
    """
    A K8sReplicaSet object is primarily used for HTTP DELETE operations.

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

    def __init__(self, name=None, image=None, namespace='default', replicas=1, model=None):
        PodBasedModel.__init__(self)
