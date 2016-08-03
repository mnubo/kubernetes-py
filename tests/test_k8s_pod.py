#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
import os
import socket
import uuid
import time
from kubernetes import K8sPod, K8sConfig, K8sContainer
from kubernetes.models.v1 import Pod, ObjectMeta, PodSpec, PodStatus
from kubernetes.K8sExceptions import *

kubeconfig_fallback = '{0}/.kube/config'.format(os.path.abspath(os.path.dirname(os.path.realpath(__file__))))


class K8sPodTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        self.cleanup_pods()

    # ------------------------------------------------------------------------------------- utils

    @staticmethod
    def _create_pod(config=None, name=None):
        if config is None:
            try:
                config = K8sConfig()
            except SyntaxError:
                config = K8sConfig(kubeconfig=kubeconfig_fallback)
        obj = K8sPod(config=config, name=name)
        return obj

    @staticmethod
    def _create_container(name=None, image="redis"):
        obj = K8sContainer(name=name, image=image)
        return obj

    @staticmethod
    def _is_reachable(api_host=None):
        scheme, host, port = api_host.replace("//", "").split(':')
        try:
            s = socket.create_connection((host, port), timeout=1)
            s.close()
            return True
        except Exception:
            return False

    @staticmethod
    def cleanup_pods():
        pod = K8sPodTest._create_pod(name="throwaway")
        if pod.config.api_host is not None and K8sPodTest._is_reachable(pod.config.api_host):
            pods = pod.list()
            for p in pods:
                result = K8sPod.get_by_name(name=p['metadata']['name'])
                [x.delete() for x in result]
                time.sleep(2)  # let the pod die

    # ------------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sPod()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_invalid_config(self):
        config = object()
        try:
            K8sPod(config=config)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_invalid_name(self):
        name = object()
        try:
            K8sPod(name=name)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_name(self):
        name = "yomama"
        pod = self._create_pod(name=name)
        self.assertIsNotNone(pod)
        self.assertIsInstance(pod, K8sPod)
        self.assertEqual(pod.name, name)

    def test_init_with_config_and_pull_secrets(self):
        ps = "yomama"
        name = "sofat"
        cfg = K8sConfig(kubeconfig=kubeconfig_fallback, pull_secret=ps)
        pod = self._create_pod(config=cfg, name=name)
        self.assertIsNotNone(pod.config)
        self.assertEqual(ps, pod.config.pull_secret)

    # ------------------------------------------------------------------------------------- struct

    def test_struct_k8spod(self):
        name = "yomama"
        pod = self._create_pod(name=name)
        self.assertIsNotNone(pod)
        self.assertIsInstance(pod, K8sPod)
        self.assertIsNotNone(pod.model)
        self.assertIsInstance(pod.model, Pod)

    def test_struct_pod(self):
        name = "yomama"
        pod = self._create_pod(name=name)
        model = pod.model
        self.assertIsInstance(model.model, dict)
        self.assertIsInstance(model.pod_metadata, ObjectMeta)
        self.assertIsInstance(model.pod_spec, PodSpec)
        self.assertIsNone(model.pod_status)

    def test_struct_pod_model(self):
        name = "yomama"
        pod = self._create_pod(name=name)
        model = pod.model.model
        self.assertIsNotNone(model)
        self.assertIsInstance(model, dict)
        self.assertIn('apiVersion', model)
        self.assertIsInstance(model['apiVersion'], str)
        self.assertIn('kind', model)
        self.assertIsInstance(model['kind'], str)
        self.assertIn('metadata', model)
        self.assertIsInstance(model['metadata'], dict)
        self.assertIn('labels', model['metadata'])
        self.assertIsInstance(model['metadata']['labels'], dict)
        self.assertIn('name', model['metadata']['labels'])
        self.assertEqual(model['metadata']['labels']['name'], name)
        self.assertIn('name', model['metadata'])
        self.assertIsInstance(model['metadata']['name'], str)
        self.assertEqual(model['metadata']['name'], name)
        self.assertIn('namespace', model['metadata'])
        self.assertIsInstance(model['metadata']['namespace'], str)
        self.assertIn('spec', model)
        self.assertIsInstance(model['spec'], dict)
        self.assertIn('containers', model['spec'])
        self.assertIsInstance(model['spec']['containers'], list)
        self.assertIn('dnsPolicy', model['spec'])
        self.assertIsInstance(model['spec']['dnsPolicy'], str)
        self.assertIn('restartPolicy', model['spec'])
        self.assertIsInstance(model['spec']['restartPolicy'], str)
        self.assertIn('volumes', model['spec'])
        self.assertIsInstance(model['spec']['volumes'], list)

    # ------------------------------------------------------------------------------------- add annotation

    def test_add_annotation_none_args(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        try:
            pod.add_annotation()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_annotation_invalid_args(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        k = object()
        v = object()
        try:
            pod.add_annotation(k, v)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_annotation(self):
        name = "yopod"
        pod = self._create_pod(name=name)

        k = "yokey"
        v = "yovalue"
        pod.add_annotation(k, v)

        meta = pod.model.model['metadata']
        self.assertIn('annotations', meta)
        self.assertIn(k, meta['annotations'])
        meta = pod.model.pod_metadata.model
        self.assertIn('annotations', meta)
        self.assertIn(k, meta['annotations'])

    # ------------------------------------------------------------------------------------- add label

    def test_add_label_none_args(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        try:
            pod.add_label()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_label_invalid_args(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        k = object()
        v = object()
        try:
            pod.add_label(k, v)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_label(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        k = "yokey"
        v_in = "yovalue"
        pod.add_label(k, v_in)
        v_out = pod.get_label(k)
        self.assertEqual(v_in, v_out)

    # ------------------------------------------------------------------------------------- delete annotation

    def test_del_annotation_none_arg(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        try:
            pod.del_annotation()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_del_annotation_invalid_arg(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        k = object()
        try:
            pod.del_annotation(k)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_del_annotation_none_yet(self):
        name = "yopod"
        pod = self._create_pod(name=name)

        k = "yokey"
        pod.del_annotation(k)

        meta = pod.model.model['metadata']
        self.assertNotIn('annotations', meta)
        meta = pod.model.pod_metadata.model
        self.assertNotIn('annotations', meta)

    def test_del_annotation(self):
        name = "yopod"
        pod = self._create_pod(name=name)

        k = "yokey"
        v = "yovalue"
        pod.add_annotation(k, v)

        meta = pod.model.model['metadata']
        self.assertIn('annotations', meta)
        self.assertIn(k, meta['annotations'])
        meta = pod.model.pod_metadata.model
        self.assertIn('annotations', meta)
        self.assertIn(k, meta['annotations'])

        pod.del_annotation(k)

        meta = pod.model.model['metadata']
        self.assertIn('annotations', meta)
        self.assertNotIn(k, meta['annotations'])
        meta = pod.model.pod_metadata.model
        self.assertIn('annotations', meta)
        self.assertNotIn(k, meta['annotations'])

    def test_del_annotation_does_not_exist(self):
        name = "yopod"
        pod = self._create_pod(name=name)

        k_1 = "yokey"
        v_1 = "yovalue"
        k_2 = "yonotexists"
        pod.add_annotation(k_1, v_1)

        meta = pod.model.model['metadata']
        self.assertIn('annotations', meta)
        self.assertIn(k_1, meta['annotations'])
        self.assertNotIn(k_2, meta['annotations'])
        meta = pod.model.pod_metadata.model
        self.assertIn('annotations', meta)
        self.assertIn(k_1, meta['annotations'])
        self.assertNotIn(k_2, meta['annotations'])

        pod.del_annotation(k_2)

        meta = pod.model.model['metadata']
        self.assertNotIn(k_2, meta)
        meta = pod.model.pod_metadata.model
        self.assertNotIn(k_2, meta)

    # ------------------------------------------------------------------------------------- delete label

    def test_del_label_none_arg(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        try:
            pod.del_label()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_del_label_invalid_arg(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        k = object()
        try:
            pod.del_label(k)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_del_label_none_yet(self):
        name = "yopod"
        pod = self._create_pod(name=name)

        k = "yokey"
        pod.del_label(k)

        meta = pod.model.model['metadata']
        self.assertIn('labels', meta)
        meta = pod.model.pod_metadata.model
        self.assertIn('labels', meta)

    def test_del_label(self):
        name = "yopod"
        pod = self._create_pod(name=name)

        k = "yokey"
        v = "yovalue"
        pod.add_label(k, v)

        meta = pod.model.model['metadata']
        self.assertIn('labels', meta)
        self.assertIn(k, meta['labels'])
        meta = pod.model.pod_metadata.model
        self.assertIn('labels', meta)
        self.assertIn(k, meta['labels'])

        pod.del_label(k)

        meta = pod.model.model['metadata']
        self.assertIn('labels', meta)
        self.assertNotIn(k, meta['labels'])
        meta = pod.model.pod_metadata.model
        self.assertIn('labels', meta)
        self.assertNotIn(k, meta['labels'])

    def test_del_label_does_not_exist(self):
        name = "yopod"
        pod = self._create_pod(name=name)

        k_1 = "yokey"
        v_1 = "yovalue"
        k_2 = "yonotexists"
        pod.add_label(k_1, v_1)

        meta = pod.model.model['metadata']
        self.assertIn('labels', meta)
        self.assertIn(k_1, meta['labels'])
        self.assertNotIn(k_2, meta['labels'])
        meta = pod.model.pod_metadata.model
        self.assertIn('labels', meta)
        self.assertIn(k_1, meta['labels'])
        self.assertNotIn(k_2, meta['labels'])

        pod.del_label(k_2)
        meta = pod.model.model['metadata']
        self.assertNotIn(k_2, meta)
        meta = pod.model.pod_metadata.model
        self.assertNotIn(k_2, meta)

    # ------------------------------------------------------------------------------------- get

    def test_get_nonexistent(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        if pod.config.api_host is not None and self._is_reachable(pod.config.api_host):
            try:
                pod.get()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_get(self):
        name = "yocontainer"
        container = self._create_container(name=name)
        name = "yopod"
        pod = self._create_pod(name=name)
        pod.add_container(container)
        if pod.config.api_host is not None and self._is_reachable(pod.config.api_host):
            from_create = pod.create()
            from_get = pod.get()
            self.assertIsInstance(from_create, K8sPod)
            self.assertIsInstance(from_get, K8sPod)
            self.assertEqual(from_create, from_get)

    # ------------------------------------------------------------------------------------- get annotation

    def test_get_annotation_none_args(self):
        name = "yopod"
        pod = self._create_pod(name=name)

        try:
            pod.get_annotation()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_annotation_invalid_args(self):
        name = "yopod"
        pod = self._create_pod(name=name)

        k = object()
        try:
            pod.get_annotation(k)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_annotation_doesnt_exist(self):
        name = "yopod"
        pod = self._create_pod(name=name)

        k = "yonotexists"
        ann = pod.get_annotation(k)
        self.assertIsNone(ann)

    def test_get_annotation(self):
        name = "yopod"
        pod = self._create_pod(name=name)

        k = "yokey"
        v_in = "yovalue"
        pod.add_annotation(k, v_in)

        v_out = pod.get_annotation(k)
        self.assertEqual(v_in, v_out)

    # ------------------------------------------------------------------------------------- get annotations

    def test_get_annotations_none(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        anns = pod.get_annotations()
        self.assertIsNone(anns)

    def test_get_annotations(self):
        name = "yopod"
        pod = self._create_pod(name=name)

        count = 4
        for i in range(0, count):
            k = "key_{0}".format(i)
            v = "value_{0}".format(i)
            pod.add_annotation(k, v)

        anns = pod.get_annotations()

        self.assertIsNotNone(anns)
        self.assertIsInstance(anns, dict)
        self.assertEqual(count, len(anns))
        for i in range(0, count):
            self.assertIn("key_{0}".format(i), anns)

    # ------------------------------------------------------------------------------------- get label

    def test_get_label_none_args(self):
        name = "yopod"
        pod = self._create_pod(name=name)

        try:
            pod.get_annotation()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_label_invalid_args(self):
        name = "yopod"
        pod = self._create_pod(name=name)

        k = object()
        try:
            pod.get_label(k)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_label_doesnt_exist(self):
        name = "yopod"
        pod = self._create_pod(name=name)

        k = "yonotexists"
        l = pod.get_label(k)
        self.assertIsNone(l)

    def test_get_label(self):
        name = "yopod"
        pod = self._create_pod(name=name)

        k = "yokey"
        v_in = "yovalue"
        pod.add_label(k, v_in)

        v_out = pod.get_label(k)
        self.assertEqual(v_in, v_out)

    # ------------------------------------------------------------------------------------- get labels

    def test_get_labels_none(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        labels = pod.get_labels()
        self.assertIsNotNone(labels)
        self.assertIn('name', labels)

    def test_get_labels(self):
        name = "yopod"
        pod = self._create_pod(name=name)

        count = 4
        for i in range(0, count):
            k = "key_{0}".format(i)
            v = "value_{0}".format(i)
            pod.add_label(k, v)

        labels = pod.get_labels()

        self.assertIsNotNone(labels)
        self.assertIsInstance(labels, dict)
        self.assertLessEqual(count, len(labels))  # 'name' already exists as a label
        for i in range(0, count):
            self.assertIn("key_{0}".format(i), labels)

    # ------------------------------------------------------------------------------------- get pod status

    def test_get_pod_status_nonexistent(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        try:
            pod.get_status()
        except Exception as err:
            self.assertIsInstance(err, NotFoundException)

    def test_get_pod_status(self):
        name = "yocontainer"
        container = self._create_container(name=name)
        name = "yopod"
        pod = self._create_pod(name=name)
        pod.add_container(container)
        if pod.config.api_host is not None and self._is_reachable(pod.config.api_host):
            p = pod.create()
            time.sleep(2)  # let creation happen
            result = p.get_status()
            self.assertIsInstance(result, PodStatus)
            for i in ['conditions', 'containerStatuses', 'hostIP', 'phase', 'podIP', 'startTime']:
                self.assertIn(i, result.model)

    # ------------------------------------------------------------------------------------- is_ready

    def test_is_ready_local(self):
        name = "yopod-{0}".format(unicode(uuid.uuid4()))
        pod = self._create_pod(name=name)
        try:
            pod.is_ready()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, NotFoundException)

    def test_is_ready_false(self):
        name = "yocontainer"
        container = self._create_container(name=name)
        name = "yopod-{0}".format(unicode(uuid.uuid4()))
        pod = self._create_pod(name=name)
        pod.add_container(container)
        if pod.config.api_host is not None and self._is_reachable(pod.config.api_host):
            p = pod.create()
            result = p.is_ready()
            self.assertFalse(result)

    def test_is_ready_true(self):
        name = "yocontainer"
        container = self._create_container(name=name)
        name = "yopod"
        pod = self._create_pod(name=name)
        pod.add_container(container)
        if pod.config.api_host is not None and self._is_reachable(pod.config.api_host):
            p = pod.create()
            count = 0
            while not p.is_ready():
                count += 1
                if count == 100:
                    self.fail("Timed out waiting on container to become ready.")
            self.assertTrue(p.is_ready())

    # ------------------------------------------------------------------------------------- set annotations

    def test_set_annotations_none_args(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        try:
            pod.set_annotations()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_annotations_invalid_args(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        anns = object()
        try:
            pod.set_annotations(anns)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_annotations(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        anns_in = {'key': 'value'}
        pod.set_annotations(anns_in)
        anns_out = pod.get_annotations()
        self.assertEqual(anns_in, anns_out)

    # ------------------------------------------------------------------------------------- set labels

    def test_set_labels_none_args(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        try:
            pod.set_labels()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_labels_invalid_args(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        labels = object()
        try:
            pod.set_labels(labels)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_labels(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        labels_in = {'key': 'value'}
        pod.set_labels(labels_in)
        labels_out = pod.get_labels()
        self.assertEqual(labels_in, labels_out)

    # ------------------------------------------------------------------------------------- set namespace

    def test_set_namespace_none_args(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        try:
            pod.set_namespace()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_namespace_invalid_args(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        nspace = object()
        try:
            pod.set_namespace(nspace)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_namespace(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        nspace_in = "yonamespace"
        pod.set_namespace(nspace_in)
        nspace_out = pod.get_namespace()
        self.assertEqual(nspace_in, nspace_out)

    # ------------------------------------------------------------------------------------- get by name

    def test_get_by_name_none_args(self):
        try:
            K8sPod.get_by_name()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_by_name_invalid_args(self):
        name = object()
        try:
            K8sPod.get_by_name(name=name)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_by_name_nonexistent(self):
        name = "yopod-{0}".format(unicode(uuid.uuid4()))
        config = K8sConfig()
        if config.api_host is not None and self._is_reachable(config.api_host):
            pods = K8sPod.get_by_name(name=name)
            self.assertIsInstance(pods, list)
            self.assertEqual(0, len(pods))

    def test_get_by_name(self):
        name = "yocontainer"
        container = self._create_container(name=name)
        name = "yopod-{0}".format(unicode(uuid.uuid4()))
        pod = self._create_pod(name=name)
        pod.add_container(container)
        if pod.config.api_host is not None and self._is_reachable(pod.config.api_host):
            pod.create()
            pods = K8sPod.get_by_name(name=name)
            self.assertIsInstance(pods, list)
            self.assertEqual(1, len(pods))

    # ------------------------------------------------------------------------------------- get by labels

    def test_get_by_labels_none_args(self):
        try:
            K8sPod.get_by_labels()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_by_labels_invalid_args(self):
        name = object()
        try:
            K8sPod.get_by_labels(labels=name)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_by_labels_nonexistent(self):
        name = "yopod-{0}".format(unicode(uuid.uuid4()))
        config = K8sConfig()
        if config.api_host is not None and self._is_reachable(config.api_host):
            pods = K8sPod.get_by_labels(labels={'name': name})
            self.assertIsInstance(pods, list)
            self.assertEqual(0, len(pods))

    def test_get_by_labels(self):
        name = "yocontainer"
        container = self._create_container(name=name)
        name = "yopod-{0}".format(unicode(uuid.uuid4()))
        pod = self._create_pod(name=name)
        pod.add_container(container)
        if pod.config.api_host is not None and self._is_reachable(pod.config.api_host):
            pod.create()
            pods = K8sPod.get_by_labels(labels={'name': name})
            self.assertIsInstance(pods, list)
            self.assertEqual(1, len(pods))

    # ------------------------------------------------------------------------------------- api - create

    def test_create_without_containers(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        if pod.config.api_host is not None and self._is_reachable(pod.config.api_host):
            try:
                pod.create()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, UnprocessableEntityException)

    def test_create_already_exists(self):
        name = "yocontainer"
        c = self._create_container(name=name)
        name = "yopod"
        pod = self._create_pod(name=name)
        pod.add_container(c)
        if pod.config.api_host is not None and self._is_reachable(pod.config.api_host):
            try:
                result = pod.create()
                self.assertIsInstance(result, K8sPod)
                self.assertEqual(pod, result)
                pod.create()
            except Exception as err:
                self.assertIsInstance(err, AlreadyExistsException)

    def test_create_unique(self):
        name = "yocontainer"
        container = self._create_container(name=name)
        config = K8sConfig()
        pods = []
        count = 3
        if config.api_host is not None and self._is_reachable(config.api_host):
            for i in range(0, count):
                name = "yopod-{0}".format(unicode(uuid.uuid4()))
                pod = self._create_pod(config, name)
                pod.add_container(container)
                result = pod.create()
                self.assertIsInstance(result, K8sPod)
                self.assertEqual(pod, result)
                pods.append(pod)
        self.assertEqual(count, len(pods))

    # ------------------------------------------------------------------------------------- api - list

    def test_list_nonexistent(self):
        name = "yopod"
        pod = self._create_pod(name=name)
        if pod.config.api_host is not None and self._is_reachable(pod.config.api_host):
            p = pod.list()
            self.assertIsInstance(p, list)
            self.assertEqual(0, len(p))

    def test_list_multiple(self):
        name = "yocontainer"
        container = self._create_container(name=name)
        config = K8sConfig()
        pods = []
        count = 3
        if config.api_host is not None and self._is_reachable(config.api_host):
            for i in range(0, count):
                name = "yopod-{0}".format(unicode(uuid.uuid4()))
                pod = self._create_pod(config, name)
                pod.add_container(container)
                result = pod.create()
                self.assertIsInstance(result, K8sPod)
                self.assertEqual(pod, result)
                pods.append(pod)
        self.assertEqual(count, len(pods))

    # ------------------------------------------------------------------------------------- api - delete

    def test_delete_nonexistent(self):
        name = "yopod-{0}".format(unicode(uuid.uuid4()))
        pod = self._create_pod(name=name)
        if pod.config.api_host is not None and self._is_reachable(pod.config.api_host):
            try:
                pod.delete()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_delete(self):
        name = "yocontainer"
        container = self._create_container(name)
        name = "yopod-{0}".format(unicode(uuid.uuid4()))
        pod = self._create_pod(name=name)
        pod.add_container(container)
        if pod.config.api_host is not None and self._is_reachable(pod.config.api_host):
            from_create = pod.create()
            from_get = pod.get()
            self.assertEqual(from_create, from_get)
            from_delete = pod.delete()
            self.assertIsInstance(from_delete, K8sPod)
            self.assertEqual(from_get, from_delete)
            time.sleep(3)  # let the pod die
            result = pod.list()
            self.assertIsInstance(result, list)
            self.assertEqual(0, len(result))
