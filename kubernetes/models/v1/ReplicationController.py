#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.unversioned.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1.ReplicationControllerSpec import ReplicationControllerSpec
from kubernetes.models.v1.ReplicationControllerStatus import ReplicationControllerStatus


class ReplicationController(BaseModel):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_replicationcontroller
    """

    def __init__(self, model=None):
        super(ReplicationController, self).__init__()

        self.kind = 'ReplicationController'
        self.api_version = 'v1'
        self.spec = ReplicationControllerSpec()
        self.status = ReplicationControllerStatus()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        super(ReplicationController, self).build_with_model(model)

        if 'spec' in model:
            self.spec = ReplicationControllerSpec(model['spec'])
        if 'status' in model:
            self.status = ReplicationControllerStatus(model['status'])

    # ------------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec=None):
        if not isinstance(spec, ReplicationControllerSpec):
            raise SyntaxError('ReplicationController: spec: [ {0} ] is invalid.'.format(spec))
        self._spec = spec

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status=None):
        if not isinstance(status, ReplicationControllerStatus):
            raise SyntaxError('ReplicationController: status: [ {0} ] is invalid.'.format(status))
        self._status = status

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(ReplicationController, self).serialize()

        if self.spec is not None:
            data['spec'] = self.spec.serialize()
        if self.status is not None:
            data['status'] = self.status.serialize()
        return data
