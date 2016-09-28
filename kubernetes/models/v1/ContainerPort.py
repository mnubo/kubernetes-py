#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.BaseModel import BaseModel


class ContainerPort(BaseModel):

    VALID_PROTOCOLS = ['TCP', 'UDP']

    def __init__(self, model=None):
        super(ContainerPort, self).__init__()

        self._container_port = None
        self._host_port = None
        self._protocol = 'TCP'

        self.name = None
        self.host_ip = None

    # ------------------------------------------------------------------------------------- container port

    @property
    def container_port(self):
        return self._container_port

    @container_port.setter
    def container_port(self, port=None):
        msg = 'ContainerPort: port: [ {0} ] is invalid.'.format(port)
        if not isinstance(port, int):
            raise SyntaxError(msg)
        if not 1 < port < 65535:
            raise SyntaxError(msg)
        self._container_port = port

    # ------------------------------------------------------------------------------------- host port

    @property
    def host_port(self):
        return self._host_port

    @host_port.setter
    def host_port(self, port=None):
        msg = 'ContainerPort: port: [ {0} ] is invalid.'.format(port)
        if not isinstance(port, int):
            raise SyntaxError(msg)
        if not 1 < port < 65535:
            raise SyntaxError(msg)
        self.host_port = port

    # ------------------------------------------------------------------------------------- protocol

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, protocol=None):
        if protocol not in ContainerPort.VALID_PROTOCOLS:
            raise SyntaxError('ContainerPort: protocol: [ {0} ] is invalid.'.format(protocol))
        self._protocol = protocol

    # ------------------------------------------------------------------------------------- serialize

    def json(self):
        data = {}
        if self.name:
            data['name'] = self.name
        if self.host_port:
            data['hostPort'] = self.host_port
        if self.container_port:
            data['containerPort'] = self.container_port
        if self.protocol:
            data['protocol'] = self.protocol
        if self.host_ip:
            data['hostIP'] = self.host_ip
        return data
