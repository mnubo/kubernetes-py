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
        self.model = Secret()
        super(K8sSecret, self).__init__(config=config, obj_type='Secret', name=name)
        self.name = name

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

    # ------------------------------------------------------------------------------------- add

    def add_annotation(self, k=None, v=None):
        self.model.add_annotation(k=k, v=v)
        return self

    def add_label(self, k=None, v=None):
        self.model.add_label(k=k, v=v)
        return self

    # ------------------------------------------------------------------------------------- annotations

    @property
    def annotations(self):
        return self.model.metadata.annotations

    @annotations.setter
    def annotations(self, anns=None):
        self.model.metadata.annotations = anns

    # ------------------------------------------------------------------------------------- labels

    @property
    def labels(self):
        return self.model.metadata.labels

    @labels.setter
    def labels(self, labels=None):
        self.model.metadata.labels = labels

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self.model.metadata.name

    @name.setter
    def name(self, name=None):
        self.model.metadata.name = name

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

    # ------------------------------------------------------------------------------------- dockercfg

    @property
    def dockercfg(self):
        return self.model.dockercfg

    @dockercfg.setter
    def dockercfg(self, secret=None):
        self.model.dockercfg = secret

    # ------------------------------------------------------------------------------------- dockercfg json

    @property
    def dockercfg_json(self):
        return self.model.dockercfg_json

    @dockercfg_json.setter
    def dockercfg_json(self, secret=None):
        self.model.dockercfg_json = secret

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
