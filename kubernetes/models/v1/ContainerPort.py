#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.BaseModel import BaseModel


class ContainerPort(BaseModel):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_containerport
    """
    
    VALID_PROTOCOLS = ['TCP', 'UDP']

    def __init__(self):
        super(ContainerPort, self).__init__()

        self._container_port = None
        self._host_port = None
        self._protocol = 'TCP'

        self.name = None
        self.host_ip = None

    @staticmethod
    def _is_valid_port(port=None):
        if not isinstance(port, int):
            return False
        if not 0 < port < 65536:
            return False
        return True

    # ------------------------------------------------------------------------------------- container port

    @property
    def container_port(self):
        return self._container_port

    @container_port.setter
    def container_port(self, port=None):
        if not ContainerPort._is_valid_port(port):
            raise SyntaxError('ContainerPort: container_port: [ {0} ] is invalid.'.format(port))
        self._container_port = port

    # ------------------------------------------------------------------------------------- host port

    @property
    def host_port(self):
        return self._host_port

    @host_port.setter
    def host_port(self, port=None):
        if not ContainerPort._is_valid_port(port):
            raise SyntaxError('ContainerPort: host_port: [ {0} ] is invalid.'.format(port))
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
