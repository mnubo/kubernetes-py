#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.PodTemplateSpec import PodTemplateSpec
from kubernetes.utils import is_valid_dict


class ReplicationControllerSpec(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_replicationcontrollerspec
    """

    def __init__(self, model=None):
        super(ReplicationControllerSpec, self).__init__()

        self._replicas = 0
        self._selector = {}
        self._template = PodTemplateSpec()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'replicas' in model:
            self.replicas = model['replicas']
        if 'selector' in model:
            self.selector = model['selector']
        if 'template' in model:
            self.template = PodTemplateSpec(model['template'])

    # ------------------------------------------------------------------------------------- template

    @property
    def replicas(self):
        return self._replicas

    @replicas.setter
    def replicas(self, replicas=None):
        if not isinstance(replicas, int) or not replicas >= 0:
            raise SyntaxError('ReplicationControllerSpec: replicas: [ {0} ] is invalid.'.format(replicas))
        self._replicas = replicas

    # ------------------------------------------------------------------------------------- selector

    @property
    def selector(self):
        return self._selector

    @selector.setter
    def selector(self, selector=None):
        if not is_valid_dict(selector):
            raise SyntaxError('ReplicationControllerSpec: selector: [ {0} ] is invalid.'.format(selector))
        self._selector = selector

    # ------------------------------------------------------------------------------------- template

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, template=None):
        if not isinstance(template, PodTemplateSpec):
            raise SyntaxError('ReplicationControllerSpec: template: [ {} ] is invalid.'.format(template))
        self._template = template

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.replicas is not None:
            data['replicas'] = self.replicas
        if self.selector is not None:
            data['selector'] = self.selector
        if self.template is not None:
            data['template'] = self.template.serialize()
        return data
