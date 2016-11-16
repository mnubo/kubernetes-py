#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1.PersistentVolumeClaimSpec import PersistentVolumeClaimSpec
from kubernetes.models.v1.PersistentVolumeClaimStatus import PersistentVolumeClaimStatus
from kubernetes.utils import is_valid_string


class PersistentVolumeClaim(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_persistentvolumeclaim
    """

    def __init__(self, model=None):
        super(PersistentVolumeClaim, self).__init__()

        self._kind = 'PersistentVolumeClaim'
        self._api_version = 'v1'
        self._metadata = ObjectMeta()
        self._spec = PersistentVolumeClaimSpec()
        self._status = PersistentVolumeClaimStatus()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'kind' in model:
            self.kind = model['kind']
        if 'apiVersion' in model:
            self.api_version = model['apiVersion']
        if 'metadata' in model:
            self.metadata = ObjectMeta(model=model['metadata'])
        if 'spec' in model:
            self.spec = PersistentVolumeClaimSpec(model=model['spec'])
        if 'status' in model:
            self.status = PersistentVolumeClaimStatus(model=model['status'])

    # ------------------------------------------------------------------------------------- kind

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, k=None):
        if not is_valid_string(k):
            raise SyntaxError('PersistentVolumeClaim: kind: [ {0} ] is invalid.'.format(k))
        self._kind = k

    # ------------------------------------------------------------------------------------- apiVersion

    @property
    def api_version(self):
        return self._api_version

    @api_version.setter
    def api_version(self, v=None):
        if not is_valid_string(v):
            raise SyntaxError('PersistentVolumeClaim: api_version: [ {0} ] is invalid.'.format(v))
        self._api_version = v

    # ------------------------------------------------------------------------------------- metadata

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, meta=None):
        if not isinstance(meta, ObjectMeta):
            raise SyntaxError('PersistentVolumeClaim: metadata: [ {0} ] is invalid.'.format(meta))
        self._metadata = meta

    # ------------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec=None):
        if not isinstance(spec, PersistentVolumeClaimSpec):
            raise SyntaxError('PersistentVolumeClaim: spec: [ {0} ] is invalid.'.format(spec))
        self._spec = spec

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status=None):
        if not isinstance(status, PersistentVolumeClaimStatus):
            raise SyntaxError('PersistentVolumeClaim: status: [ {0} ] is invalid.'.format(status))
        self._status = status

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.kind is not None:
            data['kind'] = self.kind
        if self.api_version is not None:
            data['apiVersion'] = self.api_version
        if self.metadata is not None:
            data['metadata'] = self.metadata.serialize()
        if self.spec is not None:
            data['spec'] = self.spec.serialize()
        if self.status is not None:
            data['status'] = self.status.serialize()
        return data
