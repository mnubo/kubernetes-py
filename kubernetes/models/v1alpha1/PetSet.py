#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.unversioned.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1alpha1.PetSetSpec import PetSetSpec
from kubernetes.models.v1alpha1.PetSetStatus import PetSetStatus


class PetSet(BaseModel):
    """
    http://kubernetes.io/docs/api-reference/apps/v1alpha1/definitions/#_v1alpha1_petset
    """

    def __init__(self, model=None):
        super(PetSet, self).__init__()

        self._kind = 'PetSet'
        self._api_version = 'apps/v1alpha1'

        self._spec = PetSetSpec()
        self._status = PetSetStatus()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model):
        super(PetSet, self).build_with_model(model)

        if 'spec' in model:
            self.spec = PetSetSpec(model['spec'])
        if 'status' in model:
            self.status = PetSetStatus(model['status'])

    # ------------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec=None):
        if not isinstance(spec, PetSetSpec):
            raise SyntaxError('PetSet: spec: [ {} ] is invalid.'.format(spec))
        self._spec = spec

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status=None):
        if not isinstance(status, PetSetStatus):
            raise SyntaxError('PetSet: status: [ {} ] is invalid.'.format(status))
        self._status = status

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(PetSet, self).serialize()

        if self.spec is not None:
            data['spec'] = self.spec.serialize()
        if self.status is not None:
            data['status'] = self.status.serialize()
        return data
