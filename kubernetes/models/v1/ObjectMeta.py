#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, is_valid_list, filter_model


class ObjectMeta(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_objectmeta
    """

    def __init__(self, model=None):
        super(ObjectMeta, self).__init__()
        self._annotations = None
        self._deletion_grace_period_seconds = None
        self._generate_name = None
        self._labels = None
        self._name = None
        self._namespace = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'creation_timestamp' in model:
            self.creation_timestamp = model['creation_timestamp']
        if 'name' in model:
            self.name = model['name']
        if 'namespace' in model:
            self.namespace = model['namespace']
        if 'resourceVersion' in model:
            self.resource_version = model['resourceVersion']
        if 'selfLink' in model:
            self.self_link = model['selfLink']
        if 'uid' in model:
            self.uid = model['uid']

    # ------------------------------------------------------------------------------------- annotations

    @property
    def annotations(self):
        return self._annotations

    @annotations.setter
    def annotations(self, anns=None):
        if not is_valid_list(anns, dict):
            raise SyntaxError('ObjectMeta: annotations: [ {0} ] is invalid.'.format(anns))
        self._annotations = anns

    # ------------------------------------------------------------------------------------- deletion grace period

    @property
    def deletion_grace_period_seconds(self):
        return self._annotations

    @deletion_grace_period_seconds.setter
    def deletion_grace_period_seconds(self, secs=None):
        if not isinstance(secs, int):
            raise SyntaxError('ObjectMeta: deletion_grace_period_seconds: [ {0} ] is invalid.'.format(secs))
        self._deletion_grace_period_seconds = secs

    # ------------------------------------------------------------------------------------- generate name

    @property
    def generate_name(self):
        return self._generate_name

    @generate_name.setter
    def generate_name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('ObjectMeta: generate_name: [ {0} ] is invalid.'.format(name))
        self._generate_name = name

    # ------------------------------------------------------------------------------------- labels

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, labels=None):
        if not is_valid_list(labels, dict):
            raise SyntaxError('ObjectMeta: labels: [ {0} ] is invalid.'.format(labels))
        self._labels = labels

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('ObjectMeta: name: [ {0} ] is invalid.'.format(name))
        self._name = name

    # ------------------------------------------------------------------------------------- namespace

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, namespace=None):
        if not is_valid_string(namespace):
            raise SyntaxError('ObjectMeta: namespace: [ {0} ] is invalid.'.format(namespace))
        self._namespace = namespace

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.annotations is not None:
            data['annotations'] = self.annotations
        if self.generate_name and not self.name:
            data['generateName'] = self.generate_name
        if self.labels:
            data['labels'] = self.labels
        if self.name:
            data['name'] = self.name
        if self.namespace:
            data['namespace'] = self.namespace
        return data
