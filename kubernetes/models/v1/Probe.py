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

    def __init__(self, model=None):
        super(Probe, self).__init__()

        self._exec_action = None
        self._http_get_action = None
        self._tcp_socket_action = None

        self._initial_delay_seconds = None
        self._timeout_seconds = None
        self._period_seconds = None
        self._success_threshold = None
        self._failure_threshold = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'exec' in model:
            self.exec_action = ExecAction(model['exec'])
        if 'httpGet' in model:
            self.http_get_action = HTTPGetAction(model['httpGet'])
        if 'tcpSocket' in model:
            self.tcp_socket_action = TCPSocketAction(model['tcpSocket'])
        if 'initialDelaySeconds' in model:
            self.initial_delay_seconds = model['initialDelaySeconds']
        if 'timeoutSeconds' in model:
            self.timeout_seconds = model['timeoutSeconds']
        if 'periodSeconds' in model:
            self.period_seconds = model['periodSeconds']
        if 'successThreshold' in model:
            self.success_threshold = model['successThreshold']
        if 'failureThreshold' in model:
            self.failure_threshold = model['failureThreshold']

    # ------------------------------------------------------------------------------------- exec

    @property
    def exec_action(self):
        return self._exec_action

    @exec_action.setter
    def exec_action(self, action=None):
        if not isinstance(action, ExecAction):
            raise SyntaxError('Probe: exec_action: [ {} ] is invalid.'.format(action))
        self._exec_action = action

    # ------------------------------------------------------------------------------------- httpGet

    @property
    def http_get_action(self):
        return self._http_get_action

    @http_get_action.setter
    def http_get_action(self, action=None):
        if not isinstance(action, HTTPGetAction):
            raise SyntaxError('Probe: http_get_action: [ {} ] is invalid.'.format(action))
        self._http_get_action = action

    # ------------------------------------------------------------------------------------- tcpSocket

    @property
    def tcp_socket_action(self):
        return self._tcp_socket_action

    @tcp_socket_action.setter
    def tcp_socket_action(self, action=None):
        if not isinstance(action, TCPSocketAction):
            raise SyntaxError('Probe: tcp_socket_action: [ {} ] is invalid.'.format(action))
        self._tcp_socket_action = action

    # ------------------------------------------------------------------------------------- initialDelaySeconds

    @property
    def initial_delay_seconds(self):
        return self._initial_delay_seconds

    @initial_delay_seconds.setter
    def initial_delay_seconds(self, secs=None):
        if not isinstance(secs, int):
            raise SyntaxError('Probe: initial_delay_seconds: [ {} ] is invalid.'.format(secs))
        self._initial_delay_seconds = secs

    # ------------------------------------------------------------------------------------- timeoutSeconds

    @property
    def timeout_seconds(self):
        return self._timeout_seconds

    @timeout_seconds.setter
    def timeout_seconds(self, secs=None):
        if not isinstance(secs, int):
            raise SyntaxError('Probe: timeout_seconds: [ {} ] is invalid.'.format(secs))
        self._timeout_seconds = secs

    # ------------------------------------------------------------------------------------- periodSeconds

    @property
    def period_seconds(self):
        return self._period_seconds

    @period_seconds.setter
    def period_seconds(self, secs=None):
        if not isinstance(secs, int):
            raise SyntaxError('Probe: period_seconds: [ {} ] is invalid.'.format(secs))
        self._period_seconds = secs

    # ------------------------------------------------------------------------------------- successThreshold

    @property
    def success_threshold(self):
        return self._success_threshold

    @success_threshold.setter
    def success_threshold(self, threshold=None):
        if not isinstance(threshold, int):
            raise SyntaxError('Probe: success_threshold: [ {} ] is invalid.'.format(threshold))
        self._success_threshold = threshold

    # ------------------------------------------------------------------------------------- failureThreshold

    @property
    def failure_threshold(self):
        return self._failure_threshold

    @failure_threshold.setter
    def failure_threshold(self, threshold=None):
        if not isinstance(threshold, int):
            raise SyntaxError('Probe: failure_threshold: [ {} ] is invalid.'.format(threshold))
        self._failure_threshold = threshold

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.exec_action is not None:
            data['exec'] = self.exec_action.serialize()
        if self.http_get_action is not None:
            data['httpGet'] = self.http_get_action.serialize()
        if self.tcp_socket_action is not None:
            data['tcpSocket'] = self.tcp_socket_action.serialize()
        if self.initial_delay_seconds is not None:
            data['initialDelaySeconds'] = self.initial_delay_seconds
        if self.timeout_seconds is not None:
            data['timeoutSeconds'] = self.timeout_seconds
        if self.period_seconds is not None:
            data['periodSeconds'] = self.period_seconds
        if self.success_threshold is not None:
            data['successThreshold'] = self.success_threshold
        if self.failure_threshold is not None:
            data['failureThreshold'] = self.failure_threshold
        return data
