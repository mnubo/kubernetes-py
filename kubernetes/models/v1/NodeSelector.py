#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.NodeSelectorTerm import NodeSelectorTerm
from kubernetes.utils import is_valid_list


class NodeSelector(object):
    """
    https://kubernetes.io/docs/api-reference/v1.6/#nodeselector-v1-core
    """

    def __init__(self, model=None):
        super(NodeSelector, self).__init__()

        self._node_selector_terms = []

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'nodeSelectorTerms' in model:
            terms = []
            for t in model['nodeSelectorTerms']:
                term = NodeSelectorTerm(t)
                terms.append(term)
            self.node_selector_terms = terms

    # ------------------------------------------------------------------------------------- nodeSelectorTerms

    @property
    def node_selector_terms(self):
        return self._node_selector_terms

    @node_selector_terms.setter
    def node_selector_terms(self, t=None):
        if not is_valid_list(t, NodeSelectorTerm):
            raise SyntaxError('NodeSelector: node_selector_terms: [ {} ] is invalid.'.format(t))
        self._node_selector_terms = t

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.node_selector_terms:
            terms = []
            for t in self.node_selector_terms:
                term = t.serialize()
                terms.append(term)
            data['nodeSelectorTerms'] = terms
        return data
