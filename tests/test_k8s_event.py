#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from tests.BaseTest import BaseTest
from kubernetes.K8sEvent import K8sEvent
from tests import _utils


class K8sEventTests(BaseTest):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_no_args(self):
        try:
            K8sEvent()
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
            K8sEvent(config=config)

    def test_init_with_invalid_name(self):
        name = object()
        try:
            _utils.create_event(name=name)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_name(self):
        name = "yomama"
        event = _utils.create_event(name=name)
        self.assertIsNotNone(event)
        self.assertIsInstance(event, K8sEvent)
        self.assertEqual(event.name, name)

    # --------------------------------------------------------------------------------- api - list

    def test_list(self):
        cfg = _utils.create_config()

        if _utils.is_reachable(cfg):
            objs = K8sEvent(config=cfg, name="yo").list()
            for x in objs:
                self.assertIsInstance(x, K8sEvent)
