#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import filter_model


class ResourceRequirements(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_resourcerequirements
    """

    VALID_RESOURCES = ['cpu', 'memory', 'storage']

    def __init__(self, model=None):
        super(ResourceRequirements, self).__init__()

        self._limits = {}
        self._requests = {}

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model):
        if 'requests' in model:
            self.requests = model['requests']
        if 'limits' in model:
            self.limits = model['limits']

    def _filter(self, data=None):
        msg = 'ResourceRequirements: data: [ {0} ] is invalid.'.format(data)
        if not isinstance(data, dict):
            raise SyntaxError(msg)
        for x in data:
            if x not in self.VALID_RESOURCES:
                data.pop(x)
        return data

    # ------------------------------------------------------------------------------------- limits

    @property
    def limits(self):
        return self._limits

    @limits.setter
    def limits(self, limits=None):
        self._limits = self._filter(limits)

    # ------------------------------------------------------------------------------------- limits

    @property
    def requests(self):
        return self._requests

    @requests.setter
    def requests(self, requests=None):
        self._requests = self._filter(requests)

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.limits:
            data['limits'] = self.limits
        if self.requests:
            data['requests'] = self.requests
        return data
