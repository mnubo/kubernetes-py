#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject


class K8sDaemonSet(K8sObject):

    def __init__(self, config=None, name=None):
        super(K8sDaemonSet, self).__init__(
            config=config,
            name=name,
            obj_type='DaemonSet'
        )

