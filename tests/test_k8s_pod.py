#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import uuid

from kubernetes_py.K8sConfig import K8sConfig
from kubernetes_py.K8sContainer import K8sContainer
from kubernetes_py.K8sExceptions import *
from kubernetes_py.K8sNode import K8sNode
from kubernetes_py.K8sPod import K8sPod
from kubernetes_py.models.v1.ObjectMeta import ObjectMeta
from kubernetes_py.models.v1.Pod import Pod
from kubernetes_py.models.v1.PodSpec import PodSpec
from kubernetes_py.models.v1.PodStatus import PodStatus
from tests import _utils, _constants
from tests.BaseTest import BaseTest


class K8sPodTest(BaseTest):
    def setUp(self):
        _utils.cleanup_nodes()
        _utils.cleanup_pods()
        K8sPod.POD_READY_TIMEOUT_SECONDS = 20
        pass

    def tearDown(self):
        _utils.cleanup_nodes()
        _utils.cleanup_pods()
        pass

    # ------------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sPod()
            self.fail("Should not fail.")
        except SyntaxError:
            pass
        except IOError:
            pass
        except Exception as err:
            self.fail("Unhandled exception: [ {0} ]".format(err.__class__.__name__))

    def test_init_with_invalid_config(self):
        config = object()
        try:
            K8sPod(config=config)
            self.fail("Should not fail.")
        except SyntaxError:
            pass
        except IOError:
            pass
        except Exception as err:
            self.fail("Unhandled exception: [ {0} ]".format(err.__class__.__name__))

    def test_init_with_invalid_name(self):
        name = object()
        try:
            K8sPod(name=name)
            self.fail("Should not fail.")
        except SyntaxError:
            pass
        except IOError:
            pass
        except Exception as err:
            self.fail("Unhandled exception: [ {0} ]".format(err.__class__.__name__))

    def test_init_with_name(self):
        name = "yomama"
        pod = _utils.create_pod(name=name)
        self.assertIsNotNone(pod)
        self.assertIsInstance(pod, K8sPod)
        self.assertEqual(pod.name, name)

    def test_init_with_config_and_pull_secrets(self):
        ps = [{'name': 'yomama'}]
        name = "sofat"
        cfg = K8sConfig(kubeconfig=_utils.kubeconfig_fallback, pull_secret=ps)
        pod = _utils.create_pod(config=cfg, name=name)
        self.assertIsNotNone(pod.config)
        self.assertEqual(ps, pod.config.pull_secret)

    # ------------------------------------------------------------------------------------- struct

    def test_struct_k8spod(self):
        name = "yomama"
        pod = _utils.create_pod(name=name)
        self.assertIsNotNone(pod)
        self.assertIsInstance(pod, K8sPod)
        self.assertIsNotNone(pod.model)
        self.assertIsInstance(pod.model, Pod)

    def test_struct_pod(self):
        name = "yomama"
        pod = _utils.create_pod(name=name)
        self.assertIsInstance(pod.model, Pod)
        self.assertIsInstance(pod.model.metadata, ObjectMeta)
        self.assertIsInstance(pod.model.spec, PodSpec)
        self.assertIsInstance(pod.model.status, PodStatus)

    # ------------------------------------------------------------------------------------- add annotation

    def test_add_annotation_none_args(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        try:
            pod.add_annotation()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_annotation_invalid_args(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        k = object()
        v = object()
        try:
            pod.add_annotation(k, v)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_annotation(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        k = "yokey"
        v = "yovalue"
        pod.add_annotation(k, v)
        self.assertEqual(1, len(pod.model.metadata.annotations))
        self.assertIn(k, pod.model.metadata.annotations)
        self.assertEqual(v, pod.model.metadata.annotations[k])

    # --------------------------------------------------------------------------------- add container

    def test_pod_add_container_invalid(self):
        name = "yoname"
        obj = _utils.create_pod(name=name)
        c = object()
        with self.assertRaises(SyntaxError):
            obj.add_container(c)

    def test_pod_add_container(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        self.assertEqual(0, len(pod.model.spec.containers))
        name = "yopod"
        image = "redis"
        c = K8sContainer(name=name, image=image)
        pod.add_container(c)
        self.assertEqual(1, len(pod.model.spec.containers))
        self.assertEqual(c.model, pod.model.spec.containers[0])

    # ------------------------------------------------------------------------------------- add label

    def test_add_label_none_args(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        with self.assertRaises(SyntaxError):
            pod.add_label()

    def test_add_label_invalid_args(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        k = object()
        v = object()
        with self.assertRaises(SyntaxError):
            pod.add_label(k, v)

    def test_add_label(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        k = "yokey"
        v_in = "yovalue"
        pod.add_label(k, v_in)
        v_out = pod.get_label(k)
        self.assertEqual(v_in, v_out)

    # --------------------------------------------------------------------------------- add pull secret

    def test_pod_add_image_pull_secrets_none_arg(self):
        name = "yoname"
        obj = _utils.create_pod(name=name)
        secretname = None
        try:
            obj.add_image_pull_secrets(secretname)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_image_pull_secrets_invalid_arg(self):
        name = "yoname"
        obj = _utils.create_pod(name=name)
        secretname = 666
        try:
            obj.add_image_pull_secrets(secretname)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_image_pull_secrets(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        secret = [{'name': 'yosecret'}]
        pod.add_image_pull_secrets(secret)
        self.assertEqual(1, len(pod.model.spec.image_pull_secrets))
        self.assertEqual(secret, pod.model.spec.image_pull_secrets)

    # --------------------------------------------------------------------------------- add volume

    # def test_pod_add_volume_invalid(self):
    #     name = "yoname"
    #     obj = utils.create_pod(name=name)
    #     vol = object()
    #     with self.assertRaises(SyntaxError):
    #         obj.add_volume(vol)
    #
    # def test_pod_add_volume_emptydir(self):
    #     name = "yoname"
    #     obj = utils.create_pod(name=name)
    #     config = utils.create_config()
    #     vol = K8sVolume(config=config, name=name, mount_path="/var/test", type='emptyDir')
    #     obj.add_volume(vol)
    #     self.assertEqual(1, len(obj.model.model['spec']['volumes']))
    #     self.assertEqual(1, len(obj.model.pod_spec.model['volumes']))
    #     self.assertEqual(name, obj.model.model['spec']['volumes'][0]['name'])
    #     self.assertEqual(name, obj.model.pod_spec.model['volumes'][0]['name'])
    #
    # def test_pod_add_volume_emptydir_with_medium(self):
    #     name = "yoname"
    #     obj = utils.create_pod(name=name)
    #     config = utils.create_config()
    #     vol = K8sVolume(config=config, name=name, mount_path="/var/test", type='emptyDir')
    #     vol.set_medium('Memory')
    #     obj.add_volume(vol)
    #     self.assertEqual(1, len(obj.model.model['spec']['volumes']))
    #     self.assertEqual(1, len(obj.model.pod_spec.model['volumes']))
    #     self.assertEqual(name, obj.model.model['spec']['volumes'][0]['name'])
    #     self.assertEqual(name, obj.model.pod_spec.model['volumes'][0]['name'])
    #     self.assertEqual('Memory', obj.model.model['spec']['volumes'][0][vol.type]['medium'])
    #     self.assertEqual('Memory', obj.model.pod_spec.model['volumes'][0][vol.type]['medium'])
    #
    # def test_pod_add_volume_hostpath_no_path_specified(self):
    #     name = "yoname"
    #     obj = utils.create_pod(name=name)
    #     config = utils.create_config()
    #     vol = K8sVolume(config=config, name=name, mount_path="/var/test", type='hostPath')
    #     if utils.is_reachable(config):
    #         with self.assertRaises(UnprocessableEntityException):
    #             obj.add_volume(vol)
    #             obj.create()
    #
    # def test_pod_add_volume_hostpath(self):
    #     name = "yoname"
    #     obj = utils.create_pod(name=name)
    #     config = utils.create_config()
    #     vol = K8sVolume(config=config, name=name, mount_path="/var/test", type='hostPath')
    #     host_path = '/var/lib/docker'
    #     vol.set_path(host_path)
    #     obj.add_volume(vol)
    #     self.assertEqual(1, len(obj.model.model['spec']['volumes']))
    #     self.assertEqual(1, len(obj.model.pod_spec.model['volumes']))
    #     self.assertEqual(name, obj.model.model['spec']['volumes'][0]['name'])
    #     self.assertEqual(name, obj.model.pod_spec.model['volumes'][0]['name'])
    #     self.assertEqual(host_path, obj.model.model['spec']['volumes'][0][vol.type]['path'])
    #     self.assertEqual(host_path, obj.model.pod_spec.model['volumes'][0][vol.type]['path'])

    # ------------------------------------------------------------------------------------- delete annotation

    def test_del_annotation_none_arg(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        pod.del_annotation()
        self.assertEqual({}, pod.annotations)

    def test_del_annotation_invalid_arg(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        k = object()
        pod.del_annotation(k)
        self.assertNotIn(k, pod.annotations)

    def test_del_annotation_none_yet(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        k = "yokey"
        self.assertEqual({}, pod.annotations)
        pod.del_annotation(k)
        self.assertEqual({}, pod.annotations)

    def test_del_annotation(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        k = "yokey"
        v = "yovalue"
        pod.add_annotation(k, v)
        self.assertTrue(hasattr(pod.model.metadata, 'annotations'))
        self.assertIn(k, pod.model.metadata.annotations)
        self.assertEqual(v, pod.model.metadata.annotations[k])
        pod.del_annotation(k)
        self.assertTrue(hasattr(pod.model.metadata, 'annotations'))
        self.assertNotIn(k, pod.model.metadata.annotations)

    def test_del_annotation_does_not_exist(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        k1 = "yokey"
        k_2 = "yonotexists"
        v = "yovalue"
        pod.add_annotation(k1, v)
        self.assertTrue(hasattr(pod.model.metadata, 'annotations'))
        self.assertIn(k1, pod.model.metadata.annotations)
        self.assertNotIn(k_2, pod.model.metadata.annotations)
        pod.del_annotation(k_2)
        self.assertTrue(hasattr(pod.model.metadata, 'annotations'))
        self.assertIn(k1, pod.model.metadata.annotations)
        self.assertNotIn(k_2, pod.model.metadata.annotations)

    # ------------------------------------------------------------------------------------- delete label

    def test_del_label_none_arg(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        pod.del_label()
        self.assertEqual(1, len(pod.labels))
        self.assertIn('name', pod.labels)

    def test_del_label_invalid_arg(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        k = object()
        pod.del_label(k)
        self.assertNotIn(k, pod.labels)

    def test_del_label_none_yet(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        k = "yokey"
        self.assertNotIn(k, pod.model.metadata.labels)
        pod.del_label(k)
        self.assertNotIn(k, pod.model.metadata.labels)

    def test_del_label(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        k = "yokey"
        v = "yovalue"
        pod.add_label(k, v)
        self.assertTrue(hasattr(pod.model.metadata, 'labels'))
        self.assertIn(k, pod.model.metadata.labels)
        pod.del_label(k)
        self.assertTrue(hasattr(pod.model.metadata, 'labels'))
        self.assertNotIn(k, pod.model.metadata.labels)

    def test_del_label_does_not_exist(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        k_1 = "yokey"
        k_2 = "yonotexists"
        v = "yovalue"
        pod.add_label(k_1, v)
        self.assertTrue(hasattr(pod.model.metadata, 'labels'))
        self.assertIn(k_1, pod.model.metadata.labels)
        self.assertNotIn(k_2, pod.model.metadata.labels)
        pod.del_label(k_2)
        self.assertTrue(hasattr(pod.model.metadata, 'labels'))
        self.assertIn(k_1, pod.model.metadata.labels)
        self.assertNotIn(k_2, pod.model.metadata.labels)

    # ------------------------------------------------------------------------------------- get

    def test_get_nonexistent(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)

        if _utils.is_reachable(pod.config):
            with self.assertRaises(NotFoundException):
                pod.get()

    def test_get(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        pod.add_container(container)

        if _utils.is_reachable(pod.config):
            from_create = pod.create()
            from_get = pod.get()
            self.assertIsInstance(from_create, K8sPod)
            self.assertIsInstance(from_get, K8sPod)
            self.assertEqual(from_create, from_get)

    # ------------------------------------------------------------------------------------- get annotation

    def test_get_annotation_none_args(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        ann = pod.get_annotation()
        self.assertIsNone(ann)

    def test_get_annotation_invalid_args(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        k = object()
        ann = pod.get_annotation(k)
        self.assertIsNone(ann)

    def test_get_annotation_doesnt_exist(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        k = "yonotexists"
        ann = pod.get_annotation(k)
        self.assertIsNone(ann)

    def test_get_annotation(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        k = "yokey"
        v_in = "yovalue"
        pod.add_annotation(k, v_in)
        v_out = pod.get_annotation(k)
        self.assertEqual(v_in, v_out)

    # ------------------------------------------------------------------------------------- get annotations

    def test_get_annotations_none(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        anns = pod.annotations
        self.assertEqual({}, anns)

    def test_get_annotations(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        count = 4
        for i in range(0, count):
            k = "key_{0}".format(i)
            v = "value_{0}".format(i)
            pod.add_annotation(k, v)
        anns = pod.annotations
        self.assertIsNotNone(anns)
        self.assertIsInstance(anns, dict)
        self.assertEqual(count, len(anns))
        for i in range(0, count):
            self.assertIn("key_{0}".format(i), anns)

    # ------------------------------------------------------------------------------------- get label

    def test_get_label_none_args(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        ann = pod.get_annotation()
        self.assertIsNone(ann)

    def test_get_label_invalid_args(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        k = object()
        ann = pod.get_label(k)
        self.assertIsNone(ann)

    def test_get_label_doesnt_exist(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        k = "yonotexists"
        l = pod.get_label(k)
        self.assertIsNone(l)

    def test_get_label(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        k = "yokey"
        v_in = "yovalue"
        pod.add_label(k, v_in)
        v_out = pod.get_label(k)
        self.assertEqual(v_in, v_out)

    # ------------------------------------------------------------------------------------- get labels

    def test_get_labels_none(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        labels = pod.labels
        self.assertIsNotNone(labels)
        self.assertIn('name', labels)

    def test_get_labels(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        count = 4
        for i in range(0, count):
            k = "key_{0}".format(i)
            v = "value_{0}".format(i)
            pod.add_label(k, v)
        labels = pod.labels
        self.assertIsNotNone(labels)
        self.assertIsInstance(labels, dict)
        self.assertLessEqual(count, len(labels))  # 'name' already exists as a label
        for i in range(0, count):
            self.assertIn("key_{0}".format(i), labels)

    # --------------------------------------------------------------------------------- get pod containers

    def test_pod_get_pod_containers_empty(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        self.assertEqual(0, len(pod.containers))

    def test_get_containers(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)

        count = 3
        for i in range(0, 3):
            name = "yocontainer_{0}".format(i)
            image = "redis"
            c = K8sContainer(name=name, image=image)
            pod.add_container(c)

        self.assertIsNotNone(pod.containers)
        self.assertEqual(count, len(pod.containers))
        [self.assertIsInstance(x, K8sContainer) for x in pod.containers]

    # --------------------------------------------------------------------------------- get node name

    def test_get_node_name_none(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        self.assertIsNone(pod.node_name)

    def test_get_node_name(self):
        name = "yoname"
        nodename = "yonodename"
        pod = _utils.create_pod(name=name)
        pod.node_name = nodename
        self.assertEqual(nodename, pod.node_name)
        self.assertEqual(nodename, pod.model.spec.node_name)

    # --------------------------------------------------------------------------------- get pod node selector

    def test_get_node_selector_none(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        self.assertEqual({}, pod.node_selector)

    def test_get_node_selector(self):
        name = "yoname"
        s_in = {"disktype": "ssd"}
        pod = _utils.create_pod(name=name)
        pod.node_selector = s_in
        s_out = pod.node_selector
        self.assertEqual(s_in, s_out)

    # --------------------------------------------------------------------------------- get pod restart policy

    def test_get_restart_policy_none(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        self.assertEqual('Always', pod.restart_policy)  # set to 'Always' by default

    def test_get_restart_policy(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        p = 'OnFailure'
        pod.restart_policy = p
        self.assertEqual(p, pod.restart_policy)

    # --------------------------------------------------------------------------------- get service account

    def test_pod_get_service_account_none(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        with self.assertRaises(SyntaxError):
            pod.service_account_name = None

    def test_pod_get_service_account(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        name_in = "yoservice"
        pod.service_account_name = name_in
        name_out = pod.service_account_name
        self.assertEqual(name_in, name_out)

    # ------------------------------------------------------------------------------------- get pod status

    def test_get_pod_status_nonexistent(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)

        if _utils.is_reachable(pod.config):
            with self.assertRaises(NotFoundException):
                s = pod.status

    def test_get_pod_status(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        pod.add_container(container)

        if _utils.is_reachable(pod.config):
            p = pod.create()
            result = p.status
            self.assertIsInstance(result, PodStatus)
            for i in ['conditions', 'container_statuses', 'host_ip', 'phase', 'pod_ip', 'reason', 'start_time']:
                self.assertTrue(hasattr(result, i))

    # ------------------------------------------------------------------------------------- get pod logs

    def test_get_pod_logs(self):
        cname = "yocontainer"
        container = _utils.create_container(name=cname)
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        pod.add_container(container)

        if _utils.is_reachable(pod.config):
            with self.assertRaises(NotFoundException):
                pod.get_log()
                pod.get_log(container=cname)

    # ------------------------------------------------------------------------------------- is_ready

    def test_is_ready_nonexistent(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)

        if _utils.is_reachable(pod.config):
            with self.assertRaises(NotFoundException):
                pod.is_ready()
                self.fail("Should not fail.")

    def test_is_ready(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        pod.add_container(container)

        if _utils.is_reachable(pod.config):
            p = pod.create()
            self.assertTrue(p.is_ready())

    # --------------------------------------------------------------------------------- set active deadline

    def test_pod_set_active_deadline_none_arg(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        d = None
        with self.assertRaises(SyntaxError):
            pod.active_deadline = d

    def test_pod_set_active_deadline_invalid_arg(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        d = "yodeadline"
        with self.assertRaises(SyntaxError):
            pod.active_deadline = d

    def test_pod_set_active_deadline(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        d = 600
        pod.active_deadline = d
        self.assertEqual(d, pod.active_deadline)

    # ------------------------------------------------------------------------------------- set annotations

    def test_set_annotations_none_args(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        with self.assertRaises(SyntaxError):
            pod.annotations = None

    def test_set_annotations_invalid_args(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        anns = object()
        with self.assertRaises(SyntaxError):
            pod.annotations = anns

    def test_set_annotations(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        anns = {'key': 'value'}
        pod.annotations = anns
        self.assertEqual(anns, pod.annotations)

    # ------------------------------------------------------------------------------------- set labels

    def test_set_labels_none_args(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        with self.assertRaises(SyntaxError):
            pod.labels = None

    def test_set_labels_invalid_args(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        labels = object()
        with self.assertRaises(SyntaxError):
            pod.labels = labels

    def test_set_labels(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        labels_in = {'key': 'value'}
        pod.labels = labels_in
        self.assertEqual(pod.labels, labels_in)

    # ------------------------------------------------------------------------------------- set namespace

    def test_set_namespace_none_args(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        with self.assertRaises(SyntaxError):
            pod.namespace = None

    def test_set_namespace_invalid_args(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        nspace = object()
        with self.assertRaises(SyntaxError):
            pod.namespace = nspace

    def test_set_namespace(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        nspace = "yonamespace"
        pod.namespace = nspace
        self.assertEqual(nspace, pod.namespace)

    # --------------------------------------------------------------------------------- set pod node name

    def test_pod_set_pod_node_name_none_arg(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        nn = None
        with self.assertRaises(SyntaxError):
            pod.node_name = nn

    def test_pod_set_pod_node_name_invalid_arg(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        nn = 666
        with self.assertRaises(SyntaxError):
            pod.node_name = nn

    def test_pod_set_pod_node_name(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        nn = "yonodename"
        pod.node_name = nn
        self.assertEqual(nn, pod.node_name)

    # --------------------------------------------------------------------------------- set pod node selector

    def test_pod_set_pod_node_selector_none_arg(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        s = None
        with self.assertRaises(SyntaxError):
            pod.node_selector = s

    def test_pod_set_pod_node_selector_invalid_arg(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        s = "yoselector"
        with self.assertRaises(SyntaxError):
            pod.node_selector = s

    def test_pod_set_pod_node_selector(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        s = {"disktype": "ssd"}
        pod.node_selector = s
        self.assertEqual(s, pod.node_selector)

    # --------------------------------------------------------------------------------- set pod restart policy

    def test_pod_set_pod_restart_policy_none(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        p = None
        with self.assertRaises(SyntaxError):
            pod.restart_policy = p

    def test_pod_set_pod_restart_policy_not_a_string(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        p = 666
        with self.assertRaises(SyntaxError):
            pod.restart_policy = p

    def test_pod_set_pod_restart_policy_invalid_string(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        p = 'yopolicy'
        with self.assertRaises(SyntaxError):
            pod.restart_policy = p

    def test_pod_set_pod_restart_policy(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        p = 'Always'
        pod.restart_policy = p
        self.assertEqual(p, pod.restart_policy)

    # --------------------------------------------------------------------------------- set pod service account

    def test_pod_set_service_account_none_arg(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        with self.assertRaises(SyntaxError):
            pod.service_account_name = None

    def test_pod_set_service_account_invalid_arg(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        n = 666
        with self.assertRaises(SyntaxError):
            pod.service_account_name = n

    def test_pod_set_service_account(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        n = "yoservice"
        pod.service_account_name = n
        self.assertEqual(pod.service_account_name, n)

    # --------------------------------------------------------------------------------- set termination grace period

    def test_pod_set_termination_grace_period_none_arg(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        with self.assertRaises(SyntaxError):
            pod.termination_grace_period = None

    def test_pod_set_termination_grace_period_invalid_arg(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        secs = -666
        with self.assertRaises(SyntaxError):
            pod.termination_grace_period = secs

    def test_pod_set_termination_grace_period(self):
        name = "yoname"
        pod = _utils.create_pod(name=name)
        secs = 1234
        pod.termination_grace_period = secs
        self.assertEqual(secs, pod.termination_grace_period)

    # ------------------------------------------------------------------------------------- get by name

    def test_get_by_name_none_args(self):
        config = _utils.create_config()
        with self.assertRaises(SyntaxError):
            K8sPod.get_by_name(config=config)

    def test_get_by_name_invalid_args(self):
        name = object()
        config = _utils.create_config()
        with self.assertRaises(SyntaxError):
            K8sPod.get_by_name(config=config, name=name)

    def test_get_by_name_nonexistent(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        config = K8sConfig(kubeconfig=_utils.kubeconfig_fallback)

        if _utils.is_reachable(config):
            pods = K8sPod.get_by_name(config=config, name=name)
            self.assertIsInstance(pods, list)
            self.assertEqual(0, len(pods))

    def test_get_by_name(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        pod.add_container(container)

        if _utils.is_reachable(pod.config):
            pod.create()
            pods = K8sPod.get_by_name(config=pod.config, name=name)
            self.assertIsInstance(pods, list)
            self.assertEqual(1, len(pods))

    # ------------------------------------------------------------------------------------- get by labels

    def test_get_by_labels_none_args(self):
        config = _utils.create_config()
        with self.assertRaises(SyntaxError):
            K8sPod.get_by_labels(config=config)

    def test_get_by_labels_invalid_args(self):
        name = object()
        config = _utils.create_config()
        with self.assertRaises(SyntaxError):
            K8sPod.get_by_labels(config=config, labels=name)

    def test_get_by_labels_nonexistent(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        config = K8sConfig(kubeconfig=_utils.kubeconfig_fallback)

        if _utils.is_reachable(config):
            pods = K8sPod.get_by_labels(config=config, labels={'name': name})
            self.assertIsInstance(pods, list)
            self.assertEqual(0, len(pods))

    def test_get_by_labels(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        pod.add_container(container)

        if _utils.is_reachable(pod.config):
            pod.create()
            pods = K8sPod.get_by_labels(config=pod.config, labels={'name': name})
            self.assertIsInstance(pods, list)
            self.assertEqual(1, len(pods))
            self.assertEqual(pod, pods[0])

    def test_get_by_labels_without_name(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        pod.add_container(container)
        pod.add_label("test.label", "hello")

        if _utils.is_reachable(pod.config):
            pod.create()
            pods = K8sPod.get_by_labels(config=pod.config, labels={'test.label': "hello"})
            self.assertIsInstance(pods, list)
            self.assertEqual(1, len(pods))
            self.assertEqual(pod, pods[0])

            pods = K8sPod.get_by_labels(config=pod.config, labels={'test.label': "world"})
            self.assertEqual(0, len(pods))

    # ------------------------------------------------------------------------------------- api - create

    def test_create_without_containers(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)

        if _utils.is_reachable(pod.config):
            with self.assertRaises(UnprocessableEntityException):
                pod.create()

    def test_create_already_exists(self):
        name = "yocontainer"
        c = _utils.create_container(name=name)
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        pod.add_container(c)

        if _utils.is_reachable(pod.config):
            with self.assertRaises(AlreadyExistsException):
                result = pod.create()
                self.assertIsInstance(result, K8sPod)
                self.assertEqual(pod, result)
                pod.create()

    def test_create_with_container(self):
        config = K8sConfig(kubeconfig=_utils.kubeconfig_fallback)
        pods = []
        count = 3

        if _utils.is_reachable(config):
            name = "yocontainer"
            container = _utils.create_container(name=name)
            for i in range(0, count):
                name = "yopod-{0}".format(str(uuid.uuid4()))
                pod = _utils.create_pod(config, name)
                pod.add_container(container)
                result = pod.create()
                self.assertIsInstance(result, K8sPod)
                self.assertEqual(pod, result)
                pods.append(pod)
            self.assertEqual(count, len(pods))

    # ------------------------------------------------------------------------------------- api - list

    def test_list(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        container = _utils.create_container(name=name)
        pod.add_container(container)

        if _utils.is_reachable(pod.config):
            pod.create()
            _list = pod.list()
            for x in _list:
                self.assertIsInstance(x, K8sPod)

    def test_list_multiple(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        config = K8sConfig(kubeconfig=_utils.kubeconfig_fallback)
        pods = []
        count = 3

        if _utils.is_reachable(config):
            for i in range(0, count):
                name = "yopod-{0}".format(str(uuid.uuid4()))
                pod = _utils.create_pod(config, name)
                pod.add_container(container)
                result = pod.create()
                self.assertIsInstance(result, K8sPod)
                self.assertEqual(pod, result)
                pods.append(pod)
            self.assertEqual(count, len(pods))

    # ------------------------------------------------------------------------------------- api - update

    def test_update_nonexistent(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)

        if _utils.is_reachable(pod.config):
            with self.assertRaises(NotFoundException):
                pod.update()

    def test_update_name_fails(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name1 = "yopod1"
        name2 = "yopod2"
        pod = _utils.create_pod(name=name1)
        pod.add_container(container)

        if _utils.is_reachable(pod.config):
            pod.create()
            result = K8sPod.get_by_name(config=pod.config, name=name1)
            self.assertIsInstance(result, list)
            self.assertEqual(1, len(result))
            self.assertIsInstance(result[0], K8sPod)
            result[0].name = name2
            with self.assertRaises(NotFoundException):
                result[0].update()

    def test_update_namespace_fails(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name = "yopod-{0}".format(str(uuid.uuid4()))
        nspace = "yonamespace"
        pod1 = _utils.create_pod(name=name)
        pod1.add_container(container)

        if _utils.is_reachable(pod1.config):
            pod1.create()
            result = K8sPod.get_by_name(config=pod1.config, name=name)
            self.assertIsInstance(result, list)
            self.assertEqual(1, len(result))
            pod2 = result[0]
            self.assertIsInstance(pod2, K8sPod)
            self.assertNotEqual(pod2.namespace, nspace)
            self.assertEqual(pod1, pod2)
            pod2.namespace = nspace
            with self.assertRaises(BadRequestException):
                pod2.update()

    def test_update_labels(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        pod.add_container(container)

        if _utils.is_reachable(pod.config):
            pod.create()
            labels = pod.labels
            labels['yomama'] = 'sofat'
            pods = K8sPod.get_by_labels(config=pod.config, labels=labels)
            self.assertIsInstance(pods, list)
            self.assertEqual(0, len(pods))
            pod.labels = labels
            pod.update()
            pods = K8sPod.get_by_labels(config=pod.config, labels=labels)
            self.assertIsInstance(pods, list)
            self.assertEqual(1, len(pods))

    def test_update_add_container_fails(self):
        cont_names = ["yocontainer", "yocontainer2"]
        container = _utils.create_container(name=cont_names[0])
        pod_name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=pod_name)
        pod.add_container(container)

        if _utils.is_reachable(pod.config):
            pod.create()
            container = _utils.create_container(name=cont_names[1])
            pod.add_container(container)
            with self.assertRaises(UnprocessableEntityException):
                pod.update()

    # TODO: this is the first of two update operations that are allowed
    def test_update_container_image(self):
        pass

    # TODO: this is the second of two update operations that are allowed
    def test_update_spec_active_deadline(self):
        pass

    # ------------------------------------------------------------------------------------- api - delete

    def test_delete_nonexistent(self):
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)

        if _utils.is_reachable(pod.config):
            with self.assertRaises(NotFoundException):
                pod.delete()

    def test_delete(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name = "yopod-{0}".format(str(uuid.uuid4()))
        pod = _utils.create_pod(name=name)
        pod.add_container(container)

        if _utils.is_reachable(pod.config):
            pod.create()
            _utils.cleanup_pods()
            result = pod.list()
            self.assertIsInstance(result, list)
            self.assertEqual(0, len(result))

    # ------------------------------------------------------------------------------------- api - node affinity

    def test_node_affinity_no_good_nodes(self):
        model = _constants.pod_with_node_affinity()
        pod = Pod(model)
        config = _utils.create_config()
        k8s = K8sPod(config=config, name="yo")
        k8s.model = pod

        if _utils.is_reachable(config):
            nodes = K8sNode(config=config, name="yo").list()
            # untag all nodes
            for node in nodes:
                node.labels.pop('kubernetes.io/e2e-az-name', None)
                node.update()
            with self.assertRaises(TimedOutException):
                # timeout because of required
                k8s.create()

    def test_node_affinity_with_required(self):
        model = _constants.pod_with_node_affinity()
        pod = Pod(model)
        config = _utils.create_config()
        k8s = K8sPod(config=config, name="yo")
        k8s.model = pod

        if _utils.is_reachable(config):
            # ensure we have enough nodes
            nodes = K8sNode(config=config, name="yo").list()
            if len(nodes) < 3:
                self.skipTest(reason='Not enough nodes to perform test.')
            else:
                self.assertGreaterEqual(len(nodes), 3)
            # tag the nodes
            for i in range(len(nodes)):
                node = nodes[i]
                if i == 0:
                    node.labels.update({'kubernetes.io/e2e-az-name': 'e2e-az1'})
                if i == 1:
                    node.labels.update({'kubernetes.io/e2e-az-name': 'e2e-az2'})
                if i == 2:
                    node.labels.update({'kubernetes.io/e2e-az-name': 'e2e-az3'})
                node.update()
            nodes = K8sNode(config=config, name="yo").list()
            for node in nodes:
                self.assertIn('kubernetes.io/e2e-az-name', node.labels)
            # create the pod
            k8s.create()
            # untag the nodes
            for node in nodes:
                node.labels.pop('kubernetes.io/e2e-az-name', None)
                node.update()
        pass

    def test_node_affinity_with_required_and_preferred(self):
        model = _constants.pod_with_node_affinity()
        pod = Pod(model)
        config = _utils.create_config()
        k8s = K8sPod(config=config, name="yo")
        k8s.model = pod

        if _utils.is_reachable(config):
            # ensure we have enough nodes
            nodes = K8sNode(config=config, name="yo").list()
            if len(nodes) < 3:
                self.skipTest(reason='Not enough nodes to perform test.')
            else:
                self.assertGreaterEqual(len(nodes), 3)
            # tag the nodes
            for i in range(len(nodes)):
                node = nodes[i]
                if i == 0:
                    node.labels.update({'kubernetes.io/e2e-az-name': 'e2e-az1'})
                    node.labels.update({'another-node-label-key': 'another-node-label-value'})
                if i == 1:
                    node.labels.update({'kubernetes.io/e2e-az-name': 'e2e-az2'})
                if i == 2:
                    node.labels.update({'kubernetes.io/e2e-az-name': 'e2e-az3'})
                node.update()
            nodes = K8sNode(config=config, name="yo").list()
            for node in nodes:
                self.assertIn('kubernetes.io/e2e-az-name', node.labels)
            # create the pod
            k8s.create()
            # untag the nodes
            for node in nodes:
                node.labels.pop('kubernetes.io/e2e-az-name', None)
                node.labels.pop('another-node-label-key', None)
                node.update()
        pass

    # ------------------------------------------------------------------------------------- api - pod affinity

    def test_pod_affinity_no_good_nodes(self):
        model = _constants.pod_with_pod_affinity()
        pod = Pod(model)
        config = _utils.create_config()
        k8s = K8sPod(config=config, name="yo")
        k8s.model = pod

        if _utils.is_reachable(config):
            nodes = K8sNode(config=config, name="yo").list()
            # untag all nodes
            for node in nodes:
                node.labels.pop('kubernetes.io/e2e-az-name', None)
                node.update()
            with self.assertRaises(TimedOutException):
                # timeout because of required
                k8s.create()

    def test_pod_affinities(self):
        config = _utils.create_config()
        container = _utils.create_container(name="nginx", image="nginx:latest")

        pod_s1 = _utils.create_pod(config=config, name="s1")
        pod_s1.labels.update({'security': 'S1'})
        pod_s1.node_selector = {'kubernetes.io/e2e-az-name': 'e2e-az1'}
        pod_s1.add_container(container)

        pod_s2 = _utils.create_pod(config=config, name="s2")
        pod_s2.labels.update({'security': 'S2'})
        pod_s2.node_selector = {'kubernetes.io/e2e-az-name': 'e2e-az2'}
        pod_s2.add_container(container)

        model = _constants.pod_with_pod_affinity()
        pod = Pod(model)
        config = _utils.create_config()
        k8s = K8sPod(config=config, name="yo")
        k8s.model = pod

        if _utils.is_reachable(config):
            # ensure we have enough nodes
            nodes = K8sNode(config=config, name="yo").list()
            if len(nodes) < 3:
                self.skipTest(reason='Not enough nodes to perform test.')
            else:
                self.assertGreaterEqual(len(nodes), 3)
            # tag the nodes
            for i in range(len(nodes)):
                node = nodes[i]
                if i == 0:
                    node.labels.update({'kubernetes.io/e2e-az-name': 'e2e-az1'})
                if i == 1:
                    node.labels.update({'kubernetes.io/e2e-az-name': 'e2e-az2'})
                if i == 2:
                    node.labels.update({'kubernetes.io/e2e-az-name': 'e2e-az3'})
                node.update()
            # create the pods for affinity lookup
            pod_s1.create()
            pod_s2.create()
            # create the pod with affinities
            k8s.create()
            pass

    # ------------------------------------------------------------------------------------- api - tolerations

    def test_tolerations_default(self):
        config = _utils.create_config()
        container = _utils.create_container(name="nginx", image="nginx:latest")
        pod = _utils.create_pod(config=config, name="yo")
        pod.add_container(container)

        if _utils.is_reachable(config):
            pod.create()
            pod.get()
            # default 'NoExecute' tolerations
            # 'node.alpha.kubernetes.io/notReady' && 'node.alpha.kubernetes.io/unreachable'
            self.assertEqual(2, len(pod.tolerations))

    def test_tolerations_timeout(self):
        config = _utils.create_config()
        container = _utils.create_container(name="nginx", image="nginx:latest")
        pod = _utils.create_pod(config=config, name="yo")
        pod.add_container(container)

        key = "key"
        value = "value"
        effect = "NoSchedule"

        if _utils.is_reachable(config):
            nodes = K8sNode(config=config, name="yo").list()
            for node in nodes:
                node.taint(key=key, value=value, effect=effect)
            with self.assertRaises(TimedOutException):
                pod.create()
            for node in nodes:
                node.untaint(key=key, value=value)

    def test_tolerations_noschedule(self):
        config = _utils.create_config()
        container = _utils.create_container(name="nginx", image="nginx:latest")
        pod = _utils.create_pod(config=config, name="yo")
        pod.add_container(container)

        key = "key"
        value = "value"
        effect = "NoSchedule"

        if _utils.is_reachable(config):
            nodes = K8sNode(config=config, name="yo").list()
            for node in nodes:
                node.taint(key=key, value=value, effect=effect)
            pod.add_toleration(key=key, value=value, effect=effect)
            pod.create()
            self.assertEqual(3, len(pod.tolerations))
            for node in nodes:
                node.untaint(key=key, value=value)
