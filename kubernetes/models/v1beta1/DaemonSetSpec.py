#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1beta1.LabelSelector import LabelSelector
from kubernetes.models.v1.PodTemplateSpec import PodTemplateSpec


class DaemonSetSpec(object):

    def __init__(self, model=None):
        super(DaemonSetSpec, self).__init__()

        self._selector = LabelSelector()
        self._template = PodTemplateSpec()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'selector' in model:
            self.selector = LabelSelector(model['selector'])
        if 'template' in model:
            self.template = PodTemplateSpec(model['template'])

    # ------------------------------------------------------------------------------------- selector

    @property
    def selector(self):
        return self._selector

    @selector.setter
    def selector(self, s=None):
        if not isinstance(s, LabelSelector):
            raise SyntaxError(
                'DaemonSetSpec: selector: [ {} ] is invalid.'.format(s))
        self._selector = s

    # ------------------------------------------------------------------------------------- template

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, t=None):
        if not isinstance(t, PodTemplateSpec):
            raise SyntaxError(
                'DaemonSetSpec: template: [ {} ] is invalid.'.format(t))
        self._template = t

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.selector is not None:
            data['selector'] = self.selector.serialize()
        if self.template is not None:
            data['template'] = self.template.serialize()
        return data
