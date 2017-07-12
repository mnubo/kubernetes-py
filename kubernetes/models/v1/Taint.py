#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string


class Taint(object):
    """
    https://kubernetes.io/docs/api-reference/v1.6/#taint-v1-core
    """

    VALID_TAINT_EFFECTS = ['NoSchedule', 'PreferNoSchedule', 'NoExecute']

    def __init__(self, model=None):
        super(Taint, self).__init__()

        self._effect = None
        self._key = None
        self._time_added = None
        self._value = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'effect' in model:
            self.effect = model['effect']
        if 'key' in model:
            self.key = model['key']
        if 'timeAdded' in model:
            self.time_added = model['timeAdded']
        if 'value' in model:
            self.value = model['value']

    # ------------------------------------------------------------------------------------- effect

    @property
    def effect(self):
        return self._effect

    @effect.setter
    def effect(self, e=None):
        if not is_valid_string(e) or e not in Taint.VALID_TAINT_EFFECTS:
            raise SyntaxError('Taint: effect: [ {} ] is invalid.'.format(e))
        self._effect = e

    # ------------------------------------------------------------------------------------- key

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, k=None):
        if not is_valid_string(k):
            raise SyntaxError('Taint: key: [ {} ] is invalid.'.format(k))
        self._key = k

    # ------------------------------------------------------------------------------------- timeAdded

    @property
    def time_added(self):
        return self._time_added

    @time_added.setter
    def time_added(self, t=None):
        # TODO(froch): at time of writing, K8s documentation is incomplete
        # https://kubernetes.io/docs/api-reference/v1.6/#time-v1-meta
        self._time_added = t

    # ------------------------------------------------------------------------------------- value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v=None):
        if not is_valid_string(v):
            raise SyntaxError('Taint: value: [ {} ] is invalid.'.format(v))
        self._value = v

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.effect is not None:
            data['effect'] = self.effect
        if self.key is not None:
            data['key'] = self.key
        if self.time_added is not None:
            data['timeAdded'] = self.time_added
        if self.value is not None:
            data['value'] = self.value
        return data
