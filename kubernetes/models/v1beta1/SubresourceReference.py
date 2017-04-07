#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string


class SubresourceReference(object):
    """
    https://kubernetes.io/docs/api-reference/extensions/v1beta1/definitions/#_v1beta1_subresourcereference
    """

    def __init__(self, model=None):
        super(SubresourceReference, self).__init__()

        self._kind = None
        self._name = None
        self._api_version = None
        self._subresource = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'kind' in model:
            self.kind = model['kind']
        if 'name' in model:
            self.name = model['name']
        if 'apiVersion' in model:
            self.api_version = model['apiVersion']
        if 'subresource' in model:
            self.subresource = model['subresource']

    # ------------------------------------------------------------------------------------- kind

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, k=None):
        if not is_valid_string(k):
            raise SyntaxError('SubresourceReference: kind: [ {} ] is invalid.'.format(k))
        self._kind = k
        
    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n=None):
        if not is_valid_string(n):
            raise SyntaxError('SubresourceReference: name: [ {} ] is invalid.'.format(n))
        self._name = n

    # ------------------------------------------------------------------------------------- apiVersion

    @property
    def api_version(self):
        return self._api_version

    @api_version.setter
    def api_version(self, v=None):
        if not is_valid_string(v):
            raise SyntaxError('SubresourceReference: api_version: [ {} ] is invalid.'.format(v))
        self._api_version = v

    # ------------------------------------------------------------------------------------- subresource

    @property
    def subresource(self):
        return self._subresource

    @subresource.setter
    def subresource(self, s=None):
        if not is_valid_string(s):
            raise SyntaxError('SubresourceReference: subresource: [ {} ] is invalid.'.format(s))
        self._subresource = s

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.kind is not None:
            data['kind'] = self.kind
        if self.name is not None:
            data['name'] = self.name
        if self.api_version is not None:
            data['apiVersion'] = self.api_version
        if self.subresource is not None:
            data['subresource'] = self.subresource
        return data