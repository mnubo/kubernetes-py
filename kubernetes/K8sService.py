#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1.Service import Service


class K8sService(K8sObject):

    def __init__(self, config=None, name=None):
        super(K8sService, self).__init__(
            config=config,
            name=name,
            obj_type='Service'
        )

    # -------------------------------------------------------------------------------------  override

    def create(self):
        super(K8sService, self).create()
        self.get()
        return self

    def update(self):
        super(K8sService, self).update()
        self.get()
        return self

    def list(self, pattern=None):
        ls = super(K8sService, self).list()
        svcs = list(map(lambda x: Service(x), ls))
        if pattern is not None:
            svcs = list(filter(lambda x: pattern in x.name, svcs))
        k8s = []
        for x in svcs:
            j = K8sService(config=self.config, name=x.name)
            j.model = x
            k8s.append(j)
        return k8s

    # ------------------------------------------------------------------------------------- add

    def add_annotation(self, k=None, v=None):
        self.model.add_annotation(k=k, v=v)
        return self

    def add_label(self, k=None, v=None):
        self.model.add_label(k=k, v=v)
        return self

    def add_port(self, name=None, port=None, target_port=None, protocol=None, node_port=None):
        if isinstance(target_port, int):
            target_port = str(target_port)
        self.model.add_port(
            name=name,
            port=port,
            target_port=target_port,
            protocol=protocol,
            node_port=node_port
        )
        return self

    def add_selector(self, selector=None):
        self.model.add_selector(selector=selector)
        return self

    # ------------------------------------------------------------------------------------- get

    def get(self):
        self.model = Service(self.get_model())
        return self

    def get_annotation(self, k=None):
        if k in self.model.metadata.annotations:
            return self.model.metadata.annotations[k]
        return None

    def get_label(self, k=None):
        if k in self.model.metadata.labels:
            return self.model.metadata.labels[k]
        return None

    # ------------------------------------------------------------------------------------- clusterIP

    @property
    def cluster_ip(self):
        return self.model.spec.cluster_ip

    @cluster_ip.setter
    def cluster_ip(self, ip=None):
        self.model.spec.cluster_ip = ip

    # ------------------------------------------------------------------------------------- externalIPs

    @property
    def external_ips(self):
        return self.model.spec.external_ips

    @external_ips.setter
    def external_ips(self, ips=None):
        self.model.spec.external_ips = ips

    # ------------------------------------------------------------------------------------- loadBalancerIP

    @property
    def load_balancer_ip(self):
        return self.model.spec.load_balancer_ip

    @load_balancer_ip.setter
    def load_balancer_ip(self, ip=None):
        self.model.spec.load_balancer_ip = ip

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self.model.name

    @name.setter
    def name(self, name=None):
        self.model.name = name

    # ------------------------------------------------------------------------------------- namespace

    @property
    def namespace(self):
        return self.model.metadata.namespace

    @namespace.setter
    def namespace(self, nspace=None):
        self.model.metadata.namespace = nspace

    # ------------------------------------------------------------------------------------- ports

    @property
    def ports(self):
        return self.model.spec.ports

    @ports.setter
    def ports(self, ports=None):
        self.model.spec.ports = ports

    # ------------------------------------------------------------------------------------- sessionAffinity

    @property
    def session_affinity(self):
        return self.model.spec.session_affinity

    @session_affinity.setter
    def session_affinity(self, sa=None):
        self.model.spec.session_affinity = sa

    # ------------------------------------------------------------------------------------- selector

    @property
    def selector(self):
        return self.model.spec.selector

    @selector.setter
    def selector(self, s=None):
        self.model.spec.selector = s

    # ------------------------------------------------------------------------------------- type

    @property
    def type(self):
        return self.model.spec.type

    @type.setter
    def type(self, t=None):
        self.model.spec.type = t

    # ------------------------------------------------------------------------------------- filter

    @staticmethod
    def get_by_name(config=None, name=None):
        service_list = []
        data = {'labelSelector': 'name={}'.format(name)}
        services = K8sService(config=config, name=name).get_with_params(data=data)
        for svc in services:
            service_name = Service(svc).metadata.name
            service_list.append(K8sService(config=config, name=service_name).get())
        return service_list
