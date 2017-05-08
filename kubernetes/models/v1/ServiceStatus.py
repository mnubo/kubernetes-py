#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.LoadBalancerStatus import LoadBalancerStatus


class ServiceStatus(object):

    def __init__(self, model=None):
        super(ServiceStatus, self).__init__()

        self._load_balancer = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'loadBalancer' in model:
            self.load_balancer = LoadBalancerStatus(model['loadBalancer'])

    # ------------------------------------------------------------------------------------- load balancer

    @property
    def load_balancer(self):
        return self._load_balancer

    @load_balancer.setter
    def load_balancer(self, status=None):
        if not isinstance(status, LoadBalancerStatus):
            raise SyntaxError('ServiceStatus: load_balancer: [ {0} ] is invalid.'.format(status))
        self._load_balancer = status

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.load_balancer is not None:
            data['loadBalancer'] = self.load_balancer.serialize()
        return data
