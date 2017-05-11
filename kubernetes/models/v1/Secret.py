#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import base64
import json

from six import string_types
from kubernetes.models.unversioned.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.utils import is_valid_string, is_valid_dict


class Secret(BaseModel):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_secret
    """

    K8s_ANNOTATION_SERVICE_ACCOUNT_NAME = "kubernetes.io/service-account.name"
    K8s_ANNOTATION_SERVICE_ACCOUNT_UID = "kubernetes.io/service-account.uid"
    K8s_TYPE_DOCKER_CONFIG = "kubernetes.io/dockerconfigjson"
    K8s_TYPE_SERVICE_ACCOUNT = "kubernetes.io/service-account-token"
    K8s_TYPE_OPAQUE = "Opaque"
    K8s_TYPE_DOCKER_CONFIG_V1 = "kubernetes.io/dockercfg"
    K8s_TYPE_BASIC_AUTH = "kubernetes.io/basic-auth"
    K8s_TYPE_SSH_AUTH = "kubernetes.io/ssh-auth"
    K8s_TYPE_TLS = "kubernetes.io/tls"

    def __init__(self, model=None):
        super(Secret, self).__init__()

        self.kind = 'Secret'
        self.api_version = 'v1'

        self._data = {}
        self._string_data = None
        self._type = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        super(Secret, self).build_with_model(model)

        if 'data' in model:
            d = {}
            for k, v in model['data'].items():
                d[k] = base64.b64decode(v)
            self.data = d
        if 'stringData' in model:
            self.string_data = model['stringData']
        if 'type' in model:
            self.type = model['type']

    # ------------------------------------------------------------------------------------- add

    def add_annotation(self, k=None, v=None):
        anns = self.metadata.annotations
        if anns is None:
            anns = {}
        anns.update({k: v})
        self.metadata.annotations = anns
        return self

    def add_label(self, k=None, v=None):
        labels = self.metadata.labels
        if labels is None:
            labels = {}
        labels.update({k: v})
        self.metadata.labels = labels
        return self

    # ------------------------------------------------------------------------------------- kind

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, k=None):
        if not is_valid_string(k):
            raise SyntaxError('Secret: kind: [ {0} ] is invalid.'.format(k))
        self._kind = k

    # ------------------------------------------------------------------------------------- apiVersion

    @property
    def api_version(self):
        return self._api_version

    @api_version.setter
    def api_version(self, v=None):
        if not is_valid_string(v):
            raise SyntaxError('Secret: api_version: [ {0} ] is invalid.'.format(v))
        self._api_version = v

    # ------------------------------------------------------------------------------------- labels

    @property
    def labels(self):
        return self.metadata.labels

    @labels.setter
    def labels(self, labels=None):
        if not is_valid_dict(labels):
            raise SyntaxError('Secret: labels: [ {0} ] is invalid.'.format(labels))
        self.metadata.labels = labels

    # ------------------------------------------------------------------------------------- metadata

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, md=None):
        if not isinstance(md, ObjectMeta):
            raise SyntaxError('Secret: metadata: [ {0} ] is invalid.'.format(md))
        self._metadata = md

    # ------------------------------------------------------------------------------------- data

    @property
    def data(self):
        d = {}
        for k, v in self._data.items():
            d[k] = base64.b64decode(v)
            if isinstance(d[k], bytes):
                d[k] = d[k].decode()
            elif is_valid_string(d[k]):
                d[k] = d[k].decode()
        return d

    @data.setter
    def data(self, data=None):
        msg = 'Secret: data: [ {0} ] is invalid.'.format(data)

        if isinstance(data, string_types):
            try:
                data = json.loads(data)
            except ValueError:
                raise SyntaxError(msg)

        if not is_valid_dict(data):
            raise SyntaxError(msg)

        for k, v in data.items():
            if not is_valid_string(k):
                raise SyntaxError(msg)
            if not isinstance(v, bytes):
                try:
                    v = bytearray(v, 'UTF-8')
                except:
                    raise SyntaxError('Could not convert [ {0} ] to bytes.'.format(v))
            self._data[k] = base64.b64encode(v)

    # ------------------------------------------------------------------------------------- stringData

    @property
    def string_data(self):
        return self._string_data

    @string_data.setter
    def string_data(self, data=None):
        if not is_valid_dict(data):
            raise SyntaxError('Secret: string_data: [ {0} ] is invalid.'.format(data))
        self._string_data = data

    # ------------------------------------------------------------------------------------- type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, t=None):
        if not is_valid_string(t):
            raise SyntaxError('Secret: type: [ {0} ] is invalid.'.format(t))
        self._type = t

    # ------------------------------------------------------------------------------------- dockercfg json

    @property
    def dockerconfigjson(self):
        if '.dockerconfigjson' in self.data:
            return self.data['.dockerconfigjson']
        return None

    @dockerconfigjson.setter
    def dockerconfigjson(self, secret=None):
        if not is_valid_dict(secret):
            raise SyntaxError('Secret: .dockerconfigjson: [ {} ] is invalid.'.format(secret))
        self.type = self.K8s_TYPE_DOCKER_CONFIG
        s = json.dumps(secret)
        utf = s.encode('utf-8')
        self.data = {'.dockerconfigjson': utf}

    # ------------------------------------------------------------------------------------- service account token

    def set_service_account_token(self, account_name=None, account_uid=None,
                                  token=None, kubecfg_data=None, cacert=None):

        for x in [account_name, account_uid, token]:
            if not is_valid_string(x):
                raise SyntaxError('Secret.set_service_account() account_name: [ {} ] is invalid.'.format(x))
        if not is_valid_string(account_uid):
            raise SyntaxError('Secret.set_service_account() account_uid: [ {} ] is invalid.'.format(account_uid))
        if not is_valid_string(token):
            raise SyntaxError('Secret.set_service_account() token: [ {} ] is invalid.'.format(token))

        anns = {
            self.K8s_ANNOTATION_SERVICE_ACCOUNT_NAME: account_name,
            self.K8s_ANNOTATION_SERVICE_ACCOUNT_UID: account_uid
        }

        self.type = self.K8s_TYPE_SERVICE_ACCOUNT
        self.metadata.annotations = anns
        self.data = {'token': token}

        if is_valid_string(kubecfg_data):
            d = self.data
            d.update({'kubernetes.kubeconfig': kubecfg_data})
            self.data = d

        if is_valid_string(cacert):
            d = self.data
            d.update({'ca.crt': cacert})
            self.data = d

        return self

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(Secret, self).serialize()

        if self.data is not None:
            d = {}
            for k, v in self.data.items():
                if is_valid_string(v):
                    v = bytearray(source=v, encoding='UTF-8')
                d[k] = base64.b64encode(v)
                if isinstance(d[k], bytes):
                    d[k] = d[k].decode()
            data['data'] = d
        if self.string_data is not None:
            data['stringData'] = self.string_data
        if self.type is not None:
            data['type'] = self.type
        return data
