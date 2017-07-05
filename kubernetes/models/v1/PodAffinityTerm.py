#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1beta1.LabelSelector import LabelSelector
from kubernetes.utils import is_valid_string, is_valid_list, convert


class PodAffinityTerm(object):

    def __init__(self, model=None):
        super(PodAffinityTerm, self).__init__()

        self._label_selector = None
        self._namespaces = []
        self._topology_key = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'labelSelector' in model:
            self.label_selector = LabelSelector(model['labelSelector'])
        if 'namespaces' in model:
            self.namespaces = model['namespaces']
        if 'topologyKey' in model:
            self.topology_key = model['topologyKey']

    # ------------------------------------------------------------------------------------- labelSelector

    @property
    def label_selector(self):
        return self._label_selector

    @label_selector.setter
    def label_selector(self, s=None):
        if not isinstance(s, LabelSelector):
            raise SyntaxError('PodAffinityTerm: label_selector: [ {} ] is invalid.'.format(s))
        self._label_selector = s

    # ------------------------------------------------------------------------------------- namespaces

    @property
    def namespaces(self):
        return self._namespaces

    @namespaces.setter
    def namespaces(self, n=None):
        if not is_valid_list(convert(n), str):
            raise SyntaxError('PodAffinityTerm: namespaces: [ {} ] is invalid.'.format(n))
        self._namespaces = n

    # ------------------------------------------------------------------------------------- topologyKey

    @property
    def topology_key(self):
        return self._topology_key

    @topology_key.setter
    def topology_key(self, t=None):
        if not is_valid_string(t):
            raise SyntaxError('PodAffinityTerm: topology_key: [ {} ] is invalid.'.format(t))
        self._topology_key = t

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.label_selector is not None:
            data['labelSelector'] = self.label_selector.serialize()
        if self.namespaces:
            data['namespaces'] = self.namespaces
        if self.topology_key is not None:
            data['topologyKey'] = self.topology_key
        return data
