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
from kubernetes.K8sExceptions import TimedOutException, NotFoundException

API_VERSION = 'extensions/v1beta1'
SCALE_WAIT_TIMEOUT_SECONDS = 60


class K8sDeployment(K8sPodBasedObject):

    def __init__(self, config=None, name=None, image=None, replicas=0):
        K8sPodBasedObject.__init__(self, config=config, obj_type='Deployment', name=name)
        self.config.version = API_VERSION
        self.model = Deployment(name=name, namespace=self.config.namespace)
        self.set_replicas(replicas)

        deployment_version = str(uuid.uuid4())
        self.model.add_pod_label(k='dep_version', v=deployment_version)
        selector = {
            'matchLabels': {
                'name': name,
                'dep_version': deployment_version
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
        return self

    # -------------------------------------------------------------------------------------  checking rollout success

    def _has_available_replicas(self):
        if 'status' in self.model.model:
            if 'availableReplicas' in self.model.model['status']:
                return True
        return False

    def _has_desired_replicas(self):
        if self._has_available_replicas():
            if self.model.model['status']['updatedReplicas'] == self.model.model['spec']['replicas']:
                return True
        return False

    def _wait_for_desired_replicas(self):
        start_time = time.time()
        while not self._has_desired_replicas():
            self.get()
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

