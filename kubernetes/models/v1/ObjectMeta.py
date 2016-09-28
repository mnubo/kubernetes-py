#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.BaseModel import BaseModel


class ObjectMeta(BaseModel):
    def __init__(self, model=None, name=None, generate_name=None, namespace='default'):
        BaseModel.__init__(self)

        self.name = name
        self.generate_name = generate_name
        self.namespace = namespace
        self.labels = {}
        self.annotations = {}

        if model is not None and isinstance(model, dict):
            self.name = model.get('name', None)
            self.generate_name = model.get('generate_name', None)
            self.namespace = model.get('namespace', None)
            self.labels = model.get('labels', {})
            self.annotations = model.get('annotations', {})

    # ------------------------------------------------------------------------------------- add

    def add_annotation(self, k=None, v=None):
        self.annotations[str(k)] = str(v)
        return self

    def add_label(self, k=None, v=None):
        self.labels[str(k)] = str(v)
        return self

    # ------------------------------------------------------------------------------------- delete

    def del_annotation(self, k=None):
        if k in self.annotations:
            self.annotations.pop(k)
        return self

    def del_label(self, k=None):
        if k in self.labels:
            self.labels.pop(k)
        return self

    # ------------------------------------------------------------------------------------- serialize

    def json(self):
        data = {}
        if self.name:
            data['name'] = self.name
        if self.generate_name:
            data['generateName'] = self.generate_name
        if self.namespace:
            data['namespace'] = self.namespace
        if self.labels:
            data['labels'] = self.labels
        if self.annotations:
            data['annotations'] = self.annotations
        return data
