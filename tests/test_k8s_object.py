#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
import uuid

from kubernetes import K8sObject, K8sConfig
from kubernetes.K8sExceptions import UnprocessableEntityException, NotFoundException
from tests import utils


class K8sObjectTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        utils.cleanup_objects()

    # ------------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sObject()
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
            K8sObject(config=config)

    def test_init_with_invalid_name(self):
        name = object()
        with self.assertRaises(SyntaxError):
            utils.create_object(name)

    def test_init_invalid_object_type(self):
        ot = 666
        with self.assertRaises(SyntaxError):
            utils.create_object(obj_type=ot)

    def test_init_unknown_object_type(self):
        ot = "yomama"
        with self.assertRaises(SyntaxError):
            utils.create_object(obj_type=ot)

    def test_init_object_type_pod(self):
        ot = "Pod"
        name = "yomama-{}".format(str(uuid.uuid4()))
        obj = utils.create_object(name=name, obj_type=ot)
        self.assertIsInstance(obj, K8sObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    def test_init_object_type_rc(self):
        ot = "ReplicationController"
        name = "yomama-{}".format(str(uuid.uuid4()))
        obj = utils.create_object(name=name, obj_type=ot)
        self.assertIsInstance(obj, K8sObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    def test_init_object_type_secret(self):
        ot = "Secret"
        name = "yomama-{}".format(str(uuid.uuid4()))
        obj = utils.create_object(name=name, obj_type=ot)
        self.assertIsInstance(obj, K8sObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    def test_init_object_type_service(self):
        ot = "Service"
        name = "yomama-{}".format(str(uuid.uuid4()))
        obj = utils.create_object(name=name, obj_type=ot)
        self.assertIsInstance(obj, K8sObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    # ------------------------------------------------------------------------------------- set

    def test_object_set_name(self):
        ot = "Pod"
        name1 = "yomama"
        obj = utils.create_object(name=name1, obj_type=ot)
        self.assertEqual(name1, obj.name)
        name2 = "sofat"
        obj.name = name2
        self.assertNotEqual(obj.name, name1)
        self.assertEqual(obj.name, name2)

    # ------------------------------------------------------------------------------------- api - list

    def test_object_pod_list_from_scratch(self):
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        if utils.is_reachable(config.api_host):
            ot = "Pod"
            name = "yomama-{}".format(str(uuid.uuid4()))
            obj = utils.create_object(config=config, name=name, obj_type=ot)
            r = obj.list()
            self.assertIsNotNone(r)
            self.assertEqual(0, len(r))

    def test_object_rc_list_from_scratch(self):
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        if config.api_host is not None and utils.is_reachable(config.api_host):
            ot = "ReplicationController"
            name = "yomama-{}".format(str(uuid.uuid4()))
            obj = utils.create_object(config=config, name=name, obj_type=ot)
            r = obj.list()
            self.assertIsNotNone(r)
            self.assertEqual(0, len(r))

    def test_object_secret_list_from_scratch(self):
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        if config.api_host is not None and utils.is_reachable(config.api_host):
            ot = "Secret"
            name = "yomama-{}".format(str(uuid.uuid4()))
            obj = utils.create_object(config=config, name=name, obj_type=ot)
            r = obj.list()
            self.assertIsNotNone(r)
            self.assertGreaterEqual(1, len(r))  # default-token
            if len(r):
                secret = r[0]
                self.assertIsInstance(secret, dict)
                self.assertEqual(3, len(secret))
                for i in ['data', 'metadata', 'type']:
                    self.assertIn(i, secret)
                self.assertIsInstance(secret['data'], dict)
                self.assertIsInstance(secret['metadata'], dict)
                self.assertIsInstance(secret['type'], str)

    def test_object_service_list_from_scratch(self):
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        if config.api_host is not None and utils.is_reachable(config.api_host):
            ot = "Service"
            name = "yomama-{}".format(str(uuid.uuid4()))
            obj = utils.create_object(config=config, name=name, obj_type=ot)
            r = obj.list()
            self.assertIsNotNone(r)
            self.assertEqual(1, len(r))
            service = r[0]
            self.assertIsInstance(service, dict)
            self.assertEqual(3, len(service))
            for i in ['metadata', 'spec', 'status']:
                self.assertIn(i, service)
                self.assertIsInstance(service[i], dict)
            for i in ['creationTimestamp', 'labels', 'name', 'namespace', 'resourceVersion', 'selfLink', 'uid']:
                self.assertIn(i, service['metadata'])
            for i in ['creationTimestamp', 'name', 'namespace', 'resourceVersion', 'selfLink', 'uid']:
                self.assertIsInstance(service['metadata'][i], str)
            self.assertIsInstance(service['metadata']['labels'], dict)
            self.assertEqual(2, len(service['metadata']['labels']))
            for i in ['component', 'provider']:
                self.assertIn(i, service['metadata']['labels'])
                self.assertIsInstance(service['metadata']['labels'][i], str)
            for i in ['clusterIP', 'ports', 'sessionAffinity', 'type']:
                self.assertIn(i, service['spec'])
            for i in ['clusterIP', 'sessionAffinity', 'type']:
                self.assertIsInstance(service['spec'][i], str)
            self.assertIsInstance(service['spec']['ports'], list)
            self.assertEqual(1, len(service['spec']['ports']))
            port = service['spec']['ports'][0]
            self.assertIsInstance(port, dict)
            self.assertEqual(4, len(port))
            for i in ['name', 'port', 'protocol', 'targetPort']:
                self.assertIn(i, port)
            for i in ['name', 'protocol']:
                self.assertIsInstance(port[i], str)
            for i in ['port', 'targetPort']:
                self.assertIsInstance(port[i], int)

    # ------------------------------------------------------------------------------------- api - get model

    def test_object_get_model_name_unset(self):
        ot = "Pod"
        name = "yomama-{}".format(str(uuid.uuid4()))
        obj = utils.create_object(name=name, obj_type=ot)
        with self.assertRaises(NotFoundException):
            obj.get_model()

    def test_object_pod_get_model_doesnt_exist(self):
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        if config.api_host is not None and utils.is_reachable(config.api_host):
            ot = "Pod"
            name = "yomama-{}".format(str(uuid.uuid4()))
            obj = utils.create_object(config=config, name=name, obj_type=ot)
            with self.assertRaises(NotFoundException):
                obj.get_model()

    def test_object_rc_get_model_doesnt_exist(self):
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        if config.api_host is not None and utils.is_reachable(config.api_host):
            ot = "ReplicationController"
            name = "yomama-{}".format(str(uuid.uuid4()))
            obj = utils.create_object(config=config, name=name, obj_type=ot)
            with self.assertRaises(NotFoundException):
                obj.get_model()

    def test_object_secret_get_model_doesnt_exist(self):
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        if config.api_host is not None and utils.is_reachable(config.api_host):
            ot = "Secret"
            name = "yomama-{}".format(str(uuid.uuid4()))
            obj = utils.create_object(config=config, name=name, obj_type=ot)
            with self.assertRaises(NotFoundException):
                obj.get_model()

    def test_object_service_get_model_doesnt_exist(self):
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        if config.api_host is not None and utils.is_reachable(config.api_host):
            ot = "Service"
            name = "yomama-{}".format(str(uuid.uuid4()))
            obj = utils.create_object(config=config, name=name, obj_type=ot)
            with self.assertRaises(NotFoundException):
                obj.get_model()

    # ------------------------------------------------------------------------------------- api - get with params

    def test_object_get_with_params_none_arg(self):
        ot = "Pod"
        name = "yomama-{}".format(str(uuid.uuid4()))
        obj = utils.create_object(name=name, obj_type=ot)
        try:
            obj.get_with_params()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_object_get_with_params_invalid_arg(self):
        ot = "Pod"
        name = "yomama-{}".format(str(uuid.uuid4()))
        obj = utils.create_object(name=name, obj_type=ot)
        data = object()
        try:
            obj.get_with_params(data)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_object_get_with_params_nonexistent(self):
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        if config.api_host is not None and utils.is_reachable(config.api_host):
            ot = "Pod"
            name = "yomama-{}".format(str(uuid.uuid4()))
            obj = utils.create_object(config=config, name=name, obj_type=ot)
            data = {'yokey': 'yovalue'}
            r = obj.get_with_params(data)
            self.assertIsNotNone(r)
            self.assertEqual(0, len(r))

    # ------------------------------------------------------------------------------------- api - create

    def test_object_pod_create_unprocessable(self):
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        ot = "Pod"
        name = "yomama-{}".format(str(uuid.uuid4()))
        if config.api_host is not None and utils.is_reachable(config.api_host):
            obj = utils.create_object(config=config, name=name, obj_type=ot)
            with self.assertRaises(UnprocessableEntityException):
                obj.create()

    def test_object_rc_create_unprocessable(self):
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        if config.api_host is not None and utils.is_reachable(config.api_host):
            ot = "ReplicationController"
            name = "yomama-{}".format(str(uuid.uuid4()))
            obj = utils.create_object(config=config, name=name, obj_type=ot)
            with self.assertRaises(UnprocessableEntityException):
                obj.create()

    def test_object_secret_create(self):
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        if config.api_host is not None and utils.is_reachable(config.api_host):
            ot = "Secret"
            name = "yomama-{}".format(str(uuid.uuid4()))
            obj = utils.create_object(config=config, name=name, obj_type=ot)
            obj.create()
            self.assertIsInstance(obj, K8sObject)

    def test_object_service_create_unprocessable(self):
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        if config.api_host is not None and utils.is_reachable(config.api_host):
            ot = "Service"
            name = "yomama-{}".format(str(uuid.uuid4()))
            obj = utils.create_object(config=config, name=name, obj_type=ot)
            with self.assertRaises(UnprocessableEntityException):
                obj.create()

    # ------------------------------------------------------------------------------------- api - update

    def test_object_update_not_found(self):
        ot = "Pod"
        name = "yomama-{}".format(str(uuid.uuid4()))
        obj = utils.create_object(name=name, obj_type=ot)
        with self.assertRaises(NotFoundException):
            obj.update()

    def test_object_secret_update(self):
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        ot = "Secret"
        name = "yomama-{}".format(str(uuid.uuid4()))
        obj = utils.create_object(config=config, name=name, obj_type=ot)
        if config.api_host is not None and utils.is_reachable(config.api_host):
            obj.create()
            obj.update()

    # ------------------------------------------------------------------------------------- api - delete

    def test_object_delete_not_found(self):
        ot = "Pod"
        name = "yomama-{}".format(str(uuid.uuid4()))
        obj = utils.create_object(name=name, obj_type=ot)
        with self.assertRaises(NotFoundException):
            obj.delete()

    def test_object_pod_delete_not_found(self):
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        ot = "Pod"
        name = "yomama-{}".format(str(uuid.uuid4()))
        if config.api_host is not None and utils.is_reachable(config.api_host):
            obj = utils.create_object(config=config, name=name, obj_type=ot)
            with self.assertRaises(NotFoundException):
                obj.delete()

    def test_object_rc_delete_not_found(self):
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        if config.api_host is not None and utils.is_reachable(config.api_host):
            ot = "ReplicationController"
            name = "yomama-{}".format(str(uuid.uuid4()))
            obj = utils.create_object(config=config, name=name, obj_type=ot)
            with self.assertRaises(NotFoundException):
                obj.delete()

    def test_object_secret_delete_not_found(self):
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        ot = "Secret"
        name = "yomama-{}".format(str(uuid.uuid4()))
        if config.api_host is not None and utils.is_reachable(config.api_host):
            obj = utils.create_object(config=config, name=name, obj_type=ot)
            with self.assertRaises(NotFoundException):
                obj.delete()

    def test_object_service_delete_not_found(self):
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        ot = "Service"
        name = "yomama-{}".format(str(uuid.uuid4()))
        if config.api_host is not None and utils.is_reachable(config.api_host):
            obj = utils.create_object(config=config, name=name, obj_type=ot)
            with self.assertRaises(NotFoundException):
                obj.delete()
