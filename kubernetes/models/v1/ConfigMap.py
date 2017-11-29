#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import re

from kubernetes.models.unversioned.BaseModel import BaseModel


class ConfigMap(BaseModel):
    """
    https://kubernetes.io/docs/api-reference/v1.8/#configmap-v1-core
    """

    def __init__(self, model=None):
        super(ConfigMap, self).__init__()

        self.kind = 'ConfigMap'
        self.api_version = 'v1'

        self._data = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        super(ConfigMap, self).build_with_model(model)

        if 'data' in model:
            self.data = model['data']

    # --------------------------------------------------------------------------------- data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, v=None):
        if not isinstance(v, dict):
            raise SyntaxError('ConfigMap: data: [ {} ] is invalid.'.format(v))
        pattern = re.compile(r'^[0-9a-zA-Z\-\.\_]+$')
        for k in v.keys():
            if not pattern.match(k):
                raise SyntaxError('ConfigMap: data: Key [ {} ] is invalid.'.format(k))
        self._data = v

    def serialize(self):
        tmp_data = super(ConfigMap, self).serialize()

        if self.data is not None:
            tmp_data['data'] = self.data
        return tmp_data
