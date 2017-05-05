#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string


class EventSource(object):
    """
    https://kubernetes.io/docs/api-reference/v1.5/#eventsource-v1
    """

    def __init__(self, model=None):
        super(EventSource, self).__init__()

        self._component = None
        self._host = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'component' in model:
            self._component = model['component']
        if 'host' in model:
            self._host = model['host']

    # ------------------------------------------------------------------------------------- component

    @property
    def component(self):
        return self._component

    @component.setter
    def component(self, c=None):
        if not is_valid_string(c):
            raise SyntaxError("EventSource: component: [ {} ] is invalid.".format(c))
        self._component = c

    # ------------------------------------------------------------------------------------- host

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, h=None):
        if not is_valid_string(h):
            raise SyntaxError("EventSource: host: [ {} ] is invalid.".format(h))
        self._host = h

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.component is not None:
            data['component'] = self.component
        if self.host is not None:
            data['host'] = self.host
        return data
