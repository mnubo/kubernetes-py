#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string


class SecretKeySelector(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_secretkeyselector
    """

    def __init__(self, model=None):
        super(SecretKeySelector, self).__init__()

        self._name = None
        self._key = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'name' in model:
            self.name = model['name']
        if 'key' in model:
            self.key = model['key']

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n=None):
        if not is_valid_string(n):
            raise SyntaxError('SecretKeySelector: name: [ {} ] is invalid.'.format(n))
        self._name = n

    # ------------------------------------------------------------------------------------- key

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, k=None):
        if not is_valid_string(k):
            raise SyntaxError('SecretKeySelector: key: [ {} ] is invalid.'.format(k))
        self._key = k

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.name is not None:
            data['name'] = self.name
        if self.key is not None:
            data['key'] = self.key
        return data
