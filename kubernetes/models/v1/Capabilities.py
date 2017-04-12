#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_list


class Capabilities(object):
    """
    https://kubernetes.io/docs/api-reference/v1.5/#capabilities-v1-core
    """

    def __init__(self, model=None):
        super(Capabilities, self).__init__()

        self._add = None
        self._drop = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'add' in model:
            self.add = model['add']
        if 'drop' in model:
            self.drop = model['drop']

    # ------------------------------------------------------------------------------------- add

    @property
    def add(self):
        return self._add

    @add.setter
    def add(self, a=None):
        if not is_valid_list(a, str):
            raise SyntaxError('Capabilities: add: [ {} ] is invalid.'.format(a))
        self._add = a

    # ------------------------------------------------------------------------------------- drop

    @property
    def drop(self):
        return self._drop

    @drop.setter
    def drop(self, d=None):
        if not is_valid_list(d, str):
            raise SyntaxError('Capabilities: add: [ {} ] is invalid.'.format(d))
        self._drop = d

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.add is not None:
            data['add'] = self.add
        if self.drop is not None:
            data['drop'] = self.drop
        return data
