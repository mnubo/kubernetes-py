#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import uuid

from tests import utils
from tests.BaseTest import BaseTest
from kubernetes import K8sNamespace, K8sConfig
from kubernetes.K8sExceptions import *
from kubernetes.models.v1.Namespace import Namespace
from kubernetes.models.v1.NamespaceSpec import NamespaceSpec
from kubernetes.models.v1.NamespaceStatus import NamespaceStatus
from kubernetes.models.v1.ObjectMeta import ObjectMeta


class K8sNamespaceTest(BaseTest):

    def setUp(self):
        utils.cleanup_namespaces()

    def tearDown(self):
        utils.cleanup_namespaces()

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sNamespace()
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
            K8sNamespace(config=config)

    def test_init_with_invalid_name(self):
        name = object()
        with self.assertRaises(SyntaxError):
            utils.create_namespace(name=name)

    def test_init_with_name(self):
        name = "yoname"
        ns = utils.create_namespace(name=name)
        self.assertIsNotNone(ns)
        self.assertIsInstance(ns, K8sNamespace)
        self.assertEqual('Namespace', ns.obj_type)
        self.assertEqual(ns.name, name)
        self.assertIsInstance(ns.config, K8sConfig)

    def test_init_with_name_and_config(self):
        nspace = "default"
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback, namespace=nspace)
        name = "yoname"
        ns = utils.create_namespace(config=config, name=name)
        self.assertIsNotNone(ns)
        self.assertIsInstance(ns, K8sNamespace)
        self.assertEqual(ns.name, name)
        self.assertEqual('Namespace', ns.obj_type)
        self.assertIsInstance(ns.config, K8sConfig)
        self.assertEqual(nspace, ns.config.namespace)

    # --------------------------------------------------------------------------------- struct

    def test_struct_k8s_namespace(self):
        name = "yoname"
        ns = utils.create_namespace(name=name)
        self.assertIsInstance(ns, K8sNamespace)
        self.assertIsInstance(ns.base_url, str)
        self.assertIsInstance(ns.config, K8sConfig)
        self.assertIsInstance(ns.model, Namespace)
        self.assertIsInstance(ns.name, str)
        self.assertIsInstance(ns.obj_type, str)

    def test_struct_namespace(self):
        name = "yoname"
        ns = utils.create_namespace(name=name)
        self.assertIsInstance(ns, K8sNamespace)
        self.assertIsInstance(ns.model, Namespace)
        self.assertIsInstance(ns.model.metadata, ObjectMeta)
        self.assertIsInstance(ns.model.spec, NamespaceSpec)
        self.assertIsInstance(ns.model.status, NamespaceStatus)

    # --------------------------------------------------------------------------------- add annotation

    def test_add_annotation_none_args(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        try:
            ns.add_annotation()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_annotation_invalid_args(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        k = object()
        v = object()
        try:
            ns.add_annotation(k, v)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_annotation(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        k = "yokey"
        v = "yovalue"
        ns.add_annotation(k, v)
        self.assertIn(k, ns.annotations)
        self.assertEqual(v, ns.annotations[k])

    # --------------------------------------------------------------------------------- add label

    def test_add_label_none_args(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        with self.assertRaises(SyntaxError):
            ns.add_label()

    def test_add_label_invalid_args(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        k = object()
        v = object()
        with self.assertRaises(SyntaxError):
            ns.add_label(k, v)

    def test_add_label(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        k = "yokey"
        v = "yovalue"
        ns.add_label(k, v)
        self.assertIn(k, ns.labels)
        self.assertEqual(v, ns.labels[k])

    # --------------------------------------------------------------------------------- get

    def test_get_nonexistent(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        if utils.is_reachable(ns.config):
            with self.assertRaises(NotFoundException):
                ns.get()

    def test_get(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        ns = utils.create_namespace(name=name)
        if utils.is_reachable(ns.config):
            ns.create()
            from_get = ns.get()
            self.assertIsInstance(from_get, K8sNamespace)
            self.assertEqual(ns, from_get)

    # --------------------------------------------------------------------------------- get annotation

    def test_get_annotation_none_arg(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        ann = ns.get_annotation()
        self.assertIsNone(ann)

    def test_get_annotation_invalid_arg(self):
        name = "yonamespace"
        svc = utils.create_namespace(name=name)
        k = object()
        ann = svc.get_annotation(k)
        self.assertIsNone(ann)

    def test_get_annotation_doesnt_exist(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        k = "yokey"
        v = ns.get_annotation(k)
        self.assertIsNone(v)

    def test_get_annotation(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        k = "yokey"
        v_in = "yovalue"
        ns.add_annotation(k, v_in)
        v_out = ns.get_annotation(k)
        self.assertEqual(v_in, v_out)

    # --------------------------------------------------------------------------------- get annotations

    def test_get_annotations_doesnt_exist(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        self.assertEqual({}, ns.annotations)

    def test_get_annotations(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        count = 4
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            ns.add_annotation(k, v)
        self.assertEqual(count, len(ns.annotations))
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            self.assertIn(k, ns.annotations)
            self.assertEqual(v, ns.annotations[k])

    # --------------------------------------------------------------------------------- get label

    def test_get_label_none_arg(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        self.assertIsNone(ns.get_label())

    def test_get_label_invalid_arg(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        k = object()
        self.assertIsNone(ns.get_label(k))

    def test_get_label_doesnt_exist(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        k = "yokey"
        self.assertIsNone(ns.get_label(k))

    def test_get_label(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        k = "yokey"
        v = "yovalue"
        ns.add_label(k, v)
        self.assertEqual(v, ns.get_label(k))

    # --------------------------------------------------------------------------------- get labels

    def test_get_labels(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        labels = {'yokey': 'yovalue'}
        ns.labels = labels
        self.assertEqual(labels, ns.labels)

    # --------------------------------------------------------------------------------- set annotations

    def test_set_annotations_none_arg(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        with self.assertRaises(SyntaxError):
            ns.annotations = None

    def test_set_annotations_invalid_arg(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        labels = object()
        with self.assertRaises(SyntaxError):
            ns.annotations = labels

    def test_set_annotations_str_int(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        labels = {'yokey': 1234}
        ns.annotations = labels
        self.assertEqual(ns.annotations, labels)

    def test_set_annotations(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        anns = {'yokey': 'yovalue'}
        ns.annotations = anns
        self.assertEqual(anns, ns.annotations)

    # --------------------------------------------------------------------------------- set labels

    def test_set_labels_none_arg(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        with self.assertRaises(SyntaxError):
            ns.labels = None

    def test_set_labels_invalid_arg(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        labels = object()
        with self.assertRaises(SyntaxError):
            ns.labels = labels

    def test_set_labels_invalid_dict(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        labels = {'yokey': 1234}
        with self.assertRaises(SyntaxError):
            ns.labels = labels

    def test_set_labels(self):
        name = "yonamespace"
        ns = utils.create_namespace(name=name)
        labels = {'yokey': 'yovalue'}
        ns.labels = labels
        self.assertEqual(labels, ns.labels)

    # --------------------------------------------------------------------------------- api - get by name

    # def test_get_by_name_nonexistent(self):
    #     name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
    #     ns = utils.create_namespace(name=name)
    #     if utils.is_reachable(ns.config):
    #         _list = K8sNamespace.get_by_name(config=ns.config, name=name)
    #         self.assertIsInstance(_list, list)
    #         self.assertEqual(0, len(_list))
    #
    # def test_get_by_name(self):
    #     name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
    #     ns = utils.create_namespace(name=name)
    #     if utils.is_reachable(ns.config):
    #         ns.create()
    #         _list = K8sNamespace.get_by_name(config=ns.config, name=name)
    #         self.assertIsInstance(_list, list)
    #         self.assertEqual(1, len(_list))
    #         from_get = _list[0]
    #         self.assertIsInstance(from_get, K8sNamespace)
    #         self.assertEqual(from_get, ns)

    # --------------------------------------------------------------------------------- api - list

    def test_list_without_create(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        ns = utils.create_namespace(name=name)
        if utils.is_reachable(ns.config):
            _list = ns.list()
            for x in _list:
                self.assertIsInstance(x, K8sNamespace)
            self.assertIsInstance(_list, list)
            self.assertEqual(2, len(_list))

    def test_list(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        ns = utils.create_namespace(name=name)
        if utils.is_reachable(ns.config):
            ns.create()
            _list = ns.list()
            for x in _list:
                self.assertIsInstance(x, K8sNamespace)
            self.assertIsInstance(_list, list)
            self.assertEqual(3, len(_list))
            from_query = _list[2]
            self.assertEqual(name, from_query.name)

    # --------------------------------------------------------------------------------- api - create

    def test_create(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        ns = utils.create_namespace(name=name)
        if utils.is_reachable(ns.config):
            ns.create()
            from_get = ns.get()
            self.assertEqual(ns, from_get)

    def test_create_already_exists(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        ns = utils.create_namespace(name=name)
        if utils.is_reachable(ns.config):
            ns.create()
            with self.assertRaises(AlreadyExistsException):
                ns.create()

    # --------------------------------------------------------------------------------- api - update

    def test_update_nonexistent(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        ns = utils.create_namespace(name=name)
        if utils.is_reachable(ns.config):
            with self.assertRaises(NotFoundException):
                ns.update()

    # --------------------------------------------------------------------------------- api - delete

    def test_delete_nonexistent(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        ns = utils.create_namespace(name=name)
        if utils.is_reachable(ns.config):
            with self.assertRaises(NotFoundException):
                ns.delete()

    def test_delete(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        ns = utils.create_namespace(name=name)
        if utils.is_reachable(ns.config):
            ns.create()
            from_get = K8sNamespace.get_by_name(ns.config, ns.name)
            self.assertIsInstance(from_get, K8sNamespace)
            self.assertEqual(name, from_get.name)
            ns.delete()
            from_get = K8sNamespace.get_by_name(ns.config, ns.name)
            self.assertIsNone(from_get)
