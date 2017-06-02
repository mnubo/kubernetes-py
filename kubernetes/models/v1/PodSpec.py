#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.Container import Container
from kubernetes.models.v1.PodSecurityContext import PodSecurityContext
from kubernetes.models.v1.Volume import Volume
from kubernetes.utils import is_valid_list, filter_model, is_valid_string


class PodSpec(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_podspec
    """

    VALID_DNS_POLICIES = ['ClusterFirst', 'Default']
    VALID_RESTART_POLICIES = ['Always', 'OnFailure', 'Never']

    def __init__(self, model=None):
        super(PodSpec, self).__init__()

        self._active_deadline_seconds = None
        self._containers = []
        self._dns_policy = 'Default'
        self._host_ipc = None
        self._host_network = None
        self._host_pid = None
        self._hostname = None
        self._image_pull_secrets = None
        self._node_name = None
        self._node_selector = {}
        self._restart_policy = 'Always'
        self._security_context = None
        self._service_account = None  # deprecated
        self._service_account_name = None
        self._subdomain = None
        self._termination_grace_period_seconds = 30
        self._volumes = []

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'activeDeadlineSeconds' in model:
            self.active_deadline_seconds = model['activeDeadlineSeconds']
        if 'containers' in model:
            containers = []
            for c in model['containers']:
                container = Container(c)
                containers.append(container)
            self.containers = containers
        if 'dnsPolicy' in model:
            self.dns_policy = model['dnsPolicy']
        if 'hostIPC' in model:
            self.host_ipc = model['hostIPC']
        if 'hostNetwork' in model:
            self.host_network = model['hostNetwork']
        if 'hostPID' in model:
            self.host_pid = model['hostPID']
        if 'hostname' in model:
            self.hostname = model['hostname']
        if 'imagePullSecrets' in model:
            self.image_pull_secrets = model['imagePullSecrets']
        if 'nodeName' in model:
            self.node_name = model['nodeName']
        if 'nodeSelector' in model:
            self.node_selector = model['nodeSelector']
        if 'restartPolicy' in model:
            self.restart_policy = model['restartPolicy']
        if 'securityContext' in model:
            self.security_context = PodSecurityContext(model['securityContext'])
        if 'serviceAccount' in model:
            self.service_account = model['serviceAccount']
        if 'serviceAccountName' in model:
            self.service_account_name = model['serviceAccountName']
        if 'subdomain' in model:
            self.subdomain = model['subdomain']
        if 'terminationGracePeriodSeconds' in model:
            self.termination_grace_period_seconds = model['terminationGracePeriodSeconds']
        if 'volumes' in model:
            volumes = []
            for v in model['volumes']:
                volume = Volume(v)
                volumes.append(volume)
            self.volumes = volumes

    # ------------------------------------------------------------------------------------- add

    def add_container(self, container=None):
        if not isinstance(container, Container):
            raise SyntaxError('PodSpec.add_container90: container: [ {0} ] is invalid.'.format(container.__class__.__name__))
        self._containers.append(container)
        return self

    def add_volume(self, volume=None):
        if not isinstance(volume, Volume):
            raise SyntaxError('PodSpec.add_volume(): volume: [ {0} ] is invalid'.format(volume))
        self._volumes.append(volume)

    def add_image_pull_secrets(self, secrets=None):
        if not is_valid_list(secrets, dict):
            raise SyntaxError('PodSpec.add_image_pull_secrets() secrets : [ {0} ] is invalid.'.format(secrets))

        s = self.image_pull_secrets
        if s is None:
            l = secrets
        else:
            l = s + secrets

        self.image_pull_secrets = [dict(t) for t in set([tuple(d.items()) for d in l])]
        return self

    # ------------------------------------------------------------------------------------- del

    def del_node_name(self):
        self._node_name = None

    # ------------------------------------------------------------------------------------- active deadline seconds

    @property
    def active_deadline_seconds(self):
        return self._active_deadline_seconds

    @active_deadline_seconds.setter
    def active_deadline_seconds(self, secs=None):
        if not isinstance(secs, int):
            raise SyntaxError('PodSpec: active_deadline_seconds: [ {0} ] is invalid.'.format(secs))
        self._active_deadline_seconds = secs

    # ------------------------------------------------------------------------------------- containers

    @property
    def containers(self):
        return self._containers

    @containers.setter
    def containers(self, containers=None):
        if not is_valid_list(containers, Container):
            raise SyntaxError('PodSpec: containers: [ {0} ] is invalid.'.format(containers))
        self._containers = containers

    def set_container_image(self, name=None, image=None):
        if not is_valid_string(name):
            raise SyntaxError('PodSpec: name: [ {0} ] is invalid.')
        if not is_valid_string(image):
            raise SyntaxError('PodSpec: image: [ {0} ] is invalid.')
        for c in self.containers:
            if c.name == name:
                c.image(image=image)
                break
        return self

    # ------------------------------------------------------------------------------------- dnsPolicy

    @property
    def dns_policy(self):
        return self._dns_policy

    @dns_policy.setter
    def dns_policy(self, dns_policy=None):
        if dns_policy not in PodSpec.VALID_DNS_POLICIES:
            raise SyntaxError('PodSpec: dns_policy: [ {0} ] is invalid.'.format(dns_policy))
        self._dns_policy = dns_policy

    # ------------------------------------------------------------------------------------- hostIPC

    @property
    def host_ipc(self):
        return self._host_ipc

    @host_ipc.setter
    def host_ipc(self, ipc=None):
        if not isinstance(ipc, bool):
            raise SyntaxError('PodSpec: host_ipc: [ {0} ] is invalid.'.format(ipc))
        self._host_ipc = ipc

    # ------------------------------------------------------------------------------------- hostPID

    @property
    def host_pid(self):
        return self._host_pid

    @host_pid.setter
    def host_pid(self, pid=None):
        if not isinstance(pid, bool):
            raise SyntaxError('PodSpec: host_pid: [ {0} ] is invalid.'.format(pid))
        self._host_pid = pid

    # ------------------------------------------------------------------------------------- hostNetwork

    @property
    def host_network(self):
        return self._host_network

    @host_network.setter
    def host_network(self, hn=None):
        if not isinstance(hn, bool):
            raise SyntaxError('PodSpec: host_network: [ {0} ] is invalid.'.format(hn))
        self._host_network = hn

    # ------------------------------------------------------------------------------------- hostname

    @property
    def hostname(self):
        return self._hostname

    @hostname.setter
    def hostname(self, hn=None):
        if not is_valid_string(hn):
            raise SyntaxError('PodSpec: hostname: [ {0} ] is invalid.'.format(hn))
        self._hostname = hn

    # ------------------------------------------------------------------------------------- image pull secrets

    @property
    def image_pull_secrets(self):
        return self._image_pull_secrets

    @image_pull_secrets.setter
    def image_pull_secrets(self, secrets=None):
        if not is_valid_list(secrets, dict):
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
        self._node_selector = selector

    # ------------------------------------------------------------------------------------- node name

    @property
    def node_name(self):
        return self._node_name

    @node_name.setter
    def node_name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('PodSpec: node_name: [ {0} ] is invalid.'.format(name))
        self._node_name = name

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

    # ------------------------------------------------------------------------------------- service account name

    # TODO(froch): remove 'service_account' since it's deprecated.
    # We're leaving this in until 'serviceAccount' is rejected by the Kubernetes API server.
    # You should be using 'serviceAccountName'. We're forcing use of it under the hood.

    @property
    def service_account(self):
        return self._service_account_name

    @service_account.setter
    def service_account(self, san=None):
        if not is_valid_string(san):
            raise SyntaxError('PodSpec: service_account: [ {0} ] is invalid.'.format(san))
        self._service_account_name = san
        self._service_account = san

    @property
    def service_account_name(self):
        return self._service_account_name

    @service_account_name.setter
    def service_account_name(self, san=None):
        if not is_valid_string(san):
            raise SyntaxError('PodSpec: service_account_name: [ {0} ] is invalid.'.format(san))
        self._service_account_name = san
        self._service_account = san

    # ------------------------------------------------------------------------------------- subdomain

    @property
    def subdomain(self):
        return self._subdomain

    @subdomain.setter
    def subdomain(self, subdomain=None):
        if not is_valid_string(subdomain):
            raise SyntaxError('PodSpec: subdomain: [ {0} ] is invalid.'.format(subdomain))
        self._subdomain = subdomain

    # ------------------------------------------------------------------------------------- termination grace period

    @property
    def termination_grace_period_seconds(self):
        return self._termination_grace_period_seconds

    @termination_grace_period_seconds.setter
    def termination_grace_period_seconds(self, secs=None):
        if isinstance(secs, str) and secs.isdigit():
            secs = int(secs)
        if not isinstance(secs, int) or not secs >= 0:
            raise SyntaxError('PodSpec: termination_grace_period_seconds: [ {0} ] is invalid.'.format(secs))
        self._termination_grace_period_seconds = secs

    # ------------------------------------------------------------------------------------- volumes

    @property
    def volumes(self):
        return self._volumes

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
        if self.host_network is not None:
            data['hostNetwork'] = self.host_network
        if self.host_pid is not None:
            data['hostPID'] = self.host_pid
        if self.hostname:
            data['hostname'] = self.hostname
        if self.host_ipc is not None:
            data['hostIPC'] = self.host_ipc
        if self.image_pull_secrets:
            data['imagePullSecrets'] = self.image_pull_secrets
        if self.node_name:
            data['nodeName'] = self.node_name
        if self.node_selector:
            data['nodeSelector'] = self.node_selector
        if self.restart_policy:
            data['restartPolicy'] = self.restart_policy
        if self.service_account:
            data['serviceAccount'] = self.service_account
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
