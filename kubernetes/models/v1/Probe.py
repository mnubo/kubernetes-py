#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.ExecAction import ExecAction
from kubernetes.models.v1.HTTPGetAction import HTTPGetAction
from kubernetes.models.v1.TCPSocketAction import TCPSocketAction
from kubernetes.utils import filter_model


class Probe(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_probe
    """

    VALID_HANDLERS = ['exec', 'httpGet', 'tcpSocket']

    def __init__(self, handler=None, model=None):
        super(Probe, self).__init__()

        if handler not in Probe.VALID_HANDLERS:
            raise SyntaxError('Probe: handler: [ {0} ] is invalid.'.format(handler))
        self.handler = handler

        self.exec_action = None
        self.http_get_action = None
        self.tcp_socket_action = None

        if handler == 'exec':
            self.exec_action = ExecAction()
        if handler == 'httpGet':
            self.http_get_action = HTTPGetAction()
        if handler == 'tcpSocket':
            self.tcp_socket_action = TCPSocketAction()

        self.initial_delay_seconds = 15
        self.timeout_seconds = 1
        self.period_seconds = 10
        self.success_threshold = 1
        self.failure_threshold = 3

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        pass

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.handler == 'exec':
            data[self.handler] = self.exec_action.json()
        if self.handler == 'httpGet':
            data[self.handler] = self.http_get_action.json()
        if self.handler == 'tcpSocket':
            data[self.handler] = self.tcp_socket_action.json()
        if self.initial_delay_seconds:
            data['initialDelaySeconds'] = self.initial_delay_seconds
        if self.timeout_seconds:
            data['timeoutSeconds'] = self.timeout_seconds
        if self.period_seconds:
            data['periodSeconds'] = self.period_seconds
        if self.success_threshold:
            data['successThreshold'] = self.success_threshold
        if self.failure_threshold:
            data['failureThreshold'] = self.failure_threshold
        return data
