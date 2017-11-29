#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, filter_model


class ConfigMapEnvSource(object):
    """
    https://kubernetes.io/docs/api-reference/v1.8/#configmapenvsource-v1-core

    ConfigMapEnvSource selects a ConfigMap to populate the environment variables with.

    The contents of the target ConfigMap's Data field will represent the key-value pairs as environment variables.
    """

    def __init__(self, model=None):
        super(ConfigMapEnvSource, self).__init__()

        self._name = None
        self._optional = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'name' in model:
            self.name = model['name']
        if 'optional' in model:
            self.optional = model['optional']

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('ConfigMapVolumeSource: name: [ {0} ] is invalid.'.format(name))
        self._name = name

    # ------------------------------------------------------------------------------------- optional

    @property
    def optional(self):
        return self._optional

    @optional.setter
    def optional(self, v=None):
        if not isinstance(v, bool):
            raise SyntaxError('ConfigMapVolumeSource: optional: [ {0} ] is invalid.'.format(v))
        self._optional = v

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.name is not None:
            data['name'] = self.name
        if self.optional is not None:
            data['optional'] = self.optional
        return data
