#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
from kubernetes import K8sConfig
from tests import utils

DEFAULT_API_HOST = "localhost:8888"
DEFAULT_API_VERSION = "v1"
DEFAULT_NAMESPACE = "default"


class K8sConfigTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # ------------------------------------------------------------------------------------- init without kubeconfig

    def test_init_with_kubeconfig_none(self):
        config = K8sConfig(kubeconfig=None)
        self.assertIsNotNone(config)
        self.assertIsInstance(config, K8sConfig)
        self.assertIsInstance(config.api_host, str)
        self.assertEqual(config.api_host, "http://{0}".format(DEFAULT_API_HOST))
        self.assertIsNone(config.auth)
        self.assertIsInstance(config.namespace, str)
        self.assertEqual(config.namespace, DEFAULT_NAMESPACE)
        self.assertIsNone(config.pull_secret)
        self.assertIsNone(config.token)
        self.assertEqual(config.version, DEFAULT_API_VERSION)

    # ------------------------------------------------------------------------------------- init with kubeconfig

    def test_init_with_test_kubeconfig(self):
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        self.assertIsNotNone(config)
        self.assertIsInstance(config, K8sConfig)
        if config.api_host is not None:
            self.assertIsInstance(config.api_host, str)
        if config.auth is not None:
            self.assertIsInstance(config.auth, tuple)
        if config.ca_cert is not None:
            self.assertIsInstance(config.ca_cert, str)
        if config.ca_cert_data is not None:
            self.assertIsInstance(config.ca_cert_data, str)
        if config.cert is not None:
            self.assertIsInstance(config.cert, str)
        if config.client_certificate is not None:
            self.assertIsInstance(config.client_certificate, str)
        if config.client_key is not None:
            self.assertIsInstance(config.client_key, str)
        if config.clusters is not None:
            self.assertIsInstance(config.clusters, list)
        if config.contexts is not None:
            self.assertIsInstance(config.contexts, list)
        if config.current_context is not None:
            self.assertIsInstance(config.current_context, str)
        if config.preferences is not None:
            self.assertIsInstance(config.preferences, dict)
        if config.pull_secret is not None:
            self.assertIsInstance(config.pull_secret, str)
        if config.users is not None:
            self.assertIsInstance(config.users, list)
        if config.version is not None:
            self.assertIsInstance(config.version, str)

    # ------------------------------------------------------------------------------------- init with custom args

    def test_init_api_host_invalid_hostname(self):
        try:
            K8sConfig(
                kubeconfig=None,
                api_host="yo_mama:1234"
            )
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_api_host_valid_hostname_no_port(self):
        host = "yo-mama.com"
        config = K8sConfig(
            kubeconfig=None,
            api_host=host
        )
        self.assertIn(host, config.api_host)

    def test_init_api_host_invalid_ip_address(self):
        try:
            K8sConfig(
                kubeconfig=None,
                api_host="192671.62671283.735.23322:1234"
            )
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_valid_ip_no_port(self):
        host = "192.168.99.100"
        config = K8sConfig(
            kubeconfig=None,
            api_host=host
        )
        self.assertIn(host, config.api_host)

    def test_init_invalid_auth(self):
        auth = "yomama"
        try:
            K8sConfig(
                kubeconfig=None,
                auth=auth
            )
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_auth(self):
        auth = ("yo", "mama")
        config = K8sConfig(
            kubeconfig=None,
            auth=auth
        )
        self.assertEqual(auth, config.auth)

    def test_init_invalid_namespace(self):
        namespace = 666
        try:
            K8sConfig(
                kubeconfig=None,
                namespace=namespace
            )
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_namespace(self):
        namespace = "yomama"
        config = K8sConfig(
            kubeconfig=None,
            namespace=namespace
        )
        self.assertEqual(namespace, config.namespace)

    def test_init_invalid_pull_secret(self):
        ps = 666
        try:
            K8sConfig(
                kubeconfig=None,
                pull_secret=ps
            )
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_pull_secret(self):
        ps = "yomama"
        config = K8sConfig(
            kubeconfig=None,
            pull_secret=ps
        )
        self.assertEqual(config.pull_secret, ps)

    def test_init_invalid_token(self):
        token = 666
        try:
            K8sConfig(
                kubeconfig=None,
                token=token
            )
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_token(self):
        token = "yomama"
        config = K8sConfig(
            kubeconfig=None,
            token=token
        )
        self.assertEqual(token, config.token)

    def test_init_invalid_version(self):
        try:
            K8sConfig(
                kubeconfig=None,
                version="yomama"
            )
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_version(self):
        v = "v1"
        config = K8sConfig(
            kubeconfig=None,
            version=v
        )
        self.assertEqual(v, config.version)
