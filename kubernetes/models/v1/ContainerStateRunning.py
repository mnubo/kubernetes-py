#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, filter_model


class ContainerStateRunning(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_containerstaterunning
    """

    def __init__(self, model=None):
        super(ContainerStateRunning, self).__init__()

        self._started_at = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'startedAt' in model:
            self.started_at = model['startedAt']

    # ------------------------------------------------------------------------------------- reason

    @property
    def started_at(self):
        return self._started_at

    @started_at.setter
    def started_at(self, time=None):
        if not is_valid_string(time):
            raise SyntaxError('CoùntainerStateRunning: started_at: [ {0} ] is invalid.'.format(time))
        self._started_at = time

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.started_at is not None:
            data['startedAt'] = self.started_at
        return data
