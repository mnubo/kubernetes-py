#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import copy
import time
import uuid

from kubernetes import K8sConfig
from kubernetes.K8sContainer import K8sContainer
from kubernetes.K8sExceptions import *
from kubernetes.K8sPod import K8sPod
from kubernetes.K8sPodBasedObject import K8sPodBasedObject
from kubernetes.models.v1.ReplicationController import ReplicationController

SCALE_WAIT_TIMEOUT_SECONDS = 60


class K8sReplicationController(K8sPodBasedObject):
    def __init__(self, config=None, name=None, image=None, replicas=0):
        super(K8sReplicationController, self).__init__(config=config, obj_type='ReplicationController', name=name)

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

    # -------------------------------------------------------------------------------------  override

    def create(self):
        super(K8sReplicationController, self).create()
        self.get()
        if self.get_replicas():
            self.scale(config=self.config, name=self.name, replicas=self.get_replicas())
        return self

    def update(self):
        super(K8sReplicationController, self).update()
        self.get()
        return self

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

    def set_annotations(self, annotations=None):
        self.model.set_annotations(dico=annotations)
        return self

    def set_labels(self, labels=None):
        self.model.set_labels(dico=labels)
        return self

    def set_namespace(self, name=None):
        self.model.set_namespace(name=name)
        return self

    def set_pod_annotations(self, annotations=None):
        self.model.set_pod_annotations(annotations=annotations)
        return self

    def set_pod_labels(self, labels=None):
        self.model.set_pod_labels(labels=labels)
        return self

    def set_replicas(self, replicas=None):
        self.model.set_replicas(replicas=replicas)
        return self

    def set_selector(self, selector=None):
        self.model.set_selector(dico=selector)
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
            pod_list = self._get_pods(name=name, labels=labels)
            pod_qty = len(pod_list)
            if replicas > 0:
                pods_ready = 0
                for pod in pod_list:
                    assert isinstance(pod, K8sPod)
                    try:
                        if pod.is_ready():
                            pods_ready += 1
                    except NotFoundException:
                        # while scaling down
                        pass
                if pods_ready >= len(pod_list):
                    ready_check = True
            else:
                ready_check = True

            elapsed_time = time.time() - start_time
            if elapsed_time >= SCALE_WAIT_TIMEOUT_SECONDS:  # timeout
                raise TimedOutException(
                    "Timed out scaling replicas to: [ {0} ] with labels: [ {1} ]".format(replicas, labels)
                )

            time.sleep(0.2)
        return self

    def _get_pods(self, name=None, labels=None):
        if labels is None:
            return K8sPod.get_by_name(config=self.config, name=name)
        else:
            return K8sPod.get_by_labels(config=self.config, labels=labels)

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
    def scale(config=None, name=None, replicas=None):
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
        current_labels = current_rc.get_pod_labels()
        current_rc.set_replicas(replicas)
        current_rc.update()
        current_rc.wait_for_replicas(replicas=replicas, labels=current_labels)

        return current_rc

    # -------------------------------------------------------------------------------------  rolling update

    @staticmethod
    def rolling_update(config=None, name=None, image=None, container_name=None, rc_new=None, wait_seconds=10):
        """
        Performs a simple rolling update of a ReplicationController.

        See https://github.com/kubernetes/kubernetes/blob/release-1.0/docs/design/simple-rolling-update.md
        for algorithm details.

        :param config: An instance of K8sConfig. If omitted, reads from ~/.kube/config.
        :param name: The name of the ReplicationController we want to update.
        :param image: The updated image version we want applied.
        :param container_name: The name of the container we're targeting for the update.
                               Required if more than one container is present.
        :param rc_new: An instance of K8sReplicationController with the new configuration to apply.
                       Mutually exclusive with [image, container_name] if specified.
        :param wait_seconds:

        :return:
        """

        if name is None:
            raise SyntaxError('K8sReplicationController: name: [ {0} ] cannot be None.'.format(name))
        if image is None and rc_new is None:
            raise SyntaxError("K8sReplicationController: please specify either 'image' or 'rc_new'")
        if name is not None and image is not None and rc_new is not None:
            raise SyntaxError(
                'K8sReplicationController: rc_new is mutually exclusive with a [image, container_name] pair.'
            )

        phase = 'init'
        ann_update_partner = 'update-partner'
        ann_desired_replicas = 'desired-replicas'

        name_next = "{0}-next".format(name)

        rc_current = None
        rc_next = None
        rc_current_exists = False
        rc_next_exists = False

        try:
            rc_current = K8sReplicationController(config=config, name=name).get()
            rc_current_exists = True
        except NotFoundException:
            pass

        try:
            rc_next = K8sReplicationController(config=config, name=name_next).get()
            rc_next_exists = True
        except NotFoundException:
            pass

        if not rc_current_exists and not rc_next_exists:
            raise NotFoundException('K8sReplicationController: rc: [ {0} ] does not exist.'.format(name))

        if rc_current_exists and not rc_next_exists:

            if rc_new is not None:
                rc_next = rc_new
                rc_next.add_annotation(k=ann_desired_replicas, v=str(rc_current.get_replicas()))

            else:
                rc_next = copy.deepcopy(rc_current)
                rc_next.add_annotation(k=ann_desired_replicas, v=str(rc_current.get_replicas()))

                if len(rc_next.model.pod_spec.containers) > 1 and not container_name:
                    raise UnprocessableEntityException(
                        'K8sReplicationController: unable to determine on which container to perform a rolling_update; '
                        'please specify the target container_name.'
                    )

                if len(rc_next.model.pod_spec.containers) == 1 and not container_name:
                    container_name = rc_next.model.pod_spec.containers[0].model['name']

                rc_next.set_container_image(name=container_name, image=image)

            my_version = str(uuid.uuid4())

            rc_next.set_name(name=name_next)
            rc_next.add_pod_label(k='name', v=name)
            rc_next.add_pod_label(k='rc_version', v=my_version)
            rc_next.set_selector(selector=dict(name=name, rc_version=my_version))
            rc_next.set_replicas(replicas=0)
            rc_next.set_pod_generate_name(mode=True, name=name)
            rc_next.create()

            rc_current.add_annotation(k=ann_update_partner, v=name_next)
            rc_current.update()

            phase = 'rollout'

        elif rc_next_exists and not rc_current_exists:
            phase = 'rename'

        elif rc_current_exists and rc_next_exists:
            if not rc_next.get_annotation(k=ann_desired_replicas):
                rc_next.add_annotation(k=ann_desired_replicas, v=rc_current.get_replicas())
                rc_next.update()
            phase = 'rollout'

        if phase == 'rollout':
            desired_replicas = rc_next.get_annotation(k=ann_desired_replicas)

            while rc_next.get_replicas() < int(desired_replicas):

                next_replicas = rc_next.get_replicas() + 1
                rc_next.set_replicas(replicas=next_replicas)
                rc_next.update()
                rc_next.wait_for_replicas(replicas=next_replicas, labels=rc_next.get_pod_labels())

                if rc_current.get_replicas() > 0:
                    current_replicas = rc_current.get_replicas() - 1
                    rc_current.set_replicas(replicas=current_replicas)
                    rc_current.update()
                    rc_current.wait_for_replicas(replicas=current_replicas, labels=rc_current.get_pod_labels())

            if rc_current.get_replicas() > 0:
                rc_current.set_replicas(replicas=0)
                rc_current.update()
                rc_current.wait_for_replicas(replicas=0, labels=rc_current.get_pod_labels())

            phase = 'rename'

        if phase == 'rename':
            rc_current.delete()
            new_version = str(uuid.uuid4())
            rc_current = copy.deepcopy(rc_next)
            rc_current.set_name(name=name)
            rc_current.add_pod_label(k='name', v=name)
            rc_current.add_pod_label(k='rc_version', v=new_version)
            rc_current.set_selector(selector=dict(name=name, rc_version=new_version))
            rc_current.del_annotation(k=ann_update_partner)
            rc_current.del_annotation(k=ann_desired_replicas)
            rc_current.create()
            rc_next.scale(config=rc_next.config, name=rc_next.name, replicas=0)
            rc_next.delete()

        return rc_current
