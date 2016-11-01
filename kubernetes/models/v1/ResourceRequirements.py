#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


class ResourceRequirements(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_resourcerequirements
    """

    VALID_RESOURCES = ['cpu', 'memory']

    def __init__(self):
        super(ResourceRequirements, self).__init__()

        self._limits = {}
        self._requests = {
            'cpu': '100m',
            'memory': '32M'
        }

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

    def json(self):
        data = {}
        if self.limits:
            data['limits'] = self.limits
        if self.requests:
            data['requests'] = self.requests
        return data
