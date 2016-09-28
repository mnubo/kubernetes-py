#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes import K8sObject
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1.PersistentVolumeSpec import PersistentVolumeSpec


class K8sPersistentVolume(K8sObject):

    def __init__(self, config=None, name=None, model=None):

        super(K8sPersistentVolume, self).__init__(config=config, name=name, obj_type='PersistentVolume')

        if model is not None:
            self.model = PersistentVolumeSpec
            self.meta = ObjectMeta(model['meta'])
            self.spec = PersistentVolumeSpec(model['spec'])

        if model is None:
            pass
