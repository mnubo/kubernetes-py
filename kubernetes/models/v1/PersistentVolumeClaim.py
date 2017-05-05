#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.unversioned.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1.PersistentVolumeClaimSpec import PersistentVolumeClaimSpec
from kubernetes.models.v1.PersistentVolumeClaimStatus import PersistentVolumeClaimStatus


class PersistentVolumeClaim(BaseModel):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_persistentvolumeclaim
    """

    def __init__(self, model=None):
        super(PersistentVolumeClaim, self).__init__()

        self.kind = 'PersistentVolumeClaim'
        self.api_version = 'v1'
        self.spec = PersistentVolumeClaimSpec()
        self.status = PersistentVolumeClaimStatus()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        super(PersistentVolumeClaim, self).build_with_model(model)

        if 'spec' in model:
            self.spec = PersistentVolumeClaimSpec(model['spec'])
        if 'status' in model:
            self.status = PersistentVolumeClaimStatus(model['status'])

    # ------------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec=None):
        if not isinstance(spec, PersistentVolumeClaimSpec):
            raise SyntaxError('PersistentVolumeClaim: spec: [ {0} ] is invalid.'.format(spec))
        self._spec = spec

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status=None):
        if not isinstance(status, PersistentVolumeClaimStatus):
            raise SyntaxError('PersistentVolumeClaim: status: [ {0} ] is invalid.'.format(status))
        self._status = status

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(PersistentVolumeClaim, self).serialize()

        if self.spec is not None:
            data['spec'] = self.spec.serialize()
        if self.status is not None:
            data['status'] = self.status.serialize()
        return data
