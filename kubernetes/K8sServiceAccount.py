#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject
from kubernetes.K8sSecret import K8sSecret
from kubernetes.models.v1.LocalObjectReference import LocalObjectReference
from kubernetes.models.v1.ServiceAccount import ServiceAccount


class K8sServiceAccount(K8sObject):
    def __init__(self, config=None, name=None):

        super(K8sServiceAccount, self).__init__(
            config=config,
            name=name,
            obj_type='ServiceAccount'
        )

    # -------------------------------------------------------------------------------------  override

    def get(self):
        self.model = ServiceAccount(self.get_model())
        return self

    def create(self):
        super(K8sServiceAccount, self).create()
        self.get()
        return self

    def update(self):
        super(K8sServiceAccount, self).update()
        self.get()
        return self

    def list(self, pattern=None):
        ls = super(K8sServiceAccount, self).list()
        accts = list(map(lambda x: ServiceAccount(x), ls))
        if pattern is not None:
            accts = list(filter(lambda x: pattern in x.name, accts))
        k8s = []
        for x in accts:
            j = K8sServiceAccount(config=self.config, name=x.name)
            j.model = x
            k8s.append(j)
        return k8s

    # ------------------------------------------------------------------------------------- add

    def add_api_token(self):
        return K8sSecret.create_service_account_api_token(
            config=self.config,
            name=self.name
        )

    def add_image_pull_secret(self, secret=None):
        if not isinstance(secret, K8sSecret):
            raise SyntaxError('K8sServiceAccount.add_image_pull_secret() secret: [ {} ] is invalid.'.format(secret))
        ref = LocalObjectReference()
        ref.name = secret.name
        refs = self.image_pull_secrets_refs
        refs.append(ref)
        self.image_pull_secrets = refs
        self.update()

    # ------------------------------------------------------------------------------------- secrets

    @property
    def secrets(self):
        secrets = K8sSecret.api_tokens_for_service_account(config=self.config, name=self.name)
        return secrets

    @secrets.setter
    def secrets(self, s=None):
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------- imagePullSecrets

    @property
    def image_pull_secrets_refs(self):
        refs = self.model.image_pull_secrets
        return refs

    @image_pull_secrets_refs.setter
    def image_pull_secrets_refs(self, s=None):
        raise NotImplementedError()

    @property
    def image_pull_secrets(self):
        refs = self.model.image_pull_secrets
        secrets = []
        for ref in refs:
            s = K8sSecret(config=self.config, name=ref.name).get()
            secrets.append(s)
        return secrets

    @image_pull_secrets.setter
    def image_pull_secrets(self, s=None):
        self.model.image_pull_secrets = s
