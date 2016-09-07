#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.Container import Container


class K8sContainer(object):
    def __init__(self, model=None, name=None, image=None):
        if model is not None:
            self.model = Container(model=model)
        else:
            if name is None:
                raise SyntaxError('K8sContainer: name: [ {0} ] cannot be None.'.format(name))
            if image is None:
                raise SyntaxError('K8sContainer: image: [ {0} ] cannot be None.'.format(image))
            self.model = Container(name=name, image=image)

    # -------------------------------------------------------------------------------------  add

    def add_port(self, container_port, host_port=None, protocol=None, name=None, host_ip=None):
        if host_port is not None:
            assert isinstance(host_port, int)
        if protocol is not None:
            assert isinstance(protocol, str)
        if name is not None:
            assert isinstance(name, str)
        if host_ip is not None:
            assert isinstance(host_ip, str)

        self.model.add_port(
            container_port=container_port,
            host_port=host_port,
            name=name,
            protocol=protocol,
            host_ip=host_ip
        )

        return self

    def add_env(self, k, v):
        assert isinstance(k, str)
        assert isinstance(v, str)
        self.model.add_env(name=k, value=v)
        return self

    def add_volume_mount(self, volume=None):
        self.model.add_volume_mount(volume)
        return self

    # -------------------------------------------------------------------------------------  get

    def get(self):
        return self

    def get_liveness_probe(self):
        return self.model.get_liveness_probe()

    def get_model(self):
        return self.model

    def get_readiness_probe(self):
        return self.model.get_readiness_probe()

    # -------------------------------------------------------------------------------------  set

    def set_arguments(self, args):
        assert isinstance(args, list)
        self.model.set_arguments(args=args)
        return self

    def set_command(self, cmd):
        assert isinstance(cmd, list)
        self.model.set_command(cmd=cmd)
        return self

    def set_host_network(self, mode):
        assert isinstance(mode, bool)
        self.model.set_host_network(mode=mode)
        return self

    def set_image(self, image=None):
        if image is None:
            raise SyntaxError("K8sContainer: image: [ {0} ] cannot be None.".format(image))
        if not isinstance(image, str):
            raise SyntaxError("K8sContainer: image: [ {0} ] must be a string.".format(image.__class__.__name__))
        self.model.set_image(image=image)
        return self

    def set_liveness_probe(self, **kwargs):
        self.model.set_liveness_probe(**kwargs)
        return self

    def set_name(self, name):
        assert isinstance(name, str)
        self.model.set_name(name=name)
        return self

    def set_privileged(self, mode):
        assert isinstance(mode, bool)
        self.model.set_privileged(mode=mode)
        return self

    def set_pull_policy(self, policy):
        assert isinstance(policy, str)
        self.model.set_pull_policy(policy=policy)
        return self

    def set_readiness_probe(self, **kwargs):
        self.model.set_readiness_probe(**kwargs)
        return self

    def set_requested_resources(self, cpu, mem):
        assert isinstance(cpu, str)
        assert isinstance(mem, str)
        self.model.set_requested_resources(cpu=cpu, mem=mem)
        return self

    def set_limit_resources(self, cpu, mem):
        assert isinstance(cpu, str)
        assert isinstance(mem, str)
        self.model.set_limit_resources(cpu=cpu, mem=mem)
        return self
