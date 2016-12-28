#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string


class LocalObjectReference(object):

    def __init__(self, model=None):
        super(LocalObjectReference, self).__init__()

        self._name = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'name' in model:
            self.name = model['name']

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n=None):
        if not is_valid_string(n):
            raise SyntaxError('LocalObjectReference: name: [ {} ] is invalid.'.format(n))
        self._name = n

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.name is not None:
            data['name'] = self.name
        return data
