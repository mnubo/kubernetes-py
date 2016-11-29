#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import filter_model, is_valid_string


class ContainerPort(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_containerport
    """

    VALID_PROTOCOLS = ['TCP', 'UDP']

    def __init__(self, model=None):
        super(ContainerPort, self).__init__()

        self._name = None
        self._host_port = None
        self._container_port = None
        self._protocol = 'TCP'
        self._host_ip = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'name' in model:
            self.name = model['name']
        if 'hostPort' in model:
            self.host_port = model['hostPort']
        if 'containerPort' in model:
            self.container_port = model['containerPort']
        if 'protocol' in model:
            self.protocol = model['protocol']
        if 'hostIP' in model:
            self.host_ip = model['hostIP']

    @staticmethod
    def _is_valid_port(port=None):
        if not isinstance(port, int):
            return False
        if not 0 < port < 65536:
            return False
        return True

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('ContainerPort: name: [ {0} ] is invalid.'.format(name))
        self._name = name

    # ------------------------------------------------------------------------------------- host port

    @property
    def host_port(self):
        return self._host_port

    @host_port.setter
    def host_port(self, port=None):
        if not ContainerPort._is_valid_port(port):
            raise SyntaxError('ContainerPort: host_port: [ {0} ] is invalid.'.format(port))
        self._host_port = port

    # ------------------------------------------------------------------------------------- container port

    @property
    def container_port(self):
        return self._container_port

    @container_port.setter
    def container_port(self, port=None):
        if not ContainerPort._is_valid_port(port):
            raise SyntaxError('ContainerPort: container_port: [ {0} ] is invalid.'.format(port))
        self._container_port = port

    # ------------------------------------------------------------------------------------- protocol

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, protocol=None):
        if protocol.upper() not in ContainerPort.VALID_PROTOCOLS:
            raise SyntaxError('ContainerPort: protocol: [ {0} ] is invalid.'.format(protocol))
        self._protocol = protocol.upper()

    # ------------------------------------------------------------------------------------- hostIP

    @property
    def host_ip(self):
        return self._host_ip

    @host_ip.setter
    def host_ip(self, ip=None):
        if not is_valid_string(ip):
            raise SyntaxError('ContainerPort: host_ip: [ {0} ] is invalid.'.format(ip))
        self._host_ip = ip

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
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
