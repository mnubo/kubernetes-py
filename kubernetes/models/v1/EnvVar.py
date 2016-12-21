#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.EnvVarSource import EnvVarSource
from kubernetes.utils import is_valid_string


class EnvVar(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_envvar
    """

    def __init__(self, model=None):
        super(EnvVar, self).__init__()

        self._name = None
        self._value = None
        self._value_from = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'name' in model:
            self.name = model['name']
        if 'value' in model:
            self.value = model['value']
        if 'valueFrom' in model:
            self.value_from = EnvVarSource(model['valueFrom'])

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n=None):
        if not is_valid_string(n):
            raise SyntaxError('EnvVar: name: [ {} ] is invalid.'.format(n))
        self._name = n

    # ------------------------------------------------------------------------------------- value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v=None):
        if not is_valid_string(v):
            raise SyntaxError('EnvVar: value: [ {} ] is invalid.'.format(v))
        self._value = v

    # ------------------------------------------------------------------------------------- valueFrom

    @property
    def value_from(self):
        return self._value_from

    @value_from.setter
    def value_from(self, v=None):
        if not isinstance(v, EnvVarSource):
            raise SyntaxError('EnvVar: value_from: [ {} ] is invalid.'.format(v))
        self._value_from = v

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.name is not None:
            data['name'] = self.name
        if self.value is not None:
            data['value'] = self.value
        if self.value_from is not None:
            data['valueFrom'] = self.value_from.serialize()
        return data
