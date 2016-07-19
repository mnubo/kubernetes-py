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
        pass
