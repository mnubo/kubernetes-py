#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import re
from os.path import expanduser, isfile

import yaml
from yaml import YAMLError

DEFAULT_KUBECONFIG = "{0}/.kube/config".format(expanduser("~"))
DEFAULT_API_HOST = "localhost:8888"
DEFAULT_API_VERSION = "v1"
DEFAULT_NAMESPACE = "default"

VALID_API_VERSIONS = ["v1"]

VALID_IP_RE = re.compile(
    r'^(http[s]?\:\/\/)?((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3})(:[0-9]+)?$')
VALID_HOST_RE = re.compile(r'^(http[s]?\:\/\/)?([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-\.]*[A-Za-z])+(:[0-9]+)?$')


class K8sConfig(object):
    def __init__(self, kubeconfig=DEFAULT_KUBECONFIG, api_host=DEFAULT_API_HOST, auth=None, cert=None,
                 namespace=DEFAULT_NAMESPACE, pull_secret=None, token=None, version=DEFAULT_API_VERSION):
        """
        Pulls configuration from a kubeconfig file, if present, otherwise accepts user-defined parameters.
        See http://kubernetes.io/docs/user-guide/kubeconfig-file/ for information on the kubeconfig file.

        :param kubeconfig: Absolute path to the kubeconfig file, if any.
        :param api_host: Absolute URI where the API server resides.
        :param auth: A tuple of (username, password) for basic authentication.
        :param namespace: The namespace to use. Defaults to 'default'
        :param pull_secret: The password to use when pulling images from the container repository.
        :param token: An authentication token. Mutually exclusive with 'auth'.
        :param version: The version of the API to target. Defaults to 'v1'.
        """

        super(K8sConfig, self).__init__()

        self.api_host = None
        self.auth = None
        self.ca_cert = None
        self.ca_cert_data = None
        self.cert = None
        self.client_certificate = None
        self.client_key = None
        self.pull_secret = None
        self.token = None

        dotconf = None
        if kubeconfig is not None:
            if not isfile(kubeconfig):
                raise IOError('K8sConfig: kubeconfig: [ {0} ] doesn\'t exist.'.format(kubeconfig))
            try:
                with open(kubeconfig, 'r') as stream:
                    dotconf = yaml.load(stream)
            except YAMLError as err:
                raise SyntaxError('K8sConfig: kubeconfig: [ {0} ] is not a valid YAML file.'.format(kubeconfig))

        # we're pulling configuration from a kubeconfig file
        if dotconf is not None:
            self.clusters = dotconf['clusters']
            self.contexts = dotconf['contexts']
            self.current_context = dotconf['current-context']
            self.current_context_dict = [context['context']
                                         for context in self.contexts
                                         if context['name'] == self.current_context][0]
            self.preferences = dotconf['preferences']
            self.pull_secret = pull_secret
            self.users = dotconf['users']
            self.version = dotconf['apiVersion']

            if self.clusters:
                for cluster in self.clusters:
                    if cluster['name'] == self.current_context_dict['cluster']:
                        if 'server' in cluster['cluster']:
                            self.api_host = cluster['cluster']['server']
                        if 'certificate-authority' in cluster['cluster']:
                            self.ca_cert = cluster['cluster']['certificate-authority']
                        if 'certificate-authority-data' in cluster['cluster']:
                            self.ca_cert_data = cluster['cluster']['certificate-authority-data']

            if self.users:
                for user in self.users:
                    if user['name'] == self.current_context_dict['user']:
                        if 'username' in user['user'] and 'password' in user['user']:
                            self.auth = (user['user']['username'], user['user']['password'])
                        if 'token' in user['user']:
                            self.token = user['user']['token']
                        if 'client-certificate' in user['user'] and 'client-key' in user['user']:
                            self.client_certificate = user['user']['client-certificate']
                            self.client_key = user['user']['client-key']
                            self.cert = (self.client_certificate, self.client_key)

            if self.contexts:
                for context in self.contexts:
                    if context['name'] == self.current_context:
                        if 'namespace' in context['context']:
                            self.namespace = context['context']['namespace']
                        else:
                            self.namespace = namespace

        # we're using user-supplied config; run some sanity checks.
        if dotconf is None:

            if not isinstance(api_host, str) or not isinstance(version, str):
                raise SyntaxError(
                    'K8sConfig: host: [ {0} ] and version: [ {1} ] must be strings.'.format(api_host, version))
            if not (VALID_IP_RE.match(api_host) or VALID_HOST_RE.match(api_host)):
                raise SyntaxError('K8sConfig: host: [ {0} ] is invalid.'.format(api_host))
            if auth is not None and not isinstance(auth, tuple):
                raise SyntaxError('K8sConfig: auth: [ {0} ] must be a tuple for basic authentication.'.format(auth))
            if not isinstance(namespace, str):
                raise SyntaxError('K8sConfig: namespace: [ {0} ] must be a string.'.format(namespace))
            if pull_secret is not None and not isinstance(pull_secret, list):
                raise SyntaxError('K8sConfig: pull_secret: [ {0} ] must be a list.'.format(pull_secret))
            if token is not None and not isinstance(token, str):
                raise SyntaxError('K8sConfig: token: [ {0} ] must be a string.'.format(token))
            if version not in VALID_API_VERSIONS:
                valid = ", ".join(VALID_API_VERSIONS)
                raise SyntaxError('K8sConfig: api_version: [ {0} ] must be in: [ {1} ]'.format(version, valid))

            schema_re = re.compile(r"^http[s]*")
            if not schema_re.search(api_host):
                api_host = "http://{0}".format(api_host)
            self.api_host = api_host
            self.auth = auth
            self.cert = cert
            self.namespace = namespace
            self.pull_secret = pull_secret
            self.token = token
            self.version = version

    def serialize(self):
        data = {}
        if self.api_host is not None:
            data['api_host'] = self.api_host
        if self.auth is not None:
            data['auth'] = self.auth
        if self.cert is not None:
            data['cert'] = self.cert
        if self.namespace is not None:
            data['namespace'] = self.namespace
        if self.pull_secret is not None:
            data['pull_secret'] = self.pull_secret
        if self.token is not None:
            data['token'] = self.token
        if self.version is not None:
            data['version'] = self.version
        return data
