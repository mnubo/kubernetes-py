#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.WeightedPodAffinityTerm import WeightedPodAffinityTerm
from kubernetes.models.v1.PodAffinityTerm import PodAffinityTerm
from kubernetes.utils import is_valid_list


class PodAntiAffinity(object):
    """
    https://kubernetes.io/docs/api-reference/v1.6/#podantiaffinity-v1-core
    https://github.com/kubernetes/community/blob/master/contributors/design-proposals/podaffinity.md
    """

    def __init__(self, model=None):
        super(PodAntiAffinity, self).__init__()

        self._preferred_during_scheduling_ignored_during_execution = []
        self._required_during_scheduling_ignored_during_execution = []

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'preferredDuringSchedulingIgnoredDuringExecution' in model:
            wpats = []
            for x in model['preferredDuringSchedulingIgnoredDuringExecution']:
                wpat = WeightedPodAffinityTerm(x)
                wpats.append(wpat)
            self.preferred_during_scheduling_ignored_during_execution = wpats
        if 'requiredDuringSchedulingIgnoredDuringExecution' in model:
            pats = []
            for x in model['requiredDuringSchedulingIgnoredDuringExecution']:
                pat = PodAffinityTerm(x)
                pats.append(pat)
            self.required_during_scheduling_ignored_during_execution = pats

    # ----------------------------------------------------------------- preferredDuringSchedulingIgnoredDuringExecution

    @property
    def preferred_during_scheduling_ignored_during_execution(self):
        return self._preferred_during_scheduling_ignored_during_execution

    @preferred_during_scheduling_ignored_during_execution.setter
    def preferred_during_scheduling_ignored_during_execution(self, wpats=None):
        if not is_valid_list(wpats, WeightedPodAffinityTerm):
            raise SyntaxError(
                'PodAffinity: preferred_during_scheduling_ignored_during_execution: [ {} ] is invald.'.format(wpats))
        self._preferred_during_scheduling_ignored_during_execution = wpats

    # ----------------------------------------------------------------- requiredDuringSchedulingIgnoredDuringExecution

    @property
    def required_during_scheduling_ignored_during_execution(self):
        return self._required_during_scheduling_ignored_during_execution

    @required_during_scheduling_ignored_during_execution.setter
    def required_during_scheduling_ignored_during_execution(self, pats=None):
        if not is_valid_list(pats, PodAffinityTerm):
            raise SyntaxError(
                'PodAffinity: required_during_scheduling_ignored_during_execution: [ {} ] is invald.'.format(pats))
        self._required_during_scheduling_ignored_during_execution = pats

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.preferred_during_scheduling_ignored_during_execution:
            wpats = []
            for x in self.preferred_during_scheduling_ignored_during_execution:
                wpat = x.serialize()
                wpats.append(wpat)
            data['preferredDuringSchedulingIgnoredDuringExecution'] = wpats
        if self.required_during_scheduling_ignored_during_execution:
            pats = []
            for x in self.required_during_scheduling_ignored_during_execution:
                pat = x.serialize()
                pats.append(pat)
            data['requiredDuringSchedulingIgnoredDuringExecution'] = pats
        return data
