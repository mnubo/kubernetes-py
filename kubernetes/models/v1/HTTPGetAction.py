#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_list, is_valid_dict, is_valid_string


class HTTPGetAction(object):

    VALID_SCHEMES = ['HTTP', 'HTTPS']

    def __init__(self):
        super(HTTPGetAction, self).__init__()

        self._http_headers = []
        self._scheme = 'HTTP'

        self.host = None
        self.path = None
        self.port = None

    # ------------------------------------------------------------------------------------- add

    def add_header(self, name=None, value=None):
        if not is_valid_string(name) or not is_valid_string(value):
            raise SyntaxError('HTTPGetAction: header: [ {0} : {1} ] is invalid.'.format(name, value))
        data = {'name': name, 'value': value}
        self._http_headers.append(data)

    # ------------------------------------------------------------------------------------- http headers

    @property
    def http_headers(self):
        return self._http_headers

    @http_headers.setter
    def http_headers(self, headers=None):
        msg = 'HTTPGetAction: headers: [ {0} ] is invalid.'.format(headers)
        if not is_valid_list(headers, dict):
            raise SyntaxError(msg)
        for x in headers:
            if not is_valid_dict(x, ['name', 'value']):
                raise SyntaxError(msg)
        self._http_headers = headers

    # ------------------------------------------------------------------------------------- http headers

    @property
    def scheme(self):
        return self._scheme

    @scheme.setter
    def scheme(self, scheme=None):
        if not is_valid_string(scheme) or scheme not in HTTPGetAction.VALID_SCHEMES:
            raise SyntaxError('HTTPGetAction: scheme: [ {0} ] is invalid.'.format(scheme))
        self._scheme = scheme

    # ------------------------------------------------------------------------------------- serialize

    def json(self):
        data = {}
        if self.http_headers:
            data['httpHeaders'] = self.http_headers
        if self.host is not None:
            data['host'] = self.host
        if self.path is not None:
            data['path'] = self.path
        if self.port is not None:
            data['port'] = self.port
        if self.scheme:
            data['scheme'] = self.scheme
        return data
