#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest

from kubernetes.K8sCronJob import K8sCronJob
from tests import utils


class K8sCronJobTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sCronJob()
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
            K8sCronJob(config=config)

    def test_init_with_invalid_name(self):
        name = object()
        with self.assertRaises(SyntaxError):
            utils.create_cronjob(name=name)

    def test_init_with_name(self):
        name = "yomama"
        rc = utils.create_cronjob(name=name)
        self.assertIsNotNone(rc)
        self.assertIsInstance(rc, K8sCronJob)
        self.assertEqual(rc.name, name)
