#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, is_valid_list


class LabelSelectorRequirement(object):
    """
    http://kubernetes.io/docs/api-reference/extensions/v1beta1/definitions/#_v1beta1_labelselectorrequirement
    """

    def __init__(self, model=None):
        super(LabelSelectorRequirement, self).__init__()

        self._key = None
        self._operator = None
        self._values = []

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'key' in model:
            self.key = model['key']
        if 'operator' in model:
            self.operator = model['operator']
        if 'values' in model:
            self.values = model['values']

    # ------------------------------------------------------------------------------------- key

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key=None):
        if not is_valid_string(key):
            raise SyntaxError('LabelSelectorRequirements: key: [ {} ] is invalid.'.format(key))
        self._key = key

    # ------------------------------------------------------------------------------------- operator

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, op=None):
        if not is_valid_string(op):
            raise SyntaxError('LabelSelectorRequirements: operator: [ {} ] is invalid.'.format(op))
        self._operator = op

    # ------------------------------------------------------------------------------------- values

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, v=None):
        if not is_valid_list(v, str):
            raise SyntaxError('LabelSelectorRequirements: values: [ {} ] is invalid.'.format(v))
        self._values = v

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.key is not None:
            data['key'] = self.key
        if self.operator is not None:
            data['operator'] = self.operator
        if self.values is not None:
            data['values'] = self.values
        return data
