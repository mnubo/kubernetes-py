#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1alpha1.PetSet import PetSet
from kubernetes.K8sObject import K8sObject


class K8sPetSet(K8sObject):
    """
    Warning: Starting in Kubernetes version 1.5, PetSet has been renamed to StatefulSet.

    To use (or continue to use) PetSet in Kubernetes 1.5 or higher,
    you must migrate your existing PetSets to StatefulSets.
    """

    def __init__(self, config=None, name=None):

        super(K8sPetSet, self).__init__(
            config=config,
            name=name,
            obj_type='PetSet'
        )

    # -------------------------------------------------------------------------------------  override

    def get(self):
        self.model = PetSet(model=self.get_model())
        return self

    def create(self):
        super(K8sPetSet, self).create()
        self.get()
        return self

    def update(self):
        super(K8sPetSet, self).update()
        self.get()
        return self
