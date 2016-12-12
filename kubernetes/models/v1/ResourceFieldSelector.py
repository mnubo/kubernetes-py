#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string


class ResourceFieldSelector(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_resourcefieldselector
    """

    def __init__(self, model=None):
        super(ResourceFieldSelector, self).__init__()

        self._container_name = None
        self._resource = None
        self._divisor = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'containerName' in model:
            self.container_name = model['containerName']
        if 'resource' in model:
            self.resource = model['resource']
        if 'divisor' in model:
            self.divisor = model['divisor']

    # ------------------------------------------------------------------------------------- containerName

    @property
    def container_name(self):
        return self._container_name

    @container_name.setter
    def container_name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('ResourceFieldSelector: container_name: [ {} ] is not None'.format(name))
        self._container_name = name

    # ------------------------------------------------------------------------------------- resource

    @property
    def resource(self):
        return self._resource

    @resource.setter
    def resource(self, res=None):
        if not is_valid_string(res):
            raise SyntaxError('ResourceFieldSelector: resource: [ {} ] is not None'.format(res))
        self._resource = res

    # ------------------------------------------------------------------------------------- divisor

    @property
    def divisor(self):
        return self._divisor

    @divisor.setter
    def divisor(self, div=None):
        if not is_valid_string(div):
            raise SyntaxError('ResourceFieldSelector: divisor: [ {} ] is not None'.format(div))
        self._divisor = div

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.container_name is not None:
            data['containerName'] = self.container_name
        if self.resource is not None:
            data['resource'] = self.resource
        if self.divisor is not None:
            data['divisor'] = self.divisor
        return data
