#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import uuid

from kubernetes import K8sReplicationController, K8sConfig, K8sPod, K8sContainer
from kubernetes.K8sExceptions import *
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1.Probe import Probe
from kubernetes.models.v1.ReplicationController import ReplicationController
from kubernetes.models.v1.ReplicationControllerSpec import ReplicationControllerSpec
from kubernetes.models.v1.ReplicationControllerStatus import ReplicationControllerStatus
from tests import _utils
from tests import _constants
from tests.BaseTest import BaseTest


class K8sReplicationControllerTest(BaseTest):

    def setUp(self):
        _utils.cleanup_nodes()
        _utils.cleanup_rc()
        _utils.cleanup_pods()
        K8sReplicationController.SCALE_WAIT_TIMEOUT_SECONDS = 30
        pass

    def tearDown(self):
        _utils.cleanup_nodes()
        _utils.cleanup_rc()
        _utils.cleanup_pods()
        pass

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sReplicationController()
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
            K8sReplicationController(config=config)

    def test_init_with_invalid_name(self):
        name = object()
        with self.assertRaises(SyntaxError):
            _utils.create_rc(name=name)

    def test_init_with_name(self):
        name = "yomama"
        rc = _utils.create_rc(name=name)
        self.assertIsNotNone(rc)
        self.assertIsInstance(rc, K8sReplicationController)
        self.assertEqual(rc.name, name)

    def test_init_with_config_and_pull_secrets(self):
        ps = [{'name': 'yomama'}]
        name = "sofat"
        config = K8sConfig(pull_secret=ps, kubeconfig=_utils.kubeconfig_fallback)
        rc = _utils.create_rc(config=config, name=name)
        self.assertIsNotNone(rc.config)
        self.assertEqual(ps, rc.config.pull_secret)

    # --------------------------------------------------------------------------------- struct

    def test_struct_k8s_rc(self):
        name = "yomama"
        rc = _utils.create_rc(name=name)
        self.assertIsNotNone(rc)
        self.assertIsInstance(rc, K8sReplicationController)
        self.assertIsNotNone(rc.model)
        self.assertIsInstance(rc.model, ReplicationController)

    def test_struct_rc(self):
        name = "yomama"
        rc = _utils.create_rc(name=name)
        self.assertIsInstance(rc.model, ReplicationController)
        self.assertIsInstance(rc.model.metadata, ObjectMeta)
        self.assertIsInstance(rc.model.spec, ReplicationControllerSpec)
        self.assertIsInstance(rc.model.status, ReplicationControllerStatus)

    # --------------------------------------------------------------------------------- add annotation

    def test_add_annotation_none_args(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        with self.assertRaises(SyntaxError):
            rc.add_annotation()

    def test_add_annotation_invalid_args(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = object()
        v = object()
        with self.assertRaises(SyntaxError):
            rc.add_annotation(k, v)

    def test_add_annotation(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        v = "yovalue"
        rc.add_annotation(k, v)
        self.assertIn(k, rc.annotations)
        self.assertEqual(v, rc.annotations[k])

    # --------------------------------------------------------------------------------- add container

    def test_rc_add_container_invalid(self):
        name = "yorc"
        obj = _utils.create_rc(name=name)
        c = object()
        with self.assertRaises(SyntaxError):
            obj.add_container(c)

    def test_rc_add_container(self):
        name = "yoname"
        rc = _utils.create_rc(name=name)
        self.assertEqual(0, len(rc.containers))
        name = "redis"
        image = "redis:latest"
        c = K8sContainer(name=name, image=image)
        rc.add_container(c)
        self.assertEqual(1, len(rc.containers))
        self.assertIn(c, rc.containers)

    # --------------------------------------------------------------------------------- add label

    def test_add_label_none_args(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        with self.assertRaises(SyntaxError):
            rc.add_label()

    def test_add_label_invalid_args(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = object()
        v = object()
        with self.assertRaises(SyntaxError):
            rc.add_label(k, v)

    def test_add_label(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        v = "yovalue"
        rc.add_label(k, v)
        self.assertIn(k, rc.labels)
        self.assertEqual(v, rc.labels[k])

    # --------------------------------------------------------------------------------- add pod annotation

    def test_add_pod_annotation_none_args(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        with self.assertRaises(SyntaxError):
            rc.add_pod_annotation()

    def test_add_pod_annotation_invalid_args(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = object()
        v = object()
        with self.assertRaises(SyntaxError):
            rc.add_pod_annotation(k, v)

    def test_add_pod_annotation(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        v = "yovalue"
        rc.add_pod_annotation(k, v)
        self.assertIn(k, rc.pod_annotations)
        self.assertEqual(v, rc.pod_annotations[k])

    # --------------------------------------------------------------------------------- add pod label

    def test_add_pod_label_none_args(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        with self.assertRaises(SyntaxError):
            rc.add_pod_label()

    def test_add_pod_label_invalid_args(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = object()
        v = object()
        with self.assertRaises(SyntaxError):
            rc.add_pod_label(k, v)

    def test_add_pod_label(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        v = "yovalue"
        rc.add_pod_label(k, v)
        self.assertIn(k, rc.pod_labels)
        self.assertEqual(v, rc.pod_labels[k])

    # --------------------------------------------------------------------------------- add pull secret

    def test_rc_add_image_pull_secrets_none_arg(self):
        name = "yorc"
        obj = _utils.create_rc(name=name)
        secretname = None
        with self.assertRaises(SyntaxError):
            obj.add_image_pull_secrets(secretname)

    def test_rc_add_image_pull_secrets_invalid_arg(self):
        name = "yorc"
        obj = _utils.create_rc(name=name)
        secrets = 666
        with self.assertRaises(SyntaxError):
            obj.add_image_pull_secrets(secrets)

    def test_rc_add_image_pull_secrets(self):
        config = _utils.create_config()
        config.pull_secret = [
            {'name': 'secret-name'},
            {'name': 'other-secret-name'},
            {'name': 'secret-name'}  # duplicate
        ]
        rc = _utils.create_rc(config=config, name="yo")
        self.assertEqual(2, len(rc.image_pull_secrets))  # duplicate not present

    # --------------------------------------------------------------------------------- del annotation

    def test_del_annotation_doesnt_exist(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        self.assertNotIn(k, rc.annotations)
        rc.del_annotation(k)
        self.assertNotIn(k, rc.annotations)

    def test_del_annotation(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        v = "yovalue"
        rc.add_annotation(k, v)
        self.assertIn(k, rc.annotations)
        rc.del_annotation(k)
        self.assertNotIn(k, rc.annotations)

    # --------------------------------------------------------------------------------- del label

    def test_del_label_doesnt_exist(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        self.assertNotIn(k, rc.labels)
        rc.del_label(k)
        self.assertNotIn(k, rc.labels)

    def test_del_label(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        v = "yovalue"
        rc.add_label(k, v)
        self.assertIn(k, rc.labels)
        rc.del_label(k)
        self.assertNotIn(k, rc.labels)

    # --------------------------------------------------------------------------------- del pod annotation

    def test_del_pod_annotation_doesnt_exist(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        self.assertNotIn(k, rc.pod_annotations)
        rc.del_pod_annotation(k)
        self.assertNotIn(k, rc.pod_annotations)

    def test_del_pod_annotation(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        v = "yovalue"
        rc.add_pod_annotation(k, v)
        self.assertIn(k, rc.pod_annotations)
        rc.del_pod_annotation(k)
        self.assertNotIn(k, rc.annotations)

    # --------------------------------------------------------------------------------- del pod label

    def test_del_pod_label_doesnt_exist(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        self.assertNotIn(k, rc.pod_labels)
        rc.del_pod_label(k)

    def test_del_pod_label(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        v = "yovalue"
        rc.add_pod_label(k, v)
        self.assertIn(k, rc.pod_labels)
        rc.del_pod_label(k)
        self.assertNotIn(k, rc.pod_labels)

    # --------------------------------------------------------------------------------- del pod node name

    def test_rc_del_pod_node_name(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        nodename = "yonodename"
        rc.pod_node_name = nodename
        self.assertEqual(nodename, rc.pod_node_name)
        rc.del_pod_node_name()
        self.assertNotEqual(nodename, rc.pod_node_name)
        self.assertIsNone(rc.pod_node_name)

    # --------------------------------------------------------------------------------- get

    def test_get_nonexistent(self):
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        if _utils.is_reachable(rc.config):
            try:
                rc.get()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_get(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        rc.add_container(container)
        if _utils.is_reachable(rc.config):
            from_create = rc.create()
            from_get = rc.get()
            self.assertIsInstance(from_create, K8sReplicationController)
            self.assertIsInstance(from_get, K8sReplicationController)
            self.assertEqual(from_create, from_get)

    # --------------------------------------------------------------------------------- get annotation

    def test_get_annotation_doesnt_exist(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        ann = rc.get_annotation(k)
        self.assertIsNone(ann)

    def test_get_annotation(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        v_in = "yovalue"
        rc.add_annotation(k, v_in)
        v_out = rc.get_annotation(k)
        self.assertEqual(v_in, v_out)

    # --------------------------------------------------------------------------------- get annotations

    def test_get_annotations_none(self):
        name = "yorc-{}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        self.assertEqual({}, rc.annotations)

    def test_get_annotations(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        count = 4
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            rc.add_annotation(k, v)
        self.assertEqual(count, len(rc.annotations))
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            self.assertIn(k, rc.annotations)
            self.assertEqual(v, rc.annotations[k])

    # --------------------------------------------------------------------------------- get label

    def test_get_label_doesnt_exist(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        label = rc.get_label(k)
        self.assertIsNone(label)

    def test_get_label(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        v_in = "yovalue"
        rc.add_label(k, v_in)
        v_out = rc.get_label(k)
        self.assertEqual(v_in, v_out)

    # --------------------------------------------------------------------------------- get labels

    def test_get_labels_none(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        self.assertIsNotNone(rc.labels)  # 'name' is already a label
        self.assertIn('name', rc.labels)
        self.assertEqual(name, rc.labels['name'])

    def test_get_labels(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        count = 4
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            rc.add_label(k, v)
        self.assertLessEqual(count, len(rc.labels))  # 'name' is already a label
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            self.assertIn(k, rc.labels)
            self.assertEqual(v, rc.labels[k])

    # --------------------------------------------------------------------------------- get pod annotation

    def test_get_pod_annotation_doesnt_exist(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        self.assertNotIn(k, rc.pod_annotations)
        self.assertIsNone(rc.get_pod_annotation(k))

    def test_get_pod_annotation(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        v = "yovalue"
        self.assertNotIn(k, rc.pod_annotations)
        rc.add_pod_annotation(k, v)
        self.assertIn(k, rc.pod_annotations)
        self.assertEqual(v, rc.get_pod_annotation(k))

    # --------------------------------------------------------------------------------- get pod annotations

    def test_get_pod_annotations_none(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        self.assertEqual({}, rc.pod_annotations)

    def test_get_pod_annotations(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        count = 4
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            rc.add_pod_annotation(k, v)
        self.assertEqual(count, len(rc.pod_annotations))
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            self.assertIn(k, rc.pod_annotations)
            self.assertEqual(v, rc.pod_annotations[k])

    # --------------------------------------------------------------------------------- get pod label

    def test_get_pod_label_doesnt_exist(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        self.assertNotIn(k, rc.pod_labels)
        label = rc.get_pod_label(k)
        self.assertIsNone(label)

    def test_get_pod_label(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        k = "yokey"
        v = "yovalue"
        rc.add_pod_label(k, v)
        self.assertIn(k, rc.pod_labels)
        self.assertEqual(v, rc.get_pod_label(k))

    # --------------------------------------------------------------------------------- get pod labels

    def test_get_pod_labels_none(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        self.assertIsNotNone(rc.pod_labels)  # 'name' and 'rc_version' are already labels
        self.assertIn('name', rc.pod_labels)
        self.assertIn('rc_version', rc.pod_labels)
        self.assertEqual(name, rc.pod_labels['name'])

    def test_get_pod_labels(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        count = 4
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            rc.add_pod_label(k, v)
        self.assertLessEqual(count, len(rc.pod_labels))  # 'name' and 'rc_version' are already labels
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            self.assertIn(k, rc.pod_labels)
            self.assertEqual(v, rc.pod_labels[k])

    # --------------------------------------------------------------------------------- get pod node name

    def test_rc_get_pod_node_name_none(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        self.assertIsNone(rc.pod_node_name)

    def test_rc_get_pod_node_name(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        nodename = "yonodename"
        rc.pod_node_name = nodename
        self.assertEqual(nodename, rc.pod_node_name)

    # --------------------------------------------------------------------------------- get pod node selector

    def test_rc_get_node_selector_none(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        self.assertEqual({}, rc.node_selector)

    def test_rc_get_pod_node_selector(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        s = {"disktype": "ssd"}
        rc.node_selector = s
        self.assertEqual(s, rc.node_selector)

    # --------------------------------------------------------------------------------- get replicas

    def test_get_replicas_none(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        self.assertEqual(0, rc.desired_replicas)

    def test_get_replicas(self):
        name = "yorc"
        count = 10
        rc = _utils.create_rc(name=name, replicas=count)
        self.assertEqual(count, rc.desired_replicas)

    # --------------------------------------------------------------------------------- get dns policy

    def test_get_dns_policy_default(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        self.assertEqual('Default', rc.dns_policy)

    def test_get_dns_policy(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        rc.dns_policy = 'ClusterFirst'
        self.assertEqual('ClusterFirst', rc.dns_policy)

    # --------------------------------------------------------------------------------- get pod restart policy

    def test_rc_get_pod_restart_policy_none(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        rp = rc.restart_policy
        self.assertEqual('Always', rp)  # set to 'Always' by default

    def test_rc_get_pod_restart_policy(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        p = 'OnFailure'
        rc.restart_policy = p
        self.assertEqual(p, rc.restart_policy)

    # --------------------------------------------------------------------------------- get selector

    def test_get_selector(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        self.assertIsNotNone(rc.selector)
        self.assertIsInstance(rc.selector, dict)
        self.assertEqual(2, len(rc.selector))
        self.assertIn('name', rc.selector)
        self.assertIn('rc_version', rc.selector)
        self.assertEqual(name, rc.selector['name'])

    # --------------------------------------------------------------------------------- get service account

    def test_rc_get_service_account_none(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        self.assertIsNone(rc.service_account_name)

    def test_rc_get_service_account(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        acct = "yoservice"
        rc.service_account_name = acct
        self.assertEqual(acct, rc.service_account_name)

    # --------------------------------------------------------------------------------- set active deadline

    def test_rc_set_active_deadline_none_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        d = None
        with self.assertRaises(SyntaxError):
            rc.active_deadline = d

    def test_rc_set_active_deadline_invalid_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        d = "yodeadline"
        with self.assertRaises(SyntaxError):
            rc.active_deadline = d

    def test_rc_set_active_deadline(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        d = 600
        rc.active_deadline = d
        self.assertEqual(d, rc.active_deadline)

    # --------------------------------------------------------------------------------- set annotations

    def test_set_annotations_none_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        with self.assertRaises(SyntaxError):
            rc.annotations = None

    def test_set_annotations_invalid_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        anns = object()
        with self.assertRaises(SyntaxError):
            rc.annotations = anns

    def test_set_annotations(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        anns_in = {'k1': 'v1', 'k2': 'v2'}
        rc.annotations = anns_in
        anns_out = rc.annotations
        self.assertEqual(anns_in, anns_out)

    # --------------------------------------------------------------------------------- set labels

    def test_set_labels_none_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        with self.assertRaises(SyntaxError):
            rc.labels = None

    def test_set_labels_invalid_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        labels = object()
        with self.assertRaises(SyntaxError):
            rc.labels = labels

    def test_set_labels(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        labels = {'k1': 'v1', 'k2': 'v2'}
        rc.labels = labels
        self.assertEqual(labels, rc.labels)

    # --------------------------------------------------------------------------------- set namespace

    def test_set_namespace_none_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        with self.assertRaises(SyntaxError):
            rc.namespace = None

    def test_set_namespace_invalid_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        nspace = object()
        with self.assertRaises(SyntaxError):
            rc.namespace = nspace

    def test_set_namespace(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        nspace = "yonamespace"
        rc.namespace = nspace
        self.assertEqual(nspace, rc.namespace)

    # --------------------------------------------------------------------------------- set pod annotations

    def test_set_pod_annotations_none_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        with self.assertRaises(SyntaxError):
            rc.pod_annotations = None

    def test_set_pod_annotations_invalid_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        anns = object()
        with self.assertRaises(SyntaxError):
            rc.pod_annotations = anns

    def test_set_pod_annotations(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        anns = {'k1': 'v1', 'k2': 'v2'}
        rc.pod_annotations = anns
        self.assertEqual(anns, rc.pod_annotations)

    # --------------------------------------------------------------------------------- set pod node name

    def test_rc_set_pod_node_name_none_arg(self):
        name = "yorc"
        obj = _utils.create_rc(name=name)
        nodename = None
        with self.assertRaises(SyntaxError):
            obj.pod_node_name = nodename

    def test_rc_set_pod_node_name_invalid_arg(self):
        name = "yorc"
        obj = _utils.create_rc(name=name)
        nodename = 666
        with self.assertRaises(SyntaxError):
            obj.pod_node_name = nodename

    def test_rc_set_pod_node_name(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        nodename = "yonodename"
        rc.pod_node_name = nodename
        self.assertEqual(rc.pod_node_name, nodename)

    # --------------------------------------------------------------------------------- set pod node selector

    def test_rc_set_node_selector_none_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        s = None
        with self.assertRaises(SyntaxError):
            rc.node_selector = s

    def test_rc_set_node_selector_invalid_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        s = "yoselector"
        with self.assertRaises(SyntaxError):
            rc.node_selector = s

    def test_rc_set_node_selector(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        s = {"disktype": "ssd"}
        rc.node_selector = s
        self.assertEqual(s, rc.node_selector)

    # --------------------------------------------------------------------------------- set labels

    def test_set_pod_labels_none_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        with self.assertRaises(SyntaxError):
            rc.pod_labels = None

    def test_set_pod_labels_invalid_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        labels = object()
        with self.assertRaises(SyntaxError):
            rc.pod_labels = labels

    def test_set_pod_labels(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        labels = {'k1': 'v1', 'k2': 'v2'}
        rc.pod_labels = labels
        self.assertEqual(labels, rc.pod_labels)

    # --------------------------------------------------------------------------------- set pod restart policy

    def test_rc_set_pod_restart_policy_none_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        with self.assertRaises(SyntaxError):
            rc.restart_policy = None

    def test_rc_set_pod_restart_policy_not_a_string(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        p = 666
        with self.assertRaises(SyntaxError):
            rc.restart_policy = p

    def test_rc_set_pod_restart_policy_invalid_arg(self):
        name = "yorc"
        obj = _utils.create_rc(name=name)
        p = 'yopolicy'
        with self.assertRaises(SyntaxError):
            obj.restart_policy = p

    def test_rc_set_pod_restart_policy(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        p = 'Always'
        rc.restart_policy = p
        self.assertEqual(p, rc.restart_policy)

    # --------------------------------------------------------------------------------- set pod service account

    def test_rc_set_service_account_none_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        with self.assertRaises(SyntaxError):
            rc.service_account_name = None

    def test_rc_set_service_account_invalid_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        acct = 666
        with self.assertRaises(SyntaxError):
            rc.service_account_name = acct

    def test_rc_set_service_account(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        acct = "yoservice"
        rc.service_account_name = acct
        self.assertEqual(acct, rc.service_account_name)

    # --------------------------------------------------------------------------------- set replicas

    def test_set_replicas_none_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        with self.assertRaises(SyntaxError):
            rc.desired_replicas = None

    def test_set_replicas_invalid_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        count = -99
        with self.assertRaises(SyntaxError):
            rc.desired_replicas = count

    def test_set_replicas(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        count = 10
        before = rc.desired_replicas
        self.assertNotEqual(before, count)
        rc.desired_replicas = count
        after = rc.desired_replicas
        self.assertEqual(count, after)
        self.assertNotEqual(before, after)

    # --------------------------------------------------------------------------------- set selector

    def test_set_selector_none_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        with self.assertRaises(SyntaxError):
            rc.selector = None

    def test_set_selector_invalid_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        sel = object()
        with self.assertRaises(SyntaxError):
            rc.selector = sel

    def test_set_selector(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        sel = {'k1': 'v1', 'k2': 'v2'}
        rc.selector = sel
        self.assertEqual(sel, rc.selector)

    # --------------------------------------------------------------------------------- set termination grace period

    def test_rc_set_termination_grace_period_none_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        with self.assertRaises(SyntaxError):
            rc.termination_grace_period = None

    def test_rc_set_termination_grace_period_invalid_arg(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        secs = -666
        with self.assertRaises(SyntaxError):
            rc.termination_grace_period = secs

    def test_rc_set_termination_grace_period(self):
        name = "yorc"
        rc = _utils.create_rc(name=name)
        secs = 1234
        rc.termination_grace_period = secs
        self.assertEqual(secs, rc.termination_grace_period)

    # -------------------------------------------------------------------------------------  wait for replicas

    def test_wait_for_replicas(self):
        cont_name = "yocontainer"
        container = _utils.create_container(name=cont_name)
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        rc.add_container(container)
        if _utils.is_reachable(rc.config):
            rc.create()
            rc.desired_replicas = 2
            rc.update()
            rc._wait_for_desired_replicas()
            from_get = rc.get()
            self.assertEqual(rc.desired_replicas, from_get.desired_replicas)
            self.assertEqual(rc.current_replicas, from_get.current_replicas)
            self.assertEqual(rc.desired_replicas, from_get.current_replicas)

    # -------------------------------------------------------------------------------------  get by name

    def test_get_by_name_none_args(self):
        try:
            K8sReplicationController.get_by_name()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_by_name_invalid_config(self):
        name = "yoname"
        config = object()
        try:
            K8sReplicationController.get_by_name(config=config, name=name)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_by_name_invalid_name(self):
        name = object()
        try:
            K8sReplicationController.get_by_name(name=name)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_by_name_nonexistent(self):
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        if _utils.is_reachable(rc.config):
            result = K8sReplicationController.get_by_name(config=rc.config, name=name)
            self.assertIsInstance(result, list)
            self.assertEqual(0, len(result))

    def test_get_by_name(self):
        cont_name = "yocontainer"
        container = _utils.create_container(name=cont_name)
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        rc.add_container(container)
        if _utils.is_reachable(rc.config):
            rc.create()
            result = K8sReplicationController.get_by_name(config=rc.config, name=name)
            self.assertIsInstance(result, list)
            self.assertEqual(1, len(result))
            self.assertIsInstance(result[0], K8sReplicationController)
            self.assertEqual(rc, result[0])

    # -------------------------------------------------------------------------------------  resize

    def test_scale_none_args(self):
        config = _utils.create_config()
        with self.assertRaises(SyntaxError):
            K8sReplicationController.scale(config=config)

    def test_scale_invalid_config(self):
        config = object()
        name = "yoname"
        replicas = 1
        with self.assertRaises(SyntaxError):
            K8sReplicationController.scale(config=config, name=name, replicas=replicas)

    def test_scale_invalid_name(self):
        name = object()
        replicas = 1
        config = _utils.create_config()
        if _utils.is_reachable(config):
            with self.assertRaises(SyntaxError):
                K8sReplicationController.scale(config=config, name=name, replicas=replicas)

    def test_scale_invalid_replicas(self):
        name = "yoname"
        replicas = -99
        container = _utils.create_container(name=name)
        rc = _utils.create_rc(name=name)
        rc.add_container(container)
        if _utils.is_reachable(rc.config):
            with self.assertRaises(SyntaxError):
                rc.create()
                K8sReplicationController.scale(config=rc.config, name=rc.name, replicas=replicas)

    def test_scale_nonexistent(self):
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        replicas = 3
        if _utils.is_reachable(rc.config):
            with self.assertRaises(NotFoundException):
                K8sReplicationController.scale(config=rc.config, name=name, replicas=replicas)

    def test_scale(self):
        cont_name = "yocontainer"
        container = _utils.create_container(name=cont_name)
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        rc.add_container(container)
        replicas = 3
        if _utils.is_reachable(rc.config):
            rc.create()
            K8sReplicationController.scale(config=rc.config, name=name, replicas=replicas)
            result = rc.get()
            self.assertIsInstance(result, K8sReplicationController)
            self.assertEqual(replicas, result.desired_replicas)

    # -------------------------------------------------------------------------------------  rolling update

    def test_rolling_update_none_args(self):
        cont_name = "yocontainer"
        container = _utils.create_container(name=cont_name)
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        rc.add_container(container)
        if _utils.is_reachable(rc.config):
            try:
                K8sReplicationController.rolling_update()
            except Exception as err:
                self.assertIsInstance(err, SyntaxError)

    def test_rolling_update_doesnt_exist(self):
        cont_name = "redis"
        image = "redis:3.2.0"
        new_image = "redis:3.2.3"
        container = _utils.create_container(name=cont_name, image=image)
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        rc.add_container(container)
        if _utils.is_reachable(rc.config):
            try:
                K8sReplicationController.rolling_update(config=rc.config, name=name, image=new_image)
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_rolling_update_one_container_size_0(self):
        cont_name = "redis"
        image = "redis:3.2.0"
        new_image = "redis:3.2.3"
        container = _utils.create_container(name=cont_name, image=image)
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        rc.add_container(container)
        if _utils.is_reachable(rc.config):
            rc.create()
            rollout = K8sReplicationController.rolling_update(config=rc.config, name=name, image=new_image)
            self.assertEqual(new_image, rollout.containers[0].image)

    def test_rolling_update_two_containers_size_0_fails(self):
        cont_name_1 = "redis"
        cont_name_2 = "nginx"
        image_1 = "redis:3.2.0"
        image_2 = "nginx:1.10"
        new_image = "redis:3.2.3"
        container_1 = _utils.create_container(name=cont_name_1, image=image_1)
        container_2 = _utils.create_container(name=cont_name_2, image=image_2)
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        rc.add_container(container_1)
        rc.add_container(container_2)
        if _utils.is_reachable(rc.config):
            rc.create()
            try:
                K8sReplicationController.rolling_update(config=rc.config, name=name, image=new_image)
            except Exception as err:
                self.assertIsInstance(err, UnprocessableEntityException)

    def test_rolling_update_two_containers_size_0_succeeds(self):
        cont_name_1 = "redis"
        cont_name_2 = "nginx"
        image_1 = "redis:3.2.0"
        image_2 = "nginx:1.10"
        new_image = "redis:3.2.3"
        container_1 = _utils.create_container(name=cont_name_1, image=image_1)
        container_2 = _utils.create_container(name=cont_name_2, image=image_2)
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        rc.add_container(container_1)
        rc.add_container(container_2)
        if _utils.is_reachable(rc.config):
            rc.create()
            rollout = K8sReplicationController.rolling_update(
                config=rc.config, name=name, image=new_image, container_name=cont_name_1)
            self.assertEqual(2, len(rollout.containers))
            for c in rollout.containers:
                self.assertIn(c.name, [cont_name_1, cont_name_2])
                self.assertIn(c.image, [new_image, image_2])

    def test_rolling_update_two_containers_size_1(self):
        cont_name_1 = "redis"
        cont_name_2 = "nginx"
        image_1 = "redis:3.2.0"
        image_2 = "nginx:1.10"
        new_image = "redis:3.2.3"
        count = 1
        container_1 = _utils.create_container(name=cont_name_1, image=image_1)
        container_2 = _utils.create_container(name=cont_name_2, image=image_2)
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        rc.add_container(container_1)
        rc.add_container(container_2)
        if _utils.is_reachable(rc.config):
            rc.create()
            K8sReplicationController.scale(
                config=rc.config,
                name=name,
                replicas=count
            )
            pods = K8sPod.get_by_labels(
                config=rc.config,
                labels=rc.pod_labels
            )

            self.assertEqual(count, len(pods))
            for p in pods:
                for c in p.containers:
                    self.assertIn(c.image, [image_1, image_2])

            rollout = K8sReplicationController.rolling_update(
                config=rc.config,
                name=name,
                image=new_image,
                container_name=cont_name_1
            )
            pods = K8sPod.get_by_labels(
                config=rc.config,
                labels=rollout.pod_labels
            )
            self.assertEqual(count, len(pods))
            for p in pods:
                for c in p.containers:
                    self.assertIn(c.image, [new_image, image_2])

    def test_rolling_update_two_containers_size_2(self):
        cont_name_1 = "redis"
        cont_name_2 = "nginx"
        image_1 = "redis:3.2.0"
        image_2 = "nginx:1.10"
        new_image = "redis:3.2.3"
        count = 2
        container_1 = _utils.create_container(name=cont_name_1, image=image_1)
        container_2 = _utils.create_container(name=cont_name_2, image=image_2)
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        rc.add_container(container_1)
        rc.add_container(container_2)
        if _utils.is_reachable(rc.config):
            rc.create()
            K8sReplicationController.scale(
                config=rc.config,
                name=name,
                replicas=count
            )
            pods = K8sPod.get_by_labels(
                config=rc.config,
                labels=rc.pod_labels
            )
            self.assertEqual(count, len(pods))
            for p in pods:
                for c in p.containers:
                    self.assertIn(c.image, [image_1, image_2])

            K8sReplicationController.rolling_update(
                config=rc.config,
                name=name,
                image=new_image,
                container_name=cont_name_1
            )

            rollout = rc.get()
            pods = K8sPod.get_by_labels(
                config=rc.config,
                labels=rollout.pod_labels
            )
            self.assertEqual(count, len(pods))
            for p in pods:
                for c in p.containers:
                    self.assertIn(c.image, [new_image, image_2])

    def test_rolling_update_one_container_size_0_new_rc(self):
        cont_name = "redis"
        image = "redis:3.2.0"
        new_image = "redis:3.2.3"

        cont_1 = _utils.create_container(name=cont_name, image=image)
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc_1 = _utils.create_rc(name=name)
        rc_1.add_container(cont_1)

        cont_2 = _utils.create_container(name=cont_name, image=new_image)
        rc_2 = _utils.create_rc(name=name)
        rc_2.add_container(cont_2)

        if _utils.is_reachable(rc_1.config):
            rc_1.create()
            rollout = K8sReplicationController.rolling_update(config=rc_1.config, name=name, rc_new=rc_2)
            self.assertEqual(new_image, rollout.containers[0].image)

    def test_rolling_update_two_containers_size_0_new_rc(self):
        cont_name_1 = "redis"
        cont_name_2 = "nginx"
        image_1 = "redis:3.2.0"
        image_2 = "nginx:1.10"
        new_image = "redis:3.2.3"

        container_1 = _utils.create_container(name=cont_name_1, image=image_1)
        container_2 = _utils.create_container(name=cont_name_2, image=image_2)
        container_3 = _utils.create_container(name=cont_name_1, image=new_image)

        name_1 = "yorc-{0}".format(str(uuid.uuid4()))
        rc_1 = _utils.create_rc(name=name_1)
        rc_1.add_container(container_1)
        rc_1.add_container(container_2)

        name_2 = "yorc-{0}".format(str(uuid.uuid4()))
        rc_2 = _utils.create_rc(name=name_2)
        rc_2.add_container(container_3)
        rc_2.add_container(container_2)

        if _utils.is_reachable(rc_1.config):
            rc_1.create()
            rollout = K8sReplicationController.rolling_update(config=rc_1.config, name=name_1, rc_new=rc_2)
            self.assertEqual(new_image, rollout.containers[0].image)

    def test_rolling_update_two_containers_size_1_new_rc(self):
        cont_name_1 = "redis"
        cont_name_2 = "nginx"
        image_1 = "redis:3.2.0"
        image_2 = "nginx:1.10"
        new_image = "redis:3.2.3"
        count = 1

        container_1 = _utils.create_container(name=cont_name_1, image=image_1)
        container_2 = _utils.create_container(name=cont_name_2, image=image_2)
        container_3 = _utils.create_container(name=cont_name_1, image=new_image)

        name_1 = "yorc-{0}".format(str(uuid.uuid4()))
        rc_1 = _utils.create_rc(name=name_1)
        rc_1.add_container(container_1)
        rc_1.add_container(container_2)

        name_2 = "yorc-{0}".format(str(uuid.uuid4()))
        rc_2 = _utils.create_rc(name=name_2)
        rc_2.add_container(container_3)
        rc_2.add_container(container_2)

        if _utils.is_reachable(rc_1.config):
            rc_1.create()
            K8sReplicationController.scale(
                config=rc_1.config,
                name=name_1,
                replicas=count
            )
            pods = K8sPod.get_by_labels(
                config=rc_1.config,
                labels=rc_1.pod_labels
            )
            self.assertEqual(count, len(pods))
            for p in pods:
                for c in p.containers:
                    self.assertIn(c.image, [image_1, image_2])

            rollout = K8sReplicationController.rolling_update(
                config=rc_1.config,
                name=name_1,
                rc_new=rc_2
            )
            pods = K8sPod.get_by_labels(
                config=rc_1.config,
                labels=rollout.pod_labels
            )
            self.assertEqual(count, len(pods))
            for p in pods:
                for c in p.containers:
                    self.assertIn(c.image, [new_image, image_2])

    def test_rolling_update_two_containers_size_2_new_rc(self):
        cont_name_1 = "redis"
        cont_name_2 = "nginx"
        image_1 = "redis:3.2.0"
        image_2 = "nginx:1.10"
        new_image = "redis:3.2.3"
        count = 2

        container_1 = _utils.create_container(name=cont_name_1, image=image_1)
        container_2 = _utils.create_container(name=cont_name_2, image=image_2)
        container_3 = _utils.create_container(name=cont_name_1, image=new_image)

        name_1 = "yorc-{0}".format(str(uuid.uuid4()))
        rc_1 = _utils.create_rc(name=name_1)
        rc_1.add_container(container_1)
        rc_1.add_container(container_2)
        rc_1.desired_replicas = count

        name_2 = "yorc-{0}".format(str(uuid.uuid4()))
        rc_2 = _utils.create_rc(name=name_2)
        rc_2.add_container(container_3)
        rc_2.add_container(container_2)
        rc_2.desired_replicas = count

        if _utils.is_reachable(rc_1.config):
            rc_1.create()
            pods = K8sPod.get_by_labels(
                config=rc_1.config,
                labels=rc_1.pod_labels
            )
            self.assertEqual(count, len(pods))
            for p in pods:
                for c in p.containers:
                    self.assertIn(c.image, [image_1, image_2])

            rollout = K8sReplicationController.rolling_update(
                config=rc_1.config,
                name=name_1,
                rc_new=rc_2
            )
            pods = K8sPod.get_by_labels(
                config=rc_1.config,
                labels=rollout.pod_labels
            )
            self.assertEqual(count, len(pods))
            for p in pods:
                for c in p.containers:
                    self.assertIn(c.image, [new_image, image_2])

    def test_update_from_full_model_with_liveness_probes(self):
        data = _constants.frontend()

        rc = ReplicationController(data)
        k8s_rc = _utils.create_rc(name=rc.metadata.name)
        k8s_rc.model = rc
        self.assertEqual(1, len(k8s_rc.liveness_probes))

        liveness = k8s_rc.liveness_probes['frontend']
        self.assertIsInstance(liveness, Probe)
        self.assertEqual(15, liveness.initial_delay_seconds)

        if _utils.is_reachable(k8s_rc.config):
            k8s_rc.create()
            self.assertIsInstance(k8s_rc, K8sReplicationController)

            liveness = k8s_rc.liveness_probes['frontend']
            liveness.initial_delay_seconds = 60
            k8s_rc.liveness_probes = ('frontend', liveness)
            k8s_rc.update()

            pods = K8sPod.get_by_labels(config=k8s_rc.config, labels=k8s_rc.pod_labels)
            self.assertEqual(2, len(pods))
            for pod in pods:
                _liveness = pod.liveness_probes['frontend']
                self.assertNotEqual(_liveness.initial_delay_seconds, liveness.initial_delay_seconds)

            k8s_rc.liveness_probes = ('frontend', liveness)
            k8s_rc.rolling_update(config=k8s_rc.config, name=k8s_rc.name, rc_new=k8s_rc)

            from_update = k8s_rc.get()
            pods = K8sPod.get_by_labels(config=from_update.config, labels=from_update.pod_labels)
            self.assertEqual(2, len(pods))
            for pod in pods:
                from_get = pod.liveness_probes['frontend']
                self.assertEqual(from_get.initial_delay_seconds, liveness.initial_delay_seconds)

    def test_update_from_full_model_with_readiness_probes(self):
        data = _constants.frontend()

        rc = ReplicationController(data)
        k8s_rc = _utils.create_rc(name=rc.metadata.name)
        k8s_rc.model = rc
        self.assertEqual(1, len(k8s_rc.liveness_probes))

        readiness = k8s_rc.readiness_probes['frontend']
        self.assertIsInstance(readiness, Probe)
        self.assertEqual("/", readiness.http_get_action.path)

        if _utils.is_reachable(k8s_rc.config):
            k8s_rc.create()
            self.assertIsInstance(k8s_rc, K8sReplicationController)

            readiness = k8s_rc.readiness_probes['frontend']
            readiness.http_get_action.path = "/new/path"
            k8s_rc.readiness_probes = ('frontend', readiness)
            k8s_rc.update()

            pods = K8sPod.get_by_labels(config=k8s_rc.config, labels=k8s_rc.pod_labels)
            for pod in pods:
                _readiness = pod.readiness_probes['frontend']
                self.assertNotEqual(_readiness.http_get_action.path, readiness.http_get_action.path)

            k8s_rc.readiness_probes = ('frontend', readiness)
            with self.assertRaises(TimedOutException):
                k8s_rc.rolling_update(config=k8s_rc.config, name=k8s_rc.name, rc_new=k8s_rc)

    # -------------------------------------------------------------------------------------  api - create

    def test_create_without_containers(self):
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        if _utils.is_reachable(rc.config):
            try:
                rc.create()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, UnprocessableEntityException)

    def test_create_with_container(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        rc.add_container(container=container)
        if _utils.is_reachable(rc.config):
            obj = rc.create()
            self.assertIsNotNone(obj)
            self.assertIsInstance(obj, K8sReplicationController)

    def test_create_already_exists(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name = "yorc-{0}".format(str(uuid.uuid4()))

        rc = _utils.create_rc(name=name)
        rc.add_container(container=container)
        if _utils.is_reachable(rc.config):
            with self.assertRaises(AlreadyExistsException):
                obj = rc.create()
                self.assertIsNotNone(obj)
                self.assertIsInstance(obj, K8sReplicationController)
                rc.create()

    def test_create_from_full_model(self):
        model = _constants.admintool()
        model = ReplicationController(model)
        self.assertIsInstance(model, ReplicationController)

        rc = _utils.create_rc(name=model.metadata.name)
        rc.model = model
        if _utils.is_reachable(rc.config):
            rc.create()
            self.assertIsInstance(rc, K8sReplicationController)

    # ------------------------------------------------------------------------------------- api - list

    def test_list(self):
        model = _constants.admintool()
        model = ReplicationController(model)
        self.assertIsInstance(model, ReplicationController)
        rc = _utils.create_rc(name=model.metadata.name)
        rc.model = model
        if _utils.is_reachable(rc.config):
            rc.create()
            objs = rc.list()
            for x in objs:
                self.assertIsInstance(x, K8sReplicationController)

    def test_list_multiple(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        config = K8sConfig(kubeconfig=_utils.kubeconfig_fallback)
        rcs = []
        count = 3
        objs = []
        if _utils.is_reachable(config):
            for i in range(0, count):
                name = "yorc-{0}".format(str(uuid.uuid4()))
                rc = _utils.create_rc(config, name, replicas=1)
                rc.add_container(container)
                result = rc.create()
                self.assertIsInstance(result, K8sReplicationController)
                self.assertEqual(rc, result)
                rcs.append(rc)
                objs = rc.list()
            self.assertEqual(count, len(rcs))
            self.assertEqual(count, len(objs))

    # ------------------------------------------------------------------------------------- api - update

    def test_update_nonexistent(self):
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        if _utils.is_reachable(rc.config):
            with self.assertRaises(NotFoundException):
                rc.update()

    def test_update_name_fails(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name1 = "yorc1"
        name2 = "yorc2"
        rc = _utils.create_rc(name=name1)
        rc.add_container(container)
        if _utils.is_reachable(rc.config):
            rc.create()
            result = K8sReplicationController.get_by_name(config=rc.config, name=name1)
            self.assertIsInstance(result, list)
            self.assertEqual(1, len(result))
            self.assertIsInstance(result[0], K8sReplicationController)
            result[0].name = name2
            with self.assertRaises(NotFoundException):
                result[0].update()

    def test_update_namespace_fails(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name = "yorc-{0}".format(str(uuid.uuid4()))
        nspace = "yonamespace"
        rc = _utils.create_rc(name=name)
        rc.add_container(container)
        if _utils.is_reachable(rc.config):
            rc.create()
            result = K8sReplicationController.get_by_name(config=rc.config, name=name)
            self.assertIsInstance(result, list)
            self.assertEqual(1, len(result))
            rc2 = result[0]
            self.assertIsInstance(rc2, K8sReplicationController)
            self.assertNotEqual(rc2.namespace, nspace)
            self.assertEqual(rc, rc2)
            rc2.namespace = nspace
            with self.assertRaises(BadRequestException):
                rc2.update()

    def test_update_labels_succeeds(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        rc.add_container(container)
        if _utils.is_reachable(rc.config):
            rc.create()
            rc.labels['yomama'] = 'sofat'
            rc.update()
            result = rc.get()
            self.assertIsInstance(result, K8sReplicationController)
            self.assertIsInstance(result.labels, dict)
            for k, v in rc.labels.items():
                self.assertEqual(result.labels[k], v)

    def test_update_add_container_succeeds(self):
        cont_names = ["yocontainer", "yocontainer2"]
        container = _utils.create_container(name=cont_names[0])
        rc_name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=rc_name)
        rc.add_container(container)
        if _utils.is_reachable(rc.config):
            rc.create()
            container = _utils.create_container(name=cont_names[1])
            rc.add_container(container)
            result = rc.update()
            self.assertIsInstance(result, K8sReplicationController)
            self.assertEqual(result, rc)
            self.assertIsInstance(result.containers, list)
            self.assertEqual(2, len(result.containers))
            for c in result.containers:
                self.assertIn(c.name, cont_names)

    def test_update_with_add_container(self):
        rc_name = "nginx-{}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=rc_name)
        container_1 = _utils.create_container(name="nginx", image="nginx:1.8.1")
        container_2 = _utils.create_container(name="nginx", image="nginx:1.10.2")
        rc.add_container(container_1)
        rc.desired_replicas = 1
        if _utils.is_reachable(rc.config):
            rc.create()
            self.assertIsInstance(rc, K8sReplicationController)
            rc.add_container(container_2)
            self.assertEqual(1, len(rc.containers))
            self.assertNotEqual(container_1, rc.containers[0])
            self.assertEqual(container_2, rc.containers[0])
            rc.update()
            self.assertNotEqual(container_1, rc.containers[0])
            self.assertEqual(container_2, rc.containers[0])

    # ------------------------------------------------------------------------------------- api - delete

    def test_delete_nonexistent(self):
        name = "yorc-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        if _utils.is_reachable(rc.config):
            with self.assertRaises(NotFoundException):
                rc.delete()

    def test_delete(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name = "yopod-{0}".format(str(uuid.uuid4()))
        rc = _utils.create_rc(name=name)
        rc.add_container(container)
        if _utils.is_reachable(rc.config):
            rc.create()
            _utils.cleanup_rc()
            result = rc.list()
            self.assertIsInstance(result, list)
            self.assertEqual(0, len(result))

    # ------------------------------------------------------------------------------------- api - rolling udpate rework

    def test_rolling_update_name_and_image(self):
        name = "redis-{}".format(str(uuid.uuid4()))
        image_1 = "redis:3.2.0"
        new_image = "redis:3.2.3"
        count = 2
        container = _utils.create_container(name=name, image=image_1)
        rc = _utils.create_rc(name=name)
        rc.add_container(container)
        rc.desired_replicas = count
        if _utils.is_reachable(rc.config):
            rc.create()
            K8sReplicationController.rolling_update(config=rc.config, name=rc.name, image=new_image)
            rc.get()
            self.assertNotEqual(rc.container_image[name], image_1)
            self.assertEqual(rc.container_image[name], new_image)

    # ------------------------------------------------------------------------------------- api - bad cattle

    def test_restart(self):
        cont_name_1 = "redis"
        cont_name_2 = "nginx"
        image_1 = "redis:3.2.0"
        image_2 = "nginx:1.10"
        count = 2

        container_1 = _utils.create_container(name=cont_name_1, image=image_1)
        container_2 = _utils.create_container(name=cont_name_2, image=image_2)

        name_1 = "yorc-{0}".format(str(uuid.uuid4()))
        rc_1 = _utils.create_rc(name=name_1)
        rc_1.add_container(container_1)
        rc_1.add_container(container_2)
        rc_1.desired_replicas = count

        if _utils.is_reachable(rc_1.config):
            rc_1.create()
            rc_2 = rc_1.restart()
            self.assertIn(cont_name_1, rc_2.container_image)
            self.assertIn(cont_name_2, rc_2.container_image)
            self.assertEqual(image_1, rc_2.container_image[cont_name_1])
            self.assertEqual(image_2, rc_2.container_image[cont_name_2])

    # ------------------------------------------------------------------------------------- api - Probe periodSeconds

    def test_probe_period_seconds(self):
        data = _constants.frontend()
        rc = ReplicationController(data)
        k8s_rc = _utils.create_rc(name=rc.metadata.name)
        k8s_rc.model = rc
        self.assertEqual(1, len(k8s_rc.liveness_probes))
        self.assertEqual(1, len(k8s_rc.readiness_probes))

        if _utils.is_reachable(k8s_rc.config):
            k8s_rc.create()
            probe = k8s_rc.liveness_probes['frontend']
            probe.period_seconds = 60
            k8s_rc.liveness_probes = ('frontend', probe)
            k8s_rc.update()
            rc = k8s_rc.get()
            self.assertEqual(60, rc.liveness_probes['frontend'].period_seconds)

    def test_probe_period_seconds_with_model(self):
        data = _constants.frontend()
        rc = ReplicationController(data)
        k8s_rc = _utils.create_rc(name=rc.metadata.name)
        k8s_rc.model = rc
        self.assertEqual(1, len(k8s_rc.liveness_probes))
        self.assertEqual(1, len(k8s_rc.readiness_probes))

        if _utils.is_reachable(k8s_rc.config):
            k8s_rc.create()
            liveness = k8s_rc.liveness_probes['frontend']
            liveness.period_seconds = 60
            dict = liveness.serialize()
            container = k8s_rc.containers[0]
            container.add_liveness_probe(**dict)
