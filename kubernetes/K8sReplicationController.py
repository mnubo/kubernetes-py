#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import uuid
import copy
import time
from kubernetes import K8sConfig
from kubernetes.K8sPodBasedObject import K8sPodBasedObject
from kubernetes.K8sPod import K8sPod
from kubernetes.K8sContainer import K8sContainer
from kubernetes.models.v1.ReplicationController import ReplicationController
from kubernetes.K8sExceptions import *

SCALE_WAIT_TIMEOUT_SECONDS = 60


class K8sReplicationController(K8sPodBasedObject):

    def __init__(self, config=None, name=None, image=None, replicas=0):
        K8sPodBasedObject.__init__(self, config=config, obj_type='ReplicationController', name=name)
        self.model = ReplicationController(name=name, namespace=self.config.namespace)
        self.set_replicas(replicas)

        rc_version = str(uuid.uuid4())
        self.model.add_pod_label(k='rc_version', v=rc_version)
        selector = {'name': name, 'rc_version': rc_version}
        self.set_selector(selector)

        if image is not None:
            container = K8sContainer(name=name, image=image)
            self.add_container(container)
            self.model.set_pod_name(name=name)

        if self.config.pull_secret is not None:
            self.add_image_pull_secrets(name=self.config.pull_secret)

    # -------------------------------------------------------------------------------------  add

    def add_annotation(self, k=None, v=None):
        self.model.add_annotation(k=k, v=v)
        return self

    def add_label(self, k=None, v=None):
        self.model.add_label(k=k, v=v)
        return self

    def add_pod_annotation(self, k=None, v=None):
        self.model.add_pod_annotation(k=k, v=v)
        return self

    def add_pod_label(self, k=None, v=None):
        self.model.add_pod_label(k=k, v=v)
        return self

    # -------------------------------------------------------------------------------------  del

    def del_annotation(self, k=None):
        self.model.del_annotation(k=k)
        return self

    def del_label(self, k=None):
        self.model.del_label(k=k)
        return self

    def del_pod_annotation(self, k=None):
        self.model.del_pod_annotation(k=k)
        return self

    def del_pod_label(self, k=None):
        self.model.del_pod_label(k=k)
        return self

    # -------------------------------------------------------------------------------------  get

    def get(self):
        self.model = ReplicationController(model=self.get_model())
        return self

    def get_annotation(self, k=None):
        return self.model.get_annotation(k=k)

    def get_annotations(self):
        return self.model.get_annotations()

    def get_label(self, k=None):
        return self.model.get_label(k=k)

    def get_labels(self):
        return self.model.get_labels()

    def get_namespace(self):
        return self.model.get_namespace()

    def get_pod_annotation(self, k=None):
        return self.model.get_pod_annotation(k=k)

    def get_pod_annotations(self):
        return self.model.get_pod_annotations()

    def get_pod_label(self, k=None):
        return self.model.get_pod_label(k=k)

    def get_pod_labels(self):
        return self.model.get_pod_labels()

    def get_replicas(self):
        return self.model.get_replicas()

    def get_selector(self):
        return self.model.get_selector()

    # -------------------------------------------------------------------------------------  set

    def set_annotations(self, dico=None):
        self.model.set_annotations(dico=dico)
        return self

    def set_labels(self, dico=None):
        self.model.set_labels(dico=dico)
        return self

    def set_namespace(self, name=None):
        self.model.set_namespace(name=name)
        return self

    def set_pod_annotations(self, dico=None):
        self.model.set_pod_annotations(new_dict=dico)
        return self

    def set_pod_labels(self, dico=None):
        self.model.set_pod_labels(dico=dico)
        return self

    def set_replicas(self, replicas=None):
        self.model.set_replicas(replicas=replicas)
        return self

    def set_selector(self, dico=None):
        self.model.set_selector(dico=dico)
        return self

    # -------------------------------------------------------------------------------------  wait for replicas

    def wait_for_replicas(self, replicas=None, labels=None):
        if replicas is None:
            raise SyntaxError('ReplicationController: replicas: [ {0} ] cannot be None.'.format(replicas))
        if not isinstance(replicas, int) or replicas < 0:
            raise SyntaxError('ReplicationController: replicas: [ {0} ] must be a positive integer.'.format(replicas))

        if labels is None:
            labels = self.get_pod_labels()

        name = labels.get('name', None)
        pod_list = list()
        pod_qty = len(pod_list)
        ready_check = False
        start_time = time.time()

        print('Waiting for replicas to scale to: [ {0} ] with labels: [ {1} ]'.format(replicas, labels))

        while not ((pod_qty == replicas) and ready_check):
            if labels is None:
                pod_list = K8sPod.get_by_name(config=self.config, name=name)
            else:
                pod_list = K8sPod.get_by_labels(config=self.config, labels=labels)

            pod_qty = len(pod_list)
            if replicas > 0:
                pods_ready = 0
                for pod in pod_list:
                    assert isinstance(pod, K8sPod)
                    if pod.is_ready():
                        pods_ready += 1
                if pods_ready == len(pod_list):
                    ready_check = True
            else:
                ready_check = True

            elapsed_time = time.time() - start_time
            if elapsed_time >= SCALE_WAIT_TIMEOUT_SECONDS:  # timeout
                raise TimedOutException("Timed out scaling replicas to: [ {0} ] with labels: [ {1} ]".format(replicas, labels))

            time.sleep(0.2)
        return self

    # -------------------------------------------------------------------------------------  get by name

    @staticmethod
    def get_by_name(config=None, name=None):
        if name is None:
            raise SyntaxError('ReplicationController: name: [ {0} ] cannot be None.'.format(name))
        if not isinstance(name, str):
            raise SyntaxError('ReplicationController: name: [ {0} ] must be a string.'.format(name))

        if config is not None and not isinstance(config, K8sConfig):
            raise SyntaxError('ReplicationController: config: [ {0} ] must be a K8sConfig'.format(config))

        rc_list = list()
        data = {'labelSelector': 'name={0}'.format(name)}
        rcs = K8sReplicationController(config=config, name=name).get_with_params(data=data)

        for rc in rcs:
            try:
                rc_name = ReplicationController(model=rc).get_name()
                rc_list.append(K8sReplicationController(config=config, name=rc_name).get())
            except NotFoundException:
                pass

        return rc_list

    # -------------------------------------------------------------------------------------  resize

    @staticmethod
    def resize(config=None, name=None, replicas=None):
        if name is None:
            raise SyntaxError('ReplicationController: name: [ {0} ] cannot be None.'.format(name))
        if replicas is None:
            raise SyntaxError('ReplicationController: replicas: [ {0} ] cannot be None.'.format(replicas))

        if not isinstance(name, str):
            raise SyntaxError('ReplicationController: name: [ {0} ] must be a string.'.format(name))

        if not isinstance(replicas, int) or replicas < 0:
            raise SyntaxError('ReplicationController: replicas: [ {0} ] must be a positive integer.'.format(replicas))

        if config is not None and not isinstance(config, K8sConfig):
            raise SyntaxError('ReplicationController: config: [ {0} ] must be a K8sConfig'.format(config))

        current_rc = K8sReplicationController(config=config, name=name).get()
        current_rc.set_replicas(replicas)
        current_rc.update()
        current_rc.wait_for_replicas(replicas=replicas)

        return current_rc

    # -------------------------------------------------------------------------------------  rolling update

    @staticmethod
    def rolling_update(config=None, name=None, image=None, container_name=None, new_rc=None, wait_seconds=10):
        next_rc_suffix = '-next'
        partner_annotation = 'update-partner'
        replicas_annotation = 'desired-replicas'
        next_name = name + next_rc_suffix
        phase = 'init'
        next_exists = False
        next_rc = None

        try:
            current_rc = K8sReplicationController(config=config, name=name).get()
            current_exists = True
        except NotFoundException:
            raise NotFoundException('RollingUpdate: Current replication controller does not exist.')

        try:
            next_rc = K8sReplicationController(config=config, name=next_name).get()
            next_exists = True
        except NotFoundException:
            pass

        if current_exists and not next_exists:
            try:
                if new_rc is not None:
                    next_rc = new_rc
                    next_rc.add_annotation(k=replicas_annotation, v=next_rc.get_replicas())
                else:
                    next_rc = copy.deepcopy(current_rc)
                    next_rc.add_annotation(k=replicas_annotation, v=current_rc.get_replicas())
                    if container_name is not None:
                        next_rc.set_image(name=container_name, image=image)
                    else:
                        next_rc.set_image(name=name, image=image)
                next_rc.set_name(name=next_name)
                next_rc.add_pod_label(k='name', v=name)
                my_version = str(uuid.uuid4())
                next_rc.add_pod_label(k='rc_version', v=my_version)
                next_rc.set_selector(dico=dict(name=name, rc_version=my_version))
                next_rc.set_replicas(replicas=0)
                next_rc.set_pod_generate_name(mode=True, name=name)
                next_rc.create()
            except Exception as e:
                message = "Got an exception of type {my_type} with message {my_msg}"\
                    .format(my_type=type(e), my_msg=e.message)
                raise Exception(message)
            try:
                current_rc.add_annotation(k=partner_annotation, v=next_name)
                current_rc.update()
            except Exception as e:
                message = "Got an exception of type {my_type} with message {my_msg}"\
                    .format(my_type=type(e), my_msg=e.message)
                raise Exception(message)
            phase = 'rollout'

        elif next_exists and not current_exists:
            phase = 'rename'

        elif current_exists and next_exists:
            if not next_rc.get_annotation(k=replicas_annotation):
                try:
                    next_rc.add_annotation(k=replicas_annotation, v=current_rc.get_replicas())
                    next_rc.update()
                except Exception as e:
                    message = "Got an exception of type {my_type} with message {my_msg}"\
                        .format(my_type=type(e), my_msg=e.message)
                    raise Exception(message)
            phase = 'rollout'

        if phase == 'rollout':
            desired_replicas = next_rc.get_annotation(k=replicas_annotation)
            try:
                while next_rc.get_replicas() < int(desired_replicas):
                    next_replicas = next_rc.get_replicas() + 1
                    next_rc.set_replicas(replicas=next_replicas)
                    next_rc.update()
                    next_rc.wait_for_replicas(replicas=next_replicas, labels=next_rc.get_pod_labels())
                    time.sleep(wait_seconds)
                    if current_rc.get_replicas() > 0:
                        current_replicas = current_rc.get_replicas() - 1
                        current_rc.set_replicas(replicas=current_replicas)
                        current_rc.update()
                        current_rc.wait_for_replicas(replicas=current_replicas, labels=current_rc.get_pod_labels())
                if current_rc.get_replicas() > 0:
                    current_rc.set_replicas(replicas=0)
                    current_rc.update()
                    current_rc.wait_for_replicas(replicas=0, labels=current_rc.get_pod_labels())

            except Exception as e:
                message = "Got an exception of type {my_type} with message {my_msg}"\
                    .format(my_type=type(e), my_msg=e.message)
                raise Exception(message)
            phase = 'rename'

        if phase == 'rename':
            try:
                current_rc.delete()
                current_rc = copy.deepcopy(next_rc)
                current_rc.set_name(name=name)
                current_rc.del_annotation(k=partner_annotation)
                current_rc.del_annotation(k=replicas_annotation)
                current_rc.create()
                next_rc.delete()
            except Exception as e:
                message = "Got an exception of type {my_type} with message {my_msg}"\
                    .format(my_type=type(e), my_msg=e.message)
                raise Exception(message)

        return current_rc
