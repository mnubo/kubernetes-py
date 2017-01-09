#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import json
import unittest
import uuid

from kubernetes import K8sSecret, K8sConfig
from kubernetes.K8sExceptions import *
from kubernetes.models.v1 import Secret
from tests import utils


class K8sSecretTest(unittest.TestCase):

    def setUp(self):
        utils.cleanup_service_accounts()
        utils.cleanup_secrets()

    def tearDown(self):
        utils.cleanup_service_accounts()
        utils.cleanup_secrets()

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sSecret()
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
            K8sSecret(config=config)

    def test_init_with_invalid_name(self):
        name = object()
        with self.assertRaises(SyntaxError):
            utils.create_secret(name=name)

    def test_init_with_name(self):
        name = "yoname"
        secret = utils.create_secret(name=name)
        self.assertIsNotNone(secret)
        self.assertIsInstance(secret, K8sSecret)
        self.assertEqual(secret.name, name)
        self.assertEqual('default', secret.config.namespace)
        self.assertEqual('Secret', secret.obj_type)

    def test_init_with_name_and_config(self):
        name = "yoname"
        nspace = "yomama"
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback, namespace=nspace)
        secret = utils.create_secret(config=config, name=name)
        self.assertIsNotNone(secret)
        self.assertIsInstance(secret, K8sSecret)
        self.assertEqual(secret.name, name)
        self.assertEqual(secret.config.namespace, nspace)
        self.assertEqual('Secret', secret.obj_type)

    # --------------------------------------------------------------------------------- struct

    def test_struct_k8s_secret(self):
        name = "yoname"
        secret = utils.create_secret(name=name)
        self.assertIsNotNone(secret)
        self.assertIsInstance(secret.base_url, str)
        self.assertIsInstance(secret.config, K8sConfig)
        self.assertIsInstance(secret.model, Secret)
        self.assertIsInstance(secret.name, str)
        self.assertIsInstance(secret.obj_type, str)

    def test_struct(self):
        name = "yoname"
        secret = utils.create_secret(name=name)
        model = secret.model
        self.assertIsInstance(model, Secret)

    # --------------------------------------------------------------------------------- add annotation

    def test_add_annotation_none_args(self):
        name = "yosecret"
        secret = utils.create_secret(name=name)
        with self.assertRaises(SyntaxError):
            secret.add_annotation()

    def test_add_annotation_invalid_args(self):
        name = "yosecret"
        secret = utils.create_secret(name=name)
        k = object()
        v = object()
        with self.assertRaises(SyntaxError):
            secret.add_annotation(k, v)

    def test_add_annotation(self):
        name = "yosecret"
        secret = utils.create_secret(name=name)
        k = "yokey"
        v = "yovalue"
        secret.add_annotation(k, v)
        self.assertIn(k, secret.annotations)
        self.assertEqual(v, secret.annotations[k])

    # --------------------------------------------------------------------------------- add label

    def test_add_label_none_args(self):
        name = "yosecret"
        secret = utils.create_secret(name=name)
        with self.assertRaises(SyntaxError):
            secret.add_label()

    def test_add_label_invalid_args(self):
        name = "yosecret"
        secret = utils.create_secret(name=name)
        k = object()
        v = object()
        with self.assertRaises(SyntaxError):
            secret.add_label(k, v)

    def test_add_label(self):
        name = "yosecret"
        secret = utils.create_secret(name=name)
        k = "yokey"
        v = "yovalue"
        secret.add_label(k, v)
        self.assertIn(k, secret.labels)
        self.assertEqual(v, secret.labels[k])

    # --------------------------------------------------------------------------------- get

    def test_get_doesnt_exist(self):
        name = "yosecret"
        secret = utils.create_secret(name=name)
        if utils.is_reachable(secret.config.api_host):
            try:
                secret.get()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_get(self):
        name = "yosecret-{0}".format(str(uuid.uuid4()))
        secret = utils.create_secret(name=name)
        if utils.is_reachable(secret.config.api_host):
            from_create = secret.create()
            self.assertIsInstance(from_create, K8sSecret)
            self.assertEqual(from_create.name, name)
            from_get = secret.get()
            self.assertIsInstance(from_get, K8sSecret)
            self.assertEqual(from_get.name, name)
            self.assertEqual(from_create, from_get)

    # --------------------------------------------------------------------------------- set data

    def test_set_data_none_args(self):
        name = "yosecret"
        secret = utils.create_secret(name=name)
        with self.assertRaises(SyntaxError):
            secret.data = None

    def test_set_data_invalid_key(self):
        name = "yosecret"
        secret = utils.create_secret(name=name)
        k = object()
        v = {'key1': 'value1', 'key2': 'value2'}
        with self.assertRaises(SyntaxError):
            secret.data = {k: v}

    def test_set_data_invalid_value(self):
        name = "yosecret"
        secret = utils.create_secret(name=name)
        k = "yokey"
        v = {'key1': 'value1', 'key2': 'value2'}
        with self.assertRaises(SyntaxError):
            secret.data = {k: v}

    def test_set_data(self):
        name = "yosecret"
        secret = utils.create_secret(name=name)
        k = "yokey"
        v = {'key1': 'value1', 'key2': 'value2'}
        secret.data = {k: json.dumps(v)}
        self.assertIn(k, secret.data)
        self.assertEqual(json.dumps(v), secret.data[k])

    # --------------------------------------------------------------------------------- set type

    def test_set_type_none_arg(self):
        name = "yosecret"
        secret = utils.create_secret(name=name)
        with self.assertRaises(SyntaxError):
            secret.type = None

    def test_set_type_invalid_arg(self):
        name = "yosecret"
        secret = utils.create_secret(name=name)
        secret_type = object()
        with self.assertRaises(SyntaxError):
            secret.type = secret_type

    def test_set_type(self):
        name = "yosecret"
        secret = utils.create_secret(name=name)
        t = "yosecrettype"
        secret.type = t
        self.assertEqual(t, secret.type)

    # --------------------------------------------------------------------------------- set dockercfg json secret

    def test_set_dockercfg_json_secret_none_arg(self):
        name = "yosecret"
        secret = utils.create_secret(name=name)
        with self.assertRaises(SyntaxError):
            secret.dockerconfigjson = None

    def test_set_dockercfg_json_secret_invalid_arg(self):
        name = "yosecret"
        secret = utils.create_secret(name=name)
        data = object()
        with self.assertRaises(SyntaxError):
            secret.dockerconfigjson = data

    # --------------------------------------------------------------------------------- set service account token

    def test_set_service_account_token_none_args(self):
        name = "yosecret"
        secret = utils.create_secret(name=name)
        try:
            secret.set_service_account_token()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_service_account_token_invalid_args(self):
        name = "yosecret"
        account_name = object()
        account_uid = object()
        token = object()
        kubecfg_data = object()
        cacert = object()

        secret = utils.create_secret(name=name)
        try:
            secret.set_service_account_token(
                account_name=account_name,
                account_uid=account_uid,
                token=token,
                kubecfg_data=kubecfg_data,
                cacert=cacert
            )
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_service_account_token(self):
        name = "yosecret"
        account_name = "yoaccountname"
        account_uid = "yoaccountid"
        token = "yotoken"
        kubecfg_data = "yokubecfgdata"
        cacert = "yocacert"

        secret = utils.create_secret(name=name)
        secret.set_service_account_token(
            account_name=account_name,
            account_uid=account_uid,
            token=token,
            kubecfg_data=kubecfg_data,
            cacert=cacert
        )

        self.assertEqual('kubernetes.io/service-account-token', secret.type)

        self.assertIn('ca.crt', secret.data)
        self.assertIn('kubernetes.kubeconfig', secret.data)
        self.assertIn('token', secret.data)

        self.assertEqual(cacert, secret.data['ca.crt'])
        self.assertEqual(kubecfg_data, secret.data['kubernetes.kubeconfig'])
        self.assertEqual(token, secret.data['token'])

        self.assertIn('kubernetes.io/service-account.name', secret.annotations)
        self.assertIn('kubernetes.io/service-account.uid', secret.annotations)
        self.assertIn('kubernetes.io/service-account.name', secret.annotations)
        self.assertIn('kubernetes.io/service-account.uid', secret.annotations)

        self.assertEqual(account_name, secret.annotations['kubernetes.io/service-account.name'])
        self.assertEqual(account_uid, secret.annotations['kubernetes.io/service-account.uid'])
        self.assertEqual(account_name, secret.annotations['kubernetes.io/service-account.name'])
        self.assertEqual(account_uid, secret.annotations['kubernetes.io/service-account.uid'])

    # --------------------------------------------------------------------------------- api - create

    def test_create(self):
        name = "yosecret-{0}".format(str(uuid.uuid4()))
        secret = utils.create_secret(name=name)
        if utils.is_reachable(secret.config.api_host):
            secret.create()
            _list = secret.list()
            self.assertEqual(2, len(_list))  # service-account-token + 1

    def test_create_already_exists(self):
        name = "yosecret-{0}".format(str(uuid.uuid4()))
        secret = utils.create_secret(name=name)
        if utils.is_reachable(secret.config.api_host):
            secret.create()
            try:
                secret.create()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, AlreadyExistsException)

    # --------------------------------------------------------------------------------- api - list

    def test_list_without_create(self):
        name = "yosecret-{0}".format(str(uuid.uuid4()))
        secret = utils.create_secret(name=name)
        if utils.is_reachable(secret.config.api_host):
            _list = secret.list()
            self.assertGreaterEqual(1, len(_list))  # service-account-token on GCE
            secrets = []
            for x in _list:
                s = Secret(x)
                k8s = K8sSecret(config=secret.config, name=x['metadata']['name'])
                k8s.model = s
                secrets.append(k8s)
            # print(secrets)

    def test_list(self):
        count = 10
        config = utils.create_config()
        if utils.is_reachable(config.api_host):
            for i in range(0, count):
                name = "yosecret-{0}".format(str(uuid.uuid4()))
                secret = utils.create_secret(name=name)
                secret.create()
            secret = utils.create_secret(name="yosecret")
            _list = secret.list()
            self.assertGreaterEqual(count + 1, len(_list))  # including service-account-token on GCE

    # --------------------------------------------------------------------------------- api - update

    def test_update_nonexistent(self):
        name = "yosecret-{0}".format(str(uuid.uuid4()))
        secret = utils.create_secret(name=name)
        if utils.is_reachable(secret.config.api_host):
            try:
                secret.update()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_update_data(self):
        name = "yosecret-{0}".format(str(uuid.uuid4()))
        secret = utils.create_secret(name=name)
        k = "yokey"
        v = "yovalue"
        if utils.is_reachable(secret.config.api_host):
            secret.create()
            secret.data = {k: v}
            secret.update()
            from_get = secret.get()
            self.assertEqual('Opaque', from_get.type)
            d = from_get.data[k]
            self.assertEqual(d, v)

    # --------------------------------------------------------------------------------- api - delete

    def test_delete_nonexistent(self):
        name = "yosecret-{0}".format(str(uuid.uuid4()))
        secret = utils.create_secret(name=name)
        if utils.is_reachable(secret.config.api_host):
            try:
                secret.delete()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_delete(self):
        name = "yosecret-{0}".format(str(uuid.uuid4()))
        secret = utils.create_secret(name=name)
        if utils.is_reachable(secret.config.api_host):
            _list = secret.list()
            count_before_create = len(_list)
            secret.create()
            _list = secret.list()
            count_after_create = len(_list)
            self.assertEqual(count_before_create + 1, count_after_create)
            secret.delete()
            _list = secret.list()
            count_final = len(_list)
            self.assertEqual(count_before_create, count_final)

    # --------------------------------------------------------------------------------- api - system

    def test_set_default_dockerconfigjson(self):
        name = "docker-registry"
        secret = utils.create_secret(name=name)
        data = {"auths": {"repo:port": {"auth": "authstring", "email": "you@company.com"}}}
        secret.dockerconfigjson = data
        self.assertEqual('kubernetes.io/.dockerconfigjson', secret.type)
        self.assertIn('.dockerconfigjson', secret.data)
        self.assertEqual(data, secret.dockerconfigjson)
        if utils.is_reachable(secret.config.api_host):
            s = secret.create()
            self.assertIsInstance(s, K8sSecret)

    def test_set_system_dockerconfigjson(self):
        name = "docker-registry"
        config = utils.create_config()
        config.namespace = 'kube-system'
        secret = utils.create_secret(config=config, name=name)
        data = {"auths": {"repo:port": {"auth": "authstring", "email": "you@company.com"}}}
        secret.dockerconfigjson = data
        self.assertEqual('kubernetes.io/.dockerconfigjson', secret.type)
        self.assertIn('.dockerconfigjson', secret.data)
        self.assertEqual(data, secret.dockerconfigjson)
        if utils.is_reachable(secret.config.api_host):
            try:
                secret.delete()
            except NotFoundException:
                pass
            s = secret.create()
            self.assertIsInstance(s, K8sSecret)

    # --------------------------------------------------------------------------------- api - create API token

    def test_create_service_account_api_token(self):
        sa = utils.create_service_account(name='build-robot')
        if utils.is_reachable(sa.config.api_host):
            sa.create()
            secret = K8sSecret.create_service_account_api_token(
                config=sa.config,
                name=sa.name)
            self.assertIsInstance(secret, K8sSecret)
            secrets = K8sSecret.api_tokens_for_service_account(
                config=sa.config,
                name=sa.name)
            self.assertEqual(2, len(secrets))
