#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1 import (
    LoadBalancerIngress
)
from kubernetes.utils import is_valid_list


class LoadBalancerStatus(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_loadbalancerstatus
    """

    def __init__(self, model=None):
        super(LoadBalancerStatus, self).__init__()
        self._ingress = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'ingress' in model:
            statuses = []
            for i in model['ingress']:
                status = LoadBalancerIngress(i)
                statuses.append(status)
            self.ingress = statuses

    # ------------------------------------------------------------------------------------- ingress

    @property
    def ingress(self):
        return self._ingress

    @ingress.setter
    def ingress(self, ingress=None):
        if not is_valid_list(ingress, LoadBalancerIngress):
            raise SyntaxError('LoadBalancerStatus: ingress: [ {0} ] is invalid.'.format(ingress))
        self._ingress = ingress

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.ingress is not None:
            data['ingress'] = [x.serialize() for x in self.ingress]
        return data
