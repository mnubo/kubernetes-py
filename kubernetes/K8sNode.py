#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import json
import time

from kubernetes.K8sExceptions import DrainNodeException, TimedOutException
from kubernetes.K8sNamespace import K8sNamespace
from kubernetes.K8sObject import K8sObject
from kubernetes.K8sPod import K8sPod
from kubernetes.models.v1.Node import Node


class K8sNode(K8sObject):

    DRAIN_WAIT_TIMEOUT_SECONDS = 60

    def __init__(self, config=None, name=None):
        super(K8sNode, self).__init__(
            config=config,
            name=name,
            obj_type='Node'
        )

    # -------------------------------------------------------------------------------------  override

    def create(self):
        super(K8sNode, self).create()
        self.get()
        return self

    def update(self):
        super(K8sNode, self).update()
        self.get()
        return self

    def list(self, pattern=None):
        ls = super(K8sNode, self).list()
        nodes = list(map(lambda x: Node(x), ls))
        if pattern is not None:
            nodes = list(filter(lambda x: pattern in x.name, nodes))
        k8s = []
        for x in nodes:
            j = K8sNode(config=self.config, name=x.name)
            j.model = x
            k8s.append(j)
        return k8s

    # ------------------------------------------------------------------------------------- get

    def get(self):
        self.model = Node(self.get_model())
        return self

    def get_annotation(self, k=None):
        if k in self.model.metadata.annotations:
            return self.model.metadata.annotations[k]
        return None

    def get_label(self, k=None):
        if k in self.model.metadata.labels:
            return self.model.metadata.labels[k]
        return None

    # ------------------------------------------------------------------------------------- pod_cidr

    @property
    def pod_cidr(self):
        return self.model.spec.pod_cidr

    @pod_cidr.setter
    def pod_cidr(self, v=None):
        self.model.spec.pod_cidr = v

    # ------------------------------------------------------------------------------------- external_id

    @property
    def external_id(self):
        return self.model.spec.external_id

    @external_id.setter
    def external_id(self, v=None):
        self.model.spec.external_id = v

    # ------------------------------------------------------------------------------------- provider_id

    @property
    def provider_id(self):
        return self.model.spec.provider_id

    @provider_id.setter
    def provider_id(self, v=None):
        self.model.spec.provider_id = v

    # ------------------------------------------------------------------------------------- unschedulable

    @property
    def unschedulable(self):
        return self.model.spec.unschedulable

    @unschedulable.setter
    def unschedulable(self, v=None):
        self.model.spec.unschedulable = v

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self.model.status

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self.model.metadata.name

    @name.setter
    def name(self, name=None):
        self.model.metadata.name = name

    # ------------------------------------------------------------------------------------- filter

    @staticmethod
    def get_by_name(config=None, name=None):
        nodes = K8sNode(config=config, name=name).list()
        filtered = list(filter(lambda x: x.name == name, nodes))
        if filtered:
            return filtered[0]
        return None

    # ------------------------------------------------------------------------------------- pods

    @property
    def pods(self):
        return self._pod_inventory()

    @pods.setter
    def pods(self, p=None):
        raise NotImplementedError("K8sNode: pods is read-only.")

    # ------------------------------------------------------------------------------------- drain

    def drain(self, ignore_daemonsets=False, delete_local_storage=False, force=False):
        """
        Removes all K8sPods from this K8sNode, 
        and prevents additional K8sPods from being scheduled.
        
        :param ignore_daemonsets: a boolean. 
                If false, will fail if a K8sDaemonSet-managed K8sPod is present.
                If true, will continue even if a K8sDaemonSet-managed K8sPod is present.
                        
        :param delete_local_storage: a boolean.
                If false, will fail if a K8sVolume of type 'emptyDir' is found.
                If true, will continue even if an 'emptyDir' K8sVolume is found.
        
        :param force: a boolean.
                If false, will fail if any K8sPods unmanaged by a parent object are found.
                If true, will continue and any unmanaged K8sPods are lost.
        
        :return: self. 
        """

        # inventory of K8sPods found on this node.
        daemonset_pods = []
        pods = self._pod_inventory()

        # cordon the node.
        self.unschedulable = True
        self.update()

        # loop through all pods and delete them.
        for pod in pods:
            if self._is_daemonset(pod):
                if not ignore_daemonsets:
                    raise DrainNodeException("K8sNode: pod: [ {} ] is managed by a DaemonSet.".format(pod.name))
                else:
                    daemonset_pods.append(pod)
                    continue
            if self._has_local_storage(pod) and not delete_local_storage:
                raise DrainNodeException("K8sNode: pod: [ {} ] has local storage that will be lost.".format(pod.name))
            if self._is_orphan(pod) and not force:
                raise DrainNodeException("K8sNode: pod: [ {} ] is unmanaged and will be lost.".format(pod.name))

            pod.delete()

        self._wait_for_pod_deletion(daemonset_pods)

        return self

    def _pod_inventory(self):
        """
        Returns the list of all K8sPods found on this K8sNode.
        
        :return: A list of K8sPods.
        """

        pods = []
        namespaces = K8sNamespace(config=self.config, name="yo").list()
        for ns in namespaces:
            cfg = self.config
            cfg.namespace = ns.name
            p = K8sPod(config=cfg, name="yo").list()
            filtered = filter(lambda x: x.node_name == self.name, p)
            pods += filtered
        return pods

    def _is_daemonset(self, pod=None):
        """
        Determines if a K8sPod is part of a K8sDaemonSet.
        
        :param pod: The K8sPod we're interested in.

        :return: a boolean.
        """

        if 'kubernetes.io/created-by' in pod.annotations:
            parent = json.loads(pod.annotations['kubernetes.io/created-by'])
            if parent['reference']['kind'] == 'DaemonSet':
                return True
        return False

    def _has_local_storage(self, pod=None):
        """
        Determines if a K8sPod has any local storage susceptible to be lost.

        :param pod: The K8sPod we're interested in.

        :return: a boolean.
        """

        for vol in pod.volumes:
            if vol.emptyDir is not None:
                return True
        return False

    def _is_orphan(self, pod=None):
        """
        Determines if a K8sPod is unmanaged by a parent object, and is susceptible to be lost.

        :param pod: The K8sPod we're interested in.

        :return: a boolean.
        """

        if 'kubernetes.io/created-by' not in pod.annotations:
            return True
        return False

    def _wait_for_pod_deletion(self, daemonset_pods=None):
        """
        Wait until this K8sNode has evicted all its K8sPods.
        
        :param daemonset_pods: A list of K8sPods on this K8sNode that are managed by a K8sDaemonSet.
        
        :return: None
        """

        pods = self._pod_inventory()
        start_time = time.time()
        while len(pods) > 0:
            if len(pods) == len(daemonset_pods):
                break
            pods = self._pod_inventory()
            self._check_timeout(start_time)
            time.sleep(1)
        return

    def _check_timeout(self, start_time=None):
        elapsed_time = time.time() - start_time
        if elapsed_time >= self.DRAIN_WAIT_TIMEOUT_SECONDS:  # timeout
            raise TimedOutException("Timed out draining K8sNode: [ {0} ]".format(self.name))

    # ------------------------------------------------------------------------------------- uncordon

    def uncordon(self):
        """
        Returns this K8sNode into the pool addressable by the kube-scheduler.
        
        :return: self
        """

        self.unschedulable = False
        self.update()
        return self
