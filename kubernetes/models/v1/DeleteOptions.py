#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import json
import yaml

from kubernetes.utils import is_valid_string


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

    # -------------------------------------------------------------------------------------  kind

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, k=0):
        if not is_valid_string(k):
            raise SyntaxError('DeleteOptions: kind: [ {0} ] is invalid.'.format(k))
        self._kind = k

    # -------------------------------------------------------------------------------------  apiVersion

    @property
    def api_version(self):
        return self._api_version

    @api_version.setter
    def api_version(self, v=0):
        if not is_valid_string(v):
            raise SyntaxError('DeleteOptions: api_version: [ {0} ] is invalid.'.format(v))
        self._kind = v

    # -------------------------------------------------------------------------------------  grace period seconds

    @property
    def grace_period_seconds(self):
        return self._grace_period_seconds

    @grace_period_seconds.setter
    def grace_period_seconds(self, secs=0):
        if not isinstance(secs, int):
            raise SyntaxError('DeleteOptions: grace_period_seconds: [ {0} ] is invalid.'.format(secs))
        self._grace_period_seconds = secs

    # -------------------------------------------------------------------------------------  orphanDependents

    @property
    def orphan_dependents(self):
        return self._orphan_dependents

    @orphan_dependents.setter
    def orphan_dependents(self, orphan=False):
        if not isinstance(orphan, bool):
            raise SyntaxError('DeleteOptions: orphan_dependents: [ {0} ] is invalid.'.format(orphan))
        self._orphan_dependents = orphan

    # -------------------------------------------------------------------------------------  serialize

    def serialize(self):
        data = {}
        if self.kind is not None:
            data['kind'] = self.kind
        if self.api_version is not None:
            data['apiVersion'] = self.api_version
        if self.grace_period_seconds is not None:
            data['gracePeriodSeconds'] = self.grace_period_seconds
        if self.orphan_dependents is not None:
            data['orphanDependents'] = self.orphan_dependents
        return data

    def as_json(self):
        data = self.serialize()
        j = json.dumps(data, indent=4)
        return j

    def as_yaml(self):
        data = self.serialize()
        y = yaml.dump(data, default_flow_style=False)
        return y
