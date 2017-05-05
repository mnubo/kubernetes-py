#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.unversioned.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1.ServiceSpec import ServiceSpec
from kubernetes.models.v1.ServiceStatus import ServiceStatus
from kubernetes.models.v1.ServicePort import ServicePort
from kubernetes.utils import is_valid_dict, is_valid_string


class Service(BaseModel):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_service
    """

    def __init__(self, model=None):
        super(Service, self).__init__()

        self.kind = 'Service'
        self.api_version = 'v1'

        self.spec = ServiceSpec()
        self.status = ServiceStatus()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        super(Service, self).build_with_model(model)

        if 'spec' in model:
            self.spec = ServiceSpec(model['spec'])
        if 'status' in model:
            self.status = ServiceStatus(model['status'])

    # ------------------------------------------------------------------------------------- add

    def add_annotation(self, k=None, v=None):
        anns = self.metadata.annotations
        if anns is None:
            anns = {}
        anns.update({k: v})
        self.metadata.annotations = anns
        return self

    def add_label(self, k=None, v=None):
        labels = self.metadata.labels
        if labels is None:
            labels = {}
        labels.update({k: v})
        self.metadata.labels = labels
        return self

    def add_port(self, name=None, port=None, target_port=None, protocol=None, node_port=None):
        if not is_valid_string(name):
            raise SyntaxError('Service.add_port() name: [ {} ] is invalid.'.format(name))
        if port is None or not (isinstance(port, str) or isinstance(port, int)):
            raise SyntaxError('Service.add_port() port: [ {} ] is invalid.'.format(name))
        ports = []
        # exists previously
        for p in self.spec.ports:
            if int(p.port) == int(port):
                p.name = name
                p.target_port = target_port
                p.protocol = protocol
                p.node_port = node_port
            ports.append(p)
        # doesn't exist yet
        if int(port) not in [int(x.port) for x in ports]:
            p = ServicePort()
            p.name = name
            p.port = port
            p.target_port = target_port
            p.protocol = protocol
            p.node_port = node_port
            ports.append(p)
        self.spec.ports = ports

    def add_selector(self, selector=None):
        if not is_valid_dict(selector):
            raise SyntaxError('Service.add_selector() selector: [ {} ] is invalid.'.format(selector))
        s = self.spec.selector
        if s is None:
            s = {}
        s.update(selector)
        self.spec.selector = s

    # ------------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec=None):
        if not isinstance(spec, ServiceSpec):
            raise SyntaxError('Service: spec: [ {0} ] is invalid.'.format(spec))
        self._spec = spec

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status=None):
        if not isinstance(status, ServiceStatus):
            raise SyntaxError('Service: status: [ {0} ] is invalid.'.format(status))
        self._status = status

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(Service, self).serialize()

        if self.spec is not None:
            data['spec'] = self.spec.serialize()
        if self.status is not None:
            data['status'] = self.status.serialize()
        return data
