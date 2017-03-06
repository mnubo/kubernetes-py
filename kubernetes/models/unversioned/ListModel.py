#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.unversioned.ListMeta import ListMeta
from kubernetes.utils import is_valid_string


class ListModel(object):
    def __init__(self):
        super(ListModel, self).__init__()

        self._api_version = None
        self._kind = None
        self._metadata = ListMeta()
        self._items = None

    def build_with_model(self, model=None):
        if 'apiVersion' in model:
            self.api_version = model['apiVersion']
        if 'kind' in model:
            self.kind = model['kind']
        if 'metadata' in model:
            self.metadata = ListMeta(model=model['metadata'])

    # ------------------------------------------------------------------------------------- apiVersion

    @property
    def api_version(self):
        return self._api_version

    @api_version.setter
    def api_version(self, v=None):
        if not is_valid_string(v):
            raise SyntaxError('ListModel: api_version: [ {} ] is invalid.'.format(v))
        self._api_version = v

    # ------------------------------------------------------------------------------------- kind

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, k=None):
        if not is_valid_string(k):
            raise SyntaxError('ListModel: kind: [ {} ] is invalid.'.format(k))
        self._kind = k

    # ------------------------------------------------------------------------------------- metadata

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, meta=None):
        if not isinstance(meta, ListMeta):
            raise SyntaxError('ListModel: metadata: [ {} ] is invalid.'.format(meta))
        self._metadata = meta

    # ------------------------------------------------------------------------------------- items

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, l=None):
        if not isinstance(l, list):
            raise SyntaxError('ListModel: items: [ {} ] is invalid.'.format(l))
        self._items = l

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.api_version is not None:
            data['apiVersion'] = self.api_version
        if self.kind is not None:
            data['kind'] = self.kind
        if self.metadata is not None:
            data['metadata'] = self.metadata.serialize()
        if self.items is not None:
            l = list()
            for i in self.items:
                l.append(i.serialize())
            data['items'] = l
        return data
