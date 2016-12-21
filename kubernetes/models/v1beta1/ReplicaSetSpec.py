#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.PodTemplateSpec import PodTemplateSpec
from kubernetes.models.v1beta1.LabelSelector import LabelSelector


class ReplicaSetSpec(object):
    """
    http://kubernetes.io/docs/api-reference/extensions/v1beta1/definitions/#_v1beta1_replicasetspec
    """

    def __init__(self, model=None):
        super(ReplicaSetSpec, self).__init__()

        self._replicas = 0
        self._selector = LabelSelector()
        self._template = PodTemplateSpec()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'replicas' in model:
            self.replicas = model['replicas']
        if 'selector' in model:
            self.selector = LabelSelector(model['selector'])
        if 'template' in model:
            self.template = PodTemplateSpec(model['template'])

    # ------------------------------------------------------------------------------------- replicas

    @property
    def replicas(self):
        return self._replicas

    @replicas.setter
    def replicas(self, reps=None):
        if not isinstance(reps, int):
            raise SyntaxError('ReplicaSetSpec: replicas: [ {} ] is invalid.'.format(reps))
        self._replicas = reps

    # ------------------------------------------------------------------------------------- selector

    @property
    def selector(self):
        return self._selector

    @selector.setter
    def selector(self, sel=None):
        if not isinstance(sel, LabelSelector):
            raise SyntaxError('ReplicaSetSpec: selector: [ {} ] is invalid.'.format(sel))
        self._selector = sel

    # ------------------------------------------------------------------------------------- template

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, t=None):
        if not isinstance(t, PodTemplateSpec):
            raise SyntaxError('ReplicaSetSpec: template: [ {} ] is invalid.'.format(t))
        self._template = t

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.replicas is not None:
            data['replicas'] = self.replicas
        if self.selector is not None:
            data['selector'] = self.selector.serialize()
        if self.template is not None:
            data['template'] = self.template.serialize()
        return data
