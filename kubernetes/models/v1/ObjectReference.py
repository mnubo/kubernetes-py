#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string


class ObjectReference(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_objectreference
    """

    def __init__(self, model=None):
        super(ObjectReference, self).__init__()

        self._kind = None
        self._namespace = None
        self._name = None
        self._uid = None
        self._api_version = None
        self._resource_version = None
        self._field_path = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'kind' in model:
            self.kind = model['kind']
        if 'namespace' in model:
            self.namespace = model['namespace']
        if 'name' in model:
            self.name = model['name']
        if 'uid' in model:
            self.uid = model['uid']
        if 'apiVersion' in model:
            self.api_version = model['apiVersion']
        if 'resourceVersion' in model:
            self.resource_version = model['resourceVersion']
        if 'fieldPath' in model:
            self.field_path = model['fieldPath']

    # ------------------------------------------------------------------------------------- kind

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, k=None):
        if not is_valid_string(k):
            raise SyntaxError('ObjectReference: kind: [ {} ] is invalid.'.format(k))
        self._kind = k

    # ------------------------------------------------------------------------------------- namespace

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, ns=None):
        if not is_valid_string(ns):
            raise SyntaxError('ObjectReference: namespace: [ {} ] is invalid.'.format(ns))
        self._namespace = ns

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('ObjectReference: name: [ {} ] is invalid.'.format(name))
        self._name = name

    # ------------------------------------------------------------------------------------- uid

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid=None):
        if not is_valid_string(uid):
            raise SyntaxError('ObjectReference: uid: [ {} ] is invalid.'.format(uid))
        self._uid = uid

    # ------------------------------------------------------------------------------------- apiVersion

    @property
    def api_version(self):
        return self._api_version

    @api_version.setter
    def api_version(self, v=None):
        if not is_valid_string(v):
            raise SyntaxError('ObjectReference: api_version: [ {} ] is invalid.'.format(v))
        self._api_version = v

    # ------------------------------------------------------------------------------------- resourceVersion

    @property
    def resource_version(self):
        return self._resource_version

    @resource_version.setter
    def resource_version(self, v=None):
        if not is_valid_string(v):
            raise SyntaxError('ObjectReference: resource_version: [ {} ] is invalid.'.format(v))
        self._resource_version = v

    # ------------------------------------------------------------------------------------- fieldPath

    @property
    def field_path(self):
        return self._field_path

    @field_path.setter
    def field_path(self, path=None):
        if not is_valid_string(path):
            raise SyntaxError('ObjectReference: field_path: [ {} ] is invalid.'.format(path))
        self._field_path = path

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.kind is not None:
            data['kind'] = self.kind
        if self.namespace is not None:
            data['namespace'] = self.namespace
        if self.name is not None:
            data['name'] = self.name
        if self.uid is not None:
            data['uid'] = self.uid
        if self.api_version is not None:
            data['apiVersion'] = self.api_version
        if self.resource_version is not None:
            data['resourceVersion'] = self.resource_version
        if self.field_path is not None:
            data['fieldPath'] = self.field_path
        return data
