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
        return self.model.dockerconfigjson

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
