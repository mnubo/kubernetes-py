#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, filter_model


class ListMeta(object):
    """
    https://kubernetes.io/docs/api-reference/v1/definitions/#_unversioned_listmeta
    """

    def __init__(self, model=None):
        super(ListMeta, self).__init__()

        self._name = None
        self._self_link = None
        self._resource_version = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'selfLink' in model:
            self.self_link = model['selfLink']
        if 'resourceVersion' in model:
            self.resource_version = model['resourceVersion']

    # ------------------------------------------------------------------------------------- strip

    def strip(self):
        self._self_link = None
        self._resource_version = None

    # ------------------------------------------------------------------------------------- selfLink

    @property
    def self_link(self):
        return self._self_link

    @self_link.setter
    def self_link(self, link=None):
        if not is_valid_string(link):
            raise SyntaxError('ListMeta: self_link: [ {0} ] is invalid.'.format(link))
        self._self_link = link

    # ------------------------------------------------------------------------------------- resourceVersion

    @property
    def resource_version(self):
        return self._resource_version

    @resource_version.setter
    def resource_version(self, v=None):
        if v is not None:
            if not isinstance(v, str):
                raise SyntaxError('ListMeta: resource_version: [ {0} ] is invalid.'.format(v))
        self._resource_version = v

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.self_link:
            data['selfLink'] = self.self_link
        if self.resource_version:
            data['resourceVersion'] = self.resource_version
        return data
