#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
from kubernetes.K8sPetSet import K8sPetSet
import utils


class K8sPetSetTests(unittest.TestCase):

    def setUp(self):
        utils.cleanup_petset()
        utils.cleanup_pods()

    def tearDown(self):
        utils.cleanup_petset()
        utils.cleanup_pods()

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sPetSet()
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
            K8sPetSet(config=config)

    def test_init_with_invalid_name(self):
        name = object()
        with self.assertRaises(SyntaxError):
            utils.create_petset(name=name)

    def test_init_with_name(self):
        name = "yomama"
        rc = utils.create_petset(name=name)
        self.assertIsNotNone(rc)
        self.assertIsInstance(rc, K8sPetSet)
        self.assertEqual(rc.name, name)
