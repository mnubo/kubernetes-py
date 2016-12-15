#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import json
import time

import yaml

from kubernetes.K8sConfig import K8sConfig
from kubernetes.K8sExceptions import *
from kubernetes.models.unversioned.BaseUrls import BaseUrls
from kubernetes.models.v1.DeleteOptions import DeleteOptions
from kubernetes.utils import HttpRequest, is_valid_dict, str_to_class

VALID_K8s_OBJS = [
    'CronJob',
    'DaemonSet',
    'Deployment',
    'Job',
    'PersistentVolume',
    'PersistentVolumeClaim',
    'PetSet',
    'Pod',
    'ReplicaSet',
    'ReplicationController',
    'Secret',
    'Service',
    'Volume'
]


class K8sObject(object):

    DELETE_TIMEOUT_SECONDS = 60

    def __init__(self, config=None, obj_type=None, name=None):
        super(K8sObject, self).__init__()

        if config is not None and not isinstance(config, K8sConfig):
            raise SyntaxError('K8sObject: config: [ {0} ] must be of type K8sConfig.'.format(config.__class__.__name__))
        if config is None:
            config = K8sConfig()
        self.config = config

        if obj_type not in VALID_K8s_OBJS:
            valid = ", ".join(VALID_K8s_OBJS)
            raise SyntaxError('K8sObject: obj_type: [ {0} ] must be in: [ {1} ]'.format(obj_type, valid))
        self.obj_type = obj_type

        self.model = str_to_class(obj_type)
        self.name = name

        try:
            urls = BaseUrls(api=self.config.version, namespace=self.config.namespace)
            self.base_url = urls.get_base_url(object_type=obj_type)
        except:
            raise Exception('Could not set BaseUrl for type: [ {0} ]'.format(obj_type))

    def __str__(self):
        return "{}".format(self.model.serialize())

    def __eq__(self, other):
        # see https://github.com/kubernetes/kubernetes/blob/release-1.3/docs/design/identifiers.md
        if isinstance(other, self.__class__):
            return self.config.namespace == other.config.namespace and self.name == other.name
        return NotImplemented

    # ------------------------------------------------------------------------------------- get

    def get_annotation(self, k=None):
        if k in self.model.metadata.annotations:
            return self.model.metadata.annotations[k]
        return None

    def get_label(self, k=None):
        if k in self.model.metadata.labels:
            return self.model.metadata.labels[k]
        return None

    # ------------------------------------------------------------------------------------- add

    def add_annotation(self, k=None, v=None):
        anns = self.model.metadata.annotations
        if anns is None:
            anns = {}
        anns.update({k: str(v)})
        self.model.metadata.annotations = anns
        return self

    def add_label(self, k=None, v=None):
        labels = self.model.metadata.labels
        if labels is None:
            labels = {}
        labels.update({k: v})
        self.model.metadata.labels = labels
        return self

    # ------------------------------------------------------------------------------------- del

    def del_annotation(self, k=None):
        orig = self.model.metadata.annotations
        if k in orig:
            orig.pop(k)
            self.model.metadata.annotations = orig
        return self

    def del_label(self, k=None):
        orig = self.model.metadata.labels
        if k in orig:
            orig.pop(k)
            self.model.metadata.labels = orig
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
        self.model.metadata.labels['name'] = name

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        return self.model.serialize()

    def as_json(self):
        data = self.serialize()
        dump = json.dumps(data, indent=4)
        return dump

    def as_yaml(self):
        data = self.serialize()
        dump = yaml.dump(data, default_flow_style=False)
        return dump

    # ------------------------------------------------------------------------------------- remote API calls

    def request(self, method='GET', host=None, url=None, auth=None, cert=None,
                data=None, token=None, ca_cert=None, ca_cert_data=None):

        host = self.config.api_host if host is None else host
        url = self.base_url if url is None else url
        auth = self.config.auth if auth is None else auth
        cert = self.config.cert if cert is None else cert
        token = self.config.token if token is None else token
        ca_cert = self.config.ca_cert if ca_cert is None else ca_cert
        ca_cert_data = self.config.ca_cert_data if ca_cert_data is None else ca_cert_data

        r = HttpRequest(
            method=method,
            host=host,
            url=url,
            auth=auth,
            cert=cert,
            ca_cert=ca_cert,
            ca_cert_data=ca_cert_data,
            data=data,
            token=token
        )

        try:
            return r.send()
        except IOError as err:
            raise BadRequestException('K8sObject: IOError: {0}'.format(err))

    def list(self):
        state = self.request(method='GET')
        if not state.get('status'):
            raise Exception('K8sObject: Could not fetch list of objects of type: [ {0} ]'.format(self.obj_type))
        if not state.get('success'):
            status = state.get('status', '')
            state_data = state.get('data', dict())
            reason = state_data['message'] if 'message' in state_data else state_data
            message = 'K8sObject: CREATE failed : HTTP {0} : {1}'.format(status, reason)
            if int(status) == 401:
                raise UnauthorizedException(message)
            if int(status) == 409:
                raise AlreadyExistsException(message)
            if int(status) == 422:
                raise UnprocessableEntityException(message)
            raise BadRequestException(message)
        return state.get('data', dict()).get('items', list())

    def get_model(self):
        if self.name is None:
            raise SyntaxError('K8sObject: name: [ {0} ] must be set to fetch the object.'.format(self.name))

        url = '{base}/{name}'.format(base=self.base_url, name=self.name)
        state = self.request(method='GET', url=url)

        if not state.get('success'):
            status = state.get('status', '')
            reason = state.get('data', dict()).get('message', None)
            message = 'K8sObject: GET [ {0}:{1} ] failed: HTTP {2} : {3} '.format(self.obj_type, self.name, status,
                                                                                  reason)
            raise NotFoundException(message)

        model = state.get('data')
        return model

    def get_with_params(self, data=None):
        if not is_valid_dict(data):
            raise SyntaxError('K8sObject.get_with_params(): data: [ {0} ] is invalid.'.format(data))
        url = '{base}'.format(base=self.base_url)
        state = self.request(method='GET', url=url, data=data)
        return state.get('data', None).get('items', list())

    def create(self):
        if self.name is None:
            raise SyntaxError('K8sObject: name: [ {0} ] must be set to CREATE the object.'.format(self.name))

        # HTTP 500 : resourceVersion may not be set on objects to be created
        if self.model.metadata.resource_version is not None:
            self.model.metadata.resource_version = None

        url = '{base}'.format(base=self.base_url)
        post_data = self.serialize()
        state = self.request(method='POST', url=url, data=post_data)

        if not state.get('success'):
            status = state.get('status', '')
            state_data = state.get('data', dict())
            reason = state_data['message'] if 'message' in state_data else state_data
            message = 'K8sObject: CREATE failed : HTTP {0} : {1} : {2}'.format(status, reason, post_data)
            if int(status) == 401:
                raise UnauthorizedException(message)
            if int(status) == 409:
                raise AlreadyExistsException(message)
            if int(status) == 422:
                raise UnprocessableEntityException(message)
            raise BadRequestException(message)
        return self

    def update(self):
        if self.name is None:
            raise SyntaxError('K8sObject: name: [ {0} ] must be set to UPDATE the object.'.format(self.name))

        self.model.metadata.strip(self.model.kind)  # strip server-generated metadata before posting updates

        url = '{base}/{name}'.format(base=self.base_url, name=self.name)
        state = self.request(method='PUT', url=url, data=self.serialize())

        if not state.get('success'):
            status = state.get('status', '')
            reason = state.get('data', dict()).get('message', None)
            message = 'K8sObject: UPDATE failed: HTTP {0} : {1}'.format(status, reason)
            if int(status) == 404:
                raise NotFoundException(message)
            if int(status) == 422:
                raise UnprocessableEntityException(message)
            raise BadRequestException(message)

        return self

    def delete(self, orphan=False):
        if self.name is None:
            raise SyntaxError('K8sObject: name: [ {0} ] must be set to DELETE the object.'.format(self.name))

        url = '{base}/{name}'.format(base=self.base_url, name=self.name)

        delete_opts = DeleteOptions()
        delete_opts.orphan_dependents = orphan

        state = self.request(method='DELETE', url=url, data=delete_opts.serialize())

        if not state.get('success'):
            status = state.get('status', '')
            reason = state.get('data', dict()).get('message', None)
            message = 'K8sObject: DELETE failed: HTTP {0} : {1}'.format(status, reason)
            if int(status) == 404:
                raise NotFoundException(message)
            raise BadRequestException(message)

        if state.get('success'):
            start_time = time.time()
            try:
                while True:
                    time.sleep(0.2)
                    self.get_model()
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= self.DELETE_TIMEOUT_SECONDS:
                        raise TimedOutException("Timed out on DELETE object: [ {0} ]".format(self.name))
            except NotFoundException:
                pass

        return self
