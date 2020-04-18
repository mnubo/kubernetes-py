#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes_py.K8sObject import K8sObject
from kubernetes_py.models.v1alpha1.PetSet import PetSet
from kubernetes_py.utils import is_reachable, sanitize_version_number


class K8sPetSet(K8sObject):
    """
    Starting in Kubernetes version 1.5, PetSet has been refactored into StatefulSet.

    To continue to use PetSets in Kubernetes 1.5 or higher, you must migrate your existing PetSets to StatefulSets.
    See https://kubernetes.io/docs/tasks/manage-stateful-set/upgrade-pet-set-to-stateful-set/
    """

    def __init__(self, config=None, name=None):

        if config and is_reachable(config):
            temp = K8sObject(config=config, obj_type="Pod", name="temp")
            v = temp.server_version()
            major_vernum = sanitize_version_number(v["major"])
            minor_vernum = sanitize_version_number(v["minor"])
            if major_vernum <= 1 and minor_vernum < 4:
                raise NotImplementedError("PetSets exist only on Kubernetes == 1.4.x.")
            if major_vernum >= 1 and minor_vernum >= 5:
                raise NotImplementedError("PetSets were refactored into StatefulSets on Kubernetes >= 1.5.x.")

        super(K8sPetSet, self).__init__(config=config, name=name, obj_type="PetSet")

    # -------------------------------------------------------------------------------------  override

    def get(self):
        self.model = PetSet(self.get_model())
        return self

    def create(self):
        super(K8sPetSet, self).create()
        self.get()
        return self

    def update(self):
        super(K8sPetSet, self).update()
        self.get()
        return self

    def list(self, pattern=None):
        ls = super(K8sPetSet, self).list()
        pets = list(map(lambda x: PetSet(x), ls))
        if pattern is not None:
            pets = list(filter(lambda x: pattern in x.name, pets))
        k8s = []
        for x in pets:
            j = K8sPetSet(config=self.config, name=x.name)
            j.model = x
            k8s.append(j)
        return k8s
