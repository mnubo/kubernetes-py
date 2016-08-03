#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import HttpRequest
from kubernetes.models.v1.BaseUrls import BaseUrls
from kubernetes.models.v1.BaseModel import BaseModel
from kubernetes.models.v1.DeleteOptions import DeleteOptions
from kubernetes.K8sConfig import K8sConfig
from kubernetes.K8sExceptions import *
import json

VALID_K8s_OBJS = ['Pod', 'ReplicationController', 'Secret', 'Service']


class K8sObject(object):

    def __init__(self, config=None, name=None, obj_type=None):

        if config is not None and not isinstance(config, K8sConfig):
            raise SyntaxError('K8sObject: config: [ {0} ] must be of type K8sConfig.'.format(config.__class__.__name__))
        if config is None:
            config = K8sConfig()
        self.config = config

        if name is None:
            raise SyntaxError('K8sObject: name: [ {0} ] cannot be None.'.format(name))
        if not isinstance(name, str):
            raise SyntaxError('K8sObject: name: [ {0} ] must be a string.'.format(name.__class__.__name__))

        if obj_type is None or not isinstance(obj_type, str):
            raise SyntaxError('K8sObject: obj_type: [ {0} ] must be a string.'.format(obj_type.__class__.__name__))

        if obj_type not in VALID_K8s_OBJS:
            valid = ", ".join(VALID_K8s_OBJS)
            raise SyntaxError('K8sObject: obj_type: [ {0} ] must be in: [ {1} ]'.format(obj_type, valid))

        self.obj_type = obj_type
        self.name = name
        self.model = BaseModel()

        try:
            urls = BaseUrls(version=self.config.version, namespace=self.config.namespace)
            self.base_url = urls.get_base_url(object_type=obj_type)
        except:
            raise Exception('Could not set BaseUrl for type: [ {0} ]'.format(obj_type))

    def __str__(self):
        return "[ {0} ] named [ {1} ]. Model: [ {2} ]".format(self.obj_type, self.name, self.model.get())

    def as_dict(self):
        return self.model.get()

    def as_json(self):
        return json.dumps(self.model.get())

    def set_name(self, name):
        self.name = name
        if self.model is not None:
            my_method = getattr(self.model, "set_name", None)
            if callable(my_method):
                my_method(name=name)
        return self

    # ------------------------------------------------------------------------------------- remote API calls

    def request(self, method='GET', host=None, url=None, auth=None, cert=None, data=None, token=None, ca_cert=None):
        host = self.config.api_host if host is None else host
        url = self.base_url if url is None else url
        auth = self.config.auth if auth is None else auth
        cert = self.config.cert if cert is None else cert
        token = self.config.token if token is None else token
        ca_cert = self.config.ca_cert if ca_cert is None else ca_cert

        r = HttpRequest(
            method=method,
            host=host,
            url=url,
            auth=auth,
            cert=cert,
            ca_cert=ca_cert,
            data=data,
            token=token
        )
        return r.send()

    def list(self):
        state = self.request(method='GET')
        if not state.get('status'):
            raise Exception('Could not fetch list of objects of type: {this_type}.'.format(this_type=self.obj_type))
        return state.get('data', dict()).get('items', list())

    def get_model(self):
        if self.name is None:
            raise SyntaxError('K8sObject: name: [ {0} ] must be set to fetch the object.'.format(self.name))

        url = '{base}/{name}'.format(base=self.base_url, name=self.name)
        state = self.request(method='GET', url=url)

        if not state.get('success'):
            status = state.get('status', '')
            reason = state.get('data', dict()).get('message', None)
            message = 'K8sObject: GET [ {0}:{1} ] failed: HTTP {2} : {3} '.format(self.obj_type, self.name, status, reason)
            raise NotFoundException(message)

        model = state.get('data')
        return model

    def get_with_params(self, data=None):
        if data is None:
            raise SyntaxError('K8sObject: data: [ {0} ] cannot be None.'.format(data))
        if not isinstance(data, dict):
            raise SyntaxError('K8sObject: data: [ {0} ] must be a dict.'.format(data.__class__.__name__))

        url = '{base}'.format(base=self.base_url)
        state = self.request(method='GET', url=url, data=data)

        return state.get('data', None).get('items', list())

    def create(self):
        if self.name is None:
            raise SyntaxError('K8sObject: name: [ {0} ] must be set to CREATE the object.'.format(self.name))

        url = '{base}'.format(base=self.base_url)
        state = self.request(method='POST', url=url, data=self.model.get())

        if not state.get('success'):
            status = state.get('status', '')
            reason = state.get('data', dict()).get('message', None)
            message = 'K8sObject: CREATE failed : HTTP {0} : {1}'.format(status, reason)
            if int(status) == 409:
                raise AlreadyExistsException(message)
            if int(status) == 422:
                raise UnprocessableEntityException(message)
            raise BadRequestException(message)

        return self

    def update(self):
        if self.name is None:
            raise SyntaxError('K8sObject: name: [ {0} ] must be set to UPDATE the object.'.format(self.name))

        url = '{base}/{name}'.format(base=self.base_url, name=self.name)
        state = self.request(method='PUT', url=url, data=self.model.get())

        if not state.get('success'):
            status = state.get('status', '')
            reason = state.get('data', dict()).get('message', None)
            message = 'K8sObject: UPDATE failed: HTTP {0} : {1}'.format(status, reason)
            raise BadRequestException(message)

        return self

    def delete(self):
        if self.name is None:
            raise SyntaxError('K8sObject: name: [ {0} ] must be set to DELETE the object.'.format(self.name))

        url = '{base}/{name}'.format(base=self.base_url, name=self.name)
        self.model = DeleteOptions(kind='DeleteOptions')
        state = self.request(method='DELETE', url=url, data=self.model.get())

        if not state.get('success'):
            status = state.get('status', '')
            reason = state.get('data', dict()).get('message', None)
            message = 'K8sObject: DELETE failed: HTTP {0} : {1}'.format(status, reason)
            if status == 404:
                raise NotFoundException(message)
            raise BadRequestException(message)

        return self
