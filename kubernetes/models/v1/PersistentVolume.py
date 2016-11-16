#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1.PersistentVolumeSpec import PersistentVolumeSpec
from kubernetes.models.v1.PersistentVolumeStatus import PersistentVolumeStatus


class PersistentVolume(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_persistentvolume
    """

    def __init__(self, model=None):
        super(PersistentVolume, self).__init__()

        self._kind = 'PersistentVolume'
        self._api_version = 'v1'
        self._metadata = ObjectMeta()
        self._spec = PersistentVolumeSpec()
        self._status = PersistentVolumeStatus()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'kind' in model:
            self.kind = model['kind']
        if 'apiVersion' in model:
            self.api_version = model['apiVersion']
        if 'metadata' in model:
            self.metadata = ObjectMeta(model=model['metadata'])
        if 'spec' in model:
            self.spec = PersistentVolumeSpec(model=model['spec'])
        if 'status' in model:
            self.status = PersistentVolumeStatus(model=model['status'])

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.kind is not None:
            data['kind'] = self.kind
        if self.api_version is not None:
            data['apiVersion'] = self.api_version
        if self.metadata is not None:
            data['metadata'] = self.metadata.serialize()
        if self.spec is not None:
            data['spec'] = self.spec.serialize()
        if self.status is not None:
            data['status'] = self.status.serialize()
        return data
