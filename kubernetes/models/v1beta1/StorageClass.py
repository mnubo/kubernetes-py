#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.unversioned.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.utils import is_valid_string, is_valid_dict


class StorageClass(BaseModel):
    """
    https://github.com/kubernetes/kubernetes/tree/master/examples/persistent-volume-provisioning/
    https://kubernetes.io/docs/user-guide/persistent-volumes/#storageclasses
    """

    def __init__(self, model=None):
        super(StorageClass, self).__init__()

        self._kind = 'StorageClass'
        self._api_version = 'storage.k8s.io/v1beta1'

        self._metadata = ObjectMeta()
        self._provisioner = None
        self._parameters = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        super(StorageClass, self).build_with_model(model)

        if 'provisioner' in model:
            self.provisioner = model['provisioner']
        if 'parameters' in model:
            self.parameters = model['parameters']

    # ------------------------------------------------------------------------------------- kind

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, k=None):
        if not is_valid_string(k):
            raise SyntaxError('StorageClass: kind: [ {} ] is invalid.'.format(k))
        self._kind = k

    # ------------------------------------------------------------------------------------- apiVersion

    @property
    def api_version(self):
        return self._api_version

    @api_version.setter
    def api_version(self, v=None):
        if not is_valid_string(v):
            raise SyntaxError('StorageClass: api_version: [ {} ] is invalid.'.format(v))
        self._api_version = v

    # ------------------------------------------------------------------------------------- metadata

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, meta=None):
        if not isinstance(meta, ObjectMeta):
            raise SyntaxError('StorageClass: metadata: [ {} ] is invalid.'.format(meta))
        self._metadata = meta

    # ------------------------------------------------------------------------------------- provisioner

    @property
    def provisioner(self):
        return self._provisioner

    @provisioner.setter
    def provisioner(self, p=None):
        if not is_valid_string(p):
            raise SyntaxError('StorageClass: provisioner: [ {} ] is invalid.'.format(p))
        self._provisioner = p

    # ------------------------------------------------------------------------------------- parameters

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, p=None):
        if not is_valid_dict(p):
            raise SyntaxError('StorageClass: parameters: [ {} ] is invalid.'.format(p))
        self._parameters = p

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(StorageClass, self).serialize()

        if self.provisioner is not None:
            data['provisioner'] = self.provisioner
        if self.parameters is not None:
            data['parameters'] = self.parameters
        return data
