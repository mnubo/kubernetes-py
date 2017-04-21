#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1beta1.SubresourceReference import SubresourceReference


class HorizontalPodAutoscalerSpec(object):
    """
    https://kubernetes.io/docs/api-reference/extensions/v1beta1/definitions/#_v1beta1_horizontalpodautoscalerspec
    """

    def __init__(self, model=None):
        super(HorizontalPodAutoscalerSpec, self).__init__()

        self._scale_target_ref = SubresourceReference()
        self._min_replicas = 1
        self._max_replicas = 1  # cannot be smaller than min_replicas
        self._cpu_utilization = 70

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'scaleTargetRef' in model:
            self.scale_target_ref = SubresourceReference(model['scaleTargetRef'])
        if 'minReplicas' in model:
            self.min_replicas = model['minReplicas']
        if 'maxReplicas' in model:
            self.max_replicas = model['maxReplicas']
        if 'targetCPUUtilizationPercentage' in model:
            self.cpu_utilization = model['targetCPUUtilizationPercentage']

    # ------------------------------------------------------------------------------------- scaleRef

    @property
    def scale_target_ref(self):
        return self._scale_target_ref

    @scale_target_ref.setter
    def scale_target_ref(self, ref=None):
        if not isinstance(ref, SubresourceReference):
            raise SyntaxError('HorizontalPodAutoscaler: scale_target_ref: [ {} ] is invalid.'.format(ref))
        self._scale_target_ref = ref

    # ------------------------------------------------------------------------------------- minReplicas
        
    @property
    def min_replicas(self):
        return self._min_replicas

    @min_replicas.setter
    def min_replicas(self, r=None):
        if not isinstance(r, int):
            raise SyntaxError('HorizontalPodAutoscaler: min_replicas: [ {} ] is invalid.'.format(r))
        self._min_replicas = r

    # ------------------------------------------------------------------------------------- maxReplicas

    @property
    def max_replicas(self):
        return self._max_replicas

    @max_replicas.setter
    def max_replicas(self, r=None):
        if not isinstance(r, int):
            raise SyntaxError('HorizontalPodAutoscaler: max_replicas: [ {} ] is invalid.'.format(r))
        self._max_replicas = r

    # ------------------------------------------------------------------------------------- cpuUtilization

    @property
    def cpu_utilization(self):
        return self._cpu_utilization

    @cpu_utilization.setter
    def cpu_utilization(self, u=None):
        if not isinstance(u, int):
            raise SyntaxError('HorizontalPodAutoscaler: cpu_utilization: [ {} ] is invalid.'.format(u))
        self._cpu_utilization = u

    # ------------------------------------------------------------------------------------- serialize()

    def serialize(self):
        data = {}
        if self.scale_target_ref is not None:
            data['scaleTargetRef'] = self.scale_target_ref.serialize()
        if self.min_replicas is not None:
            data['minReplicas'] = self.min_replicas
        if self.max_replicas is not None:
            data['maxReplicas'] = self.max_replicas
        if self.cpu_utilization is not None:
            data['targetCPUUtilizationPercentage'] = self.cpu_utilization
        return data
