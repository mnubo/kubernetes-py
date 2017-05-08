#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.unversioned.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1.NamespaceSpec import NamespaceSpec
from kubernetes.models.v1.NamespaceStatus import NamespaceStatus


class Namespace(BaseModel):
    """
    https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_namespace
    """

    def __init__(self, model=None):
        super(Namespace, self).__init__()

        self.kind = 'Namespace'
        self.api_version = 'v1'
        self.spec = NamespaceSpec()
        self.status = NamespaceStatus()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        super(Namespace, self).build_with_model(model)

        if 'spec' in model:
            self.spec = NamespaceSpec(model['spec'])
        if 'status' in model:
            self.status = NamespaceStatus(model['status'])

    # --------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, s=None):
        if not isinstance(s, NamespaceSpec):
            raise SyntaxError('Namespace: spec: [ {} ] is invalid.'.format(s))
        self._spec = s

    # --------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, s=None):
        if not isinstance(s, NamespaceStatus):
            raise SyntaxError('Job: status: [ {} ] is invalid.'.format(s))
        self._status = s

    # --------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(Namespace, self).serialize()
        if self.spec is not None:
            data['spec'] = self.spec.serialize()
        if self.status is not None:
            data['status'] = self.status.serialize()
        return data
