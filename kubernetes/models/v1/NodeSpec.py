#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#
from kubernetes.utils import filter_model


class NodeSpec(object):
    """
    https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_nodespec
    """

    def __init__(self, model=None):
        super(NodeSpec, self).__init__()

        self._pod_cidr = None
        self._external_id = None
        self._provider_id = None
        self._unschedulable = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'podCIDR' in model:
            self.pod_cidr = model['podCIDR']
        if 'externalID' in model:
            self.external_id = model['externalID']
        if 'providerID' in model:
            self.provider_id = model['providerID']
        if 'unschedulable' in model:
            self.unschedulable = model['unschedulable']

    # ------------------------------------------------------------------------------------- pod cidr

    @property
    def pod_cidr(self):
        return self._pod_cidr

    @pod_cidr.setter
    def pod_cidr(self, cidr):
        if not isinstance(cidr, str):
            raise SyntaxError('NodeSpec: pod_cidr: [ {0} ] is invalid.'.format(cidr))
        self._pod_cidr = cidr

    # ------------------------------------------------------------------------------------- external id

    @property
    def external_id(self):
        return self._external_id

    @external_id.setter
    def external_id(self, external_id):
        if not isinstance(external_id, str):
            raise SyntaxError('NodeSpec: external_id: [ {0} ] is invalid.'.format(external_id))
        self._external_id = external_id

    # ------------------------------------------------------------------------------------- provider id

    @property
    def provider_id(self):
        return self._provider_id

    @provider_id.setter
    def provider_id(self, provider_id):
        if not isinstance(provider_id, str):
            raise SyntaxError('NodeSpec: provider_id: [ {0} ] is invalid.'.format(provider_id))
        self._provider_id = provider_id

    # ------------------------------------------------------------------------------------- unschedulable

    @property
    def unschedulable(self):
        return self._unschedulable

    @unschedulable.setter
    def unschedulable(self, value):
        if not isinstance(value, bool):
            raise SyntaxError('NodeSpec: unschedulable: [ {0} ] is invalid.'.format(value))
        self._unschedulable = value

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.pod_cidr:
            data['podCIDR'] = self.pod_cidr
        if self.external_id:
            data['externalID'] = self.external_id
        if self.provider_id:
            data['providerID'] = self.provider_id
        if self.unschedulable is not None:
            data['unschedulable'] = self.unschedulable
        return data
