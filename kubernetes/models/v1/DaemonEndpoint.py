#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#
from kubernetes.utils import filter_model


class DaemonEndpoint(object):
    """
    https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_daemonendpoint
    """

    def __init__(self, model=None):
        super(DaemonEndpoint, self).__init__()

        self._port = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'Port' in model:
            self.port = model['Port']

    # ------------------------------------------------------------------------------------- port

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, v):
        if not isinstance(v, int):
            raise SyntaxError('DaemonEndpoints: port: [ {0} ] is invalid.'.format(v))
        self._port = v

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.port:
            data['Port'] = self.port
        return data
