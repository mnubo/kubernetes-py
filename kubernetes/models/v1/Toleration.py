#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string


class Toleration(object):
    """
    https://kubernetes.io/docs/api-reference/v1.6/#toleration-v1-core
    """

    def __init__(self, model=None):
        super(Toleration, self).__init__()

        self._effect = None
        self._key = None
        self._operator = None
        self._toleration_seconds = None
        self._value = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'effect' in model:
            self.effect = model['effect']
        if 'key' in model:
            self.key = model['key']
        if 'operator' in model:
            self.operator = model['operator']
        if 'tolerationSeconds' in model:
            self.toleration_seconds = model['tolerationSeconds']
        if 'value' in model:
            self.value = model['value']

    # ------------------------------------------------------------------------------------- effect

    @property
    def effect(self):
        return self._effect

    @effect.setter
    def effect(self, e=None):
        if not is_valid_string(e):
            raise SyntaxError('Toleration: effect: [ {} ] is invalid'.format(e))
        self._effect = e

    # ------------------------------------------------------------------------------------- key

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, k=None):
        if not is_valid_string(k):
            raise SyntaxError('Toleration: effect: [ {} ] is invalid.'.format(k))
        self._key = k

    # ------------------------------------------------------------------------------------- operator

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, o=None):
        if not is_valid_string(o):
            raise SyntaxError('Toleration: operator: [ {} ] is invalid.'.format(o))
        self._operator = o

    # ------------------------------------------------------------------------------------- tolerationSeconds

    @property
    def toleration_seconds(self):
        return self._toleration_seconds

    @toleration_seconds.setter
    def toleration_seconds(self, ts=None):
        if not isinstance(ts, int):
            raise SyntaxError('Toleration: toleration_seconds: [ {} ] is invalid.'.format(ts))
        self._toleration_seconds = ts

    # ------------------------------------------------------------------------------------- value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v=None):
        if not is_valid_string(v):
            raise SyntaxError('Toleration: value: [ {} ] is invalid.'.format(v))
        self._value = v

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.effect is not None:
            data['effect'] = self.effect
        if self.key is not None:
            data['key'] = self.key
        if self.operator is not None:
            data['operator'] = self.operator
        if self.toleration_seconds is not None:
            data['tolerationSeconds'] = self.toleration_seconds
        if self.value is not None:
            data['value'] = self.value
        return data
