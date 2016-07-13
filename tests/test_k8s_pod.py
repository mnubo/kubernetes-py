#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
from kubernetes import K8sPod, K8sConfig


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

    def test_init_with_name_check_model_as_dict(self):
        name = "yomama"
        pod = K8sPod(name=name)
        self.assertIsNotNone(pod)
        dico = pod.as_dict()
        self.assertIsNotNone(dico)
        self.assertIn('apiVersion', dico)
        self.assertIsInstance(dico['apiVersion'], str)
        self.assertIn('kind', dico)
        self.assertIsInstance(dico['kind'], str)
        self.assertIn('metadata', dico)
        self.assertIsInstance(dico['metadata'], dict)
        self.assertIn('labels', dico['metadata'])
        self.assertIsInstance(dico['metadata']['labels'], dict)
        self.assertIn('name', dico['metadata']['labels'])
        self.assertEqual(dico['metadata']['labels']['name'], name)
        self.assertIn('name', dico['metadata'])
        self.assertIsInstance(dico['metadata']['name'], str)
        self.assertEqual(dico['metadata']['name'], name)
        self.assertIn('namespace', dico['metadata'])
        self.assertIsInstance(dico['metadata']['namespace'], str)
        self.assertIn('spec', dico)
        self.assertIsInstance(dico['spec'], dict)
        self.assertIn('containers', dico['spec'])
        self.assertIsInstance(dico['spec']['containers'], list)
        self.assertIn('dnsPolicy', dico['spec'])
        self.assertIsInstance(dico['spec']['dnsPolicy'], str)
        self.assertIn('restartPolicy', dico['spec'])
        self.assertIsInstance(dico['spec']['restartPolicy'], str)
        self.assertIn('volumes', dico['spec'])
        self.assertIsInstance(dico['spec']['volumes'], list)

    def test_init_with_config_and_pull_secrets(self):
        ps = "yomama"
        name = "sofat"
        config = K8sConfig(pull_secret=ps)
        pod = K8sPod(config=config, name=name)
        self.assertIsNotNone(pod.config)
        self.assertEqual(ps, pod.config.pull_secret)



