#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1 import ServicePort
from kubernetes.utils import is_valid_list, is_valid_string


class ServiceSpec(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_servicespec
    """

    VALID_TYPES = ['ExternalName', 'ClusterIP', 'NodePort', 'LoadBalancer']
    VALID_SESSION_AFFINITIES = ['ClientIP', 'None']

    def __init__(self):
        super(ServiceSpec, self).__init__()

        self._ports = []
        self._session_affinity = 'None'
        self._type = 'ClusterIP'

        self.cluster_ip = None
        self.external_ips = None
        self.external_name = None
        self.load_balancer_ip = None
        self.load_balancer_source_ranges = None
        self.selector = None

    # ------------------------------------------------------------------------------------- ports

    @property
    def ports(self):
        return self._ports

    @ports.setter
    def ports(self, ports=None):
        if not is_valid_list(ports, ServicePort):
            raise SyntaxError('ServiceSpec: ports: [ {0} ] is invalid.'.format(ports))
        self._ports = ports

    # ------------------------------------------------------------------------------------- session affinity

    @property
    def session_affinity(self):
        return self._session_affinity

    @session_affinity.setter
    def session_affinity(self, affinity=None):
        if not is_valid_string(affinity) or affinity not in ServiceSpec.VALID_SESSION_AFFINITIES:
            raise SyntaxError('ServiceSpec: affinity: [ {0} ] is invalid.'.format(affinity))
        self._session_affinity = affinity

    # ------------------------------------------------------------------------------------- session affinity

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type=None):
        if not is_valid_string(type) or type not in ServiceSpec.VALID_TYPES:
            raise SyntaxError('ServiceSpec: type: [ {0} ] is invalid.'.format(type))
        self._type = type

    # ------------------------------------------------------------------------------------- serialize

    def json(self):
        data = {}
        if self.ports:
            data['ports'] = self.ports
        if self.session_affinity:
            data['sessionAffinity'] = self.session_affinity
        if self.type:
            data['type'] = self.type
        if self.cluster_ip is not None:
            data['clusterIP'] = self.cluster_ip
        if self.external_ips is not None:
            data['externalIPs'] = self.external_ips
        if self.external_name is not None:
            data['externalName'] = self.external_name
        if self.load_balancer_ip is not None:
            data['loadBalancerIP'] = self.load_balancer_ip
        if self.load_balancer_source_ranges is not None:
            data['loadBalancerSourceRanges'] = self.load_balancer_source_ranges
        if self.selector is not None:
            data['selector'] = self.selector
        return data
