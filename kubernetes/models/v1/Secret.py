#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import base64

from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.utils import is_valid_string, is_valid_dict


class Secret(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_secret
    """

    def __init__(self, model=None):

        super(Secret, self).__init__()

        self._kind = 'Secret'
        self._api_version = 'v1'
        self._metadata = ObjectMeta()
        self._data = {}
        self._string_data = {}
        self._type = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'kind' in model:
            self.kind = model['kind']
        if 'apiVersion' in model:
            self.api_version = model['apiVersion']
        if 'metadata' in model:
            self.metadata = ObjectMeta(model=model['metadata'])
        if 'data' in model:
            d = {}
            for k, v in model['data'].items():
                d[k] = base64.b64decode(v)
            self.data = d
        if 'stringData' in model:
            self.string_data = model['stringData']
        if 'type' in model:
            self.type = model['type']

    def __eq__(self, other):
        # see https://github.com/kubernetes/kubernetes/blob/release-1.3/docs/design/identifiers.md
        if isinstance(other, self.__class__):
            return self.metadata.name == other.metadata.name
        return NotImplemented

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
        return d

    @data.setter
    def data(self, data=None):
        msg = 'Secret: data: [ {0} ] is invalid.'.format(data)
        if not is_valid_dict(data):
            raise SyntaxError(msg)
        for k, v in data.items():
            if not is_valid_string(k) or not is_valid_string(v):
                raise SyntaxError(msg)
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

    # ------------------------------------------------------------------------------------- dockercfg

    @property
    def dockercfg(self):
        s = self.data['.dockercfg']
        return base64.b64decode(s)

    @dockercfg.setter
    def dockercfg(self, secret=None):
        if not is_valid_string(secret):
            raise SyntaxError('Secret: dockercfg: [ {} ] is invalid.'.format(secret))
        self.data = {'.dockercfg': base64.b64encode(secret)}
        self.type = 'kubernetes.io/dockercfg'

    # ------------------------------------------------------------------------------------- dockercfg json

    @property
    def dockercfg_json(self):
        if '.dockerconfigjson' in self.data:
            return self.data['.dockerconfigjson']
        return None

    @dockercfg_json.setter
    def dockercfg_json(self, secret=None):
        if not is_valid_string(secret):
            raise SyntaxError('Secret: dockercfg_json: [ {} ] is invalid.'.format(secret))
        self.type = 'kubernetes.io/dockerconfigjson'
        self.data = {'.dockerconfigjson': secret}

    # ------------------------------------------------------------------------------------- service account token

    def set_service_account_token(self, account_name=None, account_uid=None,
                                  token=None, kubecfg_data=None, cacert=None):

        if not is_valid_string(account_name):
            raise SyntaxError('Secret.set_service_account() account_name: [ {} ] is invalid.'.format(account_name))
        if not is_valid_string(account_uid):
            raise SyntaxError('Secret.set_service_account() account_uid: [ {} ] is invalid.'.format(account_uid))
        if not is_valid_string(token):
            raise SyntaxError('Secret.set_service_account() token: [ {} ] is invalid.'.format(token))

        anns = {
            'kubernetes.io/service-account.name': account_name,
            'kubernetes.io/service-account.uid': account_uid
        }

        self.type = 'kubernetes.io/service-account-token'
        self.metadata.annotations = anns
        self.data = {'token': token}

        if is_valid_string(kubecfg_data):
            d = self.data
            d['kubernetes.kubeconfig'] = kubecfg_data
            self.data = d

        if is_valid_string(cacert):
            d = self.data
            d['ca.crt'] = cacert
            self.data = d

        return self

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.kind is not None:
            data['kind'] = self.kind
        if self.api_version is not None:
            data['apiVersion'] = self.api_version
        if self.metadata is not None:
            data['metadata'] = self.metadata.serialize()
        if self.data is not None:
            d = {}
            for k, v in self.data.items():
                d[k] = base64.b64encode(v)
            data['data'] = d
        if self.string_data is not None:
            data['stringData'] = self.string_data
        if self.type is not None:
            data['type'] = self.type
        return data
