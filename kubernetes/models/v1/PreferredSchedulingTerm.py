#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.NodeSelectorTerm import NodeSelectorTerm


class PreferredSchedulingTerm(object):
    """
    https://kubernetes.io/docs/api-reference/v1.6/#preferredschedulingterm-v1-core
    """

    def __init__(self, model=None):
        super(PreferredSchedulingTerm, self).__init__()

        self._weight = 1  # in the range 1 - 100
        self._preference = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'preference' in model:
            self.preference = NodeSelectorTerm(model['preference'])
        if 'weight' in model:
            self.weight = model['weight']

    # ------------------------------------------------------------------------------------- preference

    @property
    def preference(self):
        return self._preference

    @preference.setter
    def preference(self, p=None):
        if not isinstance(p, NodeSelectorTerm):
            raise SyntaxError('PreferredSchedulingTerm: preference: [ {} ] is invalid.'.format(p))
        self._preference = p

    # ------------------------------------------------------------------------------------- weight

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, w=None):
        if not isinstance(w, int):
            raise SyntaxError('PreferredSchedulingTerm: weight: [ {} ] is invalid.'.format(w))
        if not 1 <= w <= 100:
            raise SyntaxError('PreferredSchedulingTerm: weight: [ {} ] must be between 1 and 100.'.format(w))
        self._weight = w

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.preference is not None:
            data['preference'] = self.preference.serialize()
        if self.weight is not None:
            data['weight'] = self.weight
        return data
