#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1.Service import Service
from kubernetes.K8sExceptions import NotFoundException


class K8sService(K8sObject):

    def __init__(self, config=None, name=None):
        super(K8sService, self).__init__(config=config, obj_type='Service', name=name)
        self.model = Service(name=name, namespace=self.config.namespace)

    # -------------------------------------------------------------------------------------  override

    def create(self):
        super(K8sService, self).create()
        self.get()
        return self

    def update(self):
        super(K8sService, self).update()
        self.get()
        return self

    # ------------------------------------------------------------------------------------- add

    def add_annotation(self, k=None, v=None):
        self.model.add_annotation(k=k, v=v)
        return self

    def add_label(self, k=None, v=None):
        self.model.add_label(k=k, v=v)
        return self

    def add_port(self, name=None, port=None, target_port=None, protocol=None, node_port=None):
        self.model.add_port(name=name, port=port, target_port=target_port, protocol=protocol, node_port=node_port)
        return self

    def add_selector(self, selector=None):
        self.model.add_selector(selector=selector)
        return self

    # ------------------------------------------------------------------------------------- del

    def del_meta_creation_timestamp(self):
        return self.model.del_meta_creation_timestamp()

    def del_meta_generation(self):
        return self.model.del_meta_generation()

    def del_meta_resource_version(self):
        return self.model.del_meta_resource_version()

    def del_meta_self_link(self):
        return self.model.del_meta_self_link()

    def del_meta_uid(self):
        return self.model.del_meta_uid()

    def del_server_generated_meta_attr(self):
        return self.model.del_server_generated_meta_attr()

    # ------------------------------------------------------------------------------------- get

    def get(self):
        self.model = Service(model=self.get_model())
        return self

    def get_annotation(self, k=None):
        return self.model.get_annotation(k=k)

    def get_annotations(self):
        return self.model.get_annotations()

    def get_cluster_ip(self):
        return self.model.get_cluster_ip()

    def get_external_ips(self):
        return self.model.get_external_ips()

    def get_label(self, k=None):
        return self.model.get_label(k=k)

    def get_labels(self):
        return self.model.get_labels()

    def get_meta_creation_timestamp(self):
        return self.model.get_meta_creation_timestamp()

    def get_meta_generation(self):
        return self.model.get_meta_generation()

    def get_meta_resource_version(self):
        return self.model.get_meta_resource_version()

    def get_meta_self_link(self):
        return self.model.get_meta_self_link()

    def get_meta_uid(self):
        return self.model.get_meta_uid()

    # ------------------------------------------------------------------------------------- set

    def set_annotations(self, dico=None):
        self.model.set_annotations(dico=dico)
        return self

    def set_cluster_ip(self, ip=None):
        self.model.set_cluster_ip(ip=ip)
        return self

    def set_external_ips(self, ips=None):
        self.model.set_external_ips(ips=ips)
        return self

    def set_labels(self, dico=None):
        self.model.set_labels(dico=dico)
        return self

    def set_load_balancer_ip(self, ip=None):
        self.model.set_load_balancer_ip(ip=ip)
        return self

    def set_namespace(self, name=None):
        self.model.set_namespace(name=name)
        return self

    def set_meta_creation_timestamp(self, ts=None):
        return self.model.set_meta_creation_timestamp(ts=ts)

    def set_meta_generation(self, gen=None):
        return self.model.set_meta_generation(gen=gen)

    def set_meta_resource_version(self, ver=None):
        return self.model.set_meta_resource_version(ver=ver)

    def set_meta_self_link(self, link=None):
        return self.model.set_meta_self_link(link=link)

    def set_meta_uid(self, uid=None):
        return self.model.set_meta_uid(uid=uid)

    def set_session_affinity(self, affinity_type=None):
        self.model.set_session_affinity(affinity_type=affinity_type)
        return self

    def set_service_type(self, service_type=None):
        self.model.set_service_type(service_type=service_type)
        return self

    # ------------------------------------------------------------------------------------- filter

    @staticmethod
    def get_by_name(config=None, name=None):
        service_list = list()
        data = dict(labelSelector="name={svc_name}".format(svc_name=name))
        services = K8sService(config=config, name=name).get_with_params(data=data)
        for svc in services:
            service_name = Service(model=svc).get_name()
            service_list.append(K8sService(config=config, name=service_name).get())
        return service_list
