#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import json

import yaml

from kubernetes.K8sVolumeMount import K8sVolumeMount
from kubernetes.models.v1.Capabilities import Capabilities
from kubernetes.models.v1.Container import Container
from kubernetes.models.v1.ContainerPort import ContainerPort
from kubernetes.models.v1.EnvVar import EnvVar
from kubernetes.models.v1.Probe import Probe
from kubernetes.models.v1.ResourceRequirements import ResourceRequirements


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
        if container_port is not None:
            p.container_port = container_port
        if host_port is not None:
            p.host_port = host_port
        if name is not None:
            p.name = name
        if protocol is not None:
            p.protocol = protocol
        if host_ip is not None:
            p.host_ip = host_ip

        ports = self.model.ports
        if ports is None:
            ports = []
        ports.append(p)

        self.model.ports = ports

    def add_env(self, name=None, value=None):
        e = {'name': name}

        if isinstance(value, dict):
            if 'valueFrom' in value and len(value) == 1:
                e['valueFrom'] = value['valueFrom']
        elif isinstance(value, str):
            e['value'] = value
        else:
            raise SyntaxError('K8sContainer.add_env() value: [ {} ] is invalid.')

        env_var = EnvVar(e)
        env = self.model.env
        if env is None:
            env = []
        env.append(env_var)
        self.model.env = env

    def add_volume_mount(self, mount=None):
        if not isinstance(mount, K8sVolumeMount):
            raise SyntaxError('K8sContainer.add_volume_mount() mount: [ {} ] is invalid.'.format(mount))
        mounts = self.model.volume_mounts
        if mount.model not in mounts:
            mounts.append(mount.model)
        self.model.volume_mounts = mounts

    def add_liveness_probe(self, **kwargs):
        if not isinstance(kwargs, dict):
            raise SyntaxError('K8sContainer: could not add liveness_probe: [ {} ]'.format(kwargs))
        probe = Probe(kwargs)
        self.liveness_probe = probe

    def add_readiness_probe(self, **kwargs):
        if not isinstance(kwargs, dict):
            raise SyntaxError('K8sContainer: could not add readiness_probe: [ {} ]'.format(kwargs))
        probe = Probe(kwargs)
        self.readiness_probe = probe

    def add_capabilities(self, c=None):
        cap = Capabilities({'add': c})
        self.capabilities = cap

    def drop_capabilities(self, c=None):
        cap = Capabilities({'drop': c})
        self.capabilities = cap

    # -------------------------------------------------------------------------------------  args

    @property
    def args(self):
        return self.model.args

    @args.setter
    def args(self, args=None):
        self.model.args = args

    # -------------------------------------------------------------------------------------  command

    @property
    def command(self):
        return self.model.command

    @command.setter
    def command(self, cmd=None):
        self.model.command = cmd

    # -------------------------------------------------------------------------------------  env

    @property
    def env(self):
        env = []
        for x in self.model.env:
            env.append(x)
        return env

    @env.setter
    def env(self, env=None):
        raise NotImplementedError()

    # -------------------------------------------------------------------------------------  ports

    @property
    def ports(self):
        return self.model.ports

    @ports.setter
    def ports(self, ports=None):
        self.model.ports = ports

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

    # -------------------------------------------------------------------------------------  resources

    @property
    def resources(self):
        return self.model.args

    @resources.setter
    def resources(self, res=None):
        r = ResourceRequirements(res)
        self.model.resources = r

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

    # -------------------------------------------------------------------------------------  capabilities

    @property
    def capabilities(self):
        return self.model.security_context.capabilities

    @capabilities.setter
    def capabilities(self, c=None):
        self.model.security_context.capabilities = c

    # -------------------------------------------------------------------------------------  seLinuxOptions

    @property
    def se_linux_options(self):
        return self.model.security_context.se_linux_options

    @se_linux_options.setter
    def se_linux_options(self, o=None):
        self.model.security_context.se_linux_options = o

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
