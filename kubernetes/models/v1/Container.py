#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.ContainerPort import ContainerPort
from kubernetes.models.v1.EnvVar import EnvVar
from kubernetes.models.v1.Probe import Probe
from kubernetes.models.v1.ResourceRequirements import ResourceRequirements
from kubernetes.models.v1.SecurityContext import SecurityContext
from kubernetes.models.v1.VolumeMount import VolumeMount
from kubernetes.utils import is_valid_list, is_valid_string, filter_model


class Container(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_container
    """

    VALID_PULL_POLICIES = ['Always', 'Never', 'IfNotPresent']

    def __init__(self, model=None):
        super(Container, self).__init__()

        self._args = None
        self._command = None
        self._env = []
        self._image = None
        self._image_pull_policy = 'IfNotPresent'
        self._liveness_probe = None
        self._name = None
        self._ports = None
        self._readiness_probe = None
        self._resources = ResourceRequirements()
        self._security_context = SecurityContext()
        self._volume_mounts = []
        self._working_dir = None

        self.resources.requests = {
            'cpu': '100m',
            'memory': '32M'
        }

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def __eq__(self, other):
        # see https://github.com/kubernetes/kubernetes/blob/release-1.3/docs/design/identifiers.md
        if isinstance(other, self.__class__):
            # Uniquely name (via a name) an object across space.
            return self.name == other.name
        return NotImplemented

    def _build_with_model(self, model=None):
        if 'args' in model:
            self.args = model['args']
        if 'command' in model:
            self.command = model['command']
        if 'env' in model:
            envs = []
            for e in model['env']:
                env = EnvVar(e)
                envs.append(env)
            self.env = envs
        if 'image' in model:
            self.image = model['image']
        if 'imagePullPolicy' in model:
            self.image_pull_policy = model['imagePullPolicy']
        if 'livenessProbe' in model:
            self.liveness_probe = Probe(model['livenessProbe'])
        if 'name' in model:
            self.name = model['name']
        if 'ports' in model:
            ports = []
            for p in model['ports']:
                port = ContainerPort(p)
                ports.append(port)
            self.ports = ports
        if 'readinessProbe' in model:
            self.readiness_probe = Probe(model['readinessProbe'])
        if 'resources' in model:
            r = ResourceRequirements(model['resources'])
            self.resources = r
        if 'securityContext' in model:
            self.security_context = SecurityContext(model['securityContext'])
        if 'terminationMessagePath' in model:
            self.termination_message_path = model['terminationMessagePath']
        if 'volumeMounts' in model:
            mounts = []
            for v in model['volumeMounts']:
                mount = VolumeMount(v)
                mounts.append(mount)
            self.volume_mounts = mounts
        if 'workingDir' in model:
            self.working_dir = model['workingDir']

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
        if not is_valid_list(env, EnvVar):
            raise SyntaxError("Container: env: [ {0} ] is invalid.".format(env))
        self._env = env

    # ------------------------------------------------------------------------------------- image

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image=None):
        if not is_valid_string(image):
            raise SyntaxError('Container: image: [ {0} ] is invalid.'.format(image))
        self._image = image

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

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('Container: name: [ {0} ] is invalid.'.format(name))
        self._name = name

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

    # ------------------------------------------------------------------------------------- working dir
    @property
    def working_dir(self):
        return self._working_dir

    @working_dir.setter
    def working_dir(self, wdir=None):
        if not is_valid_string(wdir):
            raise SyntaxError('Container: working_dir: [ {0} ] is invalid.'.format(wdir))
        self._working_dir = wdir

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.args is not None:
            data['args'] = self.args
        if self.command is not None:
            data['command'] = self.command
        if self.env is not None:
            data['env'] = [x.serialize() for x in self.env]
        if self.image is not None:
            data['image'] = self.image
        if self.image_pull_policy is not None:
            data['imagePullPolicy'] = self.image_pull_policy
        if self.liveness_probe is not None:
            data['livenessProbe'] = self.liveness_probe.serialize()
        if self.name is not None:
            data['name'] = self.name
        if self.ports is not None:
            data['ports'] = [x.serialize() for x in self.ports]
        if self.resources is not None:
            data['resources'] = self.resources.serialize()
        if self.readiness_probe is not None:
            data['readinessProbe'] = self.readiness_probe.serialize()
        if self.security_context is not None:
            data['securityContext'] = self.security_context.serialize()
        if self.volume_mounts is not None:
            data['volumeMounts'] = [x.serialize() for x in self.volume_mounts]
        if self.working_dir is not None:
            data['workingDir'] = self.working_dir
        return data
