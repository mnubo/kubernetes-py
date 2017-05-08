#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.unversioned.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1beta1.DaemonSetSpec import DaemonSetSpec
from kubernetes.models.v1beta1.DaemonSetStatus import DaemonSetStatus


class DaemonSet(BaseModel):

    def __init__(self, model=None):
        super(DaemonSet, self).__init__()

        self.kind = 'DaemonSet'
        self.api_version = 'extensions/v1beta1'
        
        self.spec = DaemonSetSpec()
        self.status = DaemonSetStatus()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        super(DaemonSet, self).build_with_model(model)

        if 'spec' in model:
            self.spec = DaemonSetSpec(model['spec'])
        if 'status' in model:
            self.status = DaemonSetStatus(model['status'])

    # ------------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec=None):
        if not isinstance(spec, DaemonSetSpec):
            raise SyntaxError('DaemonSet: spec: [ {} ] is invalid.'.format(spec))
        self._spec = spec

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status=None):
        if not isinstance(status, DaemonSetStatus):
            raise SyntaxError('DaemonSet: status: [ {} ] is invalid.'.format(status))
        self._status = status

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(DaemonSet, self).serialize()

        if self.spec is not None:
            data['spec'] = self.spec.serialize()
        if self.status is not None:
            data['status'] = self.status.serialize()
        return data
