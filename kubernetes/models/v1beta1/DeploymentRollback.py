#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1beta1.RollbackConfig import RollbackConfig
from kubernetes.utils import is_valid_string, is_valid_dict


class DeploymentRollback(object):
    """
    http://kubernetes.io/docs/api-reference/extensions/v1beta1/definitions/#_v1beta1_deploymentrollback
    """

    def __init__(self, model=None):
        super(DeploymentRollback, self).__init__()

        self._kind = 'DeploymentRollback'
        self._api_version = 'extensions/v1beta1'

        self._name = None
        self._updated_annotations = {}
        self._rollback_to = RollbackConfig()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'kind' in model:
            self.kind = model['kind']
        if 'apiVersion' in model:
            self.api_version = model['apiVersion']
        if 'name' in model:
            self.name = model['name']
        if 'updatedAnnotations' in model:
            self.updated_annotations = model['updatedAnnotations']
        if 'rollbackTo' in model:
            self.rollback_to = model['rollbackTo']

    # ------------------------------------------------------------------------------------- kind

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, kind=None):
        if not is_valid_string(kind):
            raise SyntaxError('DeploymentRollback: kind: [ {} ] is invalid.'.format(kind))
        self._kind = kind

    # ------------------------------------------------------------------------------------- apiVersion

    @property
    def api_version(self):
        return self._api_version

    @api_version.setter
    def api_version(self, v=None):
        if not is_valid_string(v):
            raise SyntaxError('DeploymentRollback: api_version: [ {} ] is invalid.'.format(v))
        self._api_version = v

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('DeploymentRollback: name: [ {} ] is invalid.'.format(name))
        self._name = name

    # ------------------------------------------------------------------------------------- updatedAnnotations

    @property
    def updated_annotations(self):
        return self._updated_annotations

    @updated_annotations.setter
    def updated_annotations(self, anns=None):
        if not is_valid_dict(anns):
            raise SyntaxError('DeploymentRollback: updated_annotations: [ {} ] is invalid.'.format(anns))
        self._updated_annotations = anns

    # ------------------------------------------------------------------------------------- rollbackTo

    @property
    def rollback_to(self):
        return self._rollback_to

    @rollback_to.setter
    def rollback_to(self, rt=None):
        if not isinstance(rt, RollbackConfig):
            raise SyntaxError('DeploymentRollback: rollback_to: [ {} ] is invalid.'.format(rt))
        self._rollback_to = rt

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.kind is not None:
            data['kind'] = self.kind
        if self.api_version is not None:
            data['apiVersion'] = self.api_version
        if self.name is not None:
            data['name'] = self.name
        if self.updated_annotations is not None:
            data['updatedAnnotations'] = self.updated_annotations
        if self.rollback_to is not None:
            data['rollbackTo'] = self.rollback_to.serialize()
        return data
