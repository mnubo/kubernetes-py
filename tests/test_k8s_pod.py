#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
from kubernetes import K8sPod, K8sConfig
from kubernetes.models.v1 import Pod, ObjectMeta, PodSpec


class K8sPodTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # ------------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sPod()
            self.fail("Should have failed.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_name(self):
        name = "yomama"
        pod = K8sPod(name=name)
        self.assertIsNotNone(pod)
        self.assertIsInstance(pod, K8sPod)
        self.assertEqual(pod.name, name)

    def test_init_with_config_and_pull_secrets(self):
        ps = "yomama"
        name = "sofat"
        config = K8sConfig(pull_secret=ps)
        pod = K8sPod(config=config, name=name)
        self.assertIsNotNone(pod.config)
        self.assertEqual(ps, pod.config.pull_secret)

    # ------------------------------------------------------------------------------------- struct

    def test_struct_k8spod(self):
        name = "yomama"
        pod = K8sPod(name=name)
        self.assertIsNotNone(pod)
        self.assertIsInstance(pod, K8sPod)
        self.assertIsNotNone(pod.model)
        self.assertIsInstance(pod.model, Pod)

    def test_struct_pod(self):
        name = "yomama"
        pod = K8sPod(name=name)
        model = pod.model
        self.assertIsInstance(model.model, dict)
        self.assertIsInstance(model.pod_metadata, ObjectMeta)
        self.assertIsInstance(model.pod_spec, PodSpec)
        self.assertIsNone(model.pod_status)

    def test_struct_pod_model(self):
        name = "yomama"
        pod = K8sPod(name=name)
        model = pod.model
        self.assertIsInstance(model, Pod)
        self.assertIsNotNone(model)
        self.assertIn('apiVersion', model)
        self.assertIsInstance(model['apiVersion'], str)
        self.assertIn('kind', model)
        self.assertIsInstance(model['kind'], str)
        self.assertIn('metadata', model)
        self.assertIsInstance(model['metadata'], dict)
        self.assertIn('labels', model['metadata'])
        self.assertIsInstance(model['metadata']['labels'], dict)
        self.assertIn('name', model['metadata']['labels'])
        self.assertEqual(model['metadata']['labels']['name'], name)
        self.assertIn('name', model['metadata'])
        self.assertIsInstance(model['metadata']['name'], str)
        self.assertEqual(model['metadata']['name'], name)
        self.assertIn('namespace', model['metadata'])
        self.assertIsInstance(model['metadata']['namespace'], str)
        self.assertIn('spec', model)
        self.assertIsInstance(model['spec'], dict)
        self.assertIn('containers', model['spec'])
        self.assertIsInstance(model['spec']['containers'], list)
        self.assertIn('dnsPolicy', model['spec'])
        self.assertIsInstance(model['spec']['dnsPolicy'], str)
        self.assertIn('restartPolicy', model['spec'])
        self.assertIsInstance(model['spec']['restartPolicy'], str)
        self.assertIn('volumes', model['spec'])
        self.assertIsInstance(model['spec']['volumes'], list)




