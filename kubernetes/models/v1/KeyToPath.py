#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, filter_model


class KeyToPath(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_keytopath
    """

    def __init__(self, model=None):
        super(KeyToPath, self).__init__()

        self._key = None
        self._path = None
        self._mode = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'key' in model:
            self.key = model['key']
        if 'path' in model:
            self.path = model['path']
        if 'mode' in model:
            self.mode = model['mode']

    # ------------------------------------------------------------------------------------- key

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key=None):
        if not is_valid_string(key):
            raise SyntaxError('KeyToPath: key: [ {0} ] is invalid.'.format(key))
        self._key = key

    # ------------------------------------------------------------------------------------- path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path=None):
        if not is_valid_string(path):
            raise SyntaxError('KeyToPath: path: [ {0} ] is invalid.'.format(path))
        self._path = path

    # ------------------------------------------------------------------------------------- mode

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode=None):
        if not is_valid_string(mode):
            raise SyntaxError('KeyToPath: mode: [ {0} ] is invalid.'.format(mode))
        self._mode = mode

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.key is not None:
            data['key'] = self.key
        if self.path is not None:
            data['path'] = self.path
        if self.mode is not None:
            data['mode'] = self.mode
        return data
