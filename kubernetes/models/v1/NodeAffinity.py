#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.PreferredSchedulingTerm import PreferredSchedulingTerm
from kubernetes.models.v1.NodeSelector import NodeSelector
from kubernetes.utils import is_valid_list


class NodeAffinity(object):
    """
    https://kubernetes.io/docs/api-reference/v1.6/#nodeaffinity-v1-core
    """

    def __init__(self, model=None):
        super(NodeAffinity, self).__init__()

        self._preferred_during_scheduling_ignored_during_execution = []
        self._required_during_scheduling_ignored_during_execution = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'preferredDuringSchedulingIgnoredDuringExecution' in model:
            terms = []
            for t in model['preferredDuringSchedulingIgnoredDuringExecution']:
                term = PreferredSchedulingTerm(t)
                terms.append(term)
            self.preferred_during_scheduling_ignored_during_execution = terms
        if 'requiredDuringSchedulingIgnoredDuringExecution' in model:
            sel = NodeSelector(model['requiredDuringSchedulingIgnoredDuringExecution'])
            self.required_during_scheduling_ignored_during_execution = sel

    # ----------------------------------------------------------------- preferredDuringSchedulingIgnoredDuringExecution

    @property
    def preferred_during_scheduling_ignored_during_execution(self):
        return self._preferred_during_scheduling_ignored_during_execution

    @preferred_during_scheduling_ignored_during_execution.setter
    def preferred_during_scheduling_ignored_during_execution(self, p=None):
        if not is_valid_list(p, PreferredSchedulingTerm):
            raise SyntaxError(
                'NodeAffinity: preferred_during_scheduling_ignored_during_execution: [ {} ] is invalid.'.format(p))
        self._preferred_during_scheduling_ignored_during_execution = p

    # ----------------------------------------------------------------- requiredDuringSchedulingIgnoredDuringExecution

    @property
    def required_during_scheduling_ignored_during_execution(self):
        return self._required_during_scheduling_ignored_during_execution

    @required_during_scheduling_ignored_during_execution.setter
    def required_during_scheduling_ignored_during_execution(self, r=None):
        if not isinstance(r, NodeSelector):
            raise SyntaxError(
                'NodeAffinity: required_during_scheduling_ignored_during_execution: [ {} ] is invalid.'.format(r))
        self._required_during_scheduling_ignored_during_execution = r

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.preferred_during_scheduling_ignored_during_execution:
            terms = []
            for t in self.preferred_during_scheduling_ignored_during_execution:
                term = t.serialize()
                terms.append(term)
            data['preferredDuringSchedulingIgnoredDuringExecution'] = terms
        if self.required_during_scheduling_ignored_during_execution is not None:
            sel = self.required_during_scheduling_ignored_during_execution.serialize()
            data['requiredDuringSchedulingIgnoredDuringExecution'] = sel
        return data
