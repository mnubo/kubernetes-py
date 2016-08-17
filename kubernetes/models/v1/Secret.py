#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.K8sExceptions import *
import base64


class Secret(BaseModel):
    def __init__(self, name=None, namespace='default', model=None):
        BaseModel.__init__(self)

        if name is None:
            raise SyntaxError('Secret: name: [ {0} ] cannot be None.'.format(name))
        if not isinstance(name, str):
            raise SyntaxError('Secret: name: [ {0} ] must be a string.'.format(name))

        if model is not None and not isinstance(model, dict):
            raise SyntaxError('Secret: model: [ {0} ] must be a dict.'.format(model))

        if model is not None:
            if 'status' in self.model:
                self.model.pop('status', None)
            self.model = model
            self.secret_metadata = ObjectMeta(model=self.model['metadata'])

        else:
            self.model = dict(kind='Secret', apiVersion='v1')
            self.secret_metadata = ObjectMeta(name=name, namespace=namespace)
            self._update_model()

    def _update_model(self):
        self.model['metadata'] = self.secret_metadata.get()
        return self

    # ------------------------------------------------------------------------------------- add

    def add_annotation(self, k=None, v=None):
        self.secret_metadata.add_annotation(k=k, v=v)
        return self

    def add_label(self, k=None, v=None):
        self.secret_metadata.add_label(k=k, v=v)
        return self

    # ------------------------------------------------------------------------------------- get

    def get_annotation(self, k):
        assert isinstance(k, str)
        return self.secret_metadata.get_annotation(k=k)

    def get_annotations(self):
        return self.secret_metadata.get_annotations()

    def get_label(self, k):
        assert isinstance(k, str)
        return self.secret_metadata.get_label(k=k)

    def get_labels(self):
        return self.secret_metadata.get_annotations()

    def get_data(self, k=None):
        if k is None:
            raise SyntaxError('Secret: k: [ {0} ] cannot be None.'.format(k))
        if not isinstance(k, str):
            raise SyntaxError('Secret: k: [ {0} ] must be a string.'.format(k.__class__.__name__))
        if 'data' not in self.model or k not in self.model['data']:
            raise NotFoundException('Secret: k: [ {0} ] not found.'.format(k))
        encoded = self.model['data'][k]
        return base64.b64decode(encoded)

    def get_type(self):
        return self.model['type']

    def get_dockercfg_secret(self):
        return self.get_data(k='.dockercfg')

    # ------------------------------------------------------------------------------------- set

    def set_annotations(self, new_dict):
        assert isinstance(new_dict, dict)
        self.secret_metadata.set_annotations(dico=new_dict)
        return self

    def set_data(self, k=None, v=None):
        if k is None or v is None:
            raise SyntaxError('Secret: k: [ {0} ] or v: [ {1} ] cannot be None.'.format(k, v))
        if not isinstance(k, str) or not isinstance(v, str):
            raise SyntaxError('Secret: k: [ {0} ] or v: [ {1} ] must be a string.'.format(k, v))
        if 'data' not in self.model:
            self.model['data'] = dict()
        self.model['data'][k] = base64.b64encode(v)
        return self

    def set_dockercfg_secret(self, data=None):
        if data is None:
            raise SyntaxError('Secret: data: [ {0} ] cannot be None.'.format(data))
        if not isinstance(data, str):
            raise SyntaxError('Secret: data: [ {0} ] must be a string'.format(data))
        self.set_type(secret_type='kubernetes.io/dockercfg')
        self.set_data(k='.dockercfg', v=data)
        return self

    def set_dockercfg_json_secret(self, data=None):
        if data is None:
            raise SyntaxError('Secret: data: [ {0} ] cannot be None.'.format(data))
        if not isinstance(data, str):
            raise SyntaxError('Secret: data: [ {0} ] must be a string'.format(data))
        self.set_type(secret_type='kubernetes.io/dockerconfigjson')
        self.set_data(k='.dockerconfigjson', v=data)
        return self

    def set_labels(self, new_dict):
        assert isinstance(new_dict, dict)
        self.secret_metadata.set_labels(dico=new_dict)
        return self

    def set_service_account_token(self, account_name=None, account_uid=None,
                                  token=None, kubecfg_data=None, cacert=None):

        if account_name is None or account_uid is None or token is None:
            raise SyntaxError('Secret: account_name: [ {0} ], account_uid: [ {1} ] or token: [ {2} ] '
                              'cannot be None'.format(account_name, account_uid, token))
        if not isinstance(account_name, str) or not isinstance(account_uid, str) or not isinstance(token, str):
            raise SyntaxError('Secret: account_name: [ {0} ], account_uid: [ {1} ] or token: [ {2} ] '
                              'must be strings'.format(account_name, account_uid, token))

        self.set_type(secret_type='kubernetes.io/service-account-token')
        self.secret_metadata.add_annotation(k='kubernetes.io/service-account.name', v=account_name)
        self.secret_metadata.add_annotation(k='kubernetes.io/service-account.uid', v=account_uid)
        self.set_data(k='token', v=token)

        if kubecfg_data is not None and isinstance(kubecfg_data, str):
            self.set_data(k='kubernetes.kubeconfig', v=kubecfg_data)
        if cacert is not None and isinstance(cacert, str):
            self.set_data(k='ca.crt', v=cacert)

        return self

    def set_type(self, secret_type=None):
        if secret_type is None:
            raise SyntaxError('Secret: secret_type: [ {0} ] cannot be None.'.format(secret_type))
        if not isinstance(secret_type, str):
            raise SyntaxError('Secret: secret_type: [ {0} ] must be a string'.format(secret_type))
        self.model['type'] = secret_type
        return self
