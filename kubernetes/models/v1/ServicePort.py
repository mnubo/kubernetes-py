#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string


class ServicePort(object):

    VALID_PROTOCOLS = ['TCP', 'UDP']

    def __init__(self, name=None, model=None):
        super(ServicePort, self).__init__()

        self._name = None
        self._protocol = None
        self._port = None
        self._target_port = None
        self._node_port = None

        if name is not None:
            self.name = name

        if model is not None:
            if 'name' in model:
                self.name = model['name']
            if 'protocol' in model:
                self.protocol = model['protocol']
            if 'port' in model:
                self.port = model['port']
            if 'targetPort' in model:
                self.target_port = model['targetPort']
            if 'nodePort' in model:
                self.node_port = model['nodePort']

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('ServicePort: name: [ {} ] is invalid.'.format(name))
        self._name = name

    # ------------------------------------------------------------------------------------- protocol

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, protocol=None):
        if not is_valid_string(protocol) or protocol.upper() not in ServicePort.VALID_PROTOCOLS:
            raise SyntaxError('ServicePort: protocol: [ {} ] is invalid.'.format(protocol))
        self._protocol = protocol.upper()

    # ------------------------------------------------------------------------------------- port

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port=None):
        if isinstance(port, str) and port.isdigit():
            port = int(port)
        if not isinstance(port, int):
            raise SyntaxError('ServicePort: port: [ {} ] is invalid.'.format(port))
        self._port = port

    # ------------------------------------------------------------------------------------- targetPort

    @property
    def target_port(self):
        return self._target_port

    @target_port.setter
    def target_port(self, port=None):
        msg = 'ServicePort: target_port: [ {} ] is invalid.'.format(port)
        try:
            p = int(port)
        except ValueError:
            if not is_valid_string(port):
                raise SyntaxError(msg)
            p = port
        except TypeError:
            raise SyntaxError(msg)
        self._target_port = p

    # ------------------------------------------------------------------------------------- nodePort

    @property
    def node_port(self):
        return self._node_port

    @node_port.setter
    def node_port(self, port=None):
        if port is not None and isinstance(port, str) and port.isdigit():
            port = int(port)
        if port is not None and not isinstance(port, int):
            raise SyntaxError('ServicePort: node_port: [ {} ] is invalid.'.format(port))
        self._node_port = port

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.name is not None:
            data['name'] = self.name
        if self.protocol is not None:
            data['protocol'] = self.protocol
        if self.port is not None:
            data['port'] = self.port
        if self.target_port is not None:
            data['targetPort'] = self.target_port
        if self.node_port is not None:
            data['nodePort'] = self.node_port
        return data
