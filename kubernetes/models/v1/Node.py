#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.unversioned.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1.NodeSpec import NodeSpec
from kubernetes.models.v1.NodeStatus import NodeStatus
from kubernetes.utils import filter_model


class Node(BaseModel):
    """
    https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_node
    """

    def __init__(self, model=None):
        super(Node, self).__init__()

        self.kind = 'Node'
        self.api_version = 'v1'

        self.spec = NodeSpec()
        self.status = NodeStatus()

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        super(Node, self).build_with_model(model)

        if 'spec' in model:
            self.spec = NodeSpec(model['spec'])
        if 'status' in model:
            self.status = NodeStatus(model['status'])

    # ------------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec=None):
        if not isinstance(spec, NodeSpec):
            raise SyntaxError('Node: spec: [ {0} ] is invalid.'.format(spec))
        self._spec = spec

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status=None):
        if not isinstance(status, NodeStatus):
            raise SyntaxError('Node: status: [ {0} ] is invalid.'.format(status))
        self._status = status

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(Node, self).serialize()
        if self.spec is not None:
            data['spec'] = self.spec.serialize()
        if self.status is not None:
            data['status'] = self.status.serialize()
        return data
