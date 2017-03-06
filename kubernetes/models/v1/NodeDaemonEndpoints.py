#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#
from kubernetes.models.v1.DaemonEndpoint import DaemonEndpoint
from kubernetes.utils import filter_model


class NodeDaemonEndpoints(object):
    """
    https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_nodedaemonendpoints
    """

    def __init__(self, model=None):
        super(NodeDaemonEndpoints, self).__init__()

        self._kubelet_endpoint = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'kubeletEndpoint' in model:
            self.kubelet_endpoint = DaemonEndpoint(model=model['kubeletEndpoint'])

    # ------------------------------------------------------------------------------------- type

    @property
    def kubelet_endpoint(self):
        return self._kubelet_endpoint

    @kubelet_endpoint.setter
    def kubelet_endpoint(self, v):
        if not isinstance(v, DaemonEndpoint):
            raise SyntaxError('NodeDaemonEndpoints: kubelet_endpoint: [ {0} ] is invalid.'.format(v))
        self._kubelet_endpoint = v

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.kubelet_endpoint:
            data['kubeletEndpoint'] = self.kubelet_endpoint.serialize()
        return data
