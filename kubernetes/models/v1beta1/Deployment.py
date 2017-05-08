#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.unversioned.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1beta1.DeploymentSpec import DeploymentSpec
from kubernetes.models.v1beta1.DeploymentStatus import DeploymentStatus


class Deployment(BaseModel):
    """
    http://kubernetes.io/docs/api-reference/extensions/v1beta1/definitions/#_v1beta1_deployment
    """

    def __init__(self, model=None):
        super(Deployment, self).__init__()

        self.kind = 'Deployment'
        self.api_version = 'extensions/v1beta1'

        self.spec = DeploymentSpec()
        self.status = DeploymentStatus()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        super(Deployment, self).build_with_model(model)

        if 'spec' in model:
            self.spec = DeploymentSpec(model['spec'])
        if 'status' in model:
            self.status = DeploymentStatus(model['status'])

    # ------------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec=None):
        if not isinstance(spec, DeploymentSpec):
            raise SyntaxError('Deployment: spec: [ {} ] is invalid.'.format(spec))
        self._spec = spec

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status=None):
        if not isinstance(status, DeploymentStatus):
            raise SyntaxError('Deployment: status: [ {} ] is invalid.'.format(status))
        self._status = status

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(Deployment, self).serialize()
        if self.spec is not None:
            data['spec'] = self.spec.serialize()
        if self.status is not None:
            data['status'] = self.status.serialize()
        return data
