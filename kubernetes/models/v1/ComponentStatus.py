#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.unversioned.BaseModel import BaseModel
from kubernetes.models.v1.ComponentCondition import ComponentCondition
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.utils import filter_model


class ComponentStatus(BaseModel):
    """
    https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_componentstatus
    """

    def __init__(self, model=None):
        super(ComponentStatus, self).__init__(model=model)

        self._conditions = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        super(ComponentStatus, self).build_with_model(model)

        if 'conditions' in model:
            if not isinstance(model['conditions'], list):
                raise SyntaxError('ComponentStatus: _build_with_model: conditions : [ {0} ] is invalid.'
                                  .format(model['conditions']))
            l = list()
            for c in model['conditions']:
                l.append(ComponentCondition(c))
            self.conditions = l

    # ------------------------------------------------------------------------------------- conditions

    @property
    def conditions(self):
        return self._conditions

    @conditions.setter
    def conditions(self, l):
        if not isinstance(l, list):
            raise SyntaxError('ComponentStatus: conditions: [ {0} ] is invalid.'.format(l))
        self._conditions = l

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(ComponentStatus, self).serialize()

        if self.conditions:
            l = list()
            for c in self.conditions:
                l.append(c.serialize())
            data['conditions'] = l
        return data
