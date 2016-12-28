#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.ObjectFieldSelector import ObjectFieldSelector
from kubernetes.models.v1.ResourceFieldSelector import ResourceFieldSelector
from kubernetes.models.v1.ConfigMapKeySelector import ConfigMapKeySelector
from kubernetes.models.v1.SecretKeySelector import SecretKeySelector


class EnvVarSource(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_envvarsource
    """

    def __init__(self, model=None):
        super(EnvVarSource, self).__init__()

        self._field_ref = None
        self._resource_field_ref = None
        self._config_map_key_ref = None
        self._secret_key_ref = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'fieldRef' in model:
            self.field_ref = ObjectFieldSelector(model['fieldRef'])
        if 'resourceFieldRef' in model:
            self.resource_field_ref = ResourceFieldSelector(model['resourceFieldRef'])
        if 'configMapKeyRef' in model:
            self.config_map_key_ref = ConfigMapKeySelector(model['configMapKeyRef'])
        if 'secretKeyRef' is model:
            self.secret_key_ref = SecretKeySelector(model['secretKeyRef'])

    # ------------------------------------------------------------------------------------- fieldRef

    @property
    def field_ref(self):
        return self._field_ref

    @field_ref.setter
    def field_ref(self, ref=None):
        if not isinstance(ref, ObjectFieldSelector):
            raise SyntaxError('EnvVarSource: field_ref: [ {} ] is invalid.'.format(ref))
        self._field_ref = ref

    # ------------------------------------------------------------------------------------- resourceFieldRef

    @property
    def resource_field_ref(self):
        return self._resource_field_ref

    @resource_field_ref.setter
    def resource_field_ref(self, ref=None):
        if not isinstance(ref, ResourceFieldSelector):
            raise SyntaxError('EnvVarSource: resource_field_ref: [ {} ] is invalid.'.format(ref))
        self._resource_field_ref = ref

    # ------------------------------------------------------------------------------------- configMapKeyRef

    @property
    def config_map_key_ref(self):
        return self._config_map_key_ref

    @config_map_key_ref.setter
    def config_map_key_ref(self, ref=None):
        if not isinstance(ref, ConfigMapKeySelector):
            raise SyntaxError('EnvVarSource: config_map_key_ref: [ {} ] is invalid.'.format(ref))
        self._config_map_key_ref = ref

    # ------------------------------------------------------------------------------------- secretKeyRef

    @property
    def secret_key_ref(self):
        return self._secret_key_ref

    @secret_key_ref.setter
    def secret_key_ref(self, ref=None):
        if not isinstance(ref, SecretKeySelector):
            raise SyntaxError('EnvVarSource: secret_key_ref: [ {} ] is invalid.'.format(ref))
        self._secret_key_ref = ref

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.field_ref is not None:
            data['fieldRef'] = self.field_ref.serialize()
        if self.resource_field_ref is not None:
            data['resourceFieldRef'] = self.resource_field_ref.serialize()
        if self.config_map_key_ref  is not None:
            data['configMapKeyRef'] = self.config_map_key_ref.serialize()
        if self.secret_key_ref is not None:
            data['secretKeyRef'] = self.secret_key_ref.serialize()
        return data
