#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, filter_model


class NFSVolumeSource(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_nfsvolumesource
    """

    def __init__(self, model=None):
        super(NFSVolumeSource, self).__init__()

        self._server = None
        self._path = None
        self._read_only = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model):
        if 'server' in model:
            self.server = model['server']
        if 'path' in model:
            self.path = model['path']
        if 'readOnly' in model:
            self.read_only = model['readOnly']

    # ------------------------------------------------------------------------------------- server

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, server=None):
        if not is_valid_string(server):
            raise SyntaxError('NFSVolumeSource: server: [ {0} ] is invalid.'.format(server))
        self._server = server

    # ------------------------------------------------------------------------------------- path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path=None):
        if not is_valid_string(path):
            raise SyntaxError('NFSVolumeSource: path: [ {0} ] is invalid.'.format(path))
        self._path = path

    # ------------------------------------------------------------------------------------- readOnly

    @property
    def read_only(self):
        return self._read_only

    @read_only.setter
    def read_only(self, ro=None):
        if not isinstance(ro, bool):
            raise SyntaxError('NFSVolumeSource: read_only: [ {0} ] is invalid.'.format(ro))
        self._read_only = ro

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.server is not None:
            data['server'] = self.server
        if self.path is not None:
            data['path'] = self.path
        if self.read_only is not None:
            data['readOnly'] = self.read_only
        return data
