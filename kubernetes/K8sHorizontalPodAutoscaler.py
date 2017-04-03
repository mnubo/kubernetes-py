#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject


class K8sHorizontalPodAutoscaler(K8sObject):

    def __init__(self):
        super(K8sHorizontalPodAutoscaler, self).__init__()

