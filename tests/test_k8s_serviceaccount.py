#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import uuid
import unittest

from kubernetes.K8sConfig import K8sConfig
from kubernetes.K8sSecret import K8sSecret
from kubernetes.K8sServiceAccount import K8sServiceAccount
import utils


class K8sServiceAccountTests(unittest.TestCase):

    def setUp(self):
        utils.cleanup_service_accounts()
        utils.cleanup_secrets()

    def tearDown(self):
        utils.cleanup_service_accounts()
        utils.cleanup_secrets()

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sServiceAccount()
            self.fail("Should not fail.")
        except SyntaxError:
            pass
        except IOError:
            pass
        except Exception as err:
            self.fail("Unhandled exception: [ {0} ]".format(err.__class__.__name__))

    def test_init_with_invalid_config(self):
        config = object()
        with self.assertRaises(SyntaxError):
            K8sServiceAccount(config=config)

    def test_init_with_invalid_name(self):
        name = object()
        with self.assertRaises(SyntaxError):
            utils.create_service_account(name=name)

    def test_init_with_name(self):
        name = "yoname"
        secret = utils.create_service_account(name=name)
        self.assertIsNotNone(secret)
        self.assertIsInstance(secret, K8sServiceAccount)
        self.assertEqual(secret.name, name)
        self.assertEqual('default', secret.config.namespace)
        self.assertEqual('ServiceAccount', secret.obj_type)

    def test_init_with_name_and_config(self):
        name = "yoname"
        nspace = "yomama"
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback, namespace=nspace)
        secret = utils.create_service_account(config=config, name=name)
        self.assertIsNotNone(secret)
        self.assertIsInstance(secret, K8sServiceAccount)
        self.assertEqual(secret.name, name)
        self.assertEqual(secret.config.namespace, nspace)
        self.assertEqual('ServiceAccount', secret.obj_type)

    # --------------------------------------------------------------------------------- api - create

    def test_create(self):
        name = "mnubo.com-sa-{0}".format(str(uuid.uuid4().get_hex()[:4]))
        acct = utils.create_service_account(name=name)
        if utils.is_reachable(acct.config.api_host):
            acct.create()
            from_get = acct.get()
            self.assertEqual(acct, from_get)

    # --------------------------------------------------------------------------------- api - add API token

    def test_add_api_token(self):
        name = "mnubo.com-sa-{0}".format(str(uuid.uuid4().get_hex()[:4]))
        acct = utils.create_service_account(name=name)
        if utils.is_reachable(acct.config.api_host):
            acct.create()
            acct.add_api_token()
            secrets = K8sSecret.api_tokens_for_service_account(config=acct.config, name=acct.name)
            self.assertEqual(2, len(secrets))
