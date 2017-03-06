#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#
from kubernetes.utils import filter_model


class ContainerImage(object):
    """
    https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_containerimage
    """

    def __init__(self, model=None):
        super(ContainerImage, self).__init__()

        self._names = None
        self._size_bytes = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'names' in model:
            self.names = model['names']
        if 'sizeBytes' in model:
            self.size_bytes = model['sizeBytes']

    # ------------------------------------------------------------------------------------- names

    @property
    def names(self):
        return self._names

    @names.setter
    def names(self, v):
        if not isinstance(v, list):
            raise SyntaxError('ContainerImage: names: [ {0} ] is invalid.'.format(v))
        self._names = v

    # ------------------------------------------------------------------------------------- size_bytes

    @property
    def size_bytes(self):
        return self._size_bytes

    @size_bytes.setter
    def size_bytes(self, v):
        if not isinstance(v, int):
            raise SyntaxError('ContainerImage: size_bytes: [ {0} ] is invalid.'.format(v))
        self._size_bytes = v

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.names:
            data['names'] = self.names
        if self.size_bytes:
            data['sizeBytes'] = self.size_bytes
        return data
