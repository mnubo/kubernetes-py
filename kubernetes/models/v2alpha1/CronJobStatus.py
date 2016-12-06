#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


class CronJobStatus(object):

    def __init__(self, model=None):
        super(CronJobStatus, self).__init__()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        pass

    # -------------------------------------------------------------------------------------  serialize

    def serialize(self):
        data = {}
        return data
