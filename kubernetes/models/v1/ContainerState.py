#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.ContainerStateRunning import ContainerStateRunning
from kubernetes.models.v1.ContainerStateTerminated import ContainerStateTerminated
from kubernetes.models.v1.ContainerStateWaiting import ContainerStateWaiting
from kubernetes.utils import filter_model


class ContainerState(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_containerstate
    """

    def __init__(self, model=None):
        super(ContainerState, self).__init__()

        self._waiting = None
        self._running = None
        self._terminated = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'waiting' in model:
            self.waiting = ContainerStateWaiting(model['waiting'])
        if 'running' in model:
            self.running = ContainerStateRunning(model['running'])
        if 'terminated' in model:
            self.terminated = ContainerStateTerminated(model['terminated'])

    # ------------------------------------------------------------------------------------- waiting

    @property
    def waiting(self):
        return self._waiting

    @waiting.setter
    def waiting(self, state=None):
        if not isinstance(state, ContainerStateWaiting):
            raise SyntaxError('ContainerState: waiting: [ {0} ] is invalid.'.format(state))
        self._waiting = state

    # ------------------------------------------------------------------------------------- running

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, state=None):
        if not isinstance(state, ContainerStateRunning):
            raise SyntaxError('ContainerState: running: [ {0} ] is invalid.'.format(state))
        self._running = state

    # ------------------------------------------------------------------------------------- terminated

    @property
    def terminated(self):
        return self._terminated

    @terminated.setter
    def terminated(self, state=None):
        if not isinstance(state, ContainerStateTerminated):
            raise SyntaxError('ContainerState: terminated: [ {0} ] is invalid.'.format(state))
        self._terminated = state

    # ------------------------------------------------------------------------------------- serialized

    def serialize(self):
        data = {}
        if self.waiting is not None:
            data['waiting'] = self.waiting.serialize()
        if self.running is not None:
            data['running'] = self.running.serialize()
        if self.terminated is not None:
            data['terminated'] = self.terminated.serialize()
        return data
