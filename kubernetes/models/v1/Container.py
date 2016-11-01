#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1 import (
    ContainerPort,
    Probe,
    ResourceRequirements,
    SecurityContext,
    VolumeMount,
)
from kubernetes.utils import is_valid_list, is_valid_dict


class Container(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_container
    """

    VALID_PULL_POLICIES = ['Always', 'Never', 'IFNotPresent']

    def __init__(self, name=None, image=None):
        super(Container, self).__init__()

        self._args = None
        self._command = None
        self._env = None
        self._image_pull_policy = 'IfNotPresent'
        self._liveness_probe = None
        self._ports = None
        self._readiness_probe = None
        self._resources = None
        self._security_context = None
        self._volume_mounts = None

        self.image = image
        self.name = name
        self.working_dir = None

    # ------------------------------------------------------------------------------------- args

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, args=None):
        if not is_valid_list(args, str):
            raise SyntaxError('Container: args: [ {0} ] is invalid.'.format(args))
        self._args = args

    # ------------------------------------------------------------------------------------- command

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command=None):
        if not is_valid_list(command, str):
            raise SyntaxError('Container: command: [ {0} ] is invalid.'.format(command))
        self._command = command

    # ------------------------------------------------------------------------------------- env

    @property
    def env(self):
        return self._env

    @env.setter
    def env(self, env=None):
        msg = "Container: env: [ {0} ] is invalid.".format(env)
        if not is_valid_list(env, dict):
            raise SyntaxError(msg)
        for x in env:
            if not is_valid_dict(x, ['name', 'value']):
                raise SyntaxError(msg)
        self._env = env

    # ------------------------------------------------------------------------------------- image pull policy

    @property
    def image_pull_policy(self):
        return self._image_pull_policy

    @image_pull_policy.setter
    def image_pull_policy(self, policy=None):
        if policy not in Container.VALID_PULL_POLICIES:
            raise SyntaxError('Container: image_pull_policy: [ {0} ] is invalid.'.format(policy))
        self._image_pull_policy = policy

    # ------------------------------------------------------------------------------------- liveness probe

    @property
    def liveness_probe(self):
        return self._liveness_probe

    @liveness_probe.setter
    def liveness_probe(self, probe=None):
        if not isinstance(probe, Probe):
            raise SyntaxError('Container: liveness_probe: [ {0} ] is invalid.'.format(probe))
        self._liveness_probe = probe

    # ------------------------------------------------------------------------------------- ports

    @property
    def ports(self):
        return self._ports

    @ports.setter
    def ports(self, ports=None):
        if not is_valid_list(ports, ContainerPort):
            raise SyntaxError('Container: ports: [ {0} ] is invalid.'.format(ports))
        self._ports = ports

    # ------------------------------------------------------------------------------------- readiness probe

    @property
    def readiness_probe(self):
        return self._readiness_probe

    @readiness_probe.setter
    def readiness_probe(self, probe=None):
        if not isinstance(probe, Probe):
            raise SyntaxError('Container: readiness_probe: [ {0} ] is invalid.'.format(probe))
        self._readiness_probe = probe

    # ------------------------------------------------------------------------------------- resource requirements

    @property
    def resources(self):
        return self._resources

    @resources.setter
    def resources(self, resources=None):
        if not isinstance(resources, ResourceRequirements):
            raise SyntaxError('Container: resources: [ {0} ] is invalid.'.format(resources))
        self._resources = resources

    # ------------------------------------------------------------------------------------- security context

    @property
    def security_context(self):
        return self._security_context

    @security_context.setter
    def security_context(self, context=None):
        if not isinstance(context, SecurityContext):
            raise SyntaxError('Container: security_context: [ {0} ] is invalid.'.format(context))
        self._security_context = context

    # ------------------------------------------------------------------------------------- volume mounts

    @property
    def volume_mounts(self):
        return self._volume_mounts

    @volume_mounts.setter
    def volume_mounts(self, mounts=None):
        if not is_valid_list(mounts, VolumeMount):
            raise SyntaxError('Container: volume_mounts: [ {0} ] is invalid.'.format(mounts))
        self._volume_mounts = mounts

    # ------------------------------------------------------------------------------------- serialize

    def json(self):
        data = {}
        if self.args is not None:
            data['args'] = self.args
        if self.command is not None:
            data['command'] = self.command
        if self.env is not None:
            data['env'] = self.env
        if self.image is not None:
            data['image'] = self.image
        if self.image_pull_policy is not None:
            data['imagePullPolicy'] = self.image_pull_policy
        if self.liveness_probe is not None:
            data['livenessProbe'] = self.liveness_probe.json()
        if self.name is not None:
            data['name'] = self.name
        if self.ports is not None:
            data['ports'] = [x.json() for x in self.ports]
        if self.resources is not None:
            data['resources'] = self.resources.json()
        if self.readiness_probe is not None:
            data['readinessProbe'] = self.readiness_probe.json()
        if self.security_context is not None:
            data['securityContext'] = self.security_context.json()
        if self.volume_mounts is not None:
            data['volumeMounts'] = [x.json() for x in self.volume_mounts]
        if self.working_dir is not None:
            data['workingDir'] = self.working_dir
        return data
