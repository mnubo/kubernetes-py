#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import re

DEFAULT_API_HOST = "localhost:8888"
DEFAULT_API_VERSION = "v1"
DEFAULT_NAMESPACE = "default"

VALID_API_VERSIONS = ["v1"]

VALID_IP_RE = re.compile(r'^(http[s]?\:\/\/)?((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3})(:[0-9]+)?$')
VALID_HOST_RE = re.compile(r'^(http[s]?\:\/\/)?([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9]\.)*([A-Za-z]|[A-Za-z][A-Za-z\-]*[A-Za-z])(:[0-9]+)?$')


class K8sConfig:
    def __init__(self, api_host=DEFAULT_API_HOST, auth=None, namespace=DEFAULT_NAMESPACE,
                 pull_secret=None, token=None, version=DEFAULT_API_VERSION):

        if not isinstance(api_host, str) or not isinstance(version, str):
            raise SyntaxError('Please make sure api_host and version are strings.')

        if not (VALID_IP_RE.match(api_host) or VALID_HOST_RE.match(api_host)):
            raise SyntaxError('Please make sure the API host is valid: [ {0} ]'.format(api_host))

        if auth is not None and not isinstance(auth, tuple):
            raise SyntaxError('Please make sure auth is a tuple: [ {0} ]'.format(auth))

        if not isinstance(namespace, str):
            raise SyntaxError('Please make sure namespace is a string: [ {0} ]'.format(namespace))

        if pull_secret is not None and not isinstance(pull_secret, str):
            raise SyntaxError('Please make sure pull_secret is a string: [ {0} ]'.format(pull_secret))

        if token is not None and not isinstance(token, str):
            raise SyntaxError('Please make sure token is a string: [ {0} ]'.format(token))

        if version not in VALID_API_VERSIONS:
            valid = ", ".join(VALID_API_VERSIONS)
            raise SyntaxError('Please provide a valid version: [ {0} ] in: [ {1} ]'.format(version, valid))

        schema_re = re.compile(r"^http[s]*")
        if not schema_re.search(api_host):
            api_host = "http://{0}".format(api_host)

        self.api_host = api_host
        self.auth = auth
        self.namespace = namespace
        self.pull_secret = pull_secret
        self.token = token
        self.version = version
