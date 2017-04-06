#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from tests.BaseTest import BaseTest
from kubernetes.K8sHorizontalPodAutoscaler import K8sHorizontalPodAutoscaler


class K8sJobTests(BaseTest):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_no_args(self):
        try:
            K8sHorizontalPodAutoscaler()
            self.fail("Should not fail.")
        except SyntaxError:
            pass
        except IOError:
            pass
        except Exception as err:
            self.fail("Unhandled exception: [ {0} ]".format(err.__class__.__name__))
