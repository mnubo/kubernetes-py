#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.BaseModel import BaseModel


class Probe(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self)
        model = kwargs.get('model', None)
        handler = kwargs.get('handler', None)
        initial_delay_s = kwargs.get('initial_delay_s', 1)
        timeout_s = kwargs.get('timeout_s', 3)
        period_s = kwargs.get('period_s', 15)
        success_threshold = kwargs.get('success_threshold', 1)
        failure_threshold = kwargs.get('failure_threshold', 2)

        self.valid_handlers = ['exec', 'httpGet', 'tcpSocket']
        if model is not None:
            assert isinstance(model, dict)
            self.model = model
            if 'status' in self.model.keys():
                self.model.pop('status', None)
            for h in self.valid_handlers:
                if h in self.model.keys():
                    self.handler = h
                    break
        else:
            self.model = dict()
            self.handler = handler
            self.set_handler(**kwargs)
            self.model['initialDelaySeconds'] = initial_delay_s
            self.model['timeoutSeconds'] = timeout_s
            self.model['periodSeconds'] = period_s
            self.model['successThreshold'] = success_threshold
            self.model['failureThreshold'] = failure_threshold

    def get_handler(self):
        my_handler = None
        if self.handler in self.model.keys():
            my_handler = self.model[self.handler]
        return my_handler

    def get_failure_threshold(self):
        return self.model['failureThreshold']

    def get_initial_delay(self):
        return self.model['initialDelaySeconds']

    def get_period(self):
        return self.model['periodSeconds']

    def get_success_threshold(self):
        return self.model['successThreshold']

    def get_timeout(self):
        return self.model['timeoutSeconds']

    def set_handler(self, **kwargs):
        handler = kwargs.get('handler', None)

        if handler is None or not isinstance(handler, str) or handler not in self.valid_handlers:
            raise SyntaxError('Probe: handler must be: {my_list}'.format(my_list=', '.join(self.valid_handlers)))

        if self.handler is None:
            self.handler = handler

        if handler != self.handler:
            self.model.pop(self.handler, None)
            self.handler = handler

        # Creating a new one.
        self.model[handler] = dict()
        if handler == 'exec':
            if 'command' not in kwargs.keys():
                raise SyntaxError('Probe: command must be given when using an exec handler.')
            self.model[handler]['command'] = kwargs.get('command')
        elif handler == 'httpGet':
            if 'port' not in kwargs.keys():
                raise SyntaxError('Probe: port must be given when using an httpGet handler.')
            self.model[handler]['port'] = int(kwargs.get('port'))
            if 'path' in kwargs.keys():
                self.model[handler]['path'] = kwargs.get('path')
            if 'host' in kwargs.keys():
                self.model[handler]['host'] = kwargs.get('host')
            if 'scheme' in kwargs.keys():
                self.model[handler]['scheme'] = kwargs.get('scheme')
        elif handler == 'tcpSocket':
            if 'port' not in kwargs.keys():
                raise SyntaxError('Probe: port must be given when using a tcpSocket handler.')
            self.model[handler]['port'] = int(kwargs.get('port'))
        return self
