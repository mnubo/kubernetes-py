#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, filter_model
from kubernetes.models.v1.KeyToPath import KeyToPath


class ConfigMapVolumeSource(object):
    """
    https://kubernetes.io/docs/api-reference/v1.8/#configmapvolumesource-v1-core

    The contents of the target ConfigMap's Data field will be presented in a volume as files using the keys in the
    Data field as the file names, unless the items element is populated with specific mappings of keys to paths.
    ConfigMap volumes support ownership management and SELinux relabeling.
    """

    def __init__(self, model=None):
        super(ConfigMapVolumeSource, self).__init__()

        self._default_mode = None
        self._items = None
        self._name = None
        self._optional = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'defaultMode' in model:
            self.default_mode = model['defaultMode']
        if 'items' in model:
            self.items = model['items']
        if 'name' in model:
            self.name = model['name']
        if 'optional' in model:
            self.optional = model['optional']

    # ------------------------------------------------------------------------------------- default_mode

    @property
    def default_mode(self):
        return self._default_mode

    @default_mode.setter
    def default_mode(self, mode=None):
        if is_valid_string(mode):
            try:
                mode = int(mode)
            except ValueError:
                raise SyntaxError('ConfigMapVolumeSource: defaultMode: [ {0} ] is invalid.'.format(mode))
        if not isinstance(mode, int) and (0 >= mode <= 777):
            raise SyntaxError('ConfigMapVolumeSource: defaultMode: [ {0} ] is invalid.'.format(mode))
        self._default_mode = mode

    # ------------------------------------------------------------------------------------- items

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items=None):
        if not isinstance(items, list):
            raise SyntaxError('ConfigMapVolumeSource: items: [ {0} ] is invalid.'.format(items))
        modeled_items = list()
        for i in items:
            tmp_item = KeyToPath(model=i)
            modeled_items.append(tmp_item)
        self._items = items

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
        if self.default_mode is not None:
            data['defaultMode '] = self.default_mode
        if self.items is not None:
            tmp_items = list()
            for i in self.items:
                assert isinstance(i, KeyToPath)
                tmp_items.append(i.serialize())
            data['items'] = tmp_items
        if self.name is not None:
            data['name'] = self.name
        if self.optional is not None:
            data['optional'] = self.optional
        return data
