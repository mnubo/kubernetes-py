#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
import json
import base64
from kubernetes import K8sSecret, K8sConfig
from kubernetes.models.v1 import Secret, ObjectMeta


class K8sReplicationControllerTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sSecret()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_invalid_config(self):
        config = object()
        try:
            K8sSecret(config=config)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_name(self):
        name = "yoname"
        secret = K8sSecret(name=name)
        self.assertIsNotNone(secret)
        self.assertIsInstance(secret, K8sSecret)
        self.assertEqual(secret.name, name)
        self.assertEqual('default', secret.config.namespace)
        self.assertEqual('Secret', secret.obj_type)

    def test_init_with_name_and_config(self):
        name = "yoname"
        nspace = "yomama"
        config = K8sConfig(namespace=nspace)
        secret = K8sSecret(config=config, name=name)
        self.assertIsNotNone(secret)
        self.assertIsInstance(secret, K8sSecret)
        self.assertEqual(secret.name, name)
        self.assertEqual(secret.config.namespace, nspace)
        self.assertEqual('Secret', secret.obj_type)

    # --------------------------------------------------------------------------------- struct

    def test_struct_k8s_secret(self):
        name = "yoname"
        secret = K8sSecret(name=name)
        self.assertIsNotNone(secret)
        self.assertIsInstance(secret.base_url, str)
        self.assertIsInstance(secret.config, K8sConfig)
        self.assertIsInstance(secret.model, Secret)
        self.assertIsInstance(secret.name, str)
        self.assertIsInstance(secret.obj_type, str)

    def test_struct_secret(self):
        name = "yoname"
        secret = K8sSecret(name=name)
        model = secret.model
        self.assertIsInstance(model, Secret)
        self.assertIsInstance(model.model, dict)
        self.assertIsInstance(model.secret_metadata, ObjectMeta)

    def test_struct_secret_model(self):
        name = "yoname"
        secret = K8sSecret(name=name)
        model = secret.model.model
        self.assertIsInstance(model, dict)
        self.assertIn('apiVersion', model)
        self.assertIn('kind', model)
        self.assertIn('metadata', model)
        self.assertIsInstance(model['apiVersion'], str)
        self.assertIsInstance(model['kind'], str)
        self.assertIsInstance(model['metadata'], dict)
        self.assertEqual(3, len(model['metadata']))
        self.assertIn('labels', model['metadata'])
        self.assertIn('name', model['metadata'])
        self.assertIn('namespace', model['metadata'])
        self.assertEqual(name, model['metadata']['name'])

    # --------------------------------------------------------------------------------- add annotation

    def test_add_annotation_none_args(self):
        name = "yosecret"
        secret = K8sSecret(name=name)
        try:
            secret.add_annotation()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_annotation_invalid_args(self):
        name = "yosecret"
        secret = K8sSecret(name=name)
        k = object()
        v = object()
        try:
            secret.add_annotation(k, v)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_annotation(self):
        name = "yosecret"
        secret = K8sSecret(name=name)
        k = "yokey"
        v = "yovalue"
        secret.add_annotation(k, v)
        self.assertIn('annotations', secret.model.model['metadata'])
        self.assertIn(k, secret.model.model['metadata']['annotations'])
        self.assertEqual(secret.model.model['metadata']['annotations']['yokey'], v)
        self.assertIn('annotations', secret.model.secret_metadata.model)
        self.assertIn(k, secret.model.secret_metadata.model['annotations'])
        self.assertEqual(secret.model.secret_metadata.model['annotations']['yokey'], v)

    # --------------------------------------------------------------------------------- add label

    def test_add_label_none_args(self):
        name = "yosecret"
        secret = K8sSecret(name=name)
        try:
            secret.add_label()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_label_invalid_args(self):
        name = "yosecret"
        rc = K8sSecret(name=name)
        k = object()
        v = object()
        try:
            rc.add_label(k, v)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_label(self):
        name = "yosecret"
        secret = K8sSecret(name=name)
        k = "yokey"
        v = "yovalue"
        secret.add_label(k, v)
        self.assertIn('labels', secret.model.model['metadata'])
        self.assertIn(k, secret.model.model['metadata']['labels'])
        self.assertEqual(secret.model.model['metadata']['labels']['yokey'], v)
        self.assertIn('labels', secret.model.secret_metadata.model)
        self.assertIn(k, secret.model.secret_metadata.model['labels'])

    # --------------------------------------------------------------------------------- get

    # TODO: requires http call
    def test_get(self):
        # name = "yosecret"
        # secret = K8sSecret(name=name)
        # secret.get()
        pass

    # --------------------------------------------------------------------------------- set data

    def test_set_data_none_args(self):
        name = "yosecret"
        secret = K8sSecret(name=name)
        try:
            secret.set_data()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_data_invalid_key(self):
        name = "yosecret"
        secret = K8sSecret(name=name)
        k = object()
        v = {'key1': 'value1', 'key2': 'value2'}
        try:
            secret.set_data(k, v)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_data_invalid_value(self):
        name = "yosecret"
        secret = K8sSecret(name=name)
        k = "yokey"
        v = {'key1': 'value1', 'key2': 'value2'}
        try:
            secret.set_data(k, v)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_data(self):
        name = "yosecret"
        secret = K8sSecret(name=name)
        k = "yokey"
        v = {'key1': 'value1', 'key2': 'value2'}
        secret.set_data(k, json.dumps(v))
        self.assertIn('data', secret.model.model)
        self.assertIn(k, secret.model.model['data'])
        self.assertEqual(json.dumps(v), base64.b64decode(secret.model.model['data'][k]))

    # --------------------------------------------------------------------------------- set type

    def test_set_type_none_arg(self):
        name = "yosecret"
        secret = K8sSecret(name=name)
        try:
            secret.set_type()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_type_invalid_arg(self):
        name = "yosecret"
        secret = K8sSecret(name=name)
        secret_type = object()
        try:
            secret.set_type(secret_type=secret_type)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_type(self):
        name = "yosecret"
        secret = K8sSecret(name=name)
        secret_type = "yosecrettype"
        secret.set_type(secret_type=secret_type)
        self.assertIn('type', secret.model.model)
        self.assertEqual(secret_type, secret.model.model['type'])

    # --------------------------------------------------------------------------------- set dockercfg secret

    def test_set_dockercfg_secret_none_arg(self):
        name = "yosecret"
        secret = K8sSecret(name=name)
        try:
            secret.set_dockercfg_secret()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_dockercfg_secret_invalid_arg(self):
        name = "yosecret"
        secret = K8sSecret(name=name)
        data = object()
        try:
            secret.set_dockercfg_secret(data)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_dockercfg_secret(self):
        name = "yosecret"
        secret = K8sSecret(name=name)
        data = "yodockercfg"
        secret.set_dockercfg_secret(data)
        self.assertIn('data', secret.model.model)
        self.assertIn('type', secret.model.model)
        self.assertIsInstance(secret.model.model['data'], dict)
        self.assertIsInstance(secret.model.model['type'], str)
        self.assertEqual('kubernetes.io/dockercfg', secret.model.model['type'])
        self.assertIn('.dockercfg', secret.model.model['data'])
        self.assertEqual(data, base64.b64decode(secret.model.model['data']['.dockercfg']))

    # --------------------------------------------------------------------------------- set dockercfg json secret

    def test_set_dockercfg_json_secret_none_arg(self):
        name = "yosecret"
        secret = K8sSecret(name=name)
        try:
            secret.set_dockercfg_json_secret()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_dockercfg_json_secret_invalid_arg(self):
        name = "yosecret"
        secret = K8sSecret(name=name)
        data = object()
        try:
            secret.set_dockercfg_json_secret(data)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_dockercfg_json_secret(self):
        name = "yosecret"
        secret = K8sSecret(name=name)
        data = "yodockercfgjson"
        secret.set_dockercfg_json_secret(data)
        self.assertIn('data', secret.model.model)
        self.assertIn('type', secret.model.model)
        self.assertIsInstance(secret.model.model['data'], dict)
        self.assertIsInstance(secret.model.model['type'], str)
        self.assertEqual('kubernetes.io/dockerconfigjson', secret.model.model['type'])
        self.assertIn('.dockerconfigjson', secret.model.model['data'])
        self.assertEqual(data, base64.b64decode(secret.model.model['data']['.dockerconfigjson']))

    # --------------------------------------------------------------------------------- set service account token

    def test_set_service_account_token_none_args(self):
        name = "yosecret"
        secret = K8sSecret(name=name)
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

        secret = K8sSecret(name=name)
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

        secret = K8sSecret(name=name)
        secret.set_service_account_token(
            account_name=account_name,
            account_uid=account_uid,
            token=token,
            kubecfg_data=kubecfg_data,
            cacert=cacert
        )

        self.assertIn('data', secret.model.model)
        self.assertIn('type', secret.model.model)
        self.assertIsInstance(secret.model.model['data'], dict)
        self.assertIsInstance(secret.model.model['type'], str)
        self.assertEqual('kubernetes.io/service-account-token', secret.model.model['type'])
        self.assertIn('ca.crt', secret.model.model['data'])
        self.assertIn('kubernetes.kubeconfig', secret.model.model['data'])
        self.assertIn('token', secret.model.model['data'])
        self.assertEqual(cacert, base64.b64decode(secret.model.model['data']['ca.crt']))
        self.assertEqual(kubecfg_data, base64.b64decode(secret.model.model['data']['kubernetes.kubeconfig']))
        self.assertEqual(token, base64.b64decode(secret.model.model['data']['token']))
        self.assertIn('annotations', secret.model.model['metadata'])
        self.assertIsInstance(secret.model.secret_metadata.model['annotations'], dict)
        self.assertIn('kubernetes.io/service-account.name', secret.model.model['metadata']['annotations'])
        self.assertIn('kubernetes.io/service-account.uid', secret.model.model['metadata']['annotations'])
        self.assertIn('kubernetes.io/service-account.name', secret.model.secret_metadata.model['annotations'])
        self.assertIn('kubernetes.io/service-account.uid', secret.model.secret_metadata.model['annotations'])
        self.assertEqual(account_name, secret.model.model['metadata']['annotations']['kubernetes.io/service-account.name'])
        self.assertEqual(account_uid, secret.model.model['metadata']['annotations']['kubernetes.io/service-account.uid'])
        self.assertEqual(account_name, secret.model.secret_metadata.model['annotations']['kubernetes.io/service-account.name'])
        self.assertEqual(account_uid, secret.model.secret_metadata.model['annotations']['kubernetes.io/service-account.uid'])
