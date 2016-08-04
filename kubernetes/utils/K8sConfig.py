#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

valid_versions = ['v1']


class K8sConfig:

    def __init__(self, api_host='localhost:8888', version='v1', namespace='default'):

        if not isinstance(api_host, str) or not isinstance(version, str):
            raise SyntaxError('Please make sure api_host and version are strings.')
        if version not in valid_versions:
            raise SyntaxError('Please provide a valid version in: {str}'.format(str=', '.join(valid_versions)))
        if not isinstance(namespace, str):
            raise SyntaxError('Please make sure namespace is a string.')

        self.api_host = api_host
        self.version = version
        self.namespace = namespace

    def get_api_host(self):
        return self.api_host

    def get_namespace(self):
        return self.namespace

    def get_version(self):
        return self.version

    def set_api_host(self, api_host=None):
        self.api_host = api_host
        return

    def set_namespace(self, namespace='default'):
        self.namespace = namespace
        return

    def set_version(self, version=None):
        self.version = version
        return
