#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import json
import yaml

from kubernetes.K8sVolumeMount import K8sVolumeMount
from kubernetes.models.v1.Container import Container
from kubernetes.models.v1.ContainerPort import ContainerPort
from kubernetes.models.v1.Probe import Probe


class K8sContainer(object):
    """
    The K8sContainer object currently supports the default Kubernetes container runtime, ie. Docker.
    """

    def __init__(self, name=None, image=None):
        super(K8sContainer, self).__init__()
        self.model = Container()
        self.name = name
        self.image = image

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.model.name == other.model.name and self.model.image == other.model.image
        return NotImplemented

    # -------------------------------------------------------------------------------------  add

    def add_port(self, container_port=None, host_port=None, name=None, protocol=None, host_ip=None):
        p = ContainerPort()
        p.container_port = container_port
        p.host_port = host_port
        p.name = name
        p.protocol = protocol
        p.host_ip = host_ip
        ports = self.model.ports
        if ports is None:
            ports = []
        ports.append(p)
        self.model.ports = ports

    def add_env(self, name=None, value=None):
        e = {'name': name, 'value': value}
        env = self.model.env
        if env is None:
            env = []
        env.append(e)
        self.model.env = env

    def add_volume_mount(self, mount=None):
        if not isinstance(mount, K8sVolumeMount):
            raise SyntaxError('K8sContainer.add_volume_mount() mount: [ {} ] is invalid.'.format(mount))
        mounts = self.model.volume_mounts
        if mount.model not in mounts:
            mounts.append(mount.model)
        self.model.volume_mounts = mounts

    def add_liveness_probe(self, **kwargs):
        probe = Probe(model=kwargs)
        self.liveness_probe = probe

    def add_readiness_probe(self, **kwargs):
        probe = Probe(model=kwargs)
        self.readiness_probe = probe

    # -------------------------------------------------------------------------------------  livenessProbe

    @property
    def liveness_probe(self):
        return self.model.liveness_probe

    @liveness_probe.setter
    def liveness_probe(self, probe=None):
        self.model.liveness_probe = probe

    # -------------------------------------------------------------------------------------  readinessProbe

    @property
    def readiness_probe(self):
        return self.model.readiness_probe

    @readiness_probe.setter
    def readiness_probe(self, probe=None):
        self.model.readiness_probe = probe

    # -------------------------------------------------------------------------------------  name

    @property
    def name(self):
        return self.model.name

    @name.setter
    def name(self, name=None):
        self.model.name = name

    # -------------------------------------------------------------------------------------  image

    @property
    def image(self):
        return self.model.image

    @image.setter
    def image(self, image=None):
        self.model.image = image

    # -------------------------------------------------------------------------------------  volume_mounts

    @property
    def volume_mounts(self):
        return self.model.volume_mounts

    @volume_mounts.setter
    def volume_mounts(self, mounts=None):
        self.model.volume_mounts = mounts

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        return self.model.serialize()

    def as_json(self):
        data = self.serialize()
        dump = json.dumps(data, indent=4)
        return dump

    def as_yaml(self):
        data = self.serialize()
        dump = yaml.dump(data, default_flow_style=False)
        return dump
