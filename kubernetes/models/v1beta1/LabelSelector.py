#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1beta1.LabelSelectorRequirement import LabelSelectorRequirement
from kubernetes.utils import is_valid_dict, is_valid_list


class LabelSelector(object):
    """
    http://kubernetes.io/docs/api-reference/extensions/v1beta1/definitions/#_v1beta1_labelselector
    """

    def __init__(self, model=None):
        super(LabelSelector, self).__init__()

        self._match_labels = None
        self._match_expressions = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'matchLabels' in model:
            self.match_labels = model['matchLabels']
        if 'matchExpressions' in model:
            exps = []
            for me in model['matchExpressions']:
                exp = LabelSelectorRequirement(me)
                exps.append(exp)
            self.match_expressions = exps

    # ------------------------------------------------------------------------------------- matchLabels

    @property
    def match_labels(self):
        return self._match_labels

    @match_labels.setter
    def match_labels(self, ml=None):
        if not is_valid_dict(ml):
            raise SyntaxError(
                'LabelSelector: match_labels: [ {} ] is invalid.'.format(ml))

        self._match_labels = ml

    # ------------------------------------------------------------------------------------- matchExpressions

    @property
    def match_expressions(self):
        return self._match_expressions

    @match_expressions.setter
    def match_expressions(self, me=None):
        if not is_valid_list(me, LabelSelectorRequirement):
            raise SyntaxError(
                'LabelSelector: match_expressions: [ {} ] is invalid.'.format(me))

        self._match_expressions = me

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.match_labels is not None:
            data['matchLabels'] = self.match_labels
        if self.match_expressions is not None:
            data['matchExpressions'] = [x.serialize() for x in self.match_expressions]

        return data
