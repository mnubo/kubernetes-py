#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#
from kubernetes.models.v1.AttachedVolume import AttachedVolume
from kubernetes.models.v1.ContainerImage import ContainerImage
from kubernetes.models.v1.NodeAddress import NodeAddress
from kubernetes.models.v1.NodeCondition import NodeCondition
from kubernetes.models.v1.NodeDaemonEndpoints import NodeDaemonEndpoints
from kubernetes.models.v1.NodeSystemInfo import NodeSystemInfo
from kubernetes.utils import filter_model


class NodeStatus(object):
    """
    https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_nodestatus
    """

    def __init__(self, model=None):
        super(NodeStatus, self).__init__()

        self._capacity = None
        self._allocatable = None
        self._phase = None
        self._conditions = None
        self._addresses = None
        self._daemon_endpoints = None
        self._node_info = None
        self._images = None
        self._volumes_in_use = None
        self._volumes_attached = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'capacity' in model:
            self.capacity = model['capacity']
        if 'allocatable' in model:
            self.allocatable = model['allocatable']
        if 'phase' in model:
            self.phase = model['phase']
        if 'conditions' in model:
            if isinstance(model['conditions'], list):
                conditions = list()
                for c in model['conditions']:
                    conditions.append(NodeCondition(c))
                self.conditions = conditions
            else:
                raise SyntaxError('NodeStatus: conditions model: [ {0} ] is invalid.'.format(model['conditions']))
        if 'addresses' in model:
            if isinstance(model['addresses'], list):
                addresses = list()
                for a in model['addresses']:
                    addresses.append(NodeAddress(a))
                self.addresses = addresses
            else:
                raise SyntaxError('NodeStatus: addresses model: [ {0} ] is invalid.'.format(model['addresses']))
        if 'daemonEndpoints' in model:
            if isinstance(model['daemonEndpoints'], dict):
                self.daemon_endpoints = NodeDaemonEndpoints(model['daemonEndpoints'])
        if 'nodeInfo' in model:
            if isinstance(model['nodeInfo'], dict):
                self.node_info = NodeSystemInfo(model['nodeInfo'])
        if 'images' in model:
            if isinstance(model['images'], list):
                images = list()
                for i in model['images']:
                    images.append(ContainerImage(i))
                self.images = images
            else:
                raise SyntaxError('NodeStatus: images model: [ {0} ] is invalid.'.format(model['images']))
        if 'volumesInUse' in model:
            if isinstance(model['volumesInUse'], list):
                self.volumes_in_use = model['volumesInUse']
        if 'volumesAttached' in model:
            if isinstance(model['volumesAttached'], list):
                volumes = list()
                for v in model['volumesAttached']:
                    volumes.append(AttachedVolume(v))
                self.volumes_attached = volumes
            else:
                raise SyntaxError('NodeStatus: volumesAttached model: [ {0} ] is invalid.'
                                  .format(model['volumesAttached']))
            self.volumes_attached = model['volumesAttached']

    # ------------------------------------------------------------------------------------- capacity

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, v):
        if not isinstance(v, dict):
            raise SyntaxError('NodeStatus: capacity: [ {0} ] is invalid.'.format(v))
        self._capacity = v

    # ------------------------------------------------------------------------------------- allocatable

    @property
    def allocatable(self):
        return self._allocatable

    @allocatable.setter
    def allocatable(self, v):
        if not isinstance(v, dict):
            raise SyntaxError('NodeStatus: allocatable: [ {0} ] is invalid.'.format(v))
        self._allocatable = v

    # ------------------------------------------------------------------------------------- phase

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, v):
        if not isinstance(v, str):
            raise SyntaxError('NodeStatus: phase: [ {0} ] is invalid.'.format(v))
        self._phase = v

    # ------------------------------------------------------------------------------------- conditions

    @property
    def conditions(self):
        return self._conditions

    @conditions.setter
    def conditions(self, v):
        if not isinstance(v, list):
            raise SyntaxError('NodeStatus: conditions: [ {0} ] is invalid.'.format(v))
        self._conditions = v

    # ------------------------------------------------------------------------------------- addresses

    @property
    def addresses(self):
        return self._addresses

    @addresses.setter
    def addresses(self, v):
        if not isinstance(v, list):
            raise SyntaxError('NodeStatus: addresses: [ {0} ] is invalid.'.format(v))
        self._addresses = v

    # ------------------------------------------------------------------------------------- daemon endpoints

    @property
    def daemon_endpoints(self):
        return self._daemon_endpoints

    @daemon_endpoints.setter
    def daemon_endpoints(self, v):
        if not isinstance(v, NodeDaemonEndpoints):
            raise SyntaxError('NodeStatus: daemon_endpoints: [ {0} ] is invalid.'.format(v))
        self._daemon_endpoints = v

    # ------------------------------------------------------------------------------------- node info

    @property
    def node_info(self):
        return self._node_info

    @node_info.setter
    def node_info(self, v):
        if not isinstance(v, NodeSystemInfo):
            raise SyntaxError('NodeStatus: node_info: [ {0} ] is invalid.'.format(v))
        self._node_info = v

    # ------------------------------------------------------------------------------------- images

    @property
    def images(self):
        return self._images

    @images.setter
    def images(self, v):
        if not isinstance(v, list):
            raise SyntaxError('NodeStatus: images: [ {0} ] is invalid.'.format(v))
        self._images = v

    # ------------------------------------------------------------------------------------- volumes in use

    @property
    def volumes_in_use(self):
        return self._volumes_in_use

    @volumes_in_use.setter
    def volumes_in_use(self, v):
        if not isinstance(v, list):
            raise SyntaxError('NodeStatus: volumes_in_use: [ {0} ] is invalid.'.format(v))
        self._volumes_in_use = v

    # ------------------------------------------------------------------------------------- volumes attached

    @property
    def volumes_attached(self):
        return self._volumes_attached

    @volumes_attached.setter
    def volumes_attached(self, v):
        if not isinstance(v, AttachedVolume):
            raise SyntaxError('NodeStatus: volumes_attached: [ {0} ] is invalid.'.format(v))
        self._volumes_attached = v

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.capacity:
            data['capacity'] = self.capacity
        if self.allocatable:
            data['allocatable'] = self.allocatable
        if self.phase:
            data['phase'] = self.phase
        if self.conditions:
            l = list()
            for c in self.conditions:
                assert isinstance(c, NodeCondition)
                l.append(c.serialize())
            data['conditions'] = l
        if self.addresses:
            l = list()
            for a in self.addresses:
                assert isinstance(a, NodeAddress)
                l.append(a.serialize())
            data['addresses'] = l
        if self.daemon_endpoints:
            data['daemonEndpoints'] = self.daemon_endpoints.serialize()
        if self.node_info:
            data['nodeInfo'] = self.node_info.serialize()
        if self.images:
            l = list()
            for i in self.images:
                assert isinstance(i, ContainerImage)
                l.append(i.serialize())
            data['images'] = l
        if self.volumes_in_use:
            data['volumesInUse'] = self.volumes_in_use
        if self.volumes_attached:
            l = list()
            for v in self.volumes_attached:
                assert isinstance(v, AttachedVolume)
                l.append(v.serialize())
            data['volumesAttached'] = l
        return data
