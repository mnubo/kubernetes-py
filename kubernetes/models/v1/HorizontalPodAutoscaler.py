#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.HorizontalPodAutoscalerStatus import HorizontalPodAutoscalerStatus

from kubernetes.models.unversioned.BaseModel import BaseModel
from kubernetes.models.v1.HorizontalPodAutoscalerSpec import HorizontalPodAutoscalerSpec
from kubernetes.models.v1.ObjectMeta import ObjectMeta


class HorizontalPodAutoscaler(BaseModel):
    """
    https://kubernetes.io/docs/api-reference/extensions/v1beta1/definitions/#_v1beta1_horizontalpodautoscaler
    """

    def __init__(self, model=None):
        super(HorizontalPodAutoscaler, self).__init__()

        self.kind = 'HorizontalPodAutoscaler'
        self.api_version = 'autoscaling/v1'

        self.spec = HorizontalPodAutoscalerSpec()
        self.status = HorizontalPodAutoscalerStatus()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        super(HorizontalPodAutoscaler, self).build_with_model(model)

        if 'spec' in model:
            self.spec = HorizontalPodAutoscalerSpec(model['spec'])
        if 'status' in model:
            self.status = HorizontalPodAutoscalerStatus(model['status'])

    # ------------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, s=None):
        if not isinstance(s, HorizontalPodAutoscalerSpec):
            raise SyntaxError('HorizontalPodAutoscaler: spec: [ {} ] is invalid.'.format(s))
        self._spec = s

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, s=None):
        if not isinstance(s, HorizontalPodAutoscalerStatus):
            raise SyntaxError('HorizontalPodAutoscaler: status: [ {} ] is invalid.'.format(s))
        self._status = s

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(HorizontalPodAutoscaler, self).serialize()

        if self.spec is not None:
            data['spec'] = self.spec.serialize()
        if self.status is not None:
            data['status'] = self.status.serialize()
        return data
