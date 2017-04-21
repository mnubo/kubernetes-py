#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import json
import uuid

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
        self.model = Secret(self.get_model())
        return self

    def create(self):
        super(K8sSecret, self).create()
        self.get()
        return self

    def update(self):
        super(K8sSecret, self).update()
        self.get()
        return self

    def list(self, pattern=None):
        ls = super(K8sSecret, self).list()
        secrets = list(map(lambda x: Secret(x), ls))
        if pattern is not None:
            secrets = list(filter(lambda x: pattern in x.name, secrets))
        k8s = []
        for x in secrets:
            j = K8sSecret(config=self.config, name=x.name)
            j.model = x
            k8s.append(j)
        return k8s

    # -------------------------------------------------------------------------------------  image pull secrets

    @staticmethod
    def create_image_pull_secret(config=None, prefix=None, name=None, data=None):
        s = Secret()

        if name is not None:
            s.name = "{0}-docker-{1}".format(name, str(uuid.uuid4().hex[:5]))
        elif name is None and prefix is not None:
            s.name = "{0}-docker-{1}".format(prefix, str(uuid.uuid4().hex[:5]))
        else:
            s.name = "docker-{0}".format(str(uuid.uuid4().hex[:5]))

        s.dockerconfigjson = data
        k8s = K8sSecret(config=config, name=s.name)
        k8s.model = s
        k8s.create()
        return k8s

    @staticmethod
    def list_image_pull_secrets(config=None):
        _list = K8sSecret(config=config, name="yo").list()
        secrets = []
        for x in _list:
            if x.type == Secret.K8s_TYPE_DOCKER_CONFIG:
                secrets.append(x)
        return secrets

    @staticmethod
    def image_pull_secret_with_name(config=None, name=None):
        _secrets = K8sSecret.list_image_pull_secrets(config=config)
        _list = list(filter(lambda x: x.name == name, _secrets))
        if len(_list):
            return _list[0]
        return None

    # -------------------------------------------------------------------------------------  service accounts

    @staticmethod
    def create_service_account_api_token(config=None, name=None):
        s = Secret()
        s.name = "{}-token-{}".format(name, str(uuid.uuid4().hex[:5]))
        s.add_annotation(Secret.K8s_ANNOTATION_SERVICE_ACCOUNT_NAME, name)
        s.type = Secret.K8s_TYPE_SERVICE_ACCOUNT
        k8s = K8sSecret(config=config, name=s.name)
        k8s.model = s
        k8s.create()
        return k8s

    @staticmethod
    def api_tokens_for_service_account(config=None, name=None):
        _list = K8sSecret(config=config, name="yo").list()
        _tokens = []
        for x in _list:
            if x.type == Secret.K8s_TYPE_SERVICE_ACCOUNT:
                if x.annotations[Secret.K8s_ANNOTATION_SERVICE_ACCOUNT_NAME] == name:
                    _tokens.append(x)
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
