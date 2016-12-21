#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.PodTemplateSpec import PodTemplateSpec
from kubernetes.models.v1beta1.DeploymentStrategy import DeploymentStrategy
from kubernetes.models.v1beta1.LabelSelector import LabelSelector
from kubernetes.models.v1beta1.RollbackConfig import RollbackConfig


class DeploymentSpec(object):
    """
    http://kubernetes.io/docs/api-reference/extensions/v1beta1/definitions/#_v1beta1_deploymentspec
    """

    def __init__(self, model=None):
        super(DeploymentSpec, self).__init__()

        self._replicas = 1
        self._selector = LabelSelector()
        self._template = PodTemplateSpec()
        self._strategy = DeploymentStrategy()
        self._min_ready_seconds = 0
        self._revision_history_limit = None
        self._paused = False
        self._rollback_to = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'replicas' in model:
            self.replicas = model['replicas']
        if 'selector' in model:
            self.selector = LabelSelector(model['selector'])
        if 'template' in model:
            self.template = PodTemplateSpec(model['template'])
        if 'strategy' in model:
            self.strategy = DeploymentStrategy(model['strategy'])
        if 'minReadySeconds' in model:
            self.min_ready_seconds = model['minReadySeconds']
        if 'revisionHistoryLimit' in model:
            self.revision_history_limit = model['revisionHistoryLimit']
        if 'paused' in model:
            self.paused = model['paused']
        if 'rollbackTo' in model:
            self.rollback_to = model['rollbackTo']

    # ------------------------------------------------------------------------------------- replicas

    @property
    def replicas(self):
        return self._replicas

    @replicas.setter
    def replicas(self, reps=None):
        if not isinstance(reps, int):
            raise SyntaxError('DeploymentSpec: replicas: [ {} ] is invalid'.format(reps))
        self._replicas = reps

    # ------------------------------------------------------------------------------------- selector

    @property
    def selector(self):
        return self._selector

    @selector.setter
    def selector(self, sel=None):
        if not isinstance(sel, LabelSelector):
            raise SyntaxError('DeploymentSpec: selector: [ {} ] is invalid'.format(sel))
        self._selector = sel

    # ------------------------------------------------------------------------------------- template

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, t=None):
        if not isinstance(t, PodTemplateSpec):
            raise SyntaxError('DeploymentSpec: template: [ {} ] is invalid'.format(t))
        self._template = t

    # ------------------------------------------------------------------------------------- strategy

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strat=None):
        if not isinstance(strat, DeploymentStrategy):
            raise SyntaxError('DeploymentSpec: strategy: [ {} ] is invalid'.format(strat))
        self._strategy = strat

    # ------------------------------------------------------------------------------------- minReadySeconds

    @property
    def min_ready_seconds(self):
        return self._min_ready_seconds

    @min_ready_seconds.setter
    def min_ready_seconds(self, mrs=None):
        if not isinstance(mrs, int):
            raise SyntaxError('DeploymentSpec: min_ready_seconds: [ {} ] is invalid'.format(mrs))
        self._min_ready_seconds = mrs

    # ------------------------------------------------------------------------------------- revisionHistoryLimit

    @property
    def revision_history_limit(self):
        return self._revision_history_limit

    @revision_history_limit.setter
    def revision_history_limit(self, rhl=None):
        if not isinstance(rhl, int):
            raise SyntaxError('DeploymentSpec: revision_history_limit: [ {} ] is invalid'.format(rhl))
        self._revision_history_limit = rhl

    # ------------------------------------------------------------------------------------- paused

    @property
    def paused(self):
        return self._paused

    @paused.setter
    def paused(self, p=None):
        if not isinstance(p, bool):
            raise SyntaxError('DeploymentSpec: paused: [ {} ] is invalid'.format(p))
        self._paused = p

    # ------------------------------------------------------------------------------------- rollbackTo

    @property
    def rollback_to(self):
        return self._rollback_to

    @rollback_to.setter
    def rollback_to(self, rc=None):
        if not isinstance(rc, RollbackConfig):
            raise SyntaxError('DeploymentSpec: rollback_to: [ {} ] is invalid'.format(rc))
        self._rollback_to = rc

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.replicas is not None:
            data['replicas'] = self.replicas
        if self.selector is not None:
            data['selector'] = self.selector.serialize()
        if self.template is not None:
            data['template'] = self.template.serialize()
        if self.strategy is not None:
            data['strategy'] = self.strategy.serialize()
        if self.min_ready_seconds is not None:
            data['minRedySeconds'] = self.min_ready_seconds
        if self.revision_history_limit is not None:
            data['revisionHistoryLimit'] = self.revision_history_limit
        if self.paused is not None:
            data['paused'] = self.paused
        if self.rollback_to is not None:
            data['rollbackTo'] = self.rollback_to.serialize()
        return data
