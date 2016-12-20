#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import json
import yaml

from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1.Secret import Secret


class K8sSecret(K8sObject):

    def __init__(self, config=None, name=None):
        super(K8sSecret, self).__init__(
            config=config,
            obj_type='Secret',
            name=name
        )

    # -------------------------------------------------------------------------------------  override

    def get(self):
        self.model = Secret(model=self.get_model())
        return self

    def create(self):
        super(K8sSecret, self).create()
        self.get()
        return self

    def update(self):
        super(K8sSecret, self).update()
        self.get()
        return self

    # -------------------------------------------------------------------------------------  service accounts

    @staticmethod
    def create_service_account_api_token(config=None, name=None):
        s = Secret()
        s.name = "{}-secret".format(name)
        s.add_annotation('kubernetes.io/service-account.name', name)
        s.type = 'kubernetes.io/service-account-token'
        k8s = K8sSecret(config=config, name=s.name)
        k8s.model = s
        k8s.create()
        return k8s

    @staticmethod
    def api_tokens_for_service_account(config=None, name=None):
        _list = K8sSecret(config=config, name="throwaway").list()
        _tokens = []
        for x in _list:
            s = Secret(model=x)
            if s.type == 'kubernetes.io/service-account-token':
                if s.metadata.annotations['kubernetes.io/service-account.name'] == name:
                    k8s = K8sSecret(config=config, name=s.name)
                    k8s.model = s
                    _tokens.append(k8s)
        return _tokens

    # ------------------------------------------------------------------------------------- data

    @property
    def data(self):
        return self.model.data

    @data.setter
    def data(self, data=None):
        self.model.data = data

    # ------------------------------------------------------------------------------------- type

    @property
    def type(self):
        return self.model.type

    @type.setter
    def type(self, t=None):
        self.model.type = t

    # ------------------------------------------------------------------------------------- dockerconfigjson

    @property
    def dockerconfigjson(self):
        data = None
        if self.model.dockerconfigjson is not None:
            data = json.loads(self.model.dockerconfigjson)
        return data

    @dockerconfigjson.setter
    def dockerconfigjson(self, secret=None):
        self.model.dockerconfigjson = secret

    # ------------------------------------------------------------------------------------- set

    def set_service_account_token(self, account_name=None, account_uid=None, token=None,
                                  kubecfg_data=None, cacert=None):
        self.model.set_service_account_token(
            account_name=account_name,
            account_uid=account_uid,
            token=token,
            kubecfg_data=kubecfg_data,
            cacert=cacert
        )
        return self
