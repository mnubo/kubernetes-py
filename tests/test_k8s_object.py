#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
import json
import socket
import os
from kubernetes import K8sObject, K8sConfig
from kubernetes.K8sExceptions import UnprocessableEntityException, NotFoundException, BadRequestException

kubeconfig_fallback = '{0}/.kube/config'.format(os.path.abspath(os.path.dirname(os.path.realpath(__file__))))


class K8sObjectTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # ------------------------------------------------------------------------------------- utils

    @staticmethod
    def _is_reachable(api_host):
        scheme, host, port = api_host.replace("//", "").split(':')
        try:
            s = socket.create_connection((host, port), timeout=1)
            s.close()
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sObject()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_invalid_config(self):
        config = object()
        try:
            K8sObject(config=config)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_invalid_name(self):
        name = object()
        cfg = K8sConfig(kubeconfig=kubeconfig_fallback)
        try:
            K8sObject(config=cfg, name=name)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_invalid_object_type(self):
        ot = 666
        cfg = K8sConfig(kubeconfig=kubeconfig_fallback)
        try:
            K8sObject(config=cfg, obj_type=ot)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_unknown_object_type(self):
        ot = "yomama"
        cfg = K8sConfig(kubeconfig=kubeconfig_fallback)
        try:
            K8sObject(config=cfg, obj_type=ot)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_object_type_pod(self):
        ot = "Pod"
        name = "yomama"
        cfg = K8sConfig(kubeconfig=kubeconfig_fallback)
        obj = K8sObject(config=cfg, name=name, obj_type=ot)
        self.assertIsInstance(obj, K8sObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    def test_init_object_type_rc(self):
        ot = "ReplicationController"
        name = "yomama"
        cfg = K8sConfig(kubeconfig=kubeconfig_fallback)
        obj = K8sObject(config=cfg, name=name, obj_type=ot)
        self.assertIsInstance(obj, K8sObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    def test_init_object_type_secret(self):
        ot = "Secret"
        name = "yomama"
        cfg = K8sConfig(kubeconfig=kubeconfig_fallback)
        obj = K8sObject(config=cfg, name=name, obj_type=ot)
        self.assertIsInstance(obj, K8sObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    def test_init_object_type_service(self):
        ot = "Service"
        name = "yomama"
        cfg = K8sConfig(kubeconfig=kubeconfig_fallback)
        obj = K8sObject(config=cfg, name=name, obj_type=ot)
        self.assertIsInstance(obj, K8sObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    # ------------------------------------------------------------------------------------- conversions

    def test_object_as_dict(self):
        ot = "Service"
        name = "yomama"
        cfg = K8sConfig(kubeconfig=kubeconfig_fallback)
        obj = K8sObject(config=cfg, name=name, obj_type=ot)
        dico = obj.as_dict()
        self.assertIsInstance(dico, dict)

    def test_object_as_json(self):
        ot = "Service"
        name = "yomama"
        cfg = K8sConfig(kubeconfig=kubeconfig_fallback)
        obj = K8sObject(config=cfg, name=name, obj_type=ot)
        s = obj.as_json()
        self.assertIsInstance(s, str)
        valid = json.loads(s)
        self.assertIsInstance(valid, dict)

    # ------------------------------------------------------------------------------------- set

    def test_object_set_name(self):
        ot = "Pod"
        name1 = "yomama"
        cfg = K8sConfig(kubeconfig=kubeconfig_fallback)
        obj = K8sObject(config=cfg, name=name1, obj_type=ot)
        self.assertEqual(name1, obj.name)
        name2 = "sofat"
        obj.set_name(name2)
        self.assertNotEqual(obj.name, name1)
        self.assertEqual(obj.name, name2)

    # ------------------------------------------------------------------------------------- api - list

    def test_object_pod_list_from_scratch(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "Pod"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            r = obj.list()
            self.assertIsNotNone(r)
            self.assertEqual(0, len(r))

    def test_object_rc_list_from_scratch(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "ReplicationController"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            r = obj.list()
            self.assertIsNotNone(r)
            self.assertEqual(0, len(r))

    def test_object_secret_list_from_scratch(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "Secret"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            r = obj.list()
            self.assertIsNotNone(r)
            self.assertEqual(1, len(r))
            secret = r[0]
            self.assertIsInstance(secret, dict)
            self.assertEqual(3, len(secret))
            for i in ['data', 'metadata', 'type']:
                self.assertIn(i, secret)
            self.assertIsInstance(secret['data'], dict)
            self.assertIsInstance(secret['metadata'], dict)
            self.assertIsInstance(secret['type'], str)

    def test_object_service_list_from_scratch(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "Service"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
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
        name = "yomama"
        cfg = K8sConfig(kubeconfig=kubeconfig_fallback)
        obj = K8sObject(config=cfg, name=name, obj_type=ot)
        obj.name = None
        try:
            obj.get_model()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_object_pod_get_model_doesnt_exist(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "Pod"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            try:
                obj.get_model()
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_object_rc_get_model_doesnt_exist(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "ReplicationController"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            try:
                obj.get_model()
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_object_secret_get_model_doesnt_exist(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "Secret"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            try:
                obj.get_model()
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_object_service_get_model_doesnt_exist(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "Service"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            try:
                obj.get_model()
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    # ------------------------------------------------------------------------------------- api - get with params

    def test_object_get_with_params_none_arg(self):
        ot = "Pod"
        name = "yomama"
        cfg = K8sConfig(kubeconfig=kubeconfig_fallback)
        obj = K8sObject(config=cfg, name=name, obj_type=ot)
        try:
            obj.get_with_params()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_object_get_with_params_invalid_arg(self):
        ot = "Pod"
        name = "yomama"
        cfg = K8sConfig(kubeconfig=kubeconfig_fallback)
        obj = K8sObject(config=cfg, name=name, obj_type=ot)
        data = object()
        try:
            obj.get_with_params(data)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_object_get_with_params_nonexistent(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "Pod"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot)
            data = {'yokey': 'yovalue'}
            r = obj.get_with_params(data)
            self.assertIsNotNone(r)
            self.assertEqual(0, len(r))

    # ------------------------------------------------------------------------------------- api - create

    def test_object_create_name_unset(self):
        ot = "Pod"
        name = "yomama"
        cfg = K8sConfig(kubeconfig=kubeconfig_fallback)
        obj = K8sObject(config=cfg, name=name, obj_type=ot)
        obj.name = None
        try:
            obj.create()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_object_pod_create_unprocessable(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "Pod"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            try:
                obj.create()
            except Exception as err:
                self.assertIsInstance(err, UnprocessableEntityException)

    def test_object_rc_create_unprocessable(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "ReplicationController"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            try:
                obj.create()
            except Exception as err:
                self.assertIsInstance(err, UnprocessableEntityException)

    def test_object_secret_create_unprocessable(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "Secret"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            try:
                obj.create()
            except Exception as err:
                self.assertIsInstance(err, UnprocessableEntityException)

    def test_object_service_create_unprocessable(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "Service"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            try:
                obj.create()
            except Exception as err:
                self.assertIsInstance(err, UnprocessableEntityException)

    # ------------------------------------------------------------------------------------- api - update

    def test_object_update_name_unset(self):
        ot = "Pod"
        name = "yomama"
        cfg = K8sConfig(kubeconfig=kubeconfig_fallback)
        obj = K8sObject(config=cfg, name=name, obj_type=ot)
        obj.name = None
        try:
            obj.update()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_object_pod_update_bad_request(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "Pod"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            try:
                obj.update()
            except Exception as err:
                self.assertIsInstance(err, BadRequestException)

    def test_object_rc_update_bad_request(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "ReplicationController"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            try:
                obj.update()
            except Exception as err:
                self.assertIsInstance(err, BadRequestException)

    def test_object_secret_update_bad_request(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "Secret"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            try:
                obj.update()
            except Exception as err:
                self.assertIsInstance(err, BadRequestException)

    def test_object_service_update_bad_request(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "Service"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            try:
                obj.update()
            except Exception as err:
                self.assertIsInstance(err, BadRequestException)

    # ------------------------------------------------------------------------------------- api - delete

    def test_object_delete_name_unset(self):
        ot = "Pod"
        name = "yomama"
        cfg = K8sConfig(kubeconfig=kubeconfig_fallback)
        obj = K8sObject(config=cfg, name=name, obj_type=ot)
        obj.name = None
        try:
            obj.delete()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_object_pod_delete_not_found(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "Pod"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            try:
                obj.delete()
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_object_rc_delete_not_found(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "ReplicationController"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            try:
                obj.delete()
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_object_secret_delete_not_found(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "Secret"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            try:
                obj.delete()
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_object_service_delete_not_found(self):
        config = K8sConfig(kubeconfig=kubeconfig_fallback)
        if config.api_host is not None and self._is_reachable(config.api_host):
            ot = "Service"
            name = "yomama"
            obj = K8sObject(name=name, obj_type=ot, config=config)
            try:
                obj.delete()
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)
