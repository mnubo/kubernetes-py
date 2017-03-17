#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.PersistentVolumeSpec import PersistentVolumeSpec
from kubernetes.utils import is_valid_string, is_valid_list, is_valid_dict


class PersistentVolumeClaimStatus(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_persistentvolumeclaimstatus
    """

    def __init__(self, model=None):
        super(PersistentVolumeClaimStatus, self).__init__()

        self._phase = None
        self._access_modes = None
        self._capacity = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'phase' in model:
            self.phase = model['phase']
        if 'accessModes' in model:
            self.access_modes = model['accessModes']
        if 'capacity' in model:
            self.capacity = model['capacity']

    # ------------------------------------------------------------------------------------- phase

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, p=None):
        if not is_valid_string(p):
            raise SyntaxError('PersistentVolumeClaimStatus: phase: [ {} ] is invalid.'.format(p))
        self._phase = p

    # ------------------------------------------------------------------------------------- accessModes

    @property
    def access_modes(self):
        return self._access_modes

    @access_modes.setter
    def access_modes(self, modes=None):
        if not is_valid_list(modes, str):
            raise SyntaxError('PersistentVolumeClaimStatus: access_modes: [ {} ] is invalid.'.format(modes))
        filtered = list(filter(lambda x: x in PersistentVolumeSpec.VALID_ACCESS_MODES, modes))
        self._access_modes = filtered

    # ------------------------------------------------------------------------------------- capacity

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, c=None):
        if not is_valid_dict(c):
            raise SyntaxError('PersistentVolumeClaimStatus: capacity: [ {} ] is invalid.'.format(c))
        self._capacity = c

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.phase is not None:
            data['phase'] = self.phase
        if self.access_modes is not None:
            data['accessModes'] = self.access_modes
        if self.capacity is not None:
            data['capacity'] = self.capacity
        return data
