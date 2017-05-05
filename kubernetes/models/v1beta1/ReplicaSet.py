#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.unversioned.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1beta1.ReplicaSetSpec import ReplicaSetSpec
from kubernetes.models.v1beta1.ReplicaSetStatus import ReplicaSetStatus


class ReplicaSet(BaseModel):
    """
    http://kubernetes.io/docs/api-reference/extensions/v1beta1/definitions/#_v1beta1_replicaset
    """

    def __init__(self, model=None):
        super(ReplicaSet, self).__init__()

        self.kind = 'ReplicaSet'
        self.api_version = 'extensions/v1beta1'

        self.spec = ReplicaSetSpec()
        self.status = ReplicaSetStatus()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        super(ReplicaSet, self).build_with_model(model)

        if 'spec' in model:
            self.spec = ReplicaSetSpec(model['spec'])
        if 'status' in model:
            self.status = ReplicaSetStatus(model['status'])

    # ------------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec=None):
        if not isinstance(spec, ReplicaSetSpec):
            raise SyntaxError('ReplicaSet: spec: [ {} ] is invalid.'.format(spec))
        self._spec = spec

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status=None):
        if not isinstance(status, ReplicaSetStatus):
            raise SyntaxError('ReplicaSet: status: [ {} ] is invalid.'.format(status))
        self._status = status

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(ReplicaSet, self).serialize()

        if self.spec is not None:
            data['spec'] = self.spec.serialize()
        if self.status is not None:
            data['status'] = self.status.serialize()
        return data
