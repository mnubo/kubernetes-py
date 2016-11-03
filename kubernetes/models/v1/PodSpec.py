#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.Container import Container
from kubernetes.models.v1.PodSecurityContext import PodSecurityContext
from kubernetes.models.v1.Volume import Volume
from kubernetes.utils import is_valid_list, filter_model


class PodSpec(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_podspec
    """

    VALID_DNS_POLICIES = ['ClusterFirst', 'Default']
    VALID_RESTART_POLICIES = ['Always', 'OnFailure', 'Never']

    def __init__(self, model=None):
        super(PodSpec, self).__init__()

        self._containers = []
        self._dns_policy = 'ClusterFirst'
        self._image_pull_secrets = []
        self._node_selector = {}
        self._restart_policy = 'Always'
        self._security_context = None
        self._volumes = []

        self.active_deadline_seconds = None
        self.host_ipc = False
        self.host_network = False
        self.host_pid = False
        self.hostname = None
        self.node_name = None

        self.service_account = None  # deprecated
        self.service_account_name = None
        self.subdomain = None
        self.termination_grace_period_seconds = 30

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'containers' in model:
            containers = []
            for c in model['containers']:
                container = Container(model=c)
                containers.append(container)
            self.containers = containers
        if 'dnsPolicy' in model:
            self.dns_policy = model['dnsPolicy']
        if 'nodeName' in model:
            self.node_name = model['nodeName']
        if 'restartPolicy' in model:
            self.restart_policy = model['restartPolicy']
        if 'securityContext' in model:
            self.security_context = PodSecurityContext(model=model['securityContext'])
        if 'serviceAccount' in model:
            self.service_account = model['serviceAccount']
        if 'serviceAccountName' in model:
            self.service_account_name = model['serviceAccountName']
        if 'terminationGracePeriodSeconds' in model:
            self.termination_grace_period_seconds = model['terminationGracePeriodSeconds']
        if 'volumes' in model:
            volumes = []
            for v in model['volumes']:
                volume = Volume(model=v)
                volumes.append(volume)
            self.volumes = volumes

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
        if not is_valid_list(secrets, str):
            raise SyntaxError('PodSpec: image_pull_secrets: [ {0} ] is invalid.'.format(secrets))
        self._image_pull_secrets = secrets

    # ------------------------------------------------------------------------------------- node selector

    @property
    def node_selector(self):
        return self._node_selector

    @node_selector.setter
    def node_selector(self, selector=None):
        if not isinstance(selector, dict):
            raise SyntaxError('PodSpec: node_selector: [ {0} ] is invalid.'.format(selector))
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

    # ------------------------------------------------------------------------------------- security context

    @property
    def security_context(self):
        return self._security_context

    @security_context.setter
    def security_context(self, context=None):
        if not isinstance(context, PodSecurityContext):
            raise SyntaxError('PodSpec: pod_security_context: [ {0} ] is invalid.'.format(context))
        self._security_context = context

    # ------------------------------------------------------------------------------------- volumes

    @property
    def volumes(self):
        return self._containers

    @volumes.setter
    def volumes(self, volumes=None):
        if not is_valid_list(volumes, Volume):
            raise SyntaxError('PodSpec: volumes: [ {0} ] is invalid.'.format(volumes))
        self._volumes = volumes

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.active_deadline_seconds:
            data['activeDeadlineSeconds'] = self.active_deadline_seconds
        if self.containers:
            data['containers'] = []
            for c in self.containers:
                data['containers'].append(c.serialize())
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
                data['volumes'].append(v.serialize())
        return data
