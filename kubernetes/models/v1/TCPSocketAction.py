#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


class TCPSocketAction(object):

    def __init__(self, model=None):
        super(TCPSocketAction, self).__init__()

        self._port = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'port' in model:
            self.port = model['port']

    # ------------------------------------------------------------------------------------- port

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port=None):
        msg = 'TCPSocketAction: port: [ {0} ] is invalid.'.format(port)
        if isinstance(port, str) and port.isdigit():
            port = int(port)
        if isinstance(port, int) and not 1 < port < 65535:
            raise SyntaxError(msg)
        self._port = str(port)

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.port:
            data['port'] = self.port
        return data
