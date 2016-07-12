#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
from kubernetes import K8sConfig

DEFAULT_API_HOST = "localhost:8888"
DEFAULT_API_VERSION = "v1"
DEFAULT_NAMESPACE = "default"


class K8sConfigTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_instantiate_no_args(self):
        config = K8sConfig()
        self.assertEqual(config.api_host, "http://{0}".format(DEFAULT_API_HOST))
        self.assertIsNone(config.auth)
        self.assertEqual(config.namespace, DEFAULT_NAMESPACE)
        self.assertIsNone(config.pull_secret)
        self.assertIsNone(config.token)
        self.assertEqual(config.version, DEFAULT_API_VERSION)

    def test_instantiate_api_host_invalid_hostname(self):
        try:
            K8sConfig(api_host="yo_mama:1234")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_instantiate_api_host_valid_hostname_no_port(self):
        host = "yo-mama.com"
        config = K8sConfig(api_host=host)
        self.assertIn(host, config.api_host)

    def test_instantiate_api_host_invalid_ip_address(self):
        try:
            K8sConfig(api_host="192671.62671283.735.23322:1234")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_instantiate_valid_ip_no_port(self):
        host = "192.168.99.100"
        config = K8sConfig(api_host=host)
        self.assertIn(host, config.api_host)

    def test_instantiate_invalid_auth(self):
        auth = "yomama"
        try:
            K8sConfig(auth=auth)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_instantiate_auth(self):
        auth = ("yo", "mama")
        config = K8sConfig(auth=auth)
        self.assertEqual(auth, config.auth)

    def test_instantiate_invalid_namespace(self):
        namespace = 666
        try:
            K8sConfig(namespace=namespace)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_instantiate_namespace(self):
        namespace = "yomama"
        config = K8sConfig(namespace=namespace)
        self.assertEqual(namespace, config.namespace)

    def test_instantiate_invalid_pull_secret(self):
        ps = 666
        try:
            K8sConfig(pull_secret=ps)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_instantiate_pull_secret(self):
        ps = "yomama"
        config = K8sConfig(pull_secret=ps)
        self.assertEqual(config.pull_secret, ps)

    def test_instantiate_invalid_token(self):
        token = 666
        try:
            K8sConfig(token=token)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_instantiate_token(self):
        token = "yomama"
        config = K8sConfig(token=token)
        self.assertEqual(token, config.token)

    def test_instantiate_invalid_version(self):
        try:
            K8sConfig(version="yomama")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_instantiate_version(self):
        v = "v1"
        config = K8sConfig(version=v)
        self.assertEqual(v, config.version)
