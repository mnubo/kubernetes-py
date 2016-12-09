#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import filter_model, is_valid_string


class OwnerReference(object):

    def __init__(self, model=None):
        super(OwnerReference, self).__init__()

        self._api_version = None
        self._kind = None
        self._name = None
        self._uid = None
        self._controller = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'apiVersion' in model:
            self.api_version = model['apiVersion']
        if 'kind' in model:
            self.kind = model['kind']
        if 'name' in model:
            self.model = model['name']
        if 'uid' in model:
            self.uid = model['uid']
        if 'controller' in model:
            self.controller = model['controller']

    # ------------------------------------------------------------------------------------- api version

    @property
    def api_version(self):
        return self._api_version

    @api_version.setter
    def api_version(self, v=None):
        if not is_valid_string(v):
            raise SyntaxError('OwnerReference: api_version: [ {0} ] is invalid.'.format(v))
        self._api_version = v

    # ------------------------------------------------------------------------------------- kind

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, kind=None):
        if not is_valid_string(kind):
            raise SyntaxError('OwnerReference: kind: [ {0} ] is invalid.'.format(kind))
        self._kind = kind

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('OwnerReference: name: [ {0} ] is invalid.'.format(name))
        self._name = name

    # ------------------------------------------------------------------------------------- uid

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid=None):
        if not is_valid_string(uid):
            raise SyntaxError('OwnerReference: uid: [ {0} ] is invalid.'.format(uid))
        self._uid = uid

    # ------------------------------------------------------------------------------------- controller

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, c=None):
        if not isinstance(c, bool):
            raise SyntaxError('OwnerReference: controller: [ {0} ] is invalid.'.format(c))
        self._controller = c

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.api_version:
            data['apiVersion'] = self.api_version
        if self.kind:
            data['kind'] = self.kind
        if self.name:
            data['name'] = self.name
        if self.uid:
            data['uid'] = self.uid
        if self.controller:
            data['controller'] = self.controller
        return data
