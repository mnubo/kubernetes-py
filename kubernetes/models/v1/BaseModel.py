#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

valid_versions = ['v1']


class BaseModel(object):

    def __init__(self):
        self.model = dict()

    def _update_model(self):
        return self

    def get(self):
        self._update_model()
        return self.model
