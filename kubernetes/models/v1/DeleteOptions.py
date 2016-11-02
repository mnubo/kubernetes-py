#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import json
import yaml


class DeleteOptions(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_deleteoptions
    """

    def __init__(self):
        super(DeleteOptions, self).__init__()

        # TODO(froch): add support for the below.
        # self._preconditions = None

        self._kind = 'DeleteOptions'
        self._api_version = 'v1'
        self._grace_period_seconds = 0
        self._orphan_dependents = False

    # -------------------------------------------------------------------------------------  grace period seconds

    @property
    def grace_period_seconds(self):
        return self._grace_period_seconds

    @grace_period_seconds.setter
    def grace_period_seconds(self, secs=0):
        if not isinstance(secs, int):
            raise SyntaxError('DeleteOptions: grace_period_seconds: [ {0} ] is invalid.'.format(secs))
        self._grace_period_seconds = secs

    # -------------------------------------------------------------------------------------  serialize

    def serialize(self):
        data = {}
        data['kind'] = self._kind
        data['apiVersion'] = self._api_version
        data['gracePeriodSeconds'] = self._grace_period_seconds
        data['orphanDependents'] = self._orphan_dependents
        return data

    def as_json(self):
        data = self.serialize()
        j = json.dumps(data, indent=4)
        return j

    def as_yaml(self):
        data = self.serialize()
        y = yaml.dump(data, default_flow_style=False)
        return y
