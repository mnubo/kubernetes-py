#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#
from kubernetes.utils import filter_model


class AttachedVolume(object):
    """
    https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_attachedvolume
    """

    def __init__(self, model=None):
        super(AttachedVolume, self).__init__()

        self._name = None
        self._device_path = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'name' in model:
            self.name = model['name']
        if 'devicePath' in model:
            self.device_path = model['devicePath']

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, v):
        if not isinstance(v, str):
            raise SyntaxError('AttachedVolume: name: [ {0} ] is invalid.'.format(v))
        self._name = v

    # ------------------------------------------------------------------------------------- device_path

    @property
    def device_path(self):
        return self._device_path

    @device_path.setter
    def device_path(self, v):
        if not isinstance(v, str):
            raise SyntaxError('AttachedVolume: device_path: [ {0} ] is invalid.'.format(v))
        self._device_path = v

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.name:
            data['name'] = self.name
        if self.device_path:
            data['devicePath'] = self.device_path
        return data
