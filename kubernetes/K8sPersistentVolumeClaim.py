#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import time

from kubernetes.K8sExceptions import TimedOutException
from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1.PersistentVolumeClaim import PersistentVolumeClaim
from kubernetes.models.v1.ResourceRequirements import ResourceRequirements
from kubernetes.models.v1beta1.LabelSelector import LabelSelector
from kubernetes.utils import is_valid_dict

READY_WAIT_TIMEOUT_SECONDS = 60


class K8sPersistentVolumeClaim(K8sObject):

    def __init__(self, config=None, name=None):
        super(K8sPersistentVolumeClaim, self).__init__(
            config=config,
            name=name,
            obj_type='PersistentVolumeClaim'
        )

    # ------------------------------------------------------------------------------------- api calls

    def create(self):
        super(K8sPersistentVolumeClaim, self).create()
        self._wait_for_available()
        return self

    def get(self):
        self.model = PersistentVolumeClaim(model=self.get_model())
        return self

    # ------------------------------------------------------------------------------------- wait

    def _wait_for_available(self):
        start_time = time.time()
        while not self.model.status.phase == 'Bound':
            time.sleep(0.5)
            self.get()
            self._check_timeout(start_time)

    def _check_timeout(self, start_time=None):
        elapsed_time = time.time() - start_time
        if elapsed_time >= READY_WAIT_TIMEOUT_SECONDS:  # timeout
            raise TimedOutException(
                "Timed out waiting on readiness of PersistentVolumeClaim: [ {} ]".format(self.name))

    # ------------------------------------------------------------------------------------- accessModes

    @property
    def access_modes(self):
        return self.model.spec.access_modes

    @access_modes.setter
    def access_modes(self, modes=None):
        self.model.spec.access_modes = modes

    # ------------------------------------------------------------------------------------- resources

    @property
    def resources(self):
        return self.model.spec.resources

    @resources.setter
    def resources(self, res=None):
        if not is_valid_dict(res):
            raise SyntaxError('K8sPersistentVolumeClaim: resources: [ {} ] is invalid.'.format(res))
        resources = ResourceRequirements(model=res)
        self.model.spec.resources = resources

    # ------------------------------------------------------------------------------------- selector

    @property
    def selector(self):
        return self.model.spec.selector

    @selector.setter
    def selector(self, sel=None):
        if not is_valid_dict(sel):
            raise SyntaxError('K8sPersistentVolumeClaim: selector: [ {} ] is invalid.'.format(sel))
        selector = LabelSelector(model=sel)
        self.model.spec.selector = selector
