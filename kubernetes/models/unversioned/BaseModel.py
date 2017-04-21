#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.utils import is_valid_string


class BaseModel(object):

    def __init__(self, model=None):
        super(BaseModel, self).__init__()

        self._api_version = None
        self._kind = None
        self._metadata = ObjectMeta()
        self._spec = None
        self._status = None

        if model is not None:
            self.build_with_model(model)

    def build_with_model(self, model=None):
        if 'apiVersion' in model:
            self.api_version = model['apiVersion']
        if 'kind' in model:
            self.kind = model['kind']
        if 'metadata' in model:
            self.metadata = ObjectMeta(model['metadata'])

    def __eq__(self, other):
        # see https://github.com/kubernetes/kubernetes/blob/master/docs/design/identifiers.md
        if isinstance(other, self.__class__):
            return self.metadata.namespace == other.metadata.namespace \
                   and self.metadata.name == other.metadata.name
        return NotImplemented

    # ------------------------------------------------------------------------------------- apiVersion

    @property
    def api_version(self):
        return self._api_version

    @api_version.setter
    def api_version(self, v=None):
        if not is_valid_string(v):
            raise SyntaxError('BaseModel: api_version: [ {} ] is invalid.'.format(v))
        self._api_version = v

    # ------------------------------------------------------------------------------------- kind

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, k=None):
        if not is_valid_string(k):
            raise SyntaxError('BaseModel: kind: [ {} ] is invalid.'.format(k))
        self._kind = k

    # ------------------------------------------------------------------------------------- metadata

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, meta=None):
        if not isinstance(meta, ObjectMeta):
            raise SyntaxError('BaseModel: metadata: [ {} ] is invalid.'.format(meta))
        self._metadata = meta

    # ------------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, s=None):
        self._spec = s

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, s=None):
        self._status = s

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self.metadata.name

    @name.setter
    def name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('BaseModel: name: [ {} ] is invalid.'.format(name))
        self.metadata.name = name
        self.metadata.labels.update({'name': name})

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.api_version is not None:
            data['apiVersion'] = self.api_version
        if self.kind is not None:
            data['kind'] = self.kind
        if self.metadata is not None:
            data['metadata'] = self.metadata.serialize()
        return data
