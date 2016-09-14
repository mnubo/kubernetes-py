#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1.Namespace import Namespace


class K8sNamespace(K8sObject):

    def __init__(self, config=None, name=None):

        if name is None:
            name = 'default'

        super(K8sNamespace, self).__init__(
            config=config, name=name, obj_type='Namespace')

        self.model = Namespace()
