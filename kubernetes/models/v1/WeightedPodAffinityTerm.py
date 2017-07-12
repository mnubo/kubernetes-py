#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.PodAffinityTerm import PodAffinityTerm


class WeightedPodAffinityTerm(object):
    """
    https://kubernetes.io/docs/api-reference/v1.6/#weightedpodaffinityterm-v1-core
    """

    def __init__(self, model=None):
        super(WeightedPodAffinityTerm, self).__init__()

        self._pod_affinity_term = None
        self._weight = 1  # in the range 1-100

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'podAffinityTerm' in model:
            self.pod_affinity_term = PodAffinityTerm(model['podAffinityTerm'])
        if 'weight' in model:
            self.weight = model['weight']

    # ------------------------------------------------------------------------------------- podAffinityTerm

    @property
    def pod_affinity_term(self):
        return self._pod_affinity_term

    @pod_affinity_term.setter
    def pod_affinity_term(self, t=None):
        if not isinstance(t, PodAffinityTerm):
            raise SyntaxError('WeightedPodAffinityTerm: pod_affinity_term: [ {} ] is invalid.'.format(t))
        self._pod_affinity_term = t

    # ------------------------------------------------------------------------------------- weight

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, w=None):
        if not isinstance(w, int):
            raise SyntaxError('WeightedPodAffinityTerm: weight: [ {} ] is invalid.'.format(w))
        if not 1 <= w <= 100:
            raise SyntaxError('WeightedPodAffinityTerm: weight: [ {} ] must be between 1 and 100.'.format(w))
        self._weight = w

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.pod_affinity_term:
            data['podAffinityTerm'] = self.pod_affinity_term.serialize()
        if self.weight:
            data['weight'] = self.weight
        return data
