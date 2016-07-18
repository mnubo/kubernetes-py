#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1.PodSpec import PodSpec
from kubernetes.models.v1.Container import Container


class PodBasedModel(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self.pod_spec = PodSpec()
        self.pod_metadata = ObjectMeta()
        self.pod_status = None

    def _update_model(self):
        self.model['metadata'] = self.pod_metadata.get()
        self.model['spec'] = self.pod_spec.get()
        if self.pod_status is not None:
            self.model['status'] = self.pod_status.get()
        return self

    def add_container(self, container):
        try:
            assert isinstance(container, Container)
            self.pod_spec.add_container(container=container)
        except:
            raise
        return self

    def add_host_volume(self, name, path):
        try:
            self.pod_spec.add_host_volume(name=name, path=path)
        except:
            raise
        return self

    def add_emptydir_volume(self, name):
        try:
            self.pod_spec.add_emptydir_volume(name=name)
        except:
            raise
        return self

    def add_image_pull_secrets(self, name):
        try:
            self.pod_spec.add_image_pull_secrets(name=name)
        except:
            raise
        return self

    def add_pod_annotation(self, k=None, v=None):
        try:
            assert isinstance(k, str)
            assert isinstance(v, str)
            self.pod_metadata.add_annotation(k=k, v=v)
        except:
            raise
        return self

    def add_pod_label(self, k=None, v=None):
        try:
            assert isinstance(k, str)
            assert isinstance(v, str)
            self.pod_metadata.add_label(k=k, v=v)
        except:
            raise
        return self

    def del_pod_annotation(self, k):
        assert isinstance(k, str)
        self.pod_metadata.del_annotation(k=k)
        return self

    def del_pod_label(self, k):
        assert isinstance(k, str)
        self.pod_metadata.del_label(k=k)
        return self

    def del_pod_node_name(self):
        self.pod_spec.del_node_name()
        return self

    def get_pod_annotation(self, k):
        assert isinstance(k, str)
        return self.pod_metadata.get_annotation(k=k)

    def get_pod_annotations(self):
        return self.pod_metadata.get_annotations()

    def get_pod_containers(self):
        my_list = list()
        for c in self.pod_spec.get_containers():
            assert isinstance(c, Container)
            my_list.append(c.get())
        return my_list

    def get_pod_label(self, k):
        assert isinstance(k, str)
        return self.pod_metadata.get_label(k=k)

    def get_pod_labels(self):
        return self.pod_metadata.get_labels()

    def get_pod_name(self):
        return self.pod_metadata.get_name()

    def get_pod_namespace(self):
        return self.pod_metadata.get_namespace()

    def get_pod_node_name(self):
        return self.pod_spec.get_node_name()

    def get_pod_node_selector(self):
        return self.pod_spec.get_node_selector()

    def get_pod_restart_policy(self):
        return self.pod_spec.get_restart_policy()

    def get_pod_status(self):
        return self.pod_status

    def get_service_account(self):
        return self.pod_spec.get_service_account()

    def get_termination_grace_period(self):
        return self.pod_spec.get_termination_grace_period()

    def set_active_deadline(self, seconds):
        try:
            self.pod_spec.set_active_deadline(seconds)
        except:
            raise
        return self

    def set_dns_policy(self, policy):
        try:
            self.pod_spec.set_dns_policy(policy=policy)
        except:
            raise
        return self

    def set_pod_annotations(self, new_dict):
        assert isinstance(new_dict, dict)
        self.pod_metadata.set_annotations(new_dict=new_dict)
        return self

    def set_pod_generate_name(self, mode, name):
        assert isinstance(mode, bool)
        if name is not None:
            assert isinstance(name, str)
        self.pod_metadata.set_generate_name(mode=mode, name=name)
        return self

    def set_pod_labels(self, new_dict):
        assert isinstance(new_dict, dict)
        self.pod_metadata.set_labels(new_dict=new_dict)
        return self

    def set_pod_image(self, name, image):
        assert isinstance(name, str)
        assert isinstance(image, str)
        self.pod_spec.set_image(name=name, image=image)

    def set_pod_name(self, name=None):
        assert isinstance(name, str)
        try:
            self.pod_metadata.set_name(name=name)
        except:
            raise
        return self

    def set_pod_namespace(self, name=None):
        try:
            assert isinstance(name, str)
            self.pod_metadata.set_namespace(name=name)
        except:
            raise
        return self

    def set_pod_node_name(self, name):
        self.pod_spec.set_node_name(name=name)
        return self

    def set_pod_node_selector(self, new_dict):
        self.pod_spec.set_node_selector(dico=new_dict)
        return self

    def set_pod_restart_policy(self, policy):
        try:
            self.pod_spec.set_restart_policy(policy=policy)
        except:
            raise
        return self

    def set_service_account(self, name):
        try:
            self.pod_spec.set_service_account(name=name)
        except:
            raise
        return self

    def set_termination_grace_period(self, seconds=None):
        try:
            self.pod_spec.set_termination_grace_period(seconds=seconds)
        except:
            raise
        return self
