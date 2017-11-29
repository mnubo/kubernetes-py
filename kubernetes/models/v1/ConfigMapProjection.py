#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, filter_model
from kubernetes.models.v1.KeyToPath import KeyToPath


class ConfigMapProjection(object):
    """
    https://kubernetes.io/docs/api-reference/v1.8/#configmapprojection-v1-core

    Adapts a ConfigMap into a projected volume.

    The contents of the target ConfigMap's Data field will be presented in a projected volume as files using the keys
    in the Data field as the file names, unless the items element is populated with specific mappings of keys to paths.
    Note that this is identical to a configmap volume source without the default mode.
    """

    def __init__(self, model=None):
        super(ConfigMapProjection, self).__init__()

        self._items = None
        self._name = None
        self._optional = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'items' in model:
            self.items = model['items']
        if 'name' in model:
            self.name = model['name']
        if 'optional' in model:
            self.optional = model['optional']

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
