#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1beta1.RollingUpdateDeployment import RollingUpdateDeployment
from kubernetes.utils import is_valid_string


class DeploymentStrategy(object):
    """
    http://kubernetes.io/docs/api-reference/extensions/v1beta1/definitions/#_v1beta1_deploymentstrategy
    """

    def __init__(self, model=None):
        super(DeploymentStrategy, self).__init__()

        self._type = None
        self._rolling_update = RollingUpdateDeployment()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'type' in model:
            self.type = model['type']
        if 'rollingUpdate' in model:
            self.rolling_update = RollingUpdateDeployment(model['rollingUpdate'])

    # ------------------------------------------------------------------------------------- type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, t=None):
        if not is_valid_string(t):
            raise SyntaxError('DeploymentStrategy: type: [ {} ] is invalid.'.format(t))
        self._type = t

    # ------------------------------------------------------------------------------------- rollingUpdate

    @property
    def rolling_update(self):
        return self._rolling_update

    @rolling_update.setter
    def rolling_update(self, ru=None):
        if not isinstance(ru, RollingUpdateDeployment):
            raise SyntaxError('DeploymentStrategy: rolling_update: [ {} ] is invalid.'.format(ru))
        self._rolling_update = ru

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.type is not None:
            data['type'] = self.type
        if self.rolling_update is not None:
            data['rollingUpdate'] = self.rolling_update.serialize()
        return data
