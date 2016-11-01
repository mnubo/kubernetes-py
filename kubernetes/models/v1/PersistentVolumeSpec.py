#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.Volume import Volume


class PersistentVolumeSpec(object):

    VALID_CAPACITY_PARAMS = [
        'storage'
    ]

    VALID_ACCESS_MODES = [
        'ReadWriteOnce',
        'ReadOnlyMany',
        'ReadWriteMany'
    ]

    VALID_RECLAIM_POLICIES = [
        'Retain',
        'Recycle',
        'Delete'
    ]

    def __init__(self, model=None, capacity=None, access_modes=None, reclaim_policy=None, volume=None):
        super(PersistentVolumeSpec, self).__init__()

        if model is not None:
            if not isinstance(model, dict):
                raise SyntaxError('PersistentVolumeSpec: model: [ {0} ] must be a dict.'.format(model.__class__.__name__))
            self.model = model

        else:
            self.model = {
                'capacity': {'storage': '10Gi'},
                'accessModes': ['ReadOnlyMany'],
                'persistentVolumeReclaimPolicy': 'Recycle'
            }

            if capacity:
                self.set_capacity(capacity)
            if access_modes:
                self.set_access_modes(access_modes)
            if reclaim_policy:
                self.set_reclaim_policy(reclaim_policy)
            if volume:
                self.set_volume(volume)

    # -------------------------------------------------------------------------------------  capacity

    def set_capacity(self, capacity=None):
        if not isinstance(capacity, dict):
            raise SyntaxError('PersistentVolumeSpec: capacity: [ {0} ] must be a dict.'.format(capacity.__class__.__name__))
        for k, v in capacity.items():
            if k not in PersistentVolumeSpec.VALID_CAPACITY_PARAMS:
                capacity.pop(k)
        self.model['capacity'].update(capacity)

    # -------------------------------------------------------------------------------------  access_mode

    def set_access_modes(self, access_modes=None):
        if not isinstance(access_modes, list):
            raise SyntaxError(
                'PersistentVolumeSpec: access_modes: [ {0} ] must be a list.'.format(access_modes.__class__.__name__))
        access_modes = filter(lambda x: x in PersistentVolumeSpec.VALID_ACCESS_MODES, access_modes)
        self.model['accessModes'] = access_modes

    # -------------------------------------------------------------------------------------  reclaim_policy

    def set_reclaim_policy(self, reclaim_policy=None):
        if reclaim_policy not in PersistentVolumeSpec.VALID_RECLAIM_POLICIES:
            raise SyntaxError('PersistentVolumeSpec: reclaim_policy: [ {0} ] is invalid.'.format(reclaim_policy))
        if reclaim_policy in PersistentVolumeSpec.VALID_RECLAIM_POLICIES:
            self.model['persistentVolumeReclaimPolicy'] = reclaim_policy

    # -------------------------------------------------------------------------------------  volume

    def set_volume(self, volume=None):
        if not isinstance(volume, Volume):
            raise SyntaxError('PersistentVolumeSpec: volume: [ {0} ] must be a Volume.'.format(volume))
        self.model['volume'] = volume['volume']
