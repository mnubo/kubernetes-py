#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.unversioned import BaseModel


class HorizontalPodAutoscaler(BaseModel):

    def __init__(self):
        super(HorizontalPodAutoscaler, self).__init__()

