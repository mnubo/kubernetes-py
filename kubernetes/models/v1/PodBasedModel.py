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

    # ------------------------------------------------------------------------------------- add

    def add_container(self, container):
        self.pod_spec.add_container(container=container)
        self._update_model()
        return self

    def add_host_volume(self, name, path):
        self.pod_spec.add_host_volume(name=name, path=path)
        self._update_model()
        return self

    def add_emptydir_volume(self, name):
        self.pod_spec.add_emptydir_volume(name=name)
        self._update_model()
        return self

    def add_image_pull_secrets(self, name):
        self.pod_spec.add_image_pull_secrets(name=name)
        self._update_model()
        return self

    def add_pod_annotation(self, k=None, v=None):
        self.pod_metadata.add_annotation(k=k, v=v)
        self._update_model()
        return self

    def add_pod_label(self, k=None, v=None):
        self.pod_metadata.add_label(k=k, v=v)
        self._update_model()
        return self

    # ------------------------------------------------------------------------------------- delete

    def del_pod_annotation(self, k):
        self.pod_metadata.del_annotation(k=k)
        self._update_model()
        return self

    def del_pod_label(self, k):
        self.pod_metadata.del_label(k=k)
        self._update_model()
        return self

    def del_pod_node_name(self):
        self.pod_spec.del_node_name()
        self._update_model()
        return self

    # ------------------------------------------------------------------------------------- get

    def get_pod_annotation(self, k):
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

    # ------------------------------------------------------------------------------------- set

    def set_active_deadline(self, seconds):
        self.pod_spec.set_active_deadline(seconds)
        self._update_model()
        return self

    def set_dns_policy(self, policy):
        self.pod_spec.set_dns_policy(policy=policy)
        self._update_model()
        return self

    def set_pod_annotations(self, new_dict):
        self.pod_metadata.set_annotations(dico=new_dict)
        self._update_model()
        return self

    def set_pod_generate_name(self, mode, name):
        self.pod_metadata.set_generate_name(mode=mode, name=name)
        self._update_model()
        return self

    def set_pod_labels(self, labels):
        self.pod_metadata.set_labels(labels=labels)
        self._update_model()
        return self

    def set_pod_image(self, name, image):
        self.pod_spec.set_container_image(name=name, image=image)
        self._update_model()

    def set_pod_name(self, name=None):
        self.pod_metadata.set_name(name=name)
        self._update_model()
        return self

    def set_pod_namespace(self, name=None):
        self.pod_metadata.set_namespace(name=name)
        self._update_model()
        return self

    def set_pod_node_name(self, name):
        self.pod_spec.set_node_name(name=name)
        self._update_model()
        return self

    def set_pod_node_selector(self, new_dict):
        self.pod_spec.set_node_selector(dico=new_dict)
        self._update_model()
        return self

    def set_pod_restart_policy(self, policy):
        self.pod_spec.set_restart_policy(policy=policy)
        self._update_model()
        return self

    def set_service_account(self, name):
        self.pod_spec.set_service_account(name=name)
        self._update_model()
        return self

    def set_termination_grace_period(self, seconds=None):
        self.pod_spec.set_termination_grace_period(seconds=seconds)
        self._update_model()
        return self
