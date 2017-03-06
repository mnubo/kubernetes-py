#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


class StatefulSetStatus(object):

    def __init__(self, model=None):
        super(StatefulSetStatus, self).__init__()

        self._observed_generation = None
        self._replicas = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'observedGeneration' in model:
            self.observed_generation = model['observedGeneration']
        if 'replicas' in model:
            self.replicas = model['replicas']

    # ------------------------------------------------------------------------------------- observedGeneration

    @property
    def observed_generation(self):
        return self._observed_generation

    @observed_generation.setter
    def observed_generation(self, og=None):
        if not isinstance(og, int):
            raise SyntaxError("StatefulSetStatus: observed_generation: [ {} ] is invalid.".format(og))
        self._observed_generation = og

    # ------------------------------------------------------------------------------------- replicas

    @property
    def replicas(self):
        return self._replicas

    @replicas.setter
    def replicas(self, r=None):
        if not isinstance(r, int):
            raise SyntaxError('StatefulSetStatus: replicas: [ {} ] is invalid.'.format(r))
        self._replicas = r

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.observed_generation is not None:
            data['observedGeneration'] = self.observed_generation
        if self.replicas is not None:
            data['replicas'] = self.replicas
        return data
