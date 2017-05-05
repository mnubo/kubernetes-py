#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.unversioned.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1beta1.StatefulSetSpec import StatefulSetSpec
from kubernetes.models.v1beta1.StatefulSetStatus import StatefulSetStatus


class StatefulSet(BaseModel):

    def __init__(self, model=None):
        super(StatefulSet, self).__init__()

        self.kind = 'StatefulSet'
        self.api_version = 'apps/v1beta1'

        self.spec = StatefulSetSpec()
        self.status = StatefulSetStatus()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        super(StatefulSet, self).build_with_model(model)

        if 'spec' in model:
            self.spec = StatefulSetSpec(model['spec'])
        if 'status' in model:
            self.status = StatefulSetStatus(model['status'])

    # ------------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec=None):
        if not isinstance(spec, StatefulSetSpec):
            raise SyntaxError('DaemonSet: spec: [ {} ] is invalid.'.format(spec))
        self._spec = spec

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status=None):
        if not isinstance(status, StatefulSetStatus):
            raise SyntaxError('DaemonSet: status: [ {} ] is invalid.'.format(status))
        self._status = status

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(StatefulSet, self).serialize()

        if self.spec is not None:
            data['spec'] = self.spec.serialize()
        if self.status is not None:
            data['status'] = self.status.serialize()
        return data
