#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import re
from os.path import expanduser, isfile
import logging
import os

import yaml
from yaml import YAMLError

KUBECONFIG_ENV_VAR = "KUBECONFIG"
KUBECONFIG_FILE = "{0}/.kube/config".format(expanduser("~"))
DEFAULT_API_HOST = "http://localhost:8080"
DEFAULT_API_VERSION = "v1"
DEFAULT_NAMESPACE = "default"
SERVICE_ACCOUNT_ROOT = "/var/run/secrets/kubernetes.io/serviceaccount"
SERVICE_ACCOUNT_CA_PATH = "{0}/ca.crt".format(SERVICE_ACCOUNT_ROOT)
SERVICE_ACCOUNT_TOKEN = "{0}/token".format(SERVICE_ACCOUNT_ROOT)
ENV_SERVICE_HOST = "KUBERNETES_SERVICE_HOST"
ENV_SERVICE_PORT = "KUBERNETES_SERVICE_PORT"

VALID_API_VERSIONS = ["v1"]

VALID_IP_RE = re.compile(
    r"^(http[s]?\:\/\/)?((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3})(:[0-9]+)?$"
)
VALID_HOST_RE = re.compile(r"^(http[s]?\:\/\/)?([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-\.]*[A-Za-z])+(:[0-9]+)?$")


class K8sConfig(object):
    def __init__(
        self, kubeconfig=None, api_host=None, auth=None, cert=None, namespace=None, pull_secret=None, token=None, version=None
    ):
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
        self.namespace = None
        self.token = None
        self.version = None

        self._init_with_defaults()

        if kubeconfig is None:
            self._init_with_defaults()
        else:
            self._read_config(filename=kubeconfig)

        # Default fallback host.
        if self.api_host is None:
            logging.debug("Overriding api host with: [ {0} ]".format(DEFAULT_API_HOST))
            self.api_host = DEFAULT_API_HOST

        # Set defaults if not caught in kubeconfig file or environments.
        if self.namespace is None:
            logging.debug("Overriding namespace with: [ {0} ]".format(DEFAULT_NAMESPACE))
            self.namespace = DEFAULT_NAMESPACE

        if self.version is None:
            logging.debug("Overriding api version with: [ {0} ]".format(DEFAULT_API_VERSION))
            self.version = DEFAULT_API_VERSION

        # Process overrides from arguments
        if api_host is not None:
            if not isinstance(api_host, str) or not (VALID_IP_RE.match(api_host) or VALID_HOST_RE.match(api_host)):
                raise SyntaxError("K8sConfig: host: [ {0} ] is invalid.".format(api_host))
            schema_re = re.compile(r"^http[s]*")
            if not schema_re.search(api_host):
                https_port_re = re.compile(r"\:443$")
                if not https_port_re:
                    logging.debug("Pre-pending http to api host [ {0} ] since port is not 443.".format(self.api_host))
                    api_host = "http://{0}".format(api_host)
                else:
                    logging.debug("Pre-pending https to api host [ {0} ] since port is 443.".format(self.api_host))
                    api_host = "https://{0}".format(api_host)
            self.api_host = api_host

        if auth is not None:
            if not isinstance(auth, tuple):
                raise SyntaxError("K8sConfig: auth: [ {0} ] must be a tuple for basic authentication.".format(auth))
            self.auth = auth

        if cert is not None:
            if not isinstance(cert, tuple):
                raise SyntaxError("K8sConfig: cert: [ {0} ] must be a tuple for client certificate/key.".format(cert))
            self.cert = cert

        if namespace is not None:
            if not isinstance(namespace, str):
                raise SyntaxError("K8sConfig: namespace: [ {0} ] must be a string.".format(namespace))
            self.namespace = namespace

        if pull_secret is not None:
            if not isinstance(pull_secret, list):
                raise SyntaxError("K8sConfig: pull_secret: [ {0} ] must be a list.".format(pull_secret))
            self.pull_secret = pull_secret

        if token is not None:
            if not isinstance(token, str):
                raise SyntaxError("K8sConfig: token: [ {0} ] must be a string.".format(token))
            self.token = token

        if version is not None:
            if not isinstance(version, str):
                raise SyntaxError("K8sConfig: host: [ {0} ] and version: [ {1} ] must be strings.".format(api_host, version))
            if version not in VALID_API_VERSIONS:
                valid = ", ".join(VALID_API_VERSIONS)
                raise SyntaxError("K8sConfig: api_version: [ {0} ] must be in: [ {1} ]".format(version, valid))
            self.version = version
        return

    def _init_with_defaults(self):
        # Try to initialize using the environment variable.
        kubeconfig = os.getenv(KUBECONFIG_ENV_VAR, None)
        if kubeconfig is not None:
            self._read_config(filename=kubeconfig)
            return

        # Try to initialize using the ~/.kube/config file.
        if isfile(KUBECONFIG_FILE):
            self._read_config(filename=KUBECONFIG_FILE)
            return

        # Try in-cluster config
        if isfile(SERVICE_ACCOUNT_CA_PATH):
            self._from_cluster()
        return

    def _from_cluster(self):
        # Initialize CA cert.
        if not isfile(SERVICE_ACCOUNT_CA_PATH):
            raise IOError("K8sConfig: Cannot find in-cluster ca certificate [ {0} ] ".format(SERVICE_ACCOUNT_CA_PATH))
        self.ca_cert = SERVICE_ACCOUNT_CA_PATH
        # Initialize the API server host
        host = os.getenv(ENV_SERVICE_HOST, None)
        port = os.getenv(ENV_SERVICE_PORT, None)
        self.api_host = "https://{0}:{1}".format(host, port)
        # Initialize the token
        if not isfile(SERVICE_ACCOUNT_TOKEN):
            raise IOError("K8sConfig: Cannot find in-cluster token file [ {1} ]".format(SERVICE_ACCOUNT_TOKEN))
        with open(SERVICE_ACCOUNT_TOKEN, "r") as stream:
            self.token = stream.read()
        self.version = DEFAULT_API_VERSION
        return

    def _read_config(self, filename=None):

        if not isfile(filename):
            raise IOError("K8sConfig: kubeconfig: [ {0} ] doesn't exist.".format(filename))
        try:
            with open(filename, "r") as stream:
                dotconf = yaml.safe_load(stream)
        except YAMLError as err:
            raise SyntaxError("K8sConfig: kubeconfig: [ {0} ] is not a valid YAML file: {1}".format(filename, err))

        self.clusters = dotconf.get("clusters")
        self.contexts = dotconf.get("contexts")
        self.current_context = dotconf.get("current-context")
        self.current_context_dict = [
            context.get("context") for context in self.contexts if context.get("name") == self.current_context
        ][0]
        self.preferences = dotconf.get("preferences", "")
        self.users = dotconf.get("users")
        self.version = dotconf.get("apiVersion")

        if self.clusters:
            for cluster in self.clusters:
                if cluster["name"] == self.current_context_dict["cluster"]:
                    if "server" in cluster["cluster"]:
                        self.api_host = cluster["cluster"]["server"]
                    if "certificate-authority" in cluster["cluster"]:
                        self.ca_cert = cluster["cluster"]["certificate-authority"]
                    if "certificate-authority-data" in cluster["cluster"]:
                        self.ca_cert_data = cluster["cluster"]["certificate-authority-data"]

        if self.users:
            for user in self.users:
                if user["name"] == self.current_context_dict["user"]:
                    if "username" in user["user"] and "password" in user["user"]:
                        self.auth = (user["user"]["username"], user["user"]["password"])
                    if "token" in user["user"]:
                        self.token = user["user"]["token"]
                    if "client-certificate" in user["user"] and "client-key" in user["user"]:
                        self.client_certificate = user["user"]["client-certificate"]
                        self.client_key = user["user"]["client-key"]
                        self.cert = (self.client_certificate, self.client_key)
                    if "client-certificate-data" in user["user"] and "client-key-data" in user["user"]:
                        self.client_certificate_data = user["user"]["client-certificate-data"]
                        self.client_key_data = user["user"]["client-key-data"]
                        self.cert_data = (self.client_certificate_data, self.client_key_data)

        if self.contexts:
            for context in self.contexts:
                if context["name"] == self.current_context:
                    if "namespace" in context["context"]:
                        self.namespace = context["context"]["namespace"]

    def serialize(self):
        data = {}
        if self.api_host is not None:
            data["api_host"] = self.api_host
        if self.auth is not None:
            data["auth"] = self.auth
        if self.cert is not None:
            data["cert"] = self.cert
        if self.namespace is not None:
            data["namespace"] = self.namespace
        if self.pull_secret is not None:
            data["pull_secret"] = self.pull_secret
        if self.token is not None:
            data["token"] = self.token
        if self.version is not None:
            data["version"] = self.version
        return data
