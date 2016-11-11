#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string


class LoadBalancerIngress(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_loadbalanceringress
    """

    def __init__(self, model=None):
        super(LoadBalancerIngress, self).__init__()

        self._ip = None
        self._hostname = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'ip' in model:
            self.ip = model['ip']
        if 'hostname' in model:
            self.hostname = model['hostname']

    # ------------------------------------------------------------------------------------- ip

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, ip=None):
        if not is_valid_string(ip):
            raise SyntaxError('LoadBalancerIngress: ip: [ {} ] is invalid.'.format(ip))
        self._ip = ip

    # ------------------------------------------------------------------------------------- hostname

    @property
    def hostname(self):
        return self._hostname

    @hostname.setter
    def hostname(self, hostname=None):
        if not is_valid_string(hostname):
            raise SyntaxError('LoadBalancerIngress: hostname: [ {} ] is invalid.'.format(hostname))
        self._hostname = hostname

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.ip is not None:
            data['ip'] = self.ip
        if self.hostname is not None:
            data['hostname'] = self.hostname
        return data
