#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1beta1.LabelSelector import LabelSelector
from kubernetes.models.v1.PodTemplateSpec import PodTemplateSpec
from kubernetes.models.v1.PersistentVolumeClaim import PersistentVolumeClaim
from kubernetes.utils import is_valid_list, is_valid_string


class PetSetSpec(object):
    """
    http://kubernetes.io/docs/api-reference/apps/v1alpha1/definitions/#_v1alpha1_petsetspec
    """

    def __init__(self, model=None):
        super(PetSetSpec, self).__init__()

        self._replicas = 1
        self._selector = LabelSelector()
        self._template = PodTemplateSpec()
        self._volume_claim_templates = []
        self._service_name = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'replicas' in model:
            self.replicas = model['replicas']
        if 'selector' in model:
            self.selector = LabelSelector(model['selector'])
        if 'template' in model:
            self.template = PodTemplateSpec(model['template'])
        if 'volumeClaimTemplates' in model:
            claims = []
            for x in model['volumeClaimTemplates']:
                claim = PersistentVolumeClaim(x)
                claims.append(claim)
            self.volume_claim_templates = claims
        if 'serviceName' in model:
            self.service_name = model['serviceName']

    # ------------------------------------------------------------------------------------- replicas

    @property
    def replicas(self):
        return self._replicas

    @replicas.setter
    def replicas(self, r=None):
        if not isinstance(r, int):
            raise SyntaxError('PetSetSpec: replicas: [ {} ] is invalid.'.format(r))
        self._replicas = r

    # ------------------------------------------------------------------------------------- selector

    @property
    def selector(self):
        return self._selector

    @selector.setter
    def selector(self, s=None):
        if not isinstance(s, LabelSelector):
            raise SyntaxError('PetSetSpec: selector: [ {} ] is invalid.'.format(s))
        self._selector = s

    # ------------------------------------------------------------------------------------- template

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, t=None):
        if not isinstance(t, PodTemplateSpec):
            raise SyntaxError('PetSetSpec: template: [ {} ] is invalid.'.format(t))
        self._template = t

    # ------------------------------------------------------------------------------------- volumeClaimTemplates

    @property
    def volume_claim_templates(self):
        return self._volume_claim_templates

    @volume_claim_templates.setter
    def volume_claim_templates(self, t=None):
        if not is_valid_list(t, PersistentVolumeClaim):
            raise SyntaxError('PetSetSpec: volume_claim_templates: [ {} ] is invalid.'.format(t))
        self._volume_claim_templates = t

    # ------------------------------------------------------------------------------------- serviceName

    @property
    def service_name(self):
        return self._service_name

    @service_name.setter
    def service_name(self, sn=None):
        if not is_valid_string(sn):
            raise SyntaxError('PetSetSpec: service_name: [ {} ] is invalid.'.format(sn))
        self._service_name = sn

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.replicas is not None:
            data['replicas'] = self.replicas
        if self.selector is not None:
            data['selector'] = self.selector.serialize()
        if self.template is not None:
            data['template'] = self.template.serialize()
        if self.volume_claim_templates is not None:
            data['volumeClaimTemplates'] = [x.serialize() for x in self.volume_claim_templates]
        if self.service_name is not None:
            data['serviceName'] = self.service_name
        return data
