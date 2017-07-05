#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, is_valid_list, convert


class NodeSelectorRequirement(object):
    """
    https://kubernetes.io/docs/api-reference/v1.6/#nodeselectorrequirement-v1-core
    """

    VALID_OPERATORS = ['In', 'NotIn', 'Exists', 'DoesNotExist', 'Gt', 'Lt']

    def __init__(self, model=None):
        super(NodeSelectorRequirement, self).__init__()

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
    def key(self, k=None):
        if not is_valid_string(k):
            raise SyntaxError('NodeSelectorRequirement: key: [ {} ] is invalid.'.format(k))
        self._key = k

    # ------------------------------------------------------------------------------------- operator

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, o=None):
        if not is_valid_string(o) or o not in NodeSelectorRequirement.VALID_OPERATORS:
            raise SyntaxError('NodeSelectorRequirement: operator: [ {} ] is invalid.'.format(o))
        self._operator = o

    # ------------------------------------------------------------------------------------- values

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, v=None):
        if not is_valid_list(convert(v), str):
            raise SyntaxError(
                'NodeSelectorRequirement: values: [ {} ] is invalid.'.format(v))
        if self.operator in ['In, NotIn'] and v == []:
            raise SyntaxError(
                'NodeSelectorRequirement: values: [ {} ] cannot be empty, if operator in [ "In", "NotIn" ]'.format(v))
        if self.operator in ['Exists', 'NotExists'] and v != []:
            raise SyntaxError(
                'NodeSelectorRequirement: values: [ {} ] must be empty, if operator in [ "Exists", "NotExists" ]'.format(v))
        if self.operator in ['Gt', 'Lt']:
            if len(v) != 1:
                raise SyntaxError(
                    'NodeSelectorRequirement: values: [ {} ] must be an array of length 1, if operator in [ "Gt", "Lt" ]'.format(v))
            if not isinstance(v[0], int):
                raise SyntaxError(
                    'NodeSelectorRequirement: values: [ {} ] must contain a single integer, if operator in [ "Gt", "Lt" ]'.format(v))
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
