#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.unversioned.LabelSelector import LabelSelector
from kubernetes.models.v1.PodTemplateSpec import PodTemplateSpec


class JobSpec(object):
    """
    http://kubernetes.io/docs/api-reference/batch/v1/definitions/#_v1_jobspec
    """

    def __init__(self, model=None):
        super(JobSpec, self).__init__()

        self._parallelism = None
        self._completions = None
        self._active_deadline_seconds = None
        self._selector = None
        self._manual_selector = None
        self._template = PodTemplateSpec()

        self.template.spec.VALID_RESTART_POLICIES = ['OnFailure', 'Never']

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'parallelism' in model:
            self.parallelism = model['parallelism']
        if 'completions' in model:
            self.completions = model['completions']
        if 'activeDeadlineSeconds' in model:
            self.active_deadline_seconds = model['activeDeadlineSeconds']
        if 'selector' in model:
            self.selector = LabelSelector(model=model['selector'])
        if 'manualSelector' in model:
            self.manual_selector = model['manualSelector']
        if 'template' in model:
            self.template = PodTemplateSpec(model=model['template'])

    # --------------------------------------------------------------------------------- parallelism

    @property
    def parallelism(self):
        return self._parallelism

    @parallelism.setter
    def parallelism(self, p=None):
        if not isinstance(p, int):
            raise SyntaxError('JobSpec: parallelism: [ {} ] is invalid.'.format(p))
        self._parallelism = p

    # --------------------------------------------------------------------------------- completions

    @property
    def completions(self):
        return self._completions

    @completions.setter
    def completions(self, c=None):
        if not isinstance(c, int):
            raise SyntaxError('JobSpec: completions: [ {} ] is invalid.'.format(c))
        self._completions = c

    # --------------------------------------------------------------------------------- activeDeadlineSeconds

    @property
    def active_deadline_seconds(self):
        return self._active_deadline_seconds

    @active_deadline_seconds.setter
    def active_deadline_seconds(self, ads=None):
        if not isinstance(ads, int):
            raise SyntaxError('JobSpec: active_deadline_seconds: [ {} ] is invalid.'.format(ads))
        self._active_deadline_seconds = ads

    # --------------------------------------------------------------------------------- selector

    @property
    def selector(self):
        return self._selector

    @selector.setter
    def selector(self, s=None):
        if not isinstance(s, LabelSelector):
            raise SyntaxError('JobSpec: selector: [ {} ] is invalid.'.format(s))
        self._selector = s

    # --------------------------------------------------------------------------------- manualSelector

    @property
    def manual_selector(self):
        return self._manual_selector

    @manual_selector.setter
    def manual_selector(self, s=None):
        # Leave manualSelector unset unless you are certain what you are doing.
        if not isinstance(s, bool):
            raise SyntaxError('JobSpec: manual_selector: [ {} ] is invalid.'.format(s))
        self._manual_selector = s

    # --------------------------------------------------------------------------------- template

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, t=None):
        if not isinstance(t, PodTemplateSpec):
            raise SyntaxError('JobSpec: template: [ {} ] is invalid.'.format(t))
        self._template = t

    # --------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.parallelism is not None:
            data['parallelism'] = self.parallelism
        if self.completions is not None:
            data['completions'] = self.completions
        if self.active_deadline_seconds is not None:
            data['activeDeadlineSeconds'] = self.active_deadline_seconds
        if self.selector is not None:
            data['selector'] = self.selector
        if self.manual_selector is not None:
            data['manualSelector'] = self.manual_selector
        if self.template is not None:
            data['template'] = self.template.serialize()
        return data
