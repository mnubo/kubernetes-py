#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


class ReplicaSetStatus(object):
    """
    http://kubernetes.io/docs/api-reference/extensions/v1beta1/definitions/#_v1beta1_replicasetstatus
    """

    def __init__(self, model=None):
        super(ReplicaSetStatus, self).__init__()

        self._replicas = 0
        self._fully_labeled_replicas = None
        self._ready_replicas = None
        self._observed_generation = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'replicas' in model:
            self.replicas = model['replicas']
        if 'fullyLabeledReplicas' in model:
            self.fully_labeled_replicas = model['fullyLabeledReplicas']
        if 'readyReplicas' in model:
            self.ready_replicas = model['readyReplicas']
        if 'observedGeneration' in model:
            self.observed_generation = model['observedGeneration']

    # ------------------------------------------------------------------------------------- replicas

    @property
    def replicas(self):
        return self._replicas

    @replicas.setter
    def replicas(self, reps=None):
        if not isinstance(reps, int):
            raise SyntaxError('ReplicaSetStatus: replicas: [ {} ] is invalid.'.format(reps))
        self._replicas = reps

    # ------------------------------------------------------------------------------------- fullyLabeledReplicas

    @property
    def fully_labeled_replicas(self):
        return self._fully_labeled_replicas

    @fully_labeled_replicas.setter
    def fully_labeled_replicas(self, reps=None):
        if not isinstance(reps, int):
            raise SyntaxError('ReplicaSetStatus: fully_labeled_replicas: [ {} ] is invalid.'.format(reps))
        self._fully_labeled_replicas = reps

    # ------------------------------------------------------------------------------------- readyReplicas

    @property
    def ready_replicas(self):
        return self._ready_replicas

    @ready_replicas.setter
    def ready_replicas(self, reps=None):
        if not isinstance(reps, int):
            raise SyntaxError('ReplicaSetStatus: ready_replicas: [ {} ] is invalid.'.format(reps))
        self._ready_replicas = reps

    # ------------------------------------------------------------------------------------- observedGeneration

    @property
    def observed_generation(self):
        return self._observed_generation

    @observed_generation.setter
    def observed_generation(self, og=None):
        if not isinstance(og, int):
            raise SyntaxError('ReplicaSetStatus: observed_generation: [ {} ] is invalid.'.format(og))
        self._observed_generation = og

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.replicas is not None:
            data['replicas'] = self.replicas
        if self.fully_labeled_replicas is not None:
            data['fullyLabeledReplicas'] = self.fully_labeled_replicas
        if self.ready_replicas is not None:
            data['readyReplicas'] = self.ready_replicas
        if self.observed_generation is not None:
            data['observedGeneration'] = self.observed_generation
        return data
