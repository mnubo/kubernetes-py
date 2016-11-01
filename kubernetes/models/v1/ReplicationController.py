#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1 import (
    BaseModel,
    ObjectMeta,
    ReplicationControllerSpec,
    ReplicationControllerStatus
)


class ReplicationController(BaseModel):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_replicationcontroller
    """

    def __init__(self):
        super(ReplicationController, self).__init__()

        self._metadata = None
        self._spec = None
        self._status = None

        self.kind = 'ReplicationController'
        self.api_version = 'v1'

    # ------------------------------------------------------------------------------------- metadata

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata=None):
        if not isinstance(metadata, ObjectMeta):
            raise SyntaxError('ReplicationController: metadata: [ {0} ] is invalid.'.format(metadata))
        self._metadata = metadata

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

    def json(self):
        data = {}
        if self.kind:
            data['kind'] = self.kind
        if self.api_version:
            data['api_version'] = self.api_version
        if self.metadata is not None:
            data['metadata'] = self.metadata.json()
        if self.spec is not None:
            data['spec'] = self.spec.json()
        if self.status is not None:
            data['status'] = self.status.json()
        return data
