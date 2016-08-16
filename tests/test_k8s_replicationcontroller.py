#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
import uuid
from kubernetes import K8sReplicationController, K8sConfig, K8sPod
from kubernetes.K8sExceptions import *
from kubernetes.models.v1 import ReplicationController, ObjectMeta, PodSpec
from tests import utils


class K8sReplicationControllerTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        utils.cleanup_objects()

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
        try:
            K8sReplicationController(config=config)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_invalid_name(self):
        name = object()
        try:
            utils.create_rc(name=name)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_name(self):
        name = "yomama"
        rc = utils.create_rc(name=name)
        self.assertIsNotNone(rc)
        self.assertIsInstance(rc, K8sReplicationController)
        self.assertEqual(rc.name, name)

    def test_init_with_config_and_pull_secrets(self):
        ps = "yomama"
        name = "sofat"
        config = K8sConfig(pull_secret=ps, kubeconfig=utils.kubeconfig_fallback)
        rc = utils.create_rc(config=config, name=name)
        self.assertIsNotNone(rc.config)
        self.assertEqual(ps, rc.config.pull_secret)

    # --------------------------------------------------------------------------------- struct

    def test_struct_k8s_rc(self):
        name = "yomama"
        rc = utils.create_rc(name=name)
        self.assertIsNotNone(rc)
        self.assertIsInstance(rc, K8sReplicationController)
        self.assertIsNotNone(rc.model)
        self.assertIsInstance(rc.model, ReplicationController)

    def test_struct_rc(self):
        name = "yomama"
        rc = utils.create_rc(name=name)
        model = rc.model
        self.assertIsInstance(model.model, dict)
        self.assertIsInstance(model.pod_metadata, ObjectMeta)
        self.assertIsInstance(model.pod_spec, PodSpec)
        self.assertIsNone(model.pod_status)
        self.assertIsInstance(model.rc_metadata, ObjectMeta)

    def test_struct_rc_model(self):
        name = "yomama"
        rc = utils.create_rc(name=name)
        model = rc.model.model
        self.assertIsNotNone(model)
        self.assertIsInstance(model, dict)

        self.assertEqual(4, len(model))
        for i in ['apiVersion', 'kind', 'metadata', 'spec']:
            self.assertIn(i, model)
        self.assertIsInstance(model['apiVersion'], str)
        self.assertIsInstance(model['kind'], str)
        self.assertIsInstance(model['metadata'], dict)
        self.assertIsInstance(model['spec'], dict)

        self.assertEqual(3, len(model['metadata']))
        for i in ['labels', 'name', 'namespace']:
            self.assertIn(i, model['metadata'])
        self.assertIsInstance(model['metadata']['name'], str)
        self.assertEqual(model['metadata']['name'], name)
        self.assertIsInstance(model['metadata']['namespace'], str)
        self.assertIsInstance(model['metadata']['labels'], dict)

        self.assertEqual(1, len(model['metadata']['labels']))
        self.assertIn('name', model['metadata']['labels'])
        self.assertIsInstance(model['metadata']['labels']['name'], str)
        self.assertEqual(model['metadata']['labels']['name'], name)

        self.assertEqual(3, len(model['spec']))
        for i in ['replicas', 'selector', 'template']:
            self.assertIn(i, model['spec'])
        self.assertIsInstance(model['spec']['replicas'], int)
        self.assertIsInstance(model['spec']['selector'], dict)
        self.assertIsInstance(model['spec']['template'], dict)

        self.assertEqual(2, len(model['spec']['selector']))
        for i in ['name', 'rc_version']:
            self.assertIn(i, model['spec']['selector'])
            self.assertIsInstance(model['spec']['selector'][i], str)

        self.assertEqual(2, len(model['spec']['template']))
        for i in ['metadata', 'spec']:
            self.assertIn(i, model['spec']['template'])
            self.assertIsInstance(model['spec']['template'][i], dict)

        self.assertEqual(3, len(model['spec']['template']['metadata']))
        for i in ['labels', 'name', 'namespace']:
            self.assertIn(i, model['spec']['template']['metadata'])
        self.assertIsInstance(model['spec']['template']['metadata']['labels'], dict)
        self.assertIsInstance(model['spec']['template']['metadata']['name'], str)
        self.assertIsInstance(model['spec']['template']['metadata']['namespace'], str)

        self.assertEqual(2, len(model['spec']['template']['metadata']['labels']))
        for i in ['name', 'rc_version']:
            self.assertIn(i, model['spec']['template']['metadata']['labels'])
            self.assertIsInstance(model['spec']['template']['metadata']['labels'][i], str)

        self.assertEqual(4, len(model['spec']['template']['spec']))
        for i in ['containers', 'dnsPolicy', 'restartPolicy', 'volumes']:
            self.assertIn(i, model['spec']['template']['spec'])
        for i in ['containers', 'volumes']:
            self.assertIsInstance(model['spec']['template']['spec'][i], list)
            self.assertEqual(0, len(model['spec']['template']['spec'][i]))
        for i in ['dnsPolicy', 'restartPolicy']:
            self.assertIsInstance(model['spec']['template']['spec'][i], str)
        self.assertEqual('Default', model['spec']['template']['spec']['dnsPolicy'])
        self.assertEqual('Always', model['spec']['template']['spec']['restartPolicy'])

    # --------------------------------------------------------------------------------- add annotation

    def test_add_annotation_none_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.add_annotation()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_annotation_invalid_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = object()
        v = object()
        try:
            rc.add_annotation(k, v)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_annotation(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        v = "yovalue"
        rc.add_annotation(k, v)
        self.assertIn('annotations', rc.model.model['metadata'])
        self.assertIn(k, rc.model.model['metadata']['annotations'])
        self.assertEqual(rc.model.model['metadata']['annotations']['yokey'], v)
        self.assertIn('annotations', rc.model.rc_metadata.model)
        self.assertIn(k, rc.model.rc_metadata.model['annotations'])
        self.assertEqual(rc.model.rc_metadata.model['annotations']['yokey'], v)

    # --------------------------------------------------------------------------------- add label

    def test_add_label_none_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.add_label()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_label_invalid_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = object()
        v = object()
        try:
            rc.add_label(k, v)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_label(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        v = "yovalue"
        rc.add_label(k, v)
        self.assertIn('labels', rc.model.model['metadata'])
        self.assertIn(k, rc.model.model['metadata']['labels'])
        self.assertEqual(rc.model.model['metadata']['labels']['yokey'], v)
        self.assertIn('labels', rc.model.rc_metadata.model)
        self.assertIn(k, rc.model.rc_metadata.model['labels'])
        self.assertEqual(rc.model.rc_metadata.model['labels']['yokey'], v)

    # --------------------------------------------------------------------------------- add pod annotation

    def test_add_pod_annotation_none_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.add_pod_annotation()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_pod_annotation_invalid_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = object()
        v = object()
        try:
            rc.add_pod_annotation(k, v)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_pod_annotation(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        v = "yovalue"
        rc.add_pod_annotation(k, v)
        self.assertIn('annotations', rc.model.model['spec']['template']['metadata'])
        self.assertIn(k, rc.model.model['spec']['template']['metadata']['annotations'])
        self.assertEqual(rc.model.model['spec']['template']['metadata']['annotations']['yokey'], v)
        self.assertIn('annotations', rc.model.pod_metadata.model)
        self.assertIn(k, rc.model.pod_metadata.model['annotations'])
        self.assertEqual(rc.model.pod_metadata.model['annotations']['yokey'], v)

    # --------------------------------------------------------------------------------- add pod label

    def test_add_pod_label_none_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.add_pod_label()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_pod_label_invalid_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = object()
        v = object()
        try:
            rc.add_pod_label(k, v)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_pod_label(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        v = "yovalue"
        rc.add_pod_label(k, v)
        self.assertIn('labels', rc.model.model['spec']['template']['metadata'])
        self.assertIn(k, rc.model.model['spec']['template']['metadata']['labels'])
        self.assertEqual(rc.model.model['spec']['template']['metadata']['labels']['yokey'], v)
        self.assertIn('labels', rc.model.pod_metadata.model)
        self.assertIn(k, rc.model.pod_metadata.model['labels'])
        self.assertEqual(rc.model.pod_metadata.model['labels']['yokey'], v)

    # --------------------------------------------------------------------------------- del annotation

    def test_del_annotation_none_arg(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.del_annotation()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_del_annotation_invalid_arg(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = object()
        try:
            rc.del_annotation(k)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_del_annotation_doesnt_exist(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        rc.del_annotation(k)
        self.assertNotIn('annotations', rc.model.model['metadata'])
        self.assertNotIn('annotations', rc.model.rc_metadata.model)

    def test_del_annotation(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        v = "yovalue"
        rc.add_annotation(k, v)
        self.assertIn(k, rc.model.model['metadata']['annotations'])
        self.assertIn(k, rc.model.rc_metadata.model['annotations'])
        rc.del_annotation(k)
        self.assertNotIn(k, rc.model.model['metadata']['annotations'])
        self.assertNotIn(k, rc.model.rc_metadata.model['annotations'])

    # --------------------------------------------------------------------------------- del label

    def test_del_label_none_arg(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.del_label()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_del_label_invalid_arg(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = object()
        try:
            rc.del_label(k)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_del_label_doesnt_exist(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        rc.del_label(k)
        self.assertIn('labels', rc.model.model['metadata'])
        self.assertNotIn(k, rc.model.model['metadata'])
        self.assertIn('labels', rc.model.rc_metadata.model)

    def test_del_label(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        v = "yovalue"
        rc.add_annotation(k, v)
        self.assertIn(k, rc.model.model['metadata']['annotations'])
        self.assertIn(k, rc.model.rc_metadata.model['annotations'])
        rc.del_annotation(k)
        self.assertNotIn(k, rc.model.model['metadata']['annotations'])
        self.assertNotIn(k, rc.model.rc_metadata.model['annotations'])

    # --------------------------------------------------------------------------------- del pod annotation

    def test_del_pod_annotation_none_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.del_pod_annotation()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_del_pod_annotation_invalid_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = object()
        try:
            rc.del_pod_annotation(k)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_del_pod_annotation_doesnt_exist(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        rc.del_pod_annotation(k)
        self.assertNotIn('annotations', rc.model.model['spec']['template']['metadata'])
        self.assertNotIn('annotations', rc.model.pod_metadata.model)

    def test_del_pod_annotation(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        v = "yovalue"
        rc.add_pod_annotation(k, v)
        self.assertIn(k, rc.model.model['spec']['template']['metadata']['annotations'])
        self.assertIn(k, rc.model.pod_metadata.model['annotations'])
        rc.del_pod_annotation(k)
        self.assertNotIn(k, rc.model.model['spec']['template']['metadata']['annotations'])
        self.assertNotIn(k, rc.model.pod_metadata.model['annotations'])

    # --------------------------------------------------------------------------------- del pod label

    def test_del_pod_label_none_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.del_pod_label()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_del_pod_label_invalid_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = object()
        try:
            rc.del_pod_label(k)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_del_pod_label_doesnt_exist(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        rc.del_pod_label(k)
        self.assertNotIn(k, rc.model.model['spec']['template']['metadata']['labels'])
        self.assertNotIn(k, rc.model.pod_metadata.model['labels'])

    def test_del_pod_label(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        v = "yovalue"
        rc.add_pod_label(k, v)
        self.assertIn(k, rc.model.model['spec']['template']['metadata']['labels'])
        self.assertIn(k, rc.model.pod_metadata.model['labels'])
        rc.del_pod_label(k)
        self.assertNotIn(k, rc.model.model['spec']['template']['metadata']['labels'])
        self.assertNotIn(k, rc.model.pod_metadata.model['labels'])

    # --------------------------------------------------------------------------------- get

    def test_get_nonexistent(self):
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        if utils.is_reachable(rc.config.api_host):
            try:
                rc.get()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_get(self):
        name = "yocontainer"
        container = utils.create_container(name=name)
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        rc.add_container(container)
        if utils.is_reachable(rc.config.api_host):
            from_create = rc.create()
            from_get = rc.get()
            self.assertIsInstance(from_create, K8sReplicationController)
            self.assertIsInstance(from_get, K8sReplicationController)
            self.assertEqual(from_create, from_get)

    # --------------------------------------------------------------------------------- get annotation

    def test_get_annotation_none_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.get_annotation()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_annotation_invalid_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = object()
        try:
            rc.get_annotation(k)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_annotation_doesnt_exist(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        ann = rc.get_annotation(k)
        self.assertIsNone(ann)

    def test_get_annotation(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        v_in = "yovalue"
        rc.add_annotation(k, v_in)
        v_out = rc.get_annotation(k)
        self.assertEqual(v_in, v_out)

    # --------------------------------------------------------------------------------- get annotations

    def test_get_annotations_none(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        anns = rc.get_annotations()
        self.assertIsNone(anns)

    def test_get_annotations(self):
        name = "yorc"
        rc = utils.create_rc(name=name)

        count = 4
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            rc.add_annotation(k, v)

        anns = rc.get_annotations()
        self.assertEqual(count, len(anns))
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            self.assertIn(k, anns)
            self.assertEqual(v, anns[k])

    # --------------------------------------------------------------------------------- get label

    def test_get_label_none_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.get_label()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_label_invalid_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = object()
        try:
            rc.get_label(k)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_label_doesnt_exist(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        label = rc.get_label(k)
        self.assertIsNone(label)

    def test_get_label(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        v_in = "yovalue"
        rc.add_label(k, v_in)
        v_out = rc.get_label(k)
        self.assertEqual(v_in, v_out)

    # --------------------------------------------------------------------------------- get labels

    def test_get_labels_none(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        labels = rc.get_labels()
        self.assertIsNotNone(labels)  # 'name' is already a label
        self.assertIn('name', labels)
        self.assertEqual(name, labels['name'])

    def test_get_labels(self):
        name = "yorc"
        rc = utils.create_rc(name=name)

        count = 4
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            rc.add_label(k, v)

        labels = rc.get_labels()
        self.assertLessEqual(count, len(labels))  # 'name' is already a label
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            self.assertIn(k, labels)
            self.assertEqual(v, labels[k])

    # --------------------------------------------------------------------------------- get pod annotation

    def test_get_pod_annotation_none_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.get_pod_annotation()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_pod_annotation_invalid_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = object()
        try:
            rc.get_pod_annotation(k)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_pod_annotation_doesnt_exist(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        ann = rc.get_pod_annotation(k)
        self.assertIsNone(ann)

    def test_get_pod_annotation(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        v_in = "yovalue"
        rc.add_pod_annotation(k, v_in)
        v_out = rc.get_pod_annotation(k)
        self.assertEqual(v_in, v_out)

    # --------------------------------------------------------------------------------- get pod annotations

    def test_get_pod_annotations_none(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        anns = rc.get_pod_annotations()
        self.assertIsNone(anns)

    def test_get_pod_annotations(self):
        name = "yorc"
        rc = utils.create_rc(name=name)

        count = 4
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            rc.add_pod_annotation(k, v)

        anns = rc.get_pod_annotations()
        self.assertEqual(count, len(anns))
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            self.assertIn(k, anns)
            self.assertEqual(v, anns[k])

    # --------------------------------------------------------------------------------- get pod label

    def test_get_pod_label_none_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.get_pod_label()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_pod_label_invalid_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = object()
        try:
            rc.get_pod_label(k)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_pod_label_doesnt_exist(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        label = rc.get_pod_label(k)
        self.assertIsNone(label)

    def test_get_pod_label(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        k = "yokey"
        v_in = "yovalue"
        rc.add_pod_label(k, v_in)
        v_out = rc.get_pod_label(k)
        self.assertEqual(v_in, v_out)

    # --------------------------------------------------------------------------------- get pod labels

    def test_get_pod_labels_none(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        labels = rc.get_pod_labels()
        self.assertIsNotNone(labels)  # 'name' and 'rc_version' are already labels
        self.assertIn('name', labels)
        self.assertIn('rc_version', labels)
        self.assertEqual(name, labels['name'])

    def test_get_pod_labels(self):
        name = "yorc"
        rc = utils.create_rc(name=name)

        count = 4
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            rc.add_pod_label(k, v)

        labels = rc.get_pod_labels()
        self.assertLessEqual(count, len(labels))  # 'name' and 'rc_version' are already labels
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            self.assertIn(k, labels)
            self.assertEqual(v, labels[k])

    # --------------------------------------------------------------------------------- get replicas

    def test_get_replicas_none(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        reps = rc.get_replicas()
        self.assertEqual(0, reps)

    def test_get_replicas(self):
        name = "yorc"
        count = 10
        rc = utils.create_rc(name=name, replicas=count)
        reps = rc.get_replicas()
        self.assertEqual(count, reps)

    # --------------------------------------------------------------------------------- get selector

    def test_get_selector(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        sel = rc.get_selector()
        self.assertIsNotNone(sel)
        self.assertIsInstance(sel, dict)
        self.assertEqual(2, len(sel))
        self.assertIn('name', sel)
        self.assertIn('rc_version', sel)
        self.assertEqual(name, sel['name'])

    # --------------------------------------------------------------------------------- set annotations

    def test_set_annotations_none_arg(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.set_annotations()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_annotations_invalid_arg(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        anns = object()
        try:
            rc.set_annotations(anns)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_annotations(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        anns_in = {'k1': 'v1', 'k2': 'v2'}
        rc.set_annotations(anns_in)
        anns_out = rc.get_annotations()
        self.assertEqual(anns_in, anns_out)

    # --------------------------------------------------------------------------------- set labels

    def test_set_labels_none_arg(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.set_labels()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_labels_invalid_arg(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        labels = object()
        try:
            rc.set_labels(labels)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_labels(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        labels_in = {'k1': 'v1', 'k2': 'v2'}
        rc.set_labels(labels_in)
        labels_out = rc.get_labels()
        self.assertEqual(labels_in, labels_out)

    # --------------------------------------------------------------------------------- set namespace

    def test_set_namespace_none_arg(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.set_namespace()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_namespace_invalid_arg(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        nspace = object()
        try:
            rc.set_namespace(nspace)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_namespace(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        nspace_in = "yonamespace"
        rc.set_namespace(nspace_in)
        nspace_out = rc.get_namespace()
        self.assertEqual(nspace_in, nspace_out)

    # --------------------------------------------------------------------------------- set pod annotations

    def test_set_pod_annotations_none_arg(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.set_pod_annotations()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_pod_annotations_invalid_arg(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        anns = object()
        try:
            rc.set_pod_annotations(anns)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_pod_annotations(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        anns_in = {'k1': 'v1', 'k2': 'v2'}
        rc.set_pod_annotations(anns_in)
        anns_out = rc.get_pod_annotations()
        self.assertEqual(anns_in, anns_out)

    # --------------------------------------------------------------------------------- set labels

    def test_set_pod_labels_none_arg(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.set_pod_labels()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_pod_labels_invalid_arg(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        labels = object()
        try:
            rc.set_pod_labels(labels)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_pod_labels(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        labels_in = {'k1': 'v1', 'k2': 'v2'}
        rc.set_pod_labels(labels_in)
        labels_out = rc.get_pod_labels()
        self.assertEqual(labels_in, labels_out)

    # --------------------------------------------------------------------------------- set replicas

    def test_set_replicas_none_arg(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.set_replicas()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_replicas_invalid_arg(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        count = -99
        try:
            rc.set_replicas(count)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_replicas(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        count = 10
        before = rc.get_replicas()
        self.assertNotEqual(before, count)
        rc.set_replicas(count)
        after = rc.get_replicas()
        self.assertEqual(count, after)
        self.assertNotEqual(before, after)

    # --------------------------------------------------------------------------------- set selector

    def test_set_selector_none_arg(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.set_selector()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_selector_invalid_arg(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        sel = object()
        try:
            rc.set_selector(sel)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_selector(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        sel_in = {'k1': 'v1', 'k2': 'v2'}
        rc.set_selector(sel_in)
        sel_out = rc.get_selector()
        self.assertEqual(sel_in, sel_out)

    # -------------------------------------------------------------------------------------  wait for replicas

    def test_wait_for_replicas_none_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        try:
            rc.wait_for_replicas()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_wait_for_replicas_invalid_args(self):
        name = "yorc"
        rc = utils.create_rc(name=name)
        replicas = object()
        try:
            rc.wait_for_replicas(replicas=replicas)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_wait_for_replicas_timed_out(self):
        # this test makes no sense without a prior call to resize.
        # it'll wait forever on a quantity of pods that does not change.
        # please see test_resize().
        cont_name = "yocontainer"
        container = utils.create_container(name=cont_name)
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        rc.add_container(container)
        count = 99
        if utils.is_reachable(rc.config.api_host):
            try:
                rc.create()
                rc.wait_for_replicas(replicas=count)
            except Exception as err:
                self.assertIsInstance(err, TimedOutException)

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
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        if utils.is_reachable(rc.config.api_host):
            result = K8sReplicationController.get_by_name(config=rc.config, name=name)
            self.assertIsInstance(result, list)
            self.assertEqual(0, len(result))

    def test_get_by_name(self):
        cont_name = "yocontainer"
        container = utils.create_container(name=cont_name)
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        rc.add_container(container)
        if utils.is_reachable(rc.config.api_host):
            rc.create()
            result = K8sReplicationController.get_by_name(config=rc.config, name=name)
            self.assertIsInstance(result, list)
            self.assertEqual(1, len(result))
            self.assertIsInstance(result[0], K8sReplicationController)
            self.assertEqual(rc, result[0])

    # -------------------------------------------------------------------------------------  get by name

    def test_resize_none_args(self):
        try:
            K8sReplicationController.resize()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_resize_invalid_config(self):
        config = object()
        name = "yoname"
        replicas = 1
        try:
            K8sReplicationController.resize(config=config, name=name, replicas=replicas)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_resize_invalid_name(self):
        name = object()
        replicas = 1
        try:
            K8sReplicationController.resize(name=name, replicas=replicas)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_resize_invalid_replicas(self):
        name = "yoname"
        replicas = -99
        try:
            K8sReplicationController.resize(name=name, replicas=replicas)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_resize_nonexistent(self):
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        replicas = 3
        if utils.is_reachable(rc.config.api_host):
            try:
                K8sReplicationController.resize(config=rc.config, name=name, replicas=replicas)
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_resize(self):
        cont_name = "yocontainer"
        container = utils.create_container(name=cont_name)
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        rc.add_container(container)
        replicas = 3
        if utils.is_reachable(rc.config.api_host):
            rc.create()
            K8sReplicationController.resize(config=rc.config, name=name, replicas=replicas)
            result = rc.get()
            self.assertIsInstance(result, K8sReplicationController)
            self.assertEqual(replicas, result.model.model['spec']['replicas'])

    # -------------------------------------------------------------------------------------  rolling update

    def test_rolling_update_none_args(self):
        cont_name = "yocontainer"
        container = utils.create_container(name=cont_name)
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        rc.add_container(container)
        if utils.is_reachable(rc.config.api_host):
            try:
                K8sReplicationController.rolling_update()
            except Exception as err:
                self.assertIsInstance(err, SyntaxError)

    def test_rolling_update_doesnt_exist(self):
        cont_name = "redis"
        image = "redis:3.2.0"
        new_image = "redis:3.2.3"
        container = utils.create_container(name=cont_name, image=image)
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        rc.add_container(container)
        if utils.is_reachable(rc.config.api_host):
            try:
                K8sReplicationController.rolling_update(config=rc.config, name=name, image=new_image)
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_rolling_update_one_container_size_0(self):
        cont_name = "redis"
        image = "redis:3.2.0"
        new_image = "redis:3.2.3"
        container = utils.create_container(name=cont_name, image=image)
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        rc.add_container(container)
        #if utils.is_reachable(rc.config.api_host):
        rc.create()
        rollout = K8sReplicationController.rolling_update(config=rc.config, name=name, image=new_image)
        self.assertEqual(new_image, rollout.model.model['spec']['template']['spec']['containers'][0]['image'])
        self.assertEqual(new_image, rollout.model.pod_spec.containers[0].model['image'])

    def test_rolling_update_two_containers_size_0_fails(self):
        cont_name_1 = "redis"
        cont_name_2 = "nginx"
        image_1 = "redis:3.2.0"
        image_2 = "nginx:1.10"
        new_image = "redis:3.2.3"
        container_1 = utils.create_container(name=cont_name_1, image=image_1)
        container_2 = utils.create_container(name=cont_name_2, image=image_2)
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        rc.add_container(container_1)
        rc.add_container(container_2)
        if utils.is_reachable(rc.config.api_host):
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
        container_1 = utils.create_container(name=cont_name_1, image=image_1)
        container_2 = utils.create_container(name=cont_name_2, image=image_2)
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        rc.add_container(container_1)
        rc.add_container(container_2)
        if utils.is_reachable(rc.config.api_host):
            rc.create()
            rollout = K8sReplicationController.rolling_update(config=rc.config, name=name, image=new_image, container_name=cont_name_1)
            self.assertEqual(2, len(rollout.model.pod_spec.containers))
            for c in rollout.model.pod_spec.containers:
                self.assertIn(c.model['name'], [cont_name_1, cont_name_2])
                self.assertIn(c.model['image'], [new_image, image_2])

    def test_rolling_update_two_containers_size_1(self):
        cont_name_1 = "redis"
        cont_name_2 = "nginx"
        image_1 = "redis:3.2.0"
        image_2 = "nginx:1.10"
        new_image = "redis:3.2.3"
        count = 1
        container_1 = utils.create_container(name=cont_name_1, image=image_1)
        container_2 = utils.create_container(name=cont_name_2, image=image_2)
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        rc.add_container(container_1)
        rc.add_container(container_2)
        if utils.is_reachable(rc.config.api_host):
            rc.create()
            K8sReplicationController.resize(
                config=rc.config,
                name=name,
                replicas=count
            )
            labels = rc.get_pod_labels()
            pods = K8sPod.get_by_labels(
                config=rc.config,
                labels=labels
            )
            self.assertEqual(count, len(pods))
            self.assertEqual(image_1, pods[0].model.pod_spec.containers[0].model['image'])
            rollout = K8sReplicationController.rolling_update(
                config=rc.config,
                name=name,
                image=new_image,
                container_name=cont_name_1
            )
            labels = rollout.get_pod_labels()
            pods = K8sPod.get_by_labels(
                config=rc.config,
                labels=labels
            )
            self.assertEqual(count, len(pods))
            self.assertEqual(new_image, pods[0].model.pod_spec.containers[0].model['image'])

    def test_rolling_update_two_containers_size_3(self):
        cont_name_1 = "redis"
        cont_name_2 = "nginx"
        image_1 = "redis:3.2.0"
        image_2 = "nginx:1.10"
        new_image = "redis:3.2.3"
        count = 3
        container_1 = utils.create_container(name=cont_name_1, image=image_1)
        container_2 = utils.create_container(name=cont_name_2, image=image_2)
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        rc.add_container(container_1)
        rc.add_container(container_2)
        if utils.is_reachable(rc.config.api_host):
            rc.create()
            K8sReplicationController.resize(
                config=rc.config,
                name=name,
                replicas=count
            )
            labels = rc.get_pod_labels()
            pods = K8sPod.get_by_labels(
                config=rc.config,
                labels=labels
            )
            self.assertEqual(count, len(pods))
            for i in range(0, count):
                self.assertEqual(image_1, pods[i].model.pod_spec.containers[0].model['image'])
            rollout = K8sReplicationController.rolling_update(
                config=rc.config,
                name=name,
                image=new_image,
                container_name=cont_name_1
            )
            labels = rollout.get_pod_labels()
            pods = K8sPod.get_by_labels(
                config=rc.config,
                labels=labels
            )
            self.assertEqual(count, len(pods))
            for i in range(0, count):
                self.assertEqual(new_image, pods[i].model.pod_spec.containers[0].model['image'])

    def test_rolling_update_one_container_size_0_new_rc(self):
        cont_name = "redis"
        image = "redis:3.2.0"
        new_image = "redis:3.2.3"

        cont_1 = utils.create_container(name=cont_name, image=image)
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc_1 = utils.create_rc(name=name)
        rc_1.add_container(cont_1)

        cont_2 = utils.create_container(name=cont_name, image=new_image)
        rc_2 = utils.create_rc(name=name)
        rc_2.add_container(cont_2)

        if utils.is_reachable(rc_1.config.api_host):
            rc_1.create()
            rollout = K8sReplicationController.rolling_update(config=rc_1.config, name=name, rc_new=rc_2)
            self.assertEqual(new_image, rollout.model.model['spec']['template']['spec']['containers'][0]['image'])
            self.assertEqual(new_image, rollout.model.pod_spec.containers[0].model['image'])

    def test_rolling_update_two_containers_size_0_new_rc(self):
        cont_name_1 = "redis"
        cont_name_2 = "nginx"
        image_1 = "redis:3.2.0"
        image_2 = "nginx:1.10"
        new_image = "redis:3.2.3"

        container_1 = utils.create_container(name=cont_name_1, image=image_1)
        container_2 = utils.create_container(name=cont_name_2, image=image_2)
        container_3 = utils.create_container(name=cont_name_1, image=new_image)

        name_1 = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc_1 = utils.create_rc(name=name_1)
        rc_1.add_container(container_1)
        rc_1.add_container(container_2)

        name_2 = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc_2 = utils.create_rc(name=name_2)
        rc_2.add_container(container_3)
        rc_2.add_container(container_2)

        if utils.is_reachable(rc_1.config.api_host):
            rc_1.create()
            rollout = K8sReplicationController.rolling_update(config=rc_1.config, name=name_1, rc_new=rc_2)
            self.assertEqual(new_image, rollout.model.model['spec']['template']['spec']['containers'][0]['image'])
            self.assertEqual(new_image, rollout.model.pod_spec.containers[0].model['image'])

    def test_rolling_update_two_containers_size_1_new_rc(self):
        cont_name_1 = "redis"
        cont_name_2 = "nginx"
        image_1 = "redis:3.2.0"
        image_2 = "nginx:1.10"
        new_image = "redis:3.2.3"
        count = 1

        container_1 = utils.create_container(name=cont_name_1, image=image_1)
        container_2 = utils.create_container(name=cont_name_2, image=image_2)
        container_3 = utils.create_container(name=cont_name_1, image=new_image)

        name_1 = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc_1 = utils.create_rc(name=name_1)
        rc_1.add_container(container_1)
        rc_1.add_container(container_2)

        name_2 = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc_2 = utils.create_rc(name=name_2)
        rc_2.add_container(container_3)
        rc_2.add_container(container_2)

        if utils.is_reachable(rc_1.config.api_host):
            rc_1.create()
            K8sReplicationController.resize(
                config=rc_1.config,
                name=name_1,
                replicas=count
            )
            labels = rc_1.get_pod_labels()
            pods = K8sPod.get_by_labels(
                config=rc_1.config,
                labels=labels
            )
            self.assertEqual(count, len(pods))
            self.assertEqual(image_1, pods[0].model.pod_spec.containers[0].model['image'])
            rollout = K8sReplicationController.rolling_update(
                config=rc_1.config,
                name=name_1,
                rc_new=rc_2
            )
            labels = rollout.get_pod_labels()
            pods = K8sPod.get_by_labels(
                config=rc_1.config,
                labels=labels
            )
            self.assertEqual(count, len(pods))
            self.assertEqual(new_image, pods[0].model.pod_spec.containers[0].model['image'])

    def test_rolling_update_two_containers_size_3_new_rc(self):
        cont_name_1 = "redis"
        cont_name_2 = "nginx"
        image_1 = "redis:3.2.0"
        image_2 = "nginx:1.10"
        new_image = "redis:3.2.3"
        count = 3

        container_1 = utils.create_container(name=cont_name_1, image=image_1)
        container_2 = utils.create_container(name=cont_name_2, image=image_2)
        container_3 = utils.create_container(name=cont_name_1, image=new_image)

        name_1 = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc_1 = utils.create_rc(name=name_1)
        rc_1.add_container(container_1)
        rc_1.add_container(container_2)

        name_2 = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc_2 = utils.create_rc(name=name_2)
        rc_2.add_container(container_3)
        rc_2.add_container(container_2)

        if utils.is_reachable(rc_1.config.api_host):
            rc_1.create()
            K8sReplicationController.resize(
                config=rc_1.config,
                name=name_1,
                replicas=count
            )
            labels = rc_1.get_pod_labels()
            pods = K8sPod.get_by_labels(
                config=rc_1.config,
                labels=labels
            )
            self.assertEqual(count, len(pods))
            for i in range(0, count):
                self.assertEqual(image_1, pods[i].model.pod_spec.containers[0].model['image'])
            rollout = K8sReplicationController.rolling_update(
                config=rc_1.config,
                name=name_1,
                rc_new=rc_2
            )
            labels = rollout.get_pod_labels()
            pods = K8sPod.get_by_labels(
                config=rc_1.config,
                labels=labels
            )
            self.assertEqual(count, len(pods))
            for i in range(0, count):
                self.assertEqual(new_image, pods[i].model.pod_spec.containers[0].model['image'])

    # -------------------------------------------------------------------------------------  api - create

    def test_create_without_containers(self):
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        if utils.is_reachable(rc.config.api_host):
            try:
                rc.create()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, UnprocessableEntityException)

    def test_create_with_container(self):
        name = "yocontainer"
        container = utils.create_container(name=name)
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        rc.add_container(container=container)
        if utils.is_reachable(rc.config.api_host):
            obj = rc.create()
            self.assertIsNotNone(obj)
            self.assertIsInstance(obj, K8sReplicationController)

    def test_create_already_exists(self):
        name = "yocontainer"
        container = utils.create_container(name=name)
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        rc.add_container(container=container)
        if utils.is_reachable(rc.config.api_host):
            try:
                obj = rc.create()
                self.assertIsNotNone(obj)
                self.assertIsInstance(obj, K8sReplicationController)
                rc.create()
            except Exception as err:
                self.assertIsInstance(err, AlreadyExistsException)

    # ------------------------------------------------------------------------------------- api - list

    def test_list_nonexistent(self):
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        if utils.is_reachable(rc.config.api_host):
            objs = rc.list()
            self.assertIsInstance(objs, list)
            self.assertEqual(0, len(objs))

    def test_list_multiple(self):
        name = "yocontainer"
        container = utils.create_container(name=name)
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        rcs = []
        count = 3
        if utils.is_reachable(config.api_host):
            for i in range(0, count):
                name = "yorc-{0}".format(unicode(uuid.uuid4()))
                rc = utils.create_rc(config, name)
                rc.add_container(container)
                result = rc.create()
                self.assertIsInstance(result, K8sReplicationController)
                self.assertEqual(rc, result)
                rcs.append(rc)
            self.assertEqual(count, len(rcs))

    # ------------------------------------------------------------------------------------- api - update

    def test_update_nonexistent(self):
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        if utils.is_reachable(rc.config.api_host):
            try:
                rc.update()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_update_name_fails(self):
        name = "yocontainer"
        container = utils.create_container(name=name)
        name1 = "yorc1"
        name2 = "yorc2"
        rc = utils.create_rc(name=name1)
        rc.add_container(container)
        if utils.is_reachable(rc.config.api_host):
            rc.create()
            result = K8sReplicationController.get_by_name(config=rc.config, name=name1)
            self.assertIsInstance(result, list)
            self.assertEqual(1, len(result))
            self.assertIsInstance(result[0], K8sReplicationController)
            result[0].name = name2
            try:
                result[0].update()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, BadRequestException)

    def test_update_namespace_fails(self):
        name = "yocontainer"
        container = utils.create_container(name=name)
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        nspace = "yonamespace"
        rc = utils.create_rc(name=name)
        rc.add_container(container)
        if utils.is_reachable(rc.config.api_host):
            rc.create()
            result = K8sReplicationController.get_by_name(config=rc.config, name=name)
            self.assertIsInstance(result, list)
            self.assertEqual(1, len(result))
            rc2 = result[0]
            self.assertIsInstance(rc2, K8sReplicationController)
            self.assertNotEqual(rc2.get_namespace(), nspace)
            self.assertEqual(rc, rc2)
            rc2.set_namespace(nspace)
            try:
                rc2.update()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, BadRequestException)

    def test_update_labels_succeeds(self):
        name = "yocontainer"
        container = utils.create_container(name=name)
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        rc.add_container(container)
        if utils.is_reachable(rc.config.api_host):
            rc.create()
            labels = rc.get_labels()
            labels['yomama'] = 'sofat'
            rc.set_labels(labels)
            rc.update()
            result = rc.get()
            self.assertIsInstance(result, K8sReplicationController)
            dico = result.get_labels()
            self.assertIsInstance(dico, dict)
            for k, v in labels.iteritems():
                self.assertEqual(dico[k], v)

    def test_update_add_container_succeeds(self):
        cont_names = ["yocontainer", "yocontainer2"]
        container = utils.create_container(name=cont_names[0])
        rc_name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=rc_name)
        rc.add_container(container)
        if utils.is_reachable(rc.config.api_host):
            rc.create()
            container = utils.create_container(name=cont_names[1])
            rc.add_container(container)
            result = rc.update()
            self.assertIsInstance(result, K8sReplicationController)
            self.assertEqual(result, rc)
            conts = result.get_pod_containers()
            self.assertIsInstance(conts, list)
            self.assertEqual(2, len(conts))
            for c in conts:
                self.assertIsInstance(c, dict)
                self.assertIn(c['name'], cont_names)

    # ------------------------------------------------------------------------------------- api - delete

    def test_delete_nonexistent(self):
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        if utils.is_reachable(rc.config.api_host):
            try:
                rc.delete()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_delete(self):
        name = "yocontainer"
        container = utils.create_container(name=name)
        name = "yopod-{0}".format(unicode(uuid.uuid4()))
        rc = utils.create_rc(name=name)
        rc.add_container(container)
        if utils.is_reachable(rc.config.api_host):
            rc.create()
            utils.cleanup_rcs()
            result = rc.list()
            self.assertIsInstance(result, list)
            self.assertEqual(0, len(result))
