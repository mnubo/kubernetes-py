#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1.ReplicationControllerSpec import ReplicationControllerSpec
from kubernetes.models.v1.ReplicationControllerStatus import ReplicationControllerStatus


class ReplicationController(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_replicationcontroller
    """

    def __init__(self, model=None):
        super(ReplicationController, self).__init__()

        self._metadata = ObjectMeta()
        self._spec = ReplicationControllerSpec()
        self._status = ReplicationControllerStatus()

        self.kind = 'ReplicationController'
        self.api_version = 'v1'

        if model is not None:
            self._build_with_model(model)

    def __eq__(self, other):
        # see https://github.com/kubernetes/kubernetes/blob/release-1.3/docs/design/identifiers.md
        if isinstance(other, self.__class__):
            # Uniquely name (via a name) an object across space.
            return self.metadata.name == other.metadata.name and \
                   self.metadata.namespace == other.metadata.namespace
        return NotImplemented

    def _build_with_model(self, model=None):
        if 'metadata' in model:
            self.metadata = ObjectMeta(model=model['metadata'])
        if 'spec' in model:
            self.spec = ReplicationControllerSpec(model=model['spec'])
        if 'status' in model:
            self.status = ReplicationControllerStatus(model=model['status'])

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

    def serialize(self):
        data = {}
        if self.kind:
            data['kind'] = self.kind
        if self.api_version:
            data['apiVersion'] = self.api_version
        if self.metadata is not None:
            data['metadata'] = self.metadata.serialize()
        if self.spec is not None:
            data['spec'] = self.spec.serialize()
        if self.status is not None:
            data['status'] = self.status.serialize()
        return data
