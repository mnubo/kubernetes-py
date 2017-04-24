#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest

from tests import _utils
from tests.BaseTest import BaseTest
from kubernetes.K8sPetSet import K8sPetSet


def should_skip():
    config = _utils.create_config()
    return _utils.assert_server_version(
        api_host=config.api_host,
        major=1, minor=4
    )


class K8sPetSetTests(BaseTest):

    def setUp(self):
        _utils.cleanup_petsets()
        _utils.cleanup_pods()

    def tearDown(self):
        _utils.cleanup_petsets()
        _utils.cleanup_pods()

    # --------------------------------------------------------------------------------- init

    @unittest.skipUnless(should_skip(), "Incorrect Server Version")
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

    @unittest.skipUnless(should_skip(), "Incorrect Server Version")
    def test_init_with_invalid_config(self):
        config = object()
        with self.assertRaises(SyntaxError):
            K8sPetSet(config=config)

    @unittest.skipUnless(should_skip(), "Incorrect Server Version")
    def test_init_with_invalid_name(self):
        name = object()
        with self.assertRaises(SyntaxError):
            _utils.create_petset(name=name)

    @unittest.skipUnless(should_skip(), "Incorrect Server Version")
    def test_init_with_name(self):
        name = "yomama"
        rc = _utils.create_petset(name=name)
        self.assertIsNotNone(rc)
        self.assertIsInstance(rc, K8sPetSet)
        self.assertEqual(rc.name, name)
