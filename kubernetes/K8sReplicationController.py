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
from kubernetes.K8sExceptions import *
from kubernetes.K8sObject import K8sObject
from kubernetes.K8sPod import K8sPod
from kubernetes.K8sContainer import K8sContainer

from kubernetes.models.v1.ReplicationController import ReplicationController
from kubernetes.utils import is_valid_string

SCALE_WAIT_TIMEOUT_SECONDS = 60


class K8sReplicationController(K8sObject):

    def __init__(self, config=None, name=None, replicas=0):

        super(K8sReplicationController, self).__init__(
            config=config,
            obj_type='ReplicationController',
            name=name
        )

        rc_version = str(uuid.uuid4())
        labels = {'name': name, 'rc_version': rc_version}

        self.labels = labels
        self.pod_labels = labels
        self.selector = labels
        self.replicas = replicas

        if self.config.pull_secret is not None:
            self.add_image_pull_secrets(name=self.config.pull_secret)

    # -------------------------------------------------------------------------------------  override

    def create(self):
        super(K8sReplicationController, self).create()
        self.wait_for_replicas()
        return self

    def update(self):
        super(K8sReplicationController, self).update()
        self.get()
        return self

    # -------------------------------------------------------------------------------------  add

    def add_annotation(self, k=None, v=None):
        anns = self.model.metadata.annotations
        if anns is None:
            anns = {}
        anns.update({k: v})
        self.model.metadata.annotations = anns
        return self

    def add_label(self, k=None, v=None):
        labels = self.model.metadata.labels
        if labels is None:
            labels = {}
        labels.update({k: v})
        self.model.metadata.labels = labels
        return self

    def add_pod_annotation(self, k=None, v=None):
        anns = self.model.spec.template.metadata.annotations
        if anns is None:
            anns = {}
        anns.update({k: v})
        self.model.spec.template.metadata.annotations = anns
        return self

    def add_pod_label(self, k=None, v=None):
        labels = self.model.spec.template.metadata.labels
        if labels is None:
            labels = {}
        labels.update({k: v})
        self.model.spec.template.metadata.labels = labels
        return self

    def add_container(self, container=None):
        if not isinstance(container, K8sContainer):
            raise SyntaxError('K8sReplicationController.add_container() container: [ {0} ] is invalid.'.format(container))
        containers = self.model.spec.template.spec.containers
        if container.model not in containers:
            containers.append(container.model)
        self.model.spec.template.spec.containers = containers
        return self

    def add_image_pull_secrets(self, name=None):
        self.model.spec.template.spec.add_image_pull_secrets(name)
        return self

    def add_volume(self, volume=None):
        self.model.add_volume(volume)
        return self

    # -------------------------------------------------------------------------------------  del

    def del_annotation(self, k=None):
        anns = self.model.metadata.annotations
        if k in anns:
            anns.pop(k)
            self.model.metadata.annotations = anns
        return self

    def del_label(self, k=None):
        labels = self.model.metadata.labels
        if k in labels:
            labels.pop(k)
            self.model.metadata.labels = labels
        return self

    def del_pod_annotation(self, k=None):
        anns = self.model.spec.template.metadata.annotations
        if k in anns:
            anns.pop(k)
            self.model.spec.template.metadata.annotations = anns
        return self

    def del_pod_label(self, k=None):
        labels = self.model.spec.template.metadata.labels
        if k in labels:
            labels.pop(k)
            self.model.spec.template.metadata.annotations = labels
        return self

    def del_pod_node_name(self):
        self.model.spec.template.spec.del_node_name()
        return self

    # -------------------------------------------------------------------------------------  get

    def get(self):
        self.model = ReplicationController(model=self.get_model())
        return self

    def get_annotation(self, k=None):
        if k in self.annotations:
            return self.annotations[k]
        return None

    def get_label(self, k=None):
        if k in self.labels:
            return self.labels[k]
        return None

    def get_pod_annotation(self, k=None):
        if k in self.pod_annotations:
            return self.pod_annotations[k]
        return None

    def get_pod_label(self, k=None):
        if k in self.pod_labels:
            return self.pod_labels[k]
        return None

    # -------------------------------------------------------------------------------------  annotations

    @property
    def annotations(self):
        return self.model.metadata.annotations

    @annotations.setter
    def annotations(self, anns=None):
        self.model.metadata.annotations = anns

    # -------------------------------------------------------------------------------------  activeDeadlineSeconds

    @property
    def active_deadline(self):
        return self.model.spec.template.spec.active_deadline_seconds

    @active_deadline.setter
    def active_deadline(self, secs=None):
        self.model.spec.template.spec.active_deadline_seconds = secs

    # -------------------------------------------------------------------------------------  containers

    @property
    def containers(self):
        objs = []
        for c in self.model.spec.template.spec.containers:
            k8scontainer = K8sContainer(name=c.name, image=c.image)
            k8scontainer.model = c
            objs.append(k8scontainer)
        return objs

    @containers.setter
    def containers(self, containers=None):
        models = []
        for obj in containers:
            models.append(obj.model)
        self.model.spec.template.spec.containers = models

    # -------------------------------------------------------------------------------------  container_image

    @property
    def container_image(self, name=None):
        if name is None and len(self.containers) > 1:
            raise SyntaxError("K8sReplicationController.container_image() Please specify a container name.")

        if len(self.containers) == 1:
            return self.containers[0].image
        else:
            filtered = filter(lambda x: x.name == name, self.containers)
            if filtered:
                return filtered[0].image
            return None

    @container_image.setter
    def container_image(self, tup=None):
        if not isinstance(tup, tuple):
            raise SyntaxError('K8sReplicationController.container_image() must be a tuple of the form (name, image)')
        name, image = tup
        found = filter(lambda x: x.name == name, self.containers)
        if found:
            new = filter(lambda x: x.name != name, self.containers)
            found[0].image = image
            new.append(found[0])
            self.containers = new

    # -------------------------------------------------------------------------------------  image pull secrets

    @property
    def image_pull_secrets(self):
        return self.model.spec.template.spec.image_pull_secrets

    @image_pull_secrets.setter
    def image_pull_secrets(self, secrets=None):
        self.model.spec.template.spec.image_pull_secrets = secrets

    # -------------------------------------------------------------------------------------  labels

    @property
    def labels(self):
        return self.model.metadata.labels

    @labels.setter
    def labels(self, labels=None):
        self.model.metadata.labels = labels

    # -------------------------------------------------------------------------------------  name

    @property
    def name(self):
        return self.model.metadata.name

    @name.setter
    def name(self, name=None):
        self.model.metadata.name = name
        self.model.metadata.labels['name'] = name

    # -------------------------------------------------------------------------------------  namespace

    @property
    def namespace(self):
        return self.model.metadata.namespace

    @namespace.setter
    def namespace(self, nspace=None):
        self.model.metadata.namespace = nspace

    # -------------------------------------------------------------------------------------  node selector

    @property
    def pod_node_selector(self):
        return self.model.spec.template.spec.node_selector

    @pod_node_selector.setter
    def pod_node_selector(self, sel=None):
        self.model.spec.template.spec.node_selector = sel

    # -------------------------------------------------------------------------------------  pod annotations

    @property
    def pod_annotations(self):
        return self.model.spec.template.metadata.annotations

    @pod_annotations.setter
    def pod_annotations(self, anns=None):
        self.model.spec.template.metadata.annotations = anns

    # -------------------------------------------------------------------------------------  pod labels

    @property
    def pod_labels(self):
        return self.model.spec.template.metadata.labels

    @pod_labels.setter
    def pod_labels(self, labels=None):
        self.model.spec.template.metadata.labels = labels

    # -------------------------------------------------------------------------------------  pod generate name

    @property
    def pod_generate_name(self):
        return self.model.spec.template.metadata.generate_name

    @pod_generate_name.setter
    def pod_generate_name(self, name=None):
        self.model.spec.template.metadata.generate_name = name

    # -------------------------------------------------------------------------------------  pod name

    @property
    def pod_name(self):
        return self.model.spec.template.metadata.name

    @pod_name.setter
    def pod_name(self, name=None):
        self.model.spec.template.metadata.name = name

    # -------------------------------------------------------------------------------------  pod node name

    @property
    def pod_node_name(self):
        return self.model.spec.template.spec.node_name

    @pod_node_name.setter
    def pod_node_name(self, name=None):
        self.model.spec.template.spec.node_name = name

    # -------------------------------------------------------------------------------------  replicas

    @property
    def replicas(self):
        return self.model.spec.replicas

    @replicas.setter
    def replicas(self, reps=None):
        self.model.spec.replicas = reps

    # -------------------------------------------------------------------------------------  restartPolicy

    @property
    def restart_policy(self):
        return self.model.spec.template.spec.restart_policy

    @restart_policy.setter
    def restart_policy(self, policy=None):
        self.model.spec.template.spec.restart_policy = policy

    # -------------------------------------------------------------------------------------  selector

    @property
    def selector(self):
        return self.model.spec.selector

    @selector.setter
    def selector(self, selector=None):
        self.model.spec.selector = selector

    # -------------------------------------------------------------------------------------  serviceAccountName

    @property
    def service_account_name(self):
        return self.model.spec.template.spec.service_account_name

    @service_account_name.setter
    def service_account_name(self, acct=None):
        self.model.spec.template.spec.service_account_name = acct

    # -------------------------------------------------------------------------------------  terminationGracePeriod

    @property
    def termination_grace_period(self):
        return self.model.spec.template.spec.termination_grace_period_seconds

    @termination_grace_period.setter
    def termination_grace_period(self, secs=None):
        self.model.spec.template.spec.termination_grace_period_seconds = secs

    # -------------------------------------------------------------------------------------  wait for replicas

    def wait_for_replicas(self, replicas=None, labels=None):

        if replicas is None:
            replicas = self.replicas
        if labels is None:
            labels = self.labels

        name = labels.get('name', None)
        pod_list = list()
        pod_qty = len(pod_list)
        ready_check = False
        start_time = time.time()

        print('Waiting for replicas to scale to: [ {0} ] with pod labels: [ {1} ]'.format(replicas, labels))

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
        if config is not None and not isinstance(config, K8sConfig):
            raise SyntaxError('ReplicationController.get_by_name(): config: [ {0} ] is invalid.'.format(config))
        if not is_valid_string(name):
            raise SyntaxError('K8sReplicationController.get_by_name() name: [ {0} ] is invalid.'.format(name))

        rc_list = []
        data = {'labelSelector': 'name={0}'.format(name)}
        rcs = K8sReplicationController(config=config, name=name).get_with_params(data=data)

        for rc in rcs:
            try:
                model = ReplicationController(model=rc)
                obj = K8sReplicationController(config=config, name=model.metadata.name)
                rc_list.append(obj.get())
            except NotFoundException:
                pass

        return rc_list

    # -------------------------------------------------------------------------------------  resize

    @staticmethod
    def scale(config=None, name=None, replicas=None):
        """
        Scales the number of pods in the specified K8sReplicationController to the desired replica count.

        :param config: an instance of K8sConfig
        :param name: the name of the ReplicationController we want to scale.
        :param replicas: the desired number of replicas.

        :return: An instance of K8sReplicationController
        """

        current_rc = K8sReplicationController(config=config, name=name).get()
        current_labels = current_rc.pod_labels
        current_rc.replicas = replicas
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
                rc_next.add_annotation(k=ann_desired_replicas, v=str(rc_current.replicas))

            else:
                rc_next = copy.deepcopy(rc_current)
                rc_next.add_annotation(k=ann_desired_replicas, v=str(rc_current.replicas))

                if len(rc_next.containers) > 1 and not container_name:
                    raise UnprocessableEntityException(
                        'K8sReplicationController: unable to determine on which container to perform a rolling_update; '
                        'please specify the target container_name.'
                    )

                if len(rc_next.containers) == 1 and not container_name:
                    container_name = rc_next.containers[0].model.name

                rc_next.container_image = (container_name, image)

            my_version = str(uuid.uuid4())

            rc_next.name = name_next
            rc_next.add_pod_label(k='name', v=name)
            rc_next.add_pod_label(k='rc_version', v=my_version)
            rc_next.selector = {'name': name, 'rc_version': my_version}
            rc_next.replicas = 0
            rc_next.pod_generate_name = name
            rc_next.create()

            rc_current.add_annotation(k=ann_update_partner, v=name_next)
            rc_current.update()

            phase = 'rollout'

        elif rc_next_exists and not rc_current_exists:
            phase = 'rename'

        elif rc_current_exists and rc_next_exists:
            if not rc_next.get_annotation(k=ann_desired_replicas):
                rc_next.add_annotation(k=ann_desired_replicas, v=rc_current.replicas)
                rc_next.update()
            phase = 'rollout'

        if phase == 'rollout':
            desired_replicas = rc_next.get_annotation(k=ann_desired_replicas)

            while rc_next.replicas < int(desired_replicas):

                next_replicas = rc_next.replicas + 1
                rc_next.replicas = next_replicas
                rc_next.update()
                rc_next.wait_for_replicas(replicas=next_replicas, labels=rc_next.pod_labels)

                if rc_current.replicas > 0:
                    current_replicas = rc_current.replicas - 1
                    rc_current.replicas = current_replicas
                    rc_current.update()
                    rc_current.wait_for_replicas(replicas=current_replicas, labels=rc_current.pod_labels)

            if rc_current.replicas > 0:
                rc_current.replicas = 0
                rc_current.update()
                rc_current.wait_for_replicas(replicas=0, labels=rc_current.pod_labels)

            phase = 'rename'

        if phase == 'rename':
            rc_current.delete()
            new_version = str(uuid.uuid4())
            rc_current = copy.deepcopy(rc_next)
            rc_current.name = name
            rc_current.add_pod_label(k='name', v=name)
            rc_current.add_pod_label(k='rc_version', v=new_version)
            rc_current.selector = {'name': name, 'rc_version': new_version}
            rc_current.del_annotation(k=ann_update_partner)
            rc_current.del_annotation(k=ann_desired_replicas)
            rc_current.create()
            rc_next.scale(config=rc_next.config, name=rc_next.name, replicas=0)
            rc_next.delete()

        return rc_current
