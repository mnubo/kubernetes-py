#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import uuid
import time
from kubernetes.K8sConfig import K8sConfig
from kubernetes.K8sContainer import K8sContainer
from kubernetes.K8sPodBasedObject import K8sPodBasedObject
from kubernetes.models.v1.Deployment import Deployment
from kubernetes.K8sExceptions import TimedOutException, NotFoundException, BadRequestException

API_VERSION = 'extensions/v1beta1'
SCALE_WAIT_TIMEOUT_SECONDS = 60


class K8sDeployment(K8sPodBasedObject):

    def __init__(self, config=None, name=None, image=None, replicas=0):
        K8sPodBasedObject.__init__(self, config=config, obj_type='Deployment', name=name)
        self.config.version = API_VERSION
        self.model = Deployment(name=name, namespace=self.config.namespace)
        self.set_replicas(replicas)

        selector = {
            'matchLabels': {
                'name': name
            }
        }
        self.set_selector(selector)

        if image is not None:
            container = K8sContainer(name=name, image=image)
            self.add_container(container)
            self.model.set_pod_name(name=name)

        if self.config.pull_secret is not None:
            self.add_image_pull_secrets(name=self.config.pull_secret)

    # -------------------------------------------------------------------------------------  override

    def create(self):
        super(K8sDeployment, self).create()
        self.get()
        if self.model.model['spec']['replicas'] > 0:
            self._wait_for_desired_replicas()
        return self

    def update(self):
        super(K8sDeployment, self).update()
        self.get()
        if self.model.model['spec']['replicas'] > 0:
            self._wait_for_desired_replicas()
        return self

    # -------------------------------------------------------------------------------------  checking rollout success

    def _wait_for_desired_replicas(self):
        start_time = time.time()
        while not self._has_desired_replicas():
            self.get()
            self._check_timeout(start_time)

    def _has_desired_replicas(self):
        if self._has_replica_data():
            desired = self.model.model['spec']['replicas']
            updated = self.model.model['status']['updatedReplicas']
            available = self.model.model['status']['availableReplicas']
            if desired == updated and desired == available:
                return True
        return False

    def _has_replica_data(self):
        if 'status' in self.model.model:
            has_available = 'availableReplicas' in self.model.model['status']
            has_updated = 'updatedReplicas' in self.model.model['status']
            if has_available and has_updated:
                return True
        return False

    def _check_timeout(self, start_time=None):
        elapsed_time = time.time() - start_time
        if elapsed_time >= SCALE_WAIT_TIMEOUT_SECONDS:  # timeout
            raise TimedOutException(
                "Timed out scaling replicas to: [ {0} ] with labels: [ {1} ]"
                .format(
                    self.model.model['spec']['replicas'],
                    self.model.model['spec']['selector']['matchLabels']
                )
            )
        time.sleep(0.2)

    # -------------------------------------------------------------------------------------  get

    def get(self):
        model = self.get_model()
        self.model = Deployment(
            name=model['metadata']['name'],
            model=model,
            replicas=model['spec']['replicas']
        )
        return self

    # -------------------------------------------------------------------------------------  set

    def set_selector(self, dico=None):
        self.model.set_selector(dico=dico)
        return self

    def set_replicas(self, replicas=None):
        self.model.set_replicas(replicas=replicas)
        return self

    # -------------------------------------------------------------------------------------  get by name

    @staticmethod
    def get_by_name(config=None, name=None):
        if name is None:
            raise SyntaxError('Deployment: name: [ {0} ] cannot be None.'.format(name))
        if not isinstance(name, str):
            raise SyntaxError('Deployment: name: [ {0} ] must be a string.'.format(name))

        if config is not None and not isinstance(config, K8sConfig):
            raise SyntaxError('Deployment: config: [ {0} ] must be a K8sConfig'.format(config))

        dep_list = list()
        data = {'labelSelector': 'name={0}'.format(name)}
        deps = K8sDeployment(config=config, name=name).get_with_params(data=data)

        for dep in deps:
            try:
                dep_name = Deployment(model=dep).get_name()
                dep_list.append(K8sDeployment(config=config, name=dep_name).get())
            except NotFoundException:
                pass

        return dep_list
