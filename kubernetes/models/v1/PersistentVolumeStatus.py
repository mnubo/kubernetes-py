#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string


class PersistentVolumeStatus(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_persistentvolumestatus
    """

    def __init__(self, model=None):
        super(PersistentVolumeStatus, self).__init__()

        self._phase = None
        self._message = None
        self._reason = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'phase' in model:
            self.phase = model['phase']
        if 'message' in model:
            self.message = model['message']
        if 'reason' in model:
            self.reason = model['reason']

    # ------------------------------------------------------------------------------------- phase

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, p=None):
        if not is_valid_string(p):
            raise SyntaxError('PersistentVolumeStatus: phase: [ {} ] is invalid.'.format(p))
        self._phase = p

    # ------------------------------------------------------------------------------------- message

    @property
    def message(self):
        return self._phase

    @message.setter
    def message(self, m=None):
        if not is_valid_string(m):
            raise SyntaxError('PersistentVolumeStatus: message: [ {} ] is invalid.'.format(m))
        self._message = m

    # ------------------------------------------------------------------------------------- reason

    @property
    def reason(self):
        return self._reason

    @reason.setter
    def reason(self, r=None):
        if not is_valid_string(r):
            raise SyntaxError('PersistentVolumeStatus: reason: [ {} ] is invalid.'.format(r))
        self._reason = r

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.phase is not None:
            data['phase'] = self.phase
        if self.message is not None:
            data['message'] = self.message
        if self.reason is not None:
            data['reason'] = self.reason
        return data
