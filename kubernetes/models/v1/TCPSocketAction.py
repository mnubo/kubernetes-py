#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


class TCPSocketAction(object):

    def __init__(self):
        super(TCPSocketAction, self).__init__()
        self._port = None

    # ------------------------------------------------------------------------------------- port

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port=None):
        msg = 'TCPSocketAction: port: [ {0} ] is invalid.'.format(port)
        if not isinstance(port, int):
            raise SyntaxError(msg)
        if not 1 < port < 65535:
            raise SyntaxError(msg)
        self._port = str(port)

    # ------------------------------------------------------------------------------------- serialize

    def json(self):
        data = {}
        if self.port:
            data['port'] = self.port
        return data
