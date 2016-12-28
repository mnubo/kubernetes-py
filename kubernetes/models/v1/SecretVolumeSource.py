#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, is_valid_list
from kubernetes.models.v1.KeyToPath import KeyToPath
from kubernetes.utils import filter_model


class SecretVolumeSource(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_secretvolumesource
    """

    def __init__(self, model=None):
        super(SecretVolumeSource, self).__init__()

        self._secret_name = None
        self._items = None
        self._default_mode = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'secretName' in model:
            self.secret_name = model['secretName']
        if 'items' in model:
            items = []
            for i in model['items']:
                item = KeyToPath(i)
                items.append(item)
            self.items = items
        if 'defaultMode' in model:
            self.default_mode = model['defaultMode']

    # ------------------------------------------------------------------------------------- secret name

    @property
    def secret_name(self):
        return self._secret_name

    @secret_name.setter
    def secret_name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('SecretVolumeSource: secret_name: [ {0} ] is invalid.'.format(name))
        self._secret_name = name

    # ------------------------------------------------------------------------------------- items

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items=None):
        if not is_valid_list(items, KeyToPath):
            raise SyntaxError('SecretVolumeSource: items: [ {0} ] is invalid.'.format(items))
        self._items = items

    # ------------------------------------------------------------------------------------- defaultMode

    @property
    def default_mode(self):
        return self._default_mode

    @default_mode.setter
    def default_mode(self, mode=None):
        if not isinstance(mode, int):
            raise SyntaxError('SecretVolumeSource: default_mode: [ {0} ] is invalid.'.format(mode))
        self._default_mode = mode

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.secret_name is not None:
            data['secretName'] = self.secret_name
        if self.items is not None:
            data['items'] = [x.serialize() for x in self.items]
        if self.default_mode is not None:
            data['defaultMode'] = self.default_mode
        return data
