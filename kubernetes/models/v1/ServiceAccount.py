#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.unversioned.BaseModel import BaseModel
from kubernetes.models.v1.ObjectReference import ObjectReference
from kubernetes.models.v1.LocalObjectReference import LocalObjectReference
from kubernetes.utils import is_valid_list


class ServiceAccount(BaseModel):
    """
    http://kubernetes.io/docs/user-guide/service-accounts/
    """

    def __init__(self, model=None):
        super(ServiceAccount, self).__init__()

        self.kind = 'ServiceAccount'
        self.api_version = 'v1'

        self._secrets = []
        self._image_pull_secrets = []

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        super(ServiceAccount, self).build_with_model(model)

        if 'secrets' in model:
            secrets = []
            for x in model['secrets']:
                s = ObjectReference(x)
                secrets.append(s)
            self.secrets = secrets

        if 'imagePullSecrets' in model:
            secrets = []
            for x in model['imagePullSecrets']:
                s = LocalObjectReference(x)
                secrets.append(s)
            self.image_pull_secrets = secrets

    # ------------------------------------------------------------------------------------- secrets

    @property
    def secrets(self):
        return self._secrets

    @secrets.setter
    def secrets(self, s=None):
        if not is_valid_list(s, ObjectReference):
            raise SyntaxError('ServiceAccount: secrets: [ {} ] is invalid.'.format(s))
        self._secrets = s

    # ------------------------------------------------------------------------------------- image_pull_secrets

    @property
    def image_pull_secrets(self):
        return self._image_pull_secrets

    @image_pull_secrets.setter
    def image_pull_secrets(self, s=None):
        if not is_valid_list(s, LocalObjectReference):
            raise SyntaxError('ServiceAccount: image_pull_secrets: [ {} ] is invalid.'.format(s))
        self._image_pull_secrets = s

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(ServiceAccount, self).serialize()

        if self.secrets is not None:
            data['secrets'] = [x.serialize() for x in self.secrets]
        if self.image_pull_secrets is not None:
            data['imagePullSecrets'] = [x.serialize() for x in self.image_pull_secrets]
        return data
