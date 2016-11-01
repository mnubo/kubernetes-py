#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1 import (
    BaseModel,
    LoadBalancerStatus
)


class ServiceStatus(BaseModel):

    def __init__(self):
        super(ServiceStatus, self).__init__()
        self._load_balancer = None

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

    def json(self):
        data = {}
        if self.load_balancer is not None:
            data['loadBalancer'] = self.load_balancer.json()
        return data

