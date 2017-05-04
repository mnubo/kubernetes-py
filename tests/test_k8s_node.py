#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import re
import uuid

from kubernetes import K8sNode, K8sConfig
from kubernetes.K8sExceptions import *
from kubernetes.models.v1.Node import Node
from kubernetes.models.v1.NodeSpec import NodeSpec
from kubernetes.models.v1.NodeStatus import NodeStatus
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from tests import _utils
from tests.BaseTest import BaseTest


class K8sNodeTest(BaseTest):
    def setUp(self):
        #_utils.cleanup_nodes()
        _utils.cleanup_deployments()
        _utils.cleanup_rs()
        _utils.cleanup_pods()

    def tearDown(self):
        #_utils.cleanup_nodes()
        _utils.cleanup_deployments()
        _utils.cleanup_rs()
        _utils.cleanup_pods()

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sNode()
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
            K8sNode(config=config)

    def test_init_with_invalid_name(self):
        name = object()
        with self.assertRaises(SyntaxError):
            _utils.create_namespace(name=name)

    def test_init_with_name(self):
        name = "yo-name"
        n = _utils.create_node(name=name)
        self.assertIsNotNone(n)
        self.assertIsInstance(n, K8sNode)
        self.assertEqual('Node', n.obj_type)
        self.assertEqual(n.name, name)
        self.assertIsInstance(n.config, K8sConfig)

    def test_init_with_name_and_config(self):
        nspace = "default"
        config = K8sConfig(kubeconfig=_utils.kubeconfig_fallback, namespace=nspace)
        name = "yo-name"
        n = _utils.create_node(config=config, name=name)
        self.assertIsNotNone(n)
        self.assertIsInstance(n, K8sNode)
        self.assertEqual(n.name, name)
        self.assertEqual('Node', n.obj_type)
        self.assertIsInstance(n.config, K8sConfig)

    # --------------------------------------------------------------------------------- struct

    def test_struct_k8s_node(self):
        name = "yo-name"
        n = _utils.create_node(name=name)
        self.assertIsInstance(n, K8sNode)
        self.assertIsInstance(n.base_url, str)
        self.assertIsInstance(n.config, K8sConfig)
        self.assertIsInstance(n.model, Node)
        self.assertIsInstance(n.name, str)
        self.assertIsInstance(n.obj_type, str)

    def test_struct_node(self):
        name = "yo-name"
        n = _utils.create_node(name=name)
        self.assertIsInstance(n, K8sNode)
        self.assertIsInstance(n.model, Node)
        self.assertIsInstance(n.model.metadata, ObjectMeta)
        self.assertIsInstance(n.model.spec, NodeSpec)
        self.assertIsInstance(n.model.status, NodeStatus)

    # --------------------------------------------------------------------------------- add annotation

    def test_add_annotation_none_args(self):
        name = "yo-node"
        n = _utils.create_node(name=name)
        try:
            n.add_annotation()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_annotation_invalid_args(self):
        name = "yo-node"
        n = _utils.create_node(name=name)
        k = object()
        v = object()
        try:
            n.add_annotation(k, v)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_annotation(self):
        name = "yo-node"
        n = _utils.create_node(name=name)
        k = "yokey"
        v = "yovalue"
        n.add_annotation(k, v)
        self.assertIn(k, n.annotations)
        self.assertEqual(v, n.annotations[k])

    # --------------------------------------------------------------------------------- add label

    def test_add_label_none_args(self):
        name = "yo-node"
        n = _utils.create_node(name=name)
        with self.assertRaises(SyntaxError):
            n.add_label()

    def test_add_label_invalid_args(self):
        name = "yo-node"
        n = _utils.create_node(name=name)
        k = object()
        v = object()
        with self.assertRaises(SyntaxError):
            n.add_label(k, v)

    def test_add_label(self):
        name = "yo-node"
        n = _utils.create_node(name=name)
        k = "yokey"
        v = "yovalue"
        n.add_label(k, v)
        self.assertIn(k, n.labels)
        self.assertEqual(v, n.labels[k])

    # --------------------------------------------------------------------------------- get

    def test_get_nonexistent(self):
        name = "yo-node"
        n = _utils.create_node(name=name)
        if _utils.is_reachable(n.config):
            with self.assertRaises(NotFoundException):
                n.get()

    def test_get(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        n = _utils.create_node(name=name)
        if _utils.is_reachable(n.config):
            n.create()
            from_get = n.get()
            self.assertIsInstance(from_get, K8sNode)
            self.assertEqual(n, from_get)

    # --------------------------------------------------------------------------------- api - list

    def test_list_without_create(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        nodes = _utils.create_node(name=name)
        if _utils.is_reachable(nodes.config):
            _list = nodes.list()
            for x in _list:
                self.assertIsInstance(x, K8sNode)
            node_pattern = re.compile("yo\-")
            _filtered = list(filter(lambda x: node_pattern.match(x.name) is not None, _list))
            self.assertIsInstance(_filtered, list)
            self.assertLessEqual(0, len(_filtered))  # there might be a few nodes already (see setUp/tearDown)

    def test_list(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        node = _utils.create_node(name=name)

        if _utils.is_reachable(node.config):
            node_pattern = re.compile(r'yo-')
            _pre_list = node.list()
            for x in _pre_list:
                self.assertIsInstance(x, K8sNode)
            _filtered = list(filter(lambda x: node_pattern.match(x.name) is not None, _pre_list))
            pre_create_length = len(_filtered)

            node.create()
            _post_list = node.list()
            for x in _post_list:
                self.assertIsInstance(x, K8sNode)
            _filtered = list(filter(lambda x: node_pattern.match(x.name) is not None, _post_list))
            post_create_length = len(_filtered)
            self.assertIsInstance(_filtered, list)
            self.assertEqual(1 + pre_create_length, post_create_length)

            from_query = list(filter(lambda x: x.name == name, _filtered))
            self.assertIsInstance(from_query, list)
            self.assertEqual(len(from_query), 1)

    # --------------------------------------------------------------------------------- api - create

    def test_create(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        node = _utils.create_node(name=name)
        if _utils.is_reachable(node.config):
            node.create()
            from_get = node.get()
            self.assertEqual(node, from_get)

    def test_create_already_exists(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        node = _utils.create_node(name=name)
        if _utils.is_reachable(node.config):
            node.create()
            with self.assertRaises(AlreadyExistsException):
                node.create()

    # --------------------------------------------------------------------------------- api - update

    def test_update_nonexistent(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        node = _utils.create_node(name=name)
        if _utils.is_reachable(node.config):
            with self.assertRaises(NotFoundException):
                node.update()

    # --------------------------------------------------------------------------------- api - delete

    def test_delete_nonexistent(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        node = _utils.create_node(name=name)
        if _utils.is_reachable(node.config):
            with self.assertRaises(NotFoundException):
                node.delete()

    def test_delete(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        node = _utils.create_node(name=name)
        if _utils.is_reachable(node.config):
            node.create()
            from_get = K8sNode.get_by_name(node.config, node.name)
            self.assertIsInstance(from_get, K8sNode)
            self.assertEqual(from_get.name, name)
            node.delete()
            from_get = K8sNode.get_by_name(node.config, node.name)
            self.assertIsNone(from_get)

    # --------------------------------------------------------------------------------- api - nodeSelector

    def test_node_selectors(self):
        node = _utils.create_node(name="yo")

        c_nginx = _utils.create_container("yo-nginx", "nginx:latest")
        c_pg = _utils.create_container("yo-pg", "postgres:alpine")
        c_redis = _utils.create_container("yo-redis", "redis:latest")

        d_nginx = _utils.create_deployment(name="yo-nginx")
        d_nginx.desired_replicas = 1
        d_nginx.add_container(c_nginx)

        d_pg = _utils.create_deployment(name="yo-pg")
        d_pg.desired_replicas = 1
        d_pg.add_container(c_pg)

        d_redis = _utils.create_deployment(name="yo-redis")
        d_redis.desired_replicas = 1
        d_redis.add_container(c_redis)

        if _utils.is_reachable(node.config):
            nodes = node.list()

            for i in range(len(nodes)):
                node = nodes[i]
                labels = node.labels
                labels.update({'mnubo.com/selector': str(i)})
                node.labels = labels
                node.update()

            d_nginx.node_selector = {"mnubo.com/selector": "0"}
            d_pg.node_selector = {"mnubo.com/selector": "1"}
            d_redis.node_selector = {"mnubo.com/selector": "2"}

            d_nginx.create()
            d_pg.create()
            d_redis.create()

            self.assertEqual(d_nginx.node_selector, {"mnubo.com/selector": "0"})
            self.assertEqual(d_pg.node_selector, {"mnubo.com/selector": "1"})
            self.assertEqual(d_redis.node_selector, {"mnubo.com/selector": "2"})

            pass  # set breakpoint; play around with killing pods

    # --------------------------------------------------------------------------------- api - drain

    def test_drain_vanilla(self):
        cfg = _utils.create_config()

        if _utils.is_reachable(cfg):
            nodes = K8sNode(config=cfg, name="yo").list()

            for node in nodes:
                with self.assertRaises(DrainNodeException):
                    node.drain()
                    self.assertEqual(True, node.unschedulable)

    def test_drain_ignore_daemonsets(self):
        cfg = _utils.create_config()

        if _utils.is_reachable(cfg):
            nodes = K8sNode(config=cfg, name="yo").list()

            for node in nodes:
                node.drain(ignore_daemonsets=True)
                self.assertTrue(node.unschedulable)
                node.uncordon()
                self.assertFalse(node.unschedulable)
