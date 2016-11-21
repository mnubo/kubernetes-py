#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


class DeploymentStatus(object):
    """
    http://kubernetes.io/docs/api-reference/extensions/v1beta1/definitions/#_v1beta1_deploymentstatus
    """

    def __init__(self, model=None):
        super(DeploymentStatus, self).__init__()

        self._observed_generation = None
        self._replicas = None
        self._updated_replicas = None
        self._available_replicas = None
        self._unavailable_replicas = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'observedGeneration' in model:
            self.observed_generation = model['observedGeneration']
        if 'replicas' in model:
            self.replicas = model['replicas']
        if 'updatedReplicas' in model:
            self.updated_replicas = model['updatedReplicas']
        if 'availableReplicas' in model:
            self.available_replicas = model['availableReplicas']
        if 'unavailableReplicas' in model:
            self.unavailable_replicas = model['unavailableReplicas']

    # ------------------------------------------------------------------------------------- observedGeneration

    @property
    def observed_generation(self):
        return self._observed_generation

    @observed_generation.setter
    def observed_generation(self, og=None):
        if not isinstance(og, int):
            raise SyntaxError('DeploymentStatus: observed_generation: [ {} ] is invalid.'.format(og))
        self._observed_generation = og

    # ------------------------------------------------------------------------------------- replicas

    @property
    def replicas(self):
        return self._replicas

    @replicas.setter
    def replicas(self, reps=None):
        if not isinstance(reps, int):
            raise SyntaxError('DeploymentStatus: replicas: [ {} ] is invalid.'.format(reps))
        self._replicas = reps

    # ------------------------------------------------------------------------------------- updatedReplicas

    @property
    def updated_replicas(self):
        return self._updated_replicas

    @updated_replicas.setter
    def updated_replicas(self, reps=None):
        if not isinstance(reps, int):
            raise SyntaxError('DeploymentStatus: updated_replicas: [ {} ] is invalid.'.format(reps))
        self._updated_replicas = reps

    # ------------------------------------------------------------------------------------- availableReplicas

    @property
    def available_replicas(self):
        return self._available_replicas

    @available_replicas.setter
    def available_replicas(self, reps=None):
        if not isinstance(reps, int):
            raise SyntaxError('DeploymentStatus: available_replicas: [ {} ] is invalid.'.format(reps))
        self._available_replicas = reps

    # ------------------------------------------------------------------------------------- unavailableReplicas

    @property
    def unavailable_replicas(self):
        return self._unavailable_replicas

    @unavailable_replicas.setter
    def unavailable_replicas(self, reps=None):
        if not isinstance(reps, int):
            raise SyntaxError('DeploymentStatus: unavailable_replicas: [ {} ] is invalid.'.format(reps))
        self._unavailable_replicas = reps

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.observed_generation is not None:
            data['observedGeneration'] = self.observed_generation
        if self.replicas is not None:
            data['replicas'] = self.replicas
        if self.updated_replicas is not None:
            data['updatedReplicas'] = self.updated_replicas
        if self.available_replicas is not None:
            data['availableReplicas'] = self.available_replicas
        if self.unavailable_replicas is not None:
            data['unavailableReplicas'] = self.unavailable_replicas
        return data
