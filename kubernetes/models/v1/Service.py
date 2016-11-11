#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1.ServiceSpec import ServiceSpec
from kubernetes.models.v1.ServiceStatus import ServiceStatus
from kubernetes.models.v1.ServicePort import ServicePort
from kubernetes.utils import is_valid_dict, is_valid_string


class Service(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_service
    """

    def __init__(self, model=None):
        super(Service, self).__init__()
        self.kind = 'Service'
        self.api_version = 'v1'

        self._metadata = ObjectMeta()
        self._spec = ServiceSpec()
        self._status = ServiceStatus()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'kind' in model:
            self.kind = model['kind']
        if 'apiVersion' in model:
            self.api_version = model['apiVersion']
        if 'metadata' in model:
            self.metadata = ObjectMeta(model=model['metadata'])
        if 'spec' in model:
            self.spec = ServiceSpec(model=model['spec'])
        if 'status' in model:
            self.status = ServiceStatus(model=model['status'])

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
        ports = self.spec.ports
        filtered = filter(lambda x: x.name == name, ports)
        inverse = filter(lambda x: x.name != name, ports)
        if not filtered:
            sp = ServicePort(name=name)
        else:
            sp = filtered[0]
        if port:
            sp.port = port
        if target_port:
            sp.target_port = target_port
        if protocol:
            sp.protocol = protocol
        if node_port:
            sp.node_port = node_port
        inverse.append(sp)
        self.spec.ports = inverse

    def add_selector(self, selector=None):
        if not is_valid_dict(selector):
            raise SyntaxError('Service.add_selector() selector: [ {} ] is invalid.'.format(selector))
        s = self.spec.selector
        if s is None:
            s = {}
        s.update(selector)
        self.spec.selector = s

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self.metadata.name

    @name.setter
    def name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('Service: name: [ {0} ] is invalid.'.format(name))
        self.metadata.name = name
        self.add_label('name', name)

    # ------------------------------------------------------------------------------------- metadata

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata=None):
        if not isinstance(metadata, ObjectMeta):
            raise SyntaxError('Service: metadata: [ {0} ] is invalid.'.format(metadata))
        self._metadata = metadata

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
        data = {}
        if self.kind:
            data['kind'] = self.kind
        if self.api_version:
            data['apiVersion'] = self.api_version
        if self.metadata is not None:
            data['metadata'] = self.metadata.serialize()
        if self.spec is not None:
            data['spec'] = self.spec.serialize()
        if self.status is not None:
            data['status'] = self.status.serialize()
        return data
