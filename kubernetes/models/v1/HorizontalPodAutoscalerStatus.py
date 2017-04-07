#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_date_time


class HorizontalPodAutoscalerStatus(object):
    """
    https://kubernetes.io/docs/api-reference/extensions/v1beta1/definitions/#_v1beta1_horizontalpodautoscalerstatus
    """

    def __init__(self, model=None):
        super(HorizontalPodAutoscalerStatus, self).__init__()

        self._observed_generation = None
        self._last_scale_time = None
        self._current_replicas = None
        self._desired_replicas = None
        self._current_cpu_utilization_percentage = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'observedGeneration' in model:
            self.observed_generation = model['observedGeneration']
        if 'lastScaleTime' in model:
            self.last_scale_time = model['lastScaleTime']
        if 'currentReplicas' in model:
            self.current_replicas = model['currentReplicas']
        if 'desiredReplicas' in model:
            self.desired_replicas = model['desiredReplicas']
        if 'currentCpuUtilizationPercentage' in model:
            self.current_cpu_utilization_percentage = model['currentCpuUtilizationPercentage']

    # ------------------------------------------------------------------------------------- observedGeneration

    @property
    def observed_generation(self):
        return self._observed_generation

    @observed_generation.setter
    def observed_generation(self, og=None):
        if not isinstance(og, int):
            raise SyntaxError('HorizontalPodAutoscalerStatus: observed_generation: [ {} ] is invalid.'.format(og))
        self._observed_generation = og

    # ------------------------------------------------------------------------------------- lastScaleTime

    @property
    def last_scale_time(self):
        return self._last_scale_time

    @last_scale_time.setter
    def last_scale_time(self, t=None):
        if not is_valid_date_time(t):
            raise SyntaxError('HorizontalPodAutoscaler: last_scale_time: [ {} ] is invalid.'.format(t))
        self._last_scale_time = t

    # ------------------------------------------------------------------------------------- currentReplicas

    @property
    def current_replicas(self):
        return self._current_replicas

    @current_replicas.setter
    def current_replicas(self, r=None):
        if not isinstance(r, int):
            raise SyntaxError('HorizontalPodAutoscaler: current_replicas: [ {} ] is invalid.'.format(r))
        self._current_replicas = r

    # ------------------------------------------------------------------------------------- desiredReplicas

    @property
    def desired_replicas(self):
        return self._desired_replicas

    @desired_replicas.setter
    def desired_replicas(self, r=None):
        if not isinstance(r, int):
            raise SyntaxError('HorizontalPodAutoscaler: desired_replicas: [ {} ] is invalid.'.format(r))
        self._desired_replicas = r

    # ------------------------------------------------------------------------------------- currentCPU

    @property
    def current_cpu_utilization_percentage(self):
        return self._current_cpu_utilization_percentage

    @current_cpu_utilization_percentage.setter
    def current_cpu_utilization_percentage(self, pct=None):
        if not isinstance(pct, int):
            raise SyntaxError('HorizontalPodAutoscaler: current_cpu_utilization_percentage: [ {} ] is invalid.'.format(pct))
        self._current_cpu_utilization_percentage = pct
            
    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.observed_generation is not None:
            data['observedGeneration'] = self.observed_generation
        if self.last_scale_time is not None:
            data['lastScaleTime'] = self.last_scale_time
        if self.current_replicas is not None:
            data['currentReplicas'] = self.current_replicas
        if self.desired_replicas is not None:
            data['desiredReplicas'] = self.desired_replicas
        if self.current_cpu_utilization_percentage is not None:
            data['currentCpuUtilizationPercentage'] = self.current_cpu_utilization_percentage
        return data
