#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string


class PersistentVolumeClaimVolumeSource(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_persistentvolumeclaimvolumesource
    """

    def __init__(self, model=None):
        super(PersistentVolumeClaimVolumeSource, self).__init__()

        self._claim_name = None
        self._read_only = False

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'claimName' in model:
            self.claim_name = model['claimName']
        if 'readOnly' in model:
            self.read_only = model['readOnly']

    # ------------------------------------------------------------------------------------- claimName

    @property
    def claim_name(self):
        return self._claim_name

    @claim_name.setter
    def claim_name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('PersistentVolumeClaimVolumeSource: claim_name: [ {} ] is invalid.'.format(name))
        self._claim_name = name

    # ------------------------------------------------------------------------------------- readOnly

    @property
    def read_only(self):
        return self._read_only

    @read_only.setter
    def read_only(self, ro=None):
        if not isinstance(ro, bool):
            raise SyntaxError('PersistentVolumeClaimVolumeSource: read_only: [ {} ] is invalid.'.format(ro))
        self._read_only = ro

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.claim_name is not None:
            data['claimName'] = self.claim_name
        if self.read_only is not None:
            data['readOnly'] = self.read_only
        return data