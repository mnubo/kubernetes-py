#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.ServicePort import ServicePort
from kubernetes.utils import *


class ServiceSpec(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_servicespec
    """

    VALID_TYPES = ['ExternalName', 'ClusterIP', 'NodePort', 'LoadBalancer']
    VALID_SESSION_AFFINITIES = ['ClientIP', 'None']

    def __init__(self, model=None):
        super(ServiceSpec, self).__init__()

        self._cluster_ip = None
        self._external_ips = []
        self._external_name = None
        self._load_balancer_ip = None
        self._load_balancer_source_ranges = None
        self._ports = []
        self._selector = None
        self._session_affinity = 'None'
        self._type = 'ClusterIP'

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'clusterIP' in model:
            self.cluster_ip = model['clusterIP']
        if 'externalIPs' in model:
            self.external_ips = model['externalIPs']
        if 'externalName' in model:
            self.external_name = model['externalName']
        if 'loadBalancerIP' in model:
            self.load_balancer_ip = model['loadBalancerIP']
        if 'loadBalancerSourceRanges' in model:
            self.load_balancer_source_ranges = model['loadBalancerSourceRanges']
        if 'ports' in model:
            ports = []
            for p in model['ports']:
                port = ServicePort(model=p)
                ports.append(port)
            self.ports = ports
        if 'selector' in model:
            self.selector = model['selector']
        if 'sessionAffinity' in model:
            self.session_affinity = model['sessionAffinity']
        if 'type' in model:
            self.type = model['type']

    # ------------------------------------------------------------------------------------- clusterIP

    @property
    def cluster_ip(self):
        return self._cluster_ip

    @cluster_ip.setter
    def cluster_ip(self, ip=None):
        if not is_valid_string(ip):
            raise SyntaxError('ServiceSpec: cluster_ip: [ {0} ] is invalid.'.format(ip))
        self._cluster_ip = ip

    # ------------------------------------------------------------------------------------- externalIPs

    @property
    def external_ips(self):
        return self._external_ips

    @external_ips.setter
    def external_ips(self, ips=None):
        msg = 'ServiceSpec: external_ips: [ {0} ] is invalid.'.format(ips)
        if not is_valid_list(ips, str):
            raise SyntaxError(msg)
        for ip in ips:
            if not is_valid_ip(ip):
                raise SyntaxError(msg)
        self._external_ips = ips

    # ------------------------------------------------------------------------------------- externalName

    @property
    def external_name(self):
        return self._external_name

    @external_name.setter
    def external_name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('ServiceSpec: external_name: [ {0} ] is invalid.'.format(name))
        self._external_name = name

    # ------------------------------------------------------------------------------------- loadBalancerIP

    @property
    def load_balancer_ip(self):
        return self._load_balancer_ip

    @load_balancer_ip.setter
    def load_balancer_ip(self, ip=None):
        if not is_valid_string(ip) or not is_valid_ip(ip):
            raise SyntaxError('ServiceSpec: load_balancer_ip: [ {0} ] is invalid.'.format(ip))
        self._load_balancer_ip = ip

    # ------------------------------------------------------------------------------------- loadBalancerSourceRanges

    @property
    def load_balancer_source_ranges(self):
        return self._load_balancer_source_ranges

    @load_balancer_source_ranges.setter
    def load_balancer_source_ranges(self, ranges=None):
        if not is_valid_list(ranges, str):
            raise SyntaxError('ServiceSpec: load_balancer_source_ranges: [ {0} ] is invalid.'.format(ranges))
        self._load_balancer_source_ranges = ranges

    # ------------------------------------------------------------------------------------- ports

    @property
    def ports(self):
        return self._ports

    @ports.setter
    def ports(self, ports=None):
        if not is_valid_list(ports, ServicePort):
            raise SyntaxError('ServiceSpec: ports: [ {0} ] is invalid.'.format(ports))
        self._ports = ports

    # ------------------------------------------------------------------------------------- selector

    @property
    def selector(self):
        return self._selector

    @selector.setter
    def selector(self, sel=None):
        if not is_valid_dict(sel):
            raise SyntaxError('ServiceSpec: selector: [ {0} ] is invalid.'.format(sel))
        self._selector = sel

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

    def serialize(self):
        data = {}
        if self.ports:
            data['ports'] = [x.serialize() for x in self.ports]
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
