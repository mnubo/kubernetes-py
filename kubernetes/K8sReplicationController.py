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
from kubernetes.K8sObject import K8sObject
from kubernetes.K8sPod import K8sPod
from kubernetes.K8sVolume import K8sVolume
from kubernetes.models.v1.Probe import Probe
from kubernetes.models.v1.ReplicationController import ReplicationController
from kubernetes.utils import is_valid_string


class K8sReplicationController(K8sObject):

    SCALE_WAIT_TIMEOUT_SECONDS = 600
    DESIRED_REPLICAS_ANNOTATION = 'kubernetes.io/desired-replicas'

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
        self.desired_replicas = replicas

        if config is not None and config.pull_secret is not None:
            self.add_image_pull_secrets(config.pull_secret)

    # -------------------------------------------------------------------------------------  override

    def create(self):
        # _hash = base64.b64encode(self.as_json())
        # self.add_annotation('kubernetes.io/deployment', _hash)
        super(K8sReplicationController, self).create()
        self._wait_for_desired_replicas()
        return self

    def update(self):
        # _hash = base64.b64encode(self.as_json())
        # self.add_annotation('kubernetes.io/deployment', _hash)
        super(K8sReplicationController, self).update()
        self._wait_for_desired_replicas()
        return self

    def list(self, pattern=None):
        ls = super(K8sReplicationController, self).list()
        rcs = list(map(lambda x: ReplicationController(x), ls))
        if pattern is not None:
            rcs = list(filter(lambda x: pattern in x.name, rcs))
        k8s = []
        for x in rcs:
            j = K8sReplicationController(config=self.config, name=x.name)
            j.model = x
            k8s.append(j)
        return k8s

    # -------------------------------------------------------------------------------------  add

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
            raise SyntaxError(
                'K8sReplicationController.add_container() container: [ {0} ] is invalid.'.format(container))

        containers = self.model.spec.template.spec.containers
        if containers is None:
            containers = []
        filtered = list(filter(lambda x: x.name != container.name, containers))
        filtered.append(container.model)
        self.model.spec.template.spec.containers = filtered
        return self

    def add_image_pull_secrets(self, secrets=None):
        self.model.spec.template.spec.add_image_pull_secrets(secrets)
        return self

    def add_volume(self, volume=None):
        if not isinstance(volume, K8sVolume):
            raise SyntaxError(
                'K8sReplicationController.add_volume() volume: [ {0} ] is invalid.'.format(volume))

        volumes = self.model.spec.template.spec.volumes
        if volume.model not in volumes:
            volumes.append(volume.model)
        self.model.spec.template.spec.volumes = volumes
        return self

    # -------------------------------------------------------------------------------------  del

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
        self.model = ReplicationController(self.get_model())
        return self

    def get_pod_annotation(self, k=None):
        if k in self.pod_annotations:
            return self.pod_annotations[k]
        return None

    def get_pod_label(self, k=None):
        if k in self.pod_labels:
            return self.pod_labels[k]
        return None

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
    def container_image(self):
        data = {}
        for c in self.containers:
            data[c.name] = c.image
        return data

    @container_image.setter
    def container_image(self, tup=None):
        if not isinstance(tup, tuple):
            raise SyntaxError(
                'K8sReplicationController.container_image() must be a tuple of the form (name, image)')

        name, image = tup
        found = list(filter(lambda x: x.name == name, self.containers))
        if found:
            new = list(filter(lambda x: x.name != name, self.containers))
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

    # -------------------------------------------------------------------------------------  namespace

    @property
    def namespace(self):
        return self.model.metadata.namespace

    @namespace.setter
    def namespace(self, nspace=None):
        self.model.metadata.namespace = nspace

    # -------------------------------------------------------------------------------------  nodeSelector

    @property
    def node_selector(self):
        return self.model.spec.template.spec.node_selector

    @node_selector.setter
    def node_selector(self, sel=None):
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
        self.model.spec.template.metadata.labels['name'] = name

    # -------------------------------------------------------------------------------------  pod node name

    @property
    def pod_node_name(self):
        return self.model.spec.template.spec.node_name

    @pod_node_name.setter
    def pod_node_name(self, name=None):
        self.model.spec.template.spec.node_name = name

    # -------------------------------------------------------------------------------------  desiredReplicas

    @property
    def desired_replicas(self):
        return self.model.spec.replicas

    @desired_replicas.setter
    def desired_replicas(self, reps=None):
        self.model.spec.replicas = reps

    # -------------------------------------------------------------------------------------  dnsPolicy

    @property
    def dns_policy(self):
        return self.model.spec.template.spec.dns_policy

    @dns_policy.setter
    def dns_policy(self, policy='Default'):
        self.model.spec.template.spec.dns_policy = policy

    # -------------------------------------------------------------------------------------  observedReplicas

    @property
    def current_replicas(self):
        return self.model.status.replicas

    @current_replicas.setter
    def current_replicas(self, reps=None):
        self.model.status.replicas = reps

    # -------------------------------------------------------------------------------------  livenessProbes

    @property
    def liveness_probes(self):
        data = {}
        containers = self.model.spec.template.spec.containers
        for c in containers:
            if c.liveness_probe is not None:
                data[c.name] = c.liveness_probe
        return data

    @liveness_probes.setter
    def liveness_probes(self, tup=None):
        if not isinstance(tup, tuple):
            raise SyntaxError(
                'K8sReplicationController: liveness_probes: [ {} ] is invalid.'.format(tup))

        c_name, probe = tup
        container_names = [c.name for c in self.model.spec.template.spec.containers]

        if c_name not in container_names:
            raise SyntaxError(
                'K8sReplicationController: liveness_probes: container [ {} ] not found.'.format(c_name))
        if not isinstance(probe, Probe):
            raise SyntaxError(
                'K8sReplicationController: liveness_probe: probe: [ {} ] is invalid.'.format(probe))

        containers = []
        for c in self.model.spec.template.spec.containers:
            if c.name == c_name:
                c.liveness_probe = probe
            containers.append(c)
        self.model.spec.template.spec.containers = containers

    # -------------------------------------------------------------------------------------  readinessProbes

    @property
    def readiness_probes(self):
        data = {}
        containers = self.model.spec.template.spec.containers
        for c in containers:
            if c.readiness_probe is not None:
                data[c.name] = c.readiness_probe
        return data

    @readiness_probes.setter
    def readiness_probes(self, tup=None):
        if not isinstance(tup, tuple):
            raise SyntaxError(
                'K8sReplicationController: readiness_probes: [ {} ] is invalid.'.format(tup))

        c_name, probe = tup
        container_names = [c.name for c in self.model.spec.template.spec.containers]

        if c_name not in container_names:
            raise SyntaxError(
                'K8sReplicationController: readiness_probes: container [ {} ] not found.'.format(c_name))
        if not isinstance(probe, Probe):
            raise SyntaxError(
                'K8sReplicationController: readiness_probes: probe: [ {} ] is invalid.'.format(probe))

        containers = []
        for c in self.model.spec.template.spec.containers:
            if c.name == c_name:
                c.readiness_probe = probe
            containers.append(c)
        self.model.spec.template.spec.containers = containers

    # -------------------------------------------------------------------------------------  readyReplicas

    @property
    def ready_replicas(self):
        return self.model.status.ready_replicas

    @ready_replicas.setter
    def ready_replicas(self, reps=None):
        self.model.status.ready_replicas = reps

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

    # -------------------------------------------------------------------------------------  volumes

    @property
    def volumes(self):
        return self.model.spec.template.spec.volumes

    @volumes.setter
    def volumes(self, v=None):
        self.model.spec.template.spec.volumes = v

    # -------------------------------------------------------------------------------------  wait

    def _wait_for_desired_replicas(self):
        start_time = time.time()
        is_ready = False
        while not is_ready:
            time.sleep(0.5)
            self.get()
            is_ready = self._check_pod_readiness()
            self._check_timeout(start_time)
        return self

    def _check_pod_readiness(self):
        if self.current_replicas == self.desired_replicas:
            pods = K8sPod.get_by_labels(config=self.config, labels=self.pod_labels)
            for pod in pods:
                try:
                    if not pod.is_ready():
                        raise PodNotReadyException(pod.name)
                except NotFoundException:
                    pass
                except PodNotReadyException:
                    return False
            return True
        return False

    def _check_timeout(self, start_time=None):
        elapsed_time = time.time() - start_time
        if elapsed_time >= self.SCALE_WAIT_TIMEOUT_SECONDS:  # timeout
            raise TimedOutException(
                "Timed out scaling RC: [ {0} ] "
                "to replica count: [ {1} ]".format(self.name, self.desired_replicas))

    # -------------------------------------------------------------------------------------  get by name

    @staticmethod
    def get_by_name(config=None, name=None):
        if config is not None and not isinstance(config, K8sConfig):
            raise SyntaxError(
                'ReplicationController.get_by_name(): config: [ {0} ] is invalid.'.format(config))
        if not is_valid_string(name):
            raise SyntaxError(
                'K8sReplicationController.get_by_name() name: [ {0} ] is invalid.'.format(name))

        rc_list = []
        data = {'labelSelector': 'name={0}'.format(name)}
        rcs = K8sReplicationController(config=config, name=name).get_with_params(data=data)

        for rc in rcs:
            try:
                model = ReplicationController(rc)
                obj = K8sReplicationController(config=config, name=model.metadata.name)
                rc_list.append(obj.get())
            except NotFoundException:
                pass

        return rc_list

    # -------------------------------------------------------------------------------------  scale

    @staticmethod
    def scale(config=None, name=None, replicas=None):
        """
        Scales the number of pods in the specified K8sReplicationController to the desired replica count.

        :param config: an instance of K8sConfig

        :param name: the name of the ReplicationController we want to scale.

        :param replicas: the desired number of replicas.

        :return: An instance of K8sReplicationController
        """

        rc = K8sReplicationController(config=config, name=name).get()
        rc.desired_replicas = replicas
        rc.update()
        rc._wait_for_desired_replicas()
        return rc

    # -------------------------------------------------------------------------------------  rolling update

    @staticmethod
    def rolling_update(config=None, name=None, image=None, container_name=None, rc_new=None):
        """
        Performs a simple rolling update of a ReplicationController.

        See https://github.com/kubernetes/kubernetes/blob/master/docs/design/simple-rolling-update.md
        for algorithm details. We have modified it slightly to allow for keeping the same RC name
        between updates, which is not supported by default by kubectl.

        :param config: An instance of K8sConfig. If omitted, reads from ~/.kube/config.

        :param name: The name of the ReplicationController we want to update.

        :param image: The updated image version we want applied.

        :param container_name: The name of the container we're targeting for the update.
               Required if more than one container is present.

        :param rc_new: An instance of K8sReplicationController with the new configuration to apply.
               Mutually exclusive with [image, container_name] if specified.

        :return:
        """

        if name is None:
            raise SyntaxError(
                'K8sReplicationController: name: [ {0} ] cannot be None.'.format(name))
        if image is None and rc_new is None:
            raise SyntaxError(
                "K8sReplicationController: please specify either 'image' or 'rc_new'")
        if container_name is not None and image is not None and rc_new is not None:
            raise SyntaxError(
                'K8sReplicationController: rc_new is mutually exclusive with an (container_name, image) pair.')

        return K8sReplicationController._rolling_update_init(
            config=config,
            name=name,
            image=image,
            container_name=container_name,
            rc_new=rc_new)

    @staticmethod
    def _rolling_update_init(config=None, name=None, image=None, container_name=None, rc_new=None):

        foo = None
        foo_next = None
        name_next = "{}-next".format(name)

        try:
            foo = K8sReplicationController(config=config, name=name).get()
        except NotFoundException:
            pass
        try:
            foo_next = K8sReplicationController(config=config, name=name_next).get()
        except NotFoundException:
            pass

        if foo is None and foo_next is None:
            raise NotFoundException(
                'K8sReplicationController.rolling_update() RC: [ {} ] not found.'.format(name))

        if foo is not None and foo_next is None:

            if rc_new is not None:
                foo_next = copy.deepcopy(rc_new)

            else:
                foo_next = K8sReplicationController(config=config, name=name)

            foo_old = copy.deepcopy(foo)
            foo_old.name = "{}-old".format(foo.name)
            foo_old.selector = copy.deepcopy(foo.selector)
            foo_old.pod_labels = copy.deepcopy(foo.pod_labels)

            foo.delete(cascade=False)
            foo_old.create()

            if image and len(foo_old.containers) > 1 and not container_name:
                raise UnprocessableEntityException(
                    'K8sReplicationController: Please specify the target container_name '
                    'on which to apply image: [ {} ].'.format(image))

            if len(foo_old.containers) == 1 and not container_name:
                container_name = foo_old.containers[0].name

            if container_name and image:
                existing = list(filter(lambda x: x.name != container_name, foo_old.containers))
                if existing:
                    [foo_next.add_container(x) for x in existing]
                filtered = list(filter(lambda x: x.name == container_name, foo_old.containers))
                if filtered:
                    container = filtered[0]
                    container.image = image
                    foo_next.add_container(container)

            new_version = str(uuid.uuid4())
            foo_next.name = name
            foo_next.add_pod_label(k='name', v=name)
            foo_next.add_pod_label(k='rc_version', v=new_version)
            foo_next.selector = {'name': name, 'rc_version': new_version}
            foo_next.add_annotation(K8sReplicationController.DESIRED_REPLICAS_ANNOTATION, foo_old.desired_replicas)
            foo_next.desired_replicas = 0

            foo_next.create()
            return K8sReplicationController._rolling_update_rollout(config, name)

        if foo is None and foo_next is not None:
            return K8sReplicationController._rolling_update_rename(config, name)

        if foo is not None and foo_next is not None:
            if K8sReplicationController.DESIRED_REPLICAS_ANNOTATION not in foo_next.annotations:
                foo_next.add_annotation(K8sReplicationController.DESIRED_REPLICAS_ANNOTATION, foo.current_replicas)
                foo_next.update()
            return K8sReplicationController._rolling_update_rollout(config, name)

    @staticmethod
    def _rolling_update_rollout(config=None, name=None):
        name_old = "{}-old".format(name)
        foo = K8sReplicationController(config=config, name=name_old).get()
        foo_next = K8sReplicationController(config=config, name=name).get()
        desired = foo_next.get_annotation(K8sReplicationController.DESIRED_REPLICAS_ANNOTATION)

        while foo_next.current_replicas < int(desired):

            K8sReplicationController.scale(
                config=config,
                name=name,
                replicas=foo_next.current_replicas + 1)

            if foo.current_replicas > 0:
                K8sReplicationController.scale(
                    config=config,
                    name=name_old,
                    replicas=foo.current_replicas - 1)

            foo.get()
            foo_next.get()

        return K8sReplicationController._rolling_update_rename(config, name)

    @staticmethod
    def _rolling_update_rename(config=None, name=None):
        name_old = "{}-old".format(name)
        foo = K8sReplicationController(config=config, name=name_old).get()
        foo_next = K8sReplicationController(config=config, name=name).get()
        foo.delete()
        return foo_next

    @staticmethod
    def _rolling_update_abort(config=None, name=None):
        foo = None
        foo_next = None
        name_next = "{}-next".format(name)

        try:
            foo = K8sReplicationController(config=config, name=name).get()
        except NotFoundException:
            pass
        try:
            foo_next = K8sReplicationController(config=config, name=name_next).get()
        except NotFoundException:
            pass

        if foo_next is None:
            raise NotFoundException(
                'K8sReplicationController.rolling_update() '
                'No pending rollout of RC: [ {} ] to abort; perform a new rollout.'.format(name))
        if foo is None:
            raise NotFoundException(
                'K8sReplicationController.rolling_update() RC: [ {} ] not found.'.format(name))

    # -------------------------------------------------------------------------------------  bad cattle

    def restart(self):
        """
        Restart will force a rolling update of the current ReplicationController to the current revision.
        This essentially spawns a fresh copy of the RC and its pods. Useful when something is misbehaving.
        """

        rc_new = copy.deepcopy(self)
        return K8sReplicationController.rolling_update(
            config=self.config,
            name=self.name,
            rc_new=rc_new)
