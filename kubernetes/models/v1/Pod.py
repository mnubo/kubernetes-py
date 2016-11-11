#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1.PodSpec import PodSpec
from kubernetes.models.v1.PodStatus import PodStatus
from kubernetes.utils import filter_model


class Pod(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_pod
    """

    def __init__(self, model=None):
        super(Pod, self).__init__()

        self._metadata = ObjectMeta()
        self._spec = PodSpec()
        self._status = PodStatus()

        self.kind = 'Pod'
        self.api_version = 'v1'

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def __eq__(self, other):
        # see https://github.com/kubernetes/kubernetes/blob/release-1.3/docs/design/identifiers.md
        if isinstance(other, self.__class__):
            # Uniquely name (via a name) an object across space.
            return self.metadata.namespace == other.metadata.namespace \
                   and self.metadata.name == other.metadata.name
        return NotImplemented

    def _build_with_model(self, model=None):
        if 'kind' in model:
            self.kind = model['kind']
        if 'apiVersion' in model:
            self.api_version = model['apiVersion']
        if 'metadata' in model:
            metadata = ObjectMeta(model=model['metadata'])
            self.metadata = metadata
        if 'spec' in model:
            spec = PodSpec(model=model['spec'])
            self.spec = spec
        if 'status' in model:
            status = PodStatus(model=model['status'])
            self.status = status

    # ------------------------------------------------------------------------------------- metadata

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata=None):
        if not isinstance(metadata, ObjectMeta):
            raise SyntaxError('Pod: metadata: [ {0} ] is invalid.'.format(metadata))
        self._metadata = metadata

    # ------------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec=None):
        if not isinstance(spec, PodSpec):
            raise SyntaxError('Pod: spec: [ {0} ] is invalid.'.format(spec))
        self._spec = spec

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status=None):
        if not isinstance(status, PodStatus):
            raise SyntaxError('Pod: status: [ {0} ] is invalid.'.format(status))
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
