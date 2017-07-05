#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.NodeAffinity import NodeAffinity
from kubernetes.models.v1.PodAffinity import PodAffinity
from kubernetes.models.v1.PodAntiAffinity import PodAntiAffinity


class Affinity(object):
    """
    https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity
    """

    def __init__(self, model=None):
        super(Affinity, self).__init__()

        self._node_affinity = None
        self._pod_affinity = None
        self._pod_anti_affinity = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'nodeAffinity' in model:
            self.node_affinity = NodeAffinity(model['nodeAffinity'])
        if 'podAffinity' in model:
            self.pod_affinity = PodAffinity(model['podAffinity'])
        if 'podAntiAffinity' in model:
            self.pod_anti_affinity = PodAntiAffinity(model['podAntiAffinity'])

    # ------------------------------------------------------------------------------------- nodeAffinity

    @property
    def node_affinity(self):
        return self._node_affinity

    @node_affinity.setter
    def node_affinity(self, na=None):
        if not isinstance(na, NodeAffinity):
            raise SyntaxError('Affinity: node_affinity: [ {} ] is invalid.'.format(na))
        self._node_affinity = na

    # ------------------------------------------------------------------------------------- podAffinity

    @property
    def pod_affinity(self):
        return self._pod_affinity

    @pod_affinity.setter
    def pod_affinity(self, pa=None):
        if not isinstance(pa, PodAffinity):
            raise SyntaxError('Affinity: pod_affinity: [ {} ] is invalid.'.format(pa))
        self._pod_affinity = pa

    # ------------------------------------------------------------------------------------- podAntiAffinity

    @property
    def pod_anti_affinity(self):
        return self._pod_anti_affinity

    @pod_anti_affinity.setter
    def pod_anti_affinity(self, paa=None):
        if not isinstance(paa, PodAntiAffinity):
            raise SyntaxError('Affinity: pod_anti_affinity: [ {} ] is invalid.'.format(paa))
        self._pod_anti_affinity = paa

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.node_affinity is not None:
            data['nodeAffinity'] = self.node_affinity.serialize()
        if self.pod_affinity is not None:
            data['podAffinity'] = self.pod_affinity.serialize()
        if self.pod_anti_affinity is not None:
            data['podAntiAffinity'] = self.pod_anti_affinity.serialize()
        return data
