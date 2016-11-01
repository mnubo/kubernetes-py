#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.BaseModel import BaseModel


class ObjectMeta(BaseModel):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_objectmeta
    """

    def __init__(self):
        super(ObjectMeta, self).__init__()

        self.name = None
        self.generate_name = None
        self.namespace = None
        self.deletion_grace_period_seconds = None
        self.labels = None
        self.annotations = None

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
