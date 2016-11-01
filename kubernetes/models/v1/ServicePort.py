#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


class ServicePort(object):

    def __init__(self, port=None):
        super(ServicePort, self).__init__()

        self.name = None
        self.protocol = None
        self.port = port
        self.target_port = None
        self.node_port = None

    # ------------------------------------------------------------------------------------- serialize

    def json(self):
        data = {}
        if self.name is not None:
            data['name'] = self.name
        if self.protocol is not None:
            data['protocol'] = self.protocol
        if self.port is not None:
            data['port'] = self.port
        if self.target_port is not None:
            data['taretPort'] = self.target_port
        if self.node_port is not None:
            data['nodePort'] = self.node_port
        return data
