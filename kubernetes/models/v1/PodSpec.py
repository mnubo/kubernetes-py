#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.Container import Container
from kubernetes.models.v1.Volume import Volume


class PodSpec(object):

    VALID_DNS_POLICIES = ['ClusterFirst', 'Default']
    VALID_RESTART_POLICIES = ['Always', 'OnFailure', 'Never']

    def __init__(self):
        super(PodSpec, self).__init__()

        self._containers = []
        self._dns_policy = 'ClusterFirst'
        self._image_pull_secrets = []
        self._node_selector = {}
        self._restart_policy = 'Always'
        self._volumes = []

        self.active_deadline_seconds = None
        self.host_ipc = False
        self.host_network = False
        self.host_pid = False
        self.hostname = None
        self.node_name = None

        self.service_account_name = None
        self.subdomain = None
        self.termination_grace_period_seconds = 30

    # ------------------------------------------------------------------------------------- add

    def add_container(self, container=None):
        if not isinstance(container, Container):
            raise SyntaxError('PodSpec: container: [ {0} ] is invalid.'.format(container.__class__.__name__))
        self._containers.append(container)
        return self

    def add_volume(self, volume=None):
        if not isinstance(volume, Volume):
            raise SyntaxError('PodSpec: volume: [ {0} ] is invalid'.format(volume))
        self._volumes.append(volume)

    def add_image_pull_secrets(self, name=None):
        if not isinstance(name, str):
            raise SyntaxError('PodSpec: name: [ {0} ] is invalid.'.format(name))
        self._image_pull_secrets.append(name)
        return self

    # ------------------------------------------------------------------------------------- containers

    @property
    def containers(self):
        return self._containers

    @containers.setter
    def containers(self, containers=None):
        msg = 'PodSpec: containers: [ {0} ] is invalid.'.format(containers)
        if not isinstance(containers, list):
            raise SyntaxError(msg)
        try:
            for x in containers:
                assert isinstance(x, Container)
        except AssertionError:
            raise SyntaxError(msg)
        self._containers = containers

    def set_container_image(self, name=None, image=None):
        if name is None or not isinstance(name, str):
            raise SyntaxError('PodSpec: name: [ {0} ] is invalid.')
        if image is None or not isinstance(image, str):
            raise SyntaxError('PodSpec: image: [ {0} ] is invalid.')
        for c in self.containers:
            if c.name == name:
                c.image(image=image)
                break
        return self

    # ------------------------------------------------------------------------------------- DNS policy

    @property
    def dns_policy(self):
        return self._dns_policy

    @dns_policy.setter
    def dns_policy(self, dns_policy=None):
        if dns_policy not in PodSpec.VALID_DNS_POLICIES:
            raise SyntaxError('PodSpec: dns_policy: [ {0} ] is invalid.'.format(dns_policy))
        self._dns_policy = dns_policy

    # ------------------------------------------------------------------------------------- image pull secrets

    @property
    def image_pull_secrets(self):
        return self._image_pull_secrets

    @image_pull_secrets.setter
    def image_pull_secrets(self, secrets=None):
        msg = 'PodSpec: secrets: [ {0} ] is invalid.'.format(secrets)
        if not isinstance(secrets, list):
            raise SyntaxError(msg)
        for s in secrets:
            if not isinstance(s, str):
                raise SyntaxError(msg)
        self._image_pull_secrets = secrets

    # ------------------------------------------------------------------------------------- node selector

    @property
    def node_selector(self):
        return self._node_selector

    @node_selector.setter
    def node_selector(self, selector=None):
        if not isinstance(selector, dict):
            raise SyntaxError('PodSpec: Node selector: [ {0} ] is invalid.'.format(selector))
        self.node_selector = selector

    # ------------------------------------------------------------------------------------- restart policy

    @property
    def restart_policy(self):
        return self._restart_policy

    @restart_policy.setter
    def restart_policy(self, policy=None):
        if policy not in PodSpec.VALID_RESTART_POLICIES:
            raise SyntaxError('PodSpec: policy: [ {0} ] is invalid.'.format(policy))
        self._restart_policy = policy

    # ------------------------------------------------------------------------------------- volumes

    @property
    def volumes(self):
        return self._containers

    @volumes.setter
    def volumes(self, volumes=None):
        msg = 'PodSpec: volumes: [ {0} ] is invalid.'.format(volumes)
        if not isinstance(volumes, list):
            raise SyntaxError(msg)
        try:
            for x in volumes:
                assert isinstance(x, Volume)
        except AssertionError:
            raise SyntaxError(msg)
        self._volumes = volumes

    # ------------------------------------------------------------------------------------- serialize

    def json(self):
        data = {}
        if self.active_deadline_seconds:
            data['activeDeadlineSeconds'] = self.active_deadline_seconds
        if self.containers:
            data['containers'] = []
            for c in self.containers:
                data['containers'].append(c.json())
        if self.dns_policy:
            data['dnsPolicy'] = self.dns_policy
        if self.host_ipc:
            data['hostIPC'] = self.host_ipc
        if self.host_network:
            data['hostNetwork'] = self.host_network
        if self.host_pid:
            data['hostPID'] = self.host_pid
        if self.hostname:
            data['hostname'] = self.hostname
        if self.image_pull_secrets:
            data['imagePullSecrets'] = self.image_pull_secrets
        if self.node_name:
            data['nodeName'] = self.node_name
        if self.node_selector:
            data['nodeSelector'] = self.node_selector
        if self.restart_policy:
            data['restartPolicy'] = self.restart_policy
        if self.service_account_name:
            data['serviceAccountName'] = self.service_account_name
        if self.subdomain:
            data['subdomain'] = self.subdomain
        if self.termination_grace_period_seconds:
            data['terminationGracePeriodSeconds'] = self.termination_grace_period_seconds
        if self.volumes:
            data['volumes'] = []
            for v in self.volumes:
                data['volumes'].append(v.json())
        return data
