#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
from kubernetes import K8sPod, K8sConfig
from kubernetes.models.v1 import Pod, ObjectMeta, PodSpec


class K8sPodTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

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
        pod = K8sPod(name=name)
        self.assertIsNotNone(pod)
        self.assertIsInstance(pod, K8sPod)
        self.assertEqual(pod.name, name)

    def test_init_with_config_and_pull_secrets(self):
        ps = "yomama"
        name = "sofat"
        config = K8sConfig(pull_secret=ps)
        pod = K8sPod(config=config, name=name)
        self.assertIsNotNone(pod.config)
        self.assertEqual(ps, pod.config.pull_secret)

    # ------------------------------------------------------------------------------------- struct

    def test_struct_k8spod(self):
        name = "yomama"
        pod = K8sPod(name=name)
        self.assertIsNotNone(pod)
        self.assertIsInstance(pod, K8sPod)
        self.assertIsNotNone(pod.model)
        self.assertIsInstance(pod.model, Pod)

    def test_struct_pod(self):
        name = "yomama"
        pod = K8sPod(name=name)
        model = pod.model
        self.assertIsInstance(model.model, dict)
        self.assertIsInstance(model.pod_metadata, ObjectMeta)
        self.assertIsInstance(model.pod_spec, PodSpec)
        self.assertIsNone(model.pod_status)

    def test_struct_pod_model(self):
        name = "yomama"
        pod = K8sPod(name=name)
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
        obj = K8sPod(name=name)
        try:
            obj.add_annotation()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_annotation_invalid_args(self):
        name = "yopod"
        obj = K8sPod(name=name)
        k = object()
        v = object()
        try:
            obj.add_annotation(k, v)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_annotation(self):
        name = "yopod"
        obj = K8sPod(name=name)

        k = "yokey"
        v = "yovalue"
        obj.add_annotation(k, v)

        meta = obj.model.model['metadata']
        self.assertIn('annotations', meta)
        self.assertIn(k, meta['annotations'])
        meta = obj.model.pod_metadata.model
        self.assertIn('annotations', meta)
        self.assertIn(k, meta['annotations'])

    # ------------------------------------------------------------------------------------- add label

    def test_add_label_none_args(self):
        name = "yopod"
        obj = K8sPod(name=name)
        try:
            obj.add_label()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_label_invalid_args(self):
        name = "yopod"
        obj = K8sPod(name=name)
        k = object()
        v = object()
        try:
            obj.add_label(k, v)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_label(self):
        name = "yopod"
        obj = K8sPod(name=name)
        k = "yokey"
        v_in = "yovalue"
        obj.add_label(k, v_in)
        v_out = obj.get_label(k)
        self.assertEqual(v_in, v_out)

    # ------------------------------------------------------------------------------------- delete annotation

    def test_del_annotation_none_arg(self):
        name = "yopod"
        obj = K8sPod(name=name)
        try:
            obj.del_annotation()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_del_annotation_invalid_arg(self):
        name = "yopod"
        obj = K8sPod(name=name)
        k = object()
        try:
            obj.del_annotation(k)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_del_annotation_none_yet(self):
        name = "yopod"
        obj = K8sPod(name=name)

        k = "yokey"
        obj.del_annotation(k)

        meta = obj.model.model['metadata']
        self.assertNotIn('annotations', meta)
        meta = obj.model.pod_metadata.model
        self.assertNotIn('annotations', meta)

    def test_del_annotation(self):
        name = "yopod"
        obj = K8sPod(name=name)

        k = "yokey"
        v = "yovalue"
        obj.add_annotation(k, v)

        meta = obj.model.model['metadata']
        self.assertIn('annotations', meta)
        self.assertIn(k, meta['annotations'])
        meta = obj.model.pod_metadata.model
        self.assertIn('annotations', meta)
        self.assertIn(k, meta['annotations'])

        obj.del_annotation(k)

        meta = obj.model.model['metadata']
        self.assertIn('annotations', meta)
        self.assertNotIn(k, meta['annotations'])
        meta = obj.model.pod_metadata.model
        self.assertIn('annotations', meta)
        self.assertNotIn(k, meta['annotations'])

    def test_del_annotation_does_not_exist(self):
        name = "yopod"
        obj = K8sPod(name=name)

        k_1 = "yokey"
        v_1 = "yovalue"
        k_2 = "yonotexists"
        obj.add_annotation(k_1, v_1)

        meta = obj.model.model['metadata']
        self.assertIn('annotations', meta)
        self.assertIn(k_1, meta['annotations'])
        self.assertNotIn(k_2, meta['annotations'])
        meta = obj.model.pod_metadata.model
        self.assertIn('annotations', meta)
        self.assertIn(k_1, meta['annotations'])
        self.assertNotIn(k_2, meta['annotations'])

        obj.del_annotation(k_2)

        meta = obj.model.model['metadata']
        self.assertNotIn(k_2, meta)
        meta = obj.model.pod_metadata.model
        self.assertNotIn(k_2, meta)

    # ------------------------------------------------------------------------------------- delete label

    def test_del_label_none_arg(self):
        name = "yopod"
        obj = K8sPod(name=name)
        try:
            obj.del_label()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_del_label_invalid_arg(self):
        name = "yopod"
        obj = K8sPod(name=name)
        k = object()
        try:
            obj.del_label(k)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_del_label_none_yet(self):
        name = "yopod"
        obj = K8sPod(name=name)

        k = "yokey"
        obj.del_label(k)

        meta = obj.model.model['metadata']
        self.assertIn('labels', meta)
        meta = obj.model.pod_metadata.model
        self.assertIn('labels', meta)

    def test_del_label(self):
        name = "yopod"
        obj = K8sPod(name=name)

        k = "yokey"
        v = "yovalue"
        obj.add_label(k, v)

        meta = obj.model.model['metadata']
        self.assertIn('labels', meta)
        self.assertIn(k, meta['labels'])
        meta = obj.model.pod_metadata.model
        self.assertIn('labels', meta)
        self.assertIn(k, meta['labels'])

        obj.del_label(k)

        meta = obj.model.model['metadata']
        self.assertIn('labels', meta)
        self.assertNotIn(k, meta['labels'])
        meta = obj.model.pod_metadata.model
        self.assertIn('labels', meta)
        self.assertNotIn(k, meta['labels'])

    def test_del_label_does_not_exist(self):
        name = "yopod"
        obj = K8sPod(name=name)

        k_1 = "yokey"
        v_1 = "yovalue"
        k_2 = "yonotexists"
        obj.add_label(k_1, v_1)

        meta = obj.model.model['metadata']
        self.assertIn('labels', meta)
        self.assertIn(k_1, meta['labels'])
        self.assertNotIn(k_2, meta['labels'])
        meta = obj.model.pod_metadata.model
        self.assertIn('labels', meta)
        self.assertIn(k_1, meta['labels'])
        self.assertNotIn(k_2, meta['labels'])

        obj.del_label(k_2)
        meta = obj.model.model['metadata']
        self.assertNotIn(k_2, meta)
        meta = obj.model.pod_metadata.model
        self.assertNotIn(k_2, meta)

    # ------------------------------------------------------------------------------------- get

    # TODO: requires http call
    def test_get(self):
        # name = "yopod"
        # obj = K8sPod(name=name)
        # model = obj.model
        # self.assertEqual(model, obj.get())
        pass

    # ------------------------------------------------------------------------------------- get annotation

    def test_get_annotation_none_args(self):
        name = "yopod"
        obj = K8sPod(name=name)

        try:
            obj.get_annotation()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_annotation_invalid_args(self):
        name = "yopod"
        obj = K8sPod(name=name)

        k = object()
        try:
            obj.get_annotation(k)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_annotation_doesnt_exist(self):
        name = "yopod"
        obj = K8sPod(name=name)

        k = "yonotexists"
        ann = obj.get_annotation(k)
        self.assertIsNone(ann)

    def test_get_annotation(self):
        name = "yopod"
        obj = K8sPod(name=name)

        k = "yokey"
        v_in = "yovalue"
        obj.add_annotation(k, v_in)

        v_out = obj.get_annotation(k)
        self.assertEqual(v_in, v_out)

    # ------------------------------------------------------------------------------------- get annotations

    def test_get_annotations_none(self):
        name = "yopod"
        obj = K8sPod(name=name)
        anns = obj.get_annotations()
        self.assertIsNone(anns)

    def test_get_annotations(self):
        name = "yopod"
        obj = K8sPod(name=name)

        count = 4
        for i in range(0, count):
            k = "key_{0}".format(i)
            v = "value_{0}".format(i)
            obj.add_annotation(k, v)

        anns = obj.get_annotations()

        self.assertIsNotNone(anns)
        self.assertIsInstance(anns, dict)
        self.assertEqual(count, len(anns))
        for i in range(0, count):
            self.assertIn("key_{0}".format(i), anns)

    # ------------------------------------------------------------------------------------- get label

    def test_get_label_none_args(self):
        name = "yopod"
        obj = K8sPod(name=name)

        try:
            obj.get_annotation()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_label_invalid_args(self):
        name = "yopod"
        obj = K8sPod(name=name)

        k = object()
        try:
            obj.get_label(k)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_label_doesnt_exist(self):
        name = "yopod"
        obj = K8sPod(name=name)

        k = "yonotexists"
        l = obj.get_label(k)
        self.assertIsNone(l)

    def test_get_label(self):
        name = "yopod"
        obj = K8sPod(name=name)

        k = "yokey"
        v_in = "yovalue"
        obj.add_label(k, v_in)

        v_out = obj.get_label(k)
        self.assertEqual(v_in, v_out)

    # ------------------------------------------------------------------------------------- get labels

    def test_get_labels_none(self):
        name = "yopod"
        obj = K8sPod(name=name)
        labels = obj.get_labels()
        self.assertIsNotNone(labels)
        self.assertIn('name', labels)

    def test_get_labels(self):
        name = "yopod"
        obj = K8sPod(name=name)

        count = 4
        for i in range(0, count):
            k = "key_{0}".format(i)
            v = "value_{0}".format(i)
            obj.add_label(k, v)

        labels = obj.get_labels()

        self.assertIsNotNone(labels)
        self.assertIsInstance(labels, dict)
        self.assertLessEqual(count, len(labels))  # 'name' already exists as a label
        for i in range(0, count):
            self.assertIn("key_{0}".format(i), labels)

    # ------------------------------------------------------------------------------------- get pod status

    def test_get_pod_status_local(self):
        name = "yopod"
        obj = K8sPod(name=name)
        status = obj.get_status()
        self.assertIsNone(status)

    # TODO: requires http call
    def test_get_pod_status_remote(self):
        pass

    # ------------------------------------------------------------------------------------- is_ready

    def test_is_ready_local(self):
        name = "yopod"
        obj = K8sPod(name=name)
        is_ready = obj.is_ready()
        self.assertFalse(is_ready)

    # TODO: requires http call
    def test_is_ready_remote(self):
        pass

    # ------------------------------------------------------------------------------------- set annotations

    def test_set_annotations_none_args(self):
        name = "yopod"
        obj = K8sPod(name=name)
        try:
            obj.set_annotations()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_annotations_invalid_args(self):
        name = "yopod"
        obj = K8sPod(name=name)
        anns = object()
        try:
            obj.set_annotations(anns)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_annotations(self):
        name = "yopod"
        obj = K8sPod(name=name)
        anns_in = {'key': 'value'}
        obj.set_annotations(anns_in)
        anns_out = obj.get_annotations()
        self.assertEqual(anns_in, anns_out)

    # ------------------------------------------------------------------------------------- set labels

    def test_set_labels_none_args(self):
        name = "yopod"
        obj = K8sPod(name=name)
        try:
            obj.set_labels()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_labels_invalid_args(self):
        name = "yopod"
        obj = K8sPod(name=name)
        labels = object()
        try:
            obj.set_labels(labels)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_labels(self):
        name = "yopod"
        obj = K8sPod(name=name)
        labels_in = {'key': 'value'}
        obj.set_labels(labels_in)
        labels_out = obj.get_labels()
        self.assertEqual(labels_in, labels_out)

    # ------------------------------------------------------------------------------------- set namespace

    def test_set_namespace_none_args(self):
        name = "yopod"
        obj = K8sPod(name=name)
        try:
            obj.set_namespace()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_namespace_invalid_args(self):
        name = "yopod"
        obj = K8sPod(name=name)
        nspace = object()
        try:
            obj.set_namespace(nspace)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_namespace(self):
        name = "yopod"
        obj = K8sPod(name=name)
        nspace_in = "yonamespace"
        obj.set_namespace(nspace_in)
        nspace_out = obj.get_namespace()
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

    # TODO: requires http call
    def test_get_by_name(self):
        # name = "yopod"
        # pods = K8sPod.get_by_name(name=name)
        pass

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

    # TODO: requires http call
    def test_get_by_labels(self):
        # name = "yopod"
        # pods = K8sPod.get_by_name(name=name)
        pass
