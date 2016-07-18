#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
from kubernetes import K8sReplicationController, K8sConfig
from kubernetes.models.v1 import ReplicationController, ObjectMeta, PodSpec


class K8sReplicationControllerTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sReplicationController()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_name(self):
        name = "yomama"
        rc = K8sReplicationController(name=name)
        self.assertIsNotNone(rc)
        self.assertIsInstance(rc, K8sReplicationController)
        self.assertEqual(rc.name, name)

    def test_init_with_config_and_pull_secrets(self):
        ps = "yomama"
        name = "sofat"
        config = K8sConfig(pull_secret=ps)
        pod = K8sReplicationController(config=config, name=name)
        self.assertIsNotNone(pod.config)
        self.assertEqual(ps, pod.config.pull_secret)

    # --------------------------------------------------------------------------------- struct

    def test_struct_k8s_rc(self):
        name = "yomama"
        rc = K8sReplicationController(name=name)
        self.assertIsNotNone(rc)
        self.assertIsInstance(rc, K8sReplicationController)
        self.assertIsNotNone(rc.model)
        self.assertIsInstance(rc.model, ReplicationController)

    def test_struct_rc(self):
        name = "yomama"
        pod = K8sReplicationController(name=name)
        model = pod.model
        self.assertIsInstance(model.model, dict)
        self.assertIsInstance(model.pod_metadata, ObjectMeta)
        self.assertIsInstance(model.pod_spec, PodSpec)
        self.assertIsNone(model.pod_status)
        self.assertIsInstance(model.rc_metadata, ObjectMeta)

    def test_struct_rc_model(self):
        name = "yomama"
        rc = K8sReplicationController(name=name)
        model = rc.model.model
        self.assertIsNotNone(model)
        self.assertIsInstance(model, dict)
        self.assertEqual(4, len(model))
        self.assertIn('apiVersion', model)
        self.assertIsInstance(model['apiVersion'], str)
        self.assertIn('kind', model)
        self.assertIsInstance(model['kind'], str)
        self.assertIn('metadata', model)
        self.assertIsInstance(model['metadata'], dict)
        self.assertEqual(3, len(model['metadata']))
        self.assertIn('labels', model['metadata'])
        self.assertIn('name', model['metadata']['labels'])
        self.assertIn('namespace', model['metadata'])
        self.assertIsInstance(model['metadata']['labels'], dict)
        self.assertEqual(1, len(model['metadata']['labels']))
        self.assertIn('name', model['metadata']['labels'])
        self.assertEqual(model['metadata']['labels']['name'], name)
        self.assertIsInstance(model['metadata']['name'], str)
        self.assertIsInstance(model['metadata']['namespace'], str)
        self.assertIn('name', model['metadata'])
        self.assertEqual(model['metadata']['name'], name)
        self.assertIn('spec', model)
        self.assertIsInstance(model['spec'], dict)
        self.assertEqual(3, len(model['spec']))
        self.assertIn('replicas', model['spec'])
        self.assertIn('selector', model['spec'])
        self.assertIn('template', model['spec'])
        self.assertIsInstance(model['spec']['replicas'], int)
        self.assertIsInstance(model['spec']['selector'], dict)
        self.assertEqual(2, len(model['spec']['selector']))
        self.assertIn('name', model['spec']['selector'])
        self.assertIn('rc_version', model['spec']['selector'])
        self.assertIsInstance(model['spec']['selector']['name'], str)
        self.assertIsInstance(model['spec']['selector']['rc_version'], str)
        self.assertIsInstance(model['spec']['template'], dict)
        self.assertEqual(2, len(model['spec']['template']))
        self.assertIn('metadata', model['spec']['template'])
        self.assertIn('spec', model['spec']['template'])
        self.assertIsInstance(model['spec']['template']['metadata'], dict)
        self.assertEqual(3, len(model['spec']['template']['metadata']))
        self.assertIn('labels', model['spec']['template']['metadata'])
        self.assertIn('name', model['spec']['template']['metadata'])
        self.assertIn('namespace', model['spec']['template']['metadata'])
        self.assertIsInstance(model['spec']['template']['metadata']['labels'], dict)
        self.assertEqual(2, len(model['spec']['template']['metadata']['labels']))
        self.assertIn('name', model['spec']['template']['metadata']['labels'])
        self.assertIn('rc_version', model['spec']['template']['metadata']['labels'])
        self.assertIsInstance(model['spec']['template']['metadata']['labels']['name'], str)
        self.assertIsInstance(model['spec']['template']['metadata']['labels']['rc_version'], str)
        self.assertIsInstance(model['spec']['template']['metadata']['name'], str)
        self.assertIsInstance(model['spec']['template']['metadata']['namespace'], str)
        self.assertIsInstance(model['spec']['template']['spec'], dict)
        self.assertEqual(4, len(model['spec']['template']['spec']))
        self.assertIn('containers', model['spec']['template']['spec'])
        self.assertIn('dnsPolicy', model['spec']['template']['spec'])
        self.assertIn('restartPolicy', model['spec']['template']['spec'])
        self.assertIn('volumes', model['spec']['template']['spec'])
        self.assertIsInstance(model['spec']['template']['spec']['containers'], list)
        self.assertIsInstance(model['spec']['template']['spec']['dnsPolicy'], str)
        self.assertIsInstance(model['spec']['template']['spec']['restartPolicy'], str)
        self.assertIsInstance(model['spec']['template']['spec']['volumes'], list)
        self.assertEqual(0, len(model['spec']['template']['spec']['containers']))
        self.assertEqual('Default', model['spec']['template']['spec']['dnsPolicy'])
        self.assertEqual('Always', model['spec']['template']['spec']['restartPolicy'])
        self.assertEqual(0, len(model['spec']['template']['spec']['volumes']))

    # --------------------------------------------------------------------------------- add annotation

    def test_add_annotation_none_args(self):
        pass
