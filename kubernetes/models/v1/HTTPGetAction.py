#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_list, is_valid_dict, is_valid_string


class HTTPGetAction(object):

    VALID_SCHEMES = ['HTTP', 'HTTPS']

    def __init__(self, model=None):
        super(HTTPGetAction, self).__init__()

        self._http_headers = []
        self._scheme = 'HTTP'
        self._host = None
        self._path = None
        self._port = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'path' in model:
            self.path = model['path']
        if 'port' in model:
            self.port = model['port']
        if 'host' in model:
            self.host = model['host']
        if 'scheme' in model:
            self.scheme = model['scheme']
        if 'httpHeaders' in model:
            self.http_headers = model['httpHeaders']

    # ------------------------------------------------------------------------------------- add

    def add_header(self, name=None, value=None):
        if not is_valid_string(name) or not is_valid_string(value):
            raise SyntaxError('HTTPGetAction: header: [ {0} : {1} ] is invalid.'.format(name, value))
        data = {'name': name, 'value': value}
        self._http_headers.append(data)

    # ------------------------------------------------------------------------------------- path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path=None):
        if not is_valid_string(path):
            raise SyntaxError('HTTPGetAction: path: [ {0} ] is invalid.'.format(path))
        self._path = path

    # ------------------------------------------------------------------------------------- port

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port=None):
        msg = 'HTTPGetAction: port: [ {0} ] is invalid.'.format(port)
        if isinstance(port, str) and port.isdigit():
            port = int(port)
        if isinstance(port, int) and not 1 < port < 65535:
            raise SyntaxError(msg)
        self._port = port

    # ------------------------------------------------------------------------------------- host

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host=None):
        if not is_valid_string(host) :
            raise SyntaxError('HTTPGetAction: host: [ {0} ] is invalid.'.format(host))
        self._host = host

    # ------------------------------------------------------------------------------------- scheme

    @property
    def scheme(self):
        return self._scheme

    @scheme.setter
    def scheme(self, scheme=None):
        if scheme not in HTTPGetAction.VALID_SCHEMES:
            raise SyntaxError('HTTPGetAction: scheme: [ {0} ] is invalid.'.format(scheme))
        self._scheme = scheme

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

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.path is not None:
            data['path'] = self.path
        if self.port is not None:
            data['port'] = self.port
        if self.host is not None:
            data['host'] = self.host
        if self.scheme:
            data['scheme'] = self.scheme
        if self.http_headers:
            data['httpHeaders'] = self.http_headers
        return data
