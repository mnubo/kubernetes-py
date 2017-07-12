#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.NodeSelectorRequirement import NodeSelectorRequirement
from kubernetes.utils import is_valid_list


class NodeSelectorTerm(object):
    """
    https://kubernetes.io/docs/api-reference/v1.6/#nodeselectorterm-v1-core
    """

    def __init__(self, model=None):
        super(NodeSelectorTerm, self).__init__()

        self._match_expressions = []

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'matchExpressions' in model:
            exps = []
            for e in model['matchExpressions']:
                exp = NodeSelectorRequirement(e)
                exps.append(exp)
            self.match_expressions = exps

    # ------------------------------------------------------------------------------------- matchExpressions

    @property
    def match_expressions(self):
        return self._match_expressions

    @match_expressions.setter
    def match_expressions(self, e=None):
        if not is_valid_list(e, NodeSelectorRequirement):
            raise SyntaxError('NodeSelectorTerm: match_expressions: [ {} ] is invalid.'.format(e))
        self._match_expressions = e

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.match_expressions:
            reqs = []
            for r in self.match_expressions:
                req = r.serialize()
                reqs.append(req)
            data['matchExpressions'] = reqs
        return data
