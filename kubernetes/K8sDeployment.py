#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import time

from kubernetes.K8sConfig import K8sConfig
from kubernetes.K8sContainer import K8sContainer
from kubernetes.K8sExceptions import BadRequestException
from kubernetes.K8sExceptions import TimedOutException, NotFoundException
from kubernetes.K8sObject import K8sObject
from kubernetes.K8sVolume import K8sVolume
from kubernetes.K8sReplicaSet import K8sReplicaSet
from kubernetes.models.v1beta1.Deployment import Deployment
from kubernetes.models.v1beta1.DeploymentRollback import DeploymentRollback
from kubernetes.models.v1beta1.LabelSelector import LabelSelector
from kubernetes.utils import is_valid_list


class K8sDeployment(K8sObject):

    SCALE_WAIT_TIMEOUT_SECONDS = 120
    REVISION_ANNOTATION = 'deployment.kubernetes.io/revision'

    def __init__(self, config=None, name=None, image=None, replicas=0):

        super(K8sDeployment, self).__init__(
            config=config,
            obj_type='Deployment',
            name=name
        )

        self.desired_replicas = replicas

        labels = {'name': name}
        sel = LabelSelector()
        sel.match_labels = labels

        self.selector = sel
        self.labels = labels
        self.pod_labels = labels

        if image is not None:
            container = K8sContainer(name=name, image=image)
            self.add_container(container)

        if self.config.pull_secret is not None:
            self.add_image_pull_secrets(self.config.pull_secret)

    # -------------------------------------------------------------------------------------  override

    def create(self):
        super(K8sDeployment, self).create()
        self.get()
        if self.desired_replicas > 0:
            self._wait_for_desired_replicas()
        return self

    def update(self):
        super(K8sDeployment, self).update()
        self.get()
        if self.desired_replicas > 0:
            self._wait_for_desired_replicas()
        return self

    def list(self, pattern=None):
        ls = super(K8sDeployment, self).list()
        deploys = list(map(lambda x: Deployment(x), ls))
        if pattern is not None:
            deploys = list(filter(lambda x: pattern in x.name, deploys))
        k8s = []
        for x in deploys:
            j = K8sDeployment(config=self.config, name=x.name)
            j.model = x
            k8s.append(j)
        return k8s

    def delete(self, cascade=False):
        super(K8sDeployment, self).delete(cascade)
        if cascade:
            rsets = K8sReplicaSet(
                config=self.config,
                name="yo"
            ).list(pattern=self.name)
            [rset.delete(cascade=cascade) for rset in rsets]
        return self

    # -------------------------------------------------------------------------------------  wait

    def _wait_for_desired_replicas(self):
        start_time = time.time()
        while not self._has_desired_replicas():
            time.sleep(0.5)
            self.get()
            self._check_timeout(start_time)

    def _has_desired_replicas(self):
        if self.updated_replicas == self.desired_replicas \
                and self.current_replicas == self.desired_replicas \
                and self.available_replicas == self.desired_replicas:
            return True
        return False

    def _check_timeout(self, start_time=None):
        elapsed_time = time.time() - start_time
        if elapsed_time >= self.SCALE_WAIT_TIMEOUT_SECONDS:  # timeout
            raise TimedOutException(
                "Timed out scaling Deployment: [ {} ] to replica count: [ {} ]".format(
                    self.name,
                    self.desired_replicas))

    # -------------------------------------------------------------------------------------  add

    def add_container(self, container=None):
        if not isinstance(container, K8sContainer):
            raise SyntaxError('K8sDeployment.add_container() container: [ {0} ] is invalid.'.format(container))
        containers = self.model.spec.template.spec.containers
        if container.model not in containers:
            containers.append(container.model)
        self.model.spec.template.spec.containers = containers
        return self

    def add_image_pull_secrets(self, secret=None):
        self.model.spec.template.spec.add_image_pull_secrets(secret)
        return self

    def add_volume(self, volume=None):
        if not isinstance(volume, K8sVolume):
            raise SyntaxError('K8sDeployment.add_volume() volume: [ {0} ] is invalid.'.format(volume))
        volumes = self.model.spec.template.spec.volumes
        if volume.model not in volumes:
            volumes.append(volume.model)
        self.model.spec.template.spec.volumes = volumes
        return self

    # -------------------------------------------------------------------------------------  get

    def get(self):
        self.model = Deployment(self.get_model())
        return self

    # ------------------------------------------------------------------------------------- namespace

    @property
    def namespace(self):
        return self.model.metadata.namespace

    @namespace.setter
    def namespace(self, nspace=None):
        self.model.metadata.namespace = nspace

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

    # ------------------------------------------------------------------------------------- current replicas

    @property
    def current_replicas(self):
        return self.model.status.replicas

    @current_replicas.setter
    def current_replicas(self, reps=None):
        self.model.status.replicas = reps

    # ------------------------------------------------------------------------------------- desired replicas

    @property
    def desired_replicas(self):
        return self.model.spec.replicas

    @desired_replicas.setter
    def desired_replicas(self, reps=None):
        self.model.spec.replicas = reps

    # ------------------------------------------------------------------------------------- updated replicas

    @property
    def updated_replicas(self):
        return self.model.status.updated_replicas

    @updated_replicas.setter
    def updated_replicas(self, reps=None):
        self.model.status.updated_replicas = reps

    # ------------------------------------------------------------------------------------- available replicas

    @property
    def available_replicas(self):
        return self.model.status.available_replicas

    @available_replicas.setter
    def available_replicas(self, reps=None):
        self.model.status.available_replicas = reps

    # ------------------------------------------------------------------------------------- unavailable replicas

    @property
    def unavailable_replicas(self):
        return self.model.status.unavailable_replicas

    @unavailable_replicas.setter
    def unavailable_replicas(self, reps=None):
        self.model.status.unavailable_replicas = reps

    # -------------------------------------------------------------------------------------  revision

    @property
    def revision(self):
        if 'deployment.kubernetes.io/revision' in self.annotations:
            return int(self.annotations['deployment.kubernetes.io/revision'])
        return None

    @revision.setter
    def revision(self, r=None):
        raise NotImplementedError("K8sDeployment: revision is read-only.")

    # -------------------------------------------------------------------------------------  selector

    @property
    def selector(self):
        return self.model.spec.selector

    @selector.setter
    def selector(self, sel=None):
        self.model.spec.selector = sel

    # -------------------------------------------------------------------------------------  nodeSelector

    @property
    def node_selector(self):
        return self.model.spec.template.spec.node_selector

    @node_selector.setter
    def node_selector(self, sel=None):
        self.model.spec.template.spec.node_selector = sel

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
            raise SyntaxError("K8sDeployment.container_image() Please specify a container name.")

        if len(self.containers) == 1:
            return self.containers[0].image
        else:
            filtered = list(filter(lambda x: x.name == name, self.containers))
            if filtered:
                return filtered[0].image
            return None

    @container_image.setter
    def container_image(self, tup=None):
        if not isinstance(tup, tuple):
            raise SyntaxError('K8sDeployment.container_image() must be a tuple of the form (name, image)')
        name, image = tup
        found = list(filter(lambda x: x.name == name, self.containers))
        if found:
            new = list(filter(lambda x: x.name != name, self.containers))
            found[0].image = image
            new.append(found[0])
            self.containers = new

    # -------------------------------------------------------------------------------------  volumes

    @property
    def volumes(self):
        return self.model.spec.template.spec.volumes

    @volumes.setter
    def volumes(self, v=None):
        if not is_valid_list(v, K8sVolume):
            self.model.spec.template.spec.volumes = v

    # -------------------------------------------------------------------------------------  get by name

    @staticmethod
    def get_by_name(config=None, name=None):
        """
        Fetches a K8sDeployment by name.
        
        :param config: A K8sConfig object.
        :param name: The name we want.
        :return: A list of K8sDeployment objects.
        """

        if name is None:
            raise SyntaxError(
                'Deployment: name: [ {0} ] cannot be None.'.format(name))
        if not isinstance(name, str):
            raise SyntaxError(
                'Deployment: name: [ {0} ] must be a string.'.format(name))

        if config is not None and not isinstance(config, K8sConfig):
            raise SyntaxError(
                'Deployment: config: [ {0} ] must be a K8sConfig'.format(config))

        dep_list = list()
        data = {'labelSelector': 'name={0}'.format(name)}
        deps = K8sDeployment(config=config, name=name).get_with_params(data=data)

        for dep in deps:
            try:
                d = Deployment(dep)
                dep_name = d.metadata.name
                dep_list.append(K8sDeployment(config=config, name=dep_name).get())
            except NotFoundException:
                pass

        return dep_list

    # -------------------------------------------------------------------------------------  rollback

    def rollback(self, revision=None, annotations=None):
        """
        Performs a rollback of the Deployment.

        If the 'revision' parameter is omitted, we fetch the Deployment's system-generated
        annotation containing the current revision, and revert to the version immediately
        preceding the current version.

        :param revision: The revision to rollback to.
        :param annotations: Annotations we'd like to update.
        :return: self
        """

        rollback = DeploymentRollback()
        rollback.name = self.name

        # to the specified revision
        if revision is not None:
            rollback.rollback_to.revision = revision
        # to the revision immediately preceding the current revision
        else:
            current_revision = int(self.get_annotation(self.REVISION_ANNOTATION))
            rev = max(current_revision - 1, 0)
            rollback.rollback_to.revision = rev

        if annotations is not None:
            rollback.updated_annotations = annotations

        url = '{base}/{name}/rollback'.format(base=self.base_url, name=self.name)
        state = self.request(
            method='POST',
            url=url,
            data=rollback.serialize())

        self.get()
        self._wait_for_desired_replicas()

        if not state.get('success'):
            status = state.get('status', '')
            reason = state.get('data', dict()).get('message', None)
            message = 'K8sDeployment: ROLLBACK failed : HTTP {0} : {1}'.format(status, reason)
            raise BadRequestException(message)

        return self

    # -------------------------------------------------------------------------------------  scale

    def scale(self, replicas=None):
        """
        Scales up or down.
        
        :param replicas: The number of desired replicas.
        :return: self
        """

        self.desired_replicas = replicas
        self.update()
        return self

    # -------------------------------------------------------------------------------------  purge replica sets

    def purge_replica_sets(self, keep=3):
        """
        Builds a list of ReplicaSets, sorted from newest to oldest.
        Slices the array, keeping the most X most recent ReplicaSets.
        
        :param keep: The number of ReplicaSets to keep.
        :return: None
        """

        rsets = K8sReplicaSet(
            config=self.config,
            name="yo"
        ).list(pattern=self.name, reverse=True)

        to_purge = rsets[keep:]
        for rset in to_purge:
            rset.delete(cascade=True)
