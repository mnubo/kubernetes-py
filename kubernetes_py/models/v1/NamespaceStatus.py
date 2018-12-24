#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


class NamespaceStatus(object):
    """
    https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_namespacestatus
    """

    def __init__(self, model=None):
        super(NamespaceStatus, self).__init__()

        self._phase = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'phase' in model:
            self.finalizers = model['phase']

    # --------------------------------------------------------------------------------- finalizers

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, p=None):
        if not isinstance(p, str):
            raise SyntaxError('NamespaceStatus: phase: [ {} ] is invalid. Must be a string.'.format(p))
        self._phase = p

    # --------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.phase is not None:
            data['phase'] = self.phase
        return data
