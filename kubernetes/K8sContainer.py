#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.Container import Container
from kubernetes.models.v1.ContainerPort import ContainerPort
from kubernetes.models.v1.VolumeMount import VolumeMount


class K8sContainer(object):
    """
    The K8sContainer object currently supports the default Kubernetes container runtime, ie. Docker.
    """

    def __init__(self, name=None, image=None):
        super(K8sContainer, self).__init__()
        self.model = Container()
        self.model.name = name
        self.model.image = image

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

    def add_volume_mount(self, name=None, mount_path=None, read_only=False, sub_path=None):
        mount = VolumeMount()
        mount.name = name
        mount.mount_path = mount_path
        mount.read_only = read_only
        mount.sub_path = sub_path

        mounts = self.model.volume_mounts
        if mounts is None:
            mounts = []
        mounts.append(mount)
        self.model.volume_mounts = mounts

    # -------------------------------------------------------------------------------------  serialize

    def json(self):
        return self.model.json()
