#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string


class ObjectFieldSelector(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_objectfieldselector
    """

    def __init__(self, model=None):
        super(ObjectFieldSelector, self).__init__()

        self._api_version = None
        self._field_path = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'apiVersion' in model:
            self.api_version = model['apiVersion']
        if 'fieldPath' in model:
            self.field_path = model['fieldPath']

    # ------------------------------------------------------------------------------------- apiVersion

    @property
    def api_version(self):
        return self._api_version

    @api_version.setter
    def api_version(self, v=None):
        if not is_valid_string(v):
            raise SyntaxError('ObjectFieldSelector: api_version: [ {} ] is invalid.'.format(v))
        self._api_version = v

    # ------------------------------------------------------------------------------------- fieldPath

    @property
    def field_path(self):
        return self._field_path

    @field_path.setter
    def field_path(self, fp=None):
        if not is_valid_string(fp):
            raise SyntaxError('ObjectFieldSelector: field_path: [ {} ] is invalid.'.format(fp))
        self._field_path = fp

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.api_version is not None:
            data['apiVersion'] = self.api_version
        if self.field_path is not None:
            data['fieldPath'] = self.field_path
        return data
