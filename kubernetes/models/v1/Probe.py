#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.BaseModel import BaseModel


class Probe(BaseModel):

    VALID_HANDLERS = ['exec', 'httpGet', 'tcpSocket']

    def __init__(self, **kwargs):
        BaseModel.__init__(self)
        model = kwargs.get('model', None)

        if model is not None:
            filtered = filter(lambda x: x in Probe.VALID_HANDLERS, model.keys())
        else:
            filtered = filter(lambda x: x in Probe.VALID_HANDLERS, kwargs)

        if not filtered:
            raise SyntaxError('Probe: Valid handler not found. (eg. {0} )'.format(Probe.VALID_HANDLERS))
        if len(filtered) > 1:
            raise SyntaxError('Probe: More than one handler found: [ {0} ]'.format(filtered))
        handler = filtered[0]  # there can be only one.

        if model is not None:
            initial_delay_s = model.get('initialDelaySeconds', 1)
            timeout_s = model.get('timeoutSeconds', 3)
            period_s = model.get('periodSeconds', 15)
            success_threshold = model.get('successThreshold', 1)
            failure_threshold = model.get('failureThreshold', 2)
        else:
            initial_delay_s = kwargs.get('initialDelaySeconds', 1)
            timeout_s = kwargs.get('timeoutSeconds', 3)
            period_s = kwargs.get('periodSeconds', 15)
            success_threshold = kwargs.get('successThreshold', 1)
            failure_threshold = kwargs.get('failureThreshold', 2)

        if model is not None:
            assert isinstance(model, dict)
            self.model = model
            if 'status' in self.model.keys():
                self.model.pop('status', None)
            for h in Probe.VALID_HANDLERS:
                if h in self.model.keys():
                    self.handler = h
                    break
        else:
            self.model = dict()
            self.handler = handler
            handler_dict = kwargs[handler]
            self.set_handler(handler_dict)
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

    def set_handler(self, handler_dict=None):

        # Creating a new one.
        self.model[self.handler] = dict()

        if self.handler == 'exec':
            if 'command' not in handler_dict:
                raise SyntaxError('Probe: command must be given when using an exec handler.')
            self.model[self.handler]['command'] = handler_dict.get('command')

        if self.handler == 'httpGet':
            if 'port' not in handler_dict:
                raise SyntaxError('Probe: port must be given when using an httpGet handler.')
            self.model[self.handler]['port'] = int(handler_dict.get('port'))
            if 'path' in handler_dict:
                self.model[self.handler]['path'] = handler_dict.get('path')
            if 'host' in handler_dict:
                self.model[self.handler]['host'] = handler_dict.get('host')
            if 'scheme' in handler_dict:
                self.model[self.handler]['scheme'] = handler_dict.get('scheme')

        if self.handler == 'tcpSocket':
            if 'port' not in handler_dict:
                raise SyntaxError('Probe: port must be given when using a tcpSocket handler.')
            self.model[self.handler]['port'] = int(handler_dict.get('port'))

        return self
