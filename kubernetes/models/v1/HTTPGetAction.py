#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.BaseModel import BaseModel


class HTTPGetAction(BaseModel):
    
    def __init__(self, model=None):
        super(HTTPGetAction, self).__init__()

        self._http_headers = model.get('httpHeaders', [])

        self.host = model.get('host', None)
        self.path = model.get('path', None)
        self.port = model.get('port', None)
        self.scheme = model.get('scheme', 'HTTP')

    # ------------------------------------------------------------------------------------- add

    def add_header(self, key=None, value=None):
        if not isinstance(key, str) and not isinstance(value, str):
            raise SyntaxError('HTTPGetAction: header: [ {0} : {1} ] is invalid.'.format(key, value))
        data = {key: value}
        self._http_headers.append(data)

    # ------------------------------------------------------------------------------------- HTTP headers

    @property
    def http_headers(self):
        return self._http_headers

    @http_headers.setter
    def http_headers(self, headers=None):
        msg = 'HTTPGetAction: headers: [ {0} ] is invalid.'.format(headers)
        if not isinstance(headers, list):
            raise SyntaxError(msg)
        for x in headers:
            if not isinstance(x, dict):
                raise SyntaxError(msg)
            if len(x) > 1:
                raise SyntaxError(msg)
        self._http_headers = headers

    # ------------------------------------------------------------------------------------- serialize

    def json(self):
        data = {}
        if self.http_headers:
            data['httpHeaders'] = self.http_headers
        if self.host:
            data['host'] = self.host
        if self.path:
            data['path'] = self.path
        if self.port:
            data['port'] = self.port
        if self.scheme:
            data['scheme'] = self.scheme
        return data
