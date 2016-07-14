#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
from kubernetes import K8sPodBasedObject, K8sConfig, K8sContainer
from kubernetes.models.v1 import Pod, ReplicationController, ObjectMeta, PodSpec


class K8sPodBasedObjectTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # ------------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sPodBasedObject()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_object_type_pod(self):
        ot = "Pod"
        name = "yomama"
        obj = K8sPodBasedObject(name=name, obj_type=ot)
        self.assertIsNotNone(obj)
        self.assertIsInstance(obj, K8sPodBasedObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    def test_init_object_type_rc(self):
        ot = "ReplicationController"
        name = "yomama"
        obj = K8sPodBasedObject(name=name, obj_type=ot)
        self.assertIsNotNone(obj)
        self.assertIsInstance(obj, K8sPodBasedObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    # ------------------------------------------------------------------------------------- pod - init

    def test_init_with_model_pod(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)
        self.assertIsInstance(obj.model.model, dict)
        self.assertIsInstance(obj.model.pod_metadata, ObjectMeta)
        self.assertIsInstance(obj.model.pod_spec, PodSpec)
        self.assertIsNone(obj.model.pod_status)

    # ------------------------------------------------------------------------------------- pod - structure

    def test_struct_with_model_pod_check_podmeta(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        obj.model = Pod(name=name)
        meta = obj.model.pod_metadata
        self.assertIsNotNone(meta)
        self.assertIsInstance(meta, ObjectMeta)
        self.assertIsInstance(meta.model, dict)
        self.assertEqual(len(meta.model), 3)
        self.assertIn('labels', meta.model)
        self.assertIsInstance(meta.model['labels'], dict)
        self.assertIn('name', meta.model['labels'])
        self.assertEqual(meta.model['labels']['name'], name)
        self.assertIn('name', meta.model)
        self.assertIsInstance(meta.model['name'], str)
        self.assertEqual(meta.model['name'], name)
        self.assertIn('namespace', meta.model)
        self.assertIsInstance(meta.model['namespace'], str)

    def test_struct_with_model_pod_check_podspec(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        obj.model = Pod(name=name)
        spec = obj.model.pod_spec
        self.assertIsNotNone(spec)
        self.assertIsInstance(spec, PodSpec)
        self.assertIsInstance(spec.containers, list)
        self.assertEqual(0, len(spec.containers))
        self.assertIsInstance(spec.model, dict)
        self.assertEqual(len(spec.model), 4)
        self.assertIn('containers', spec.model)
        self.assertIsInstance(spec.model['containers'], list)
        self.assertIn('dnsPolicy', spec.model)
        self.assertIsInstance(spec.model['dnsPolicy'], str)
        self.assertIn('restartPolicy', spec.model)
        self.assertIsInstance(spec.model['restartPolicy'], str)
        self.assertIn('volumes', spec.model)
        self.assertIsInstance(spec.model['volumes'], list)

    # ------------------------------------------------------------------------------------- rc - init

    def test_init_with_model_rc(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='ReplicationController', name=name)
        self.assertIsNotNone(obj)
        obj.model = ReplicationController(name=name)
        self.assertIsInstance(obj.model, ReplicationController)
        self.assertIsInstance(obj.model.model, dict)
        self.assertIsInstance(obj.model.pod_metadata, ObjectMeta)
        self.assertIsInstance(obj.model.pod_spec, PodSpec)
        self.assertIsNone(obj.model.pod_status)
        self.assertIsInstance(obj.model.rc_metadata, ObjectMeta)

    # ------------------------------------------------------------------------------------- rc - structure

    def test_struct_with_model_rc_check_podmeta(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='ReplicationController', name=name)
        self.assertIsNotNone(obj)
        obj.model = ReplicationController(name=name)
        meta = obj.model.pod_metadata
        self.assertIsNotNone(meta)
        self.assertIsInstance(meta, ObjectMeta)
        self.assertIsInstance(meta.model, dict)
        self.assertEqual(len(meta.model), 3)
        self.assertIn('labels', meta.model)
        self.assertIsInstance(meta.model['labels'], dict)
        self.assertIn('name', meta.model['labels'])
        self.assertEqual(meta.model['labels']['name'], name)
        self.assertIn('name', meta.model)
        self.assertIsInstance(meta.model['name'], str)
        self.assertEqual(meta.model['name'], name)
        self.assertIn('namespace', meta.model)
        self.assertIsInstance(meta.model['namespace'], str)

    def test_struct_with_model_rc_check_podspec(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='ReplicationController', name=name)
        self.assertIsNotNone(obj)
        obj.model = ReplicationController(name=name)
        spec = obj.model.pod_spec
        self.assertIsNotNone(spec)
        self.assertIsInstance(spec, PodSpec)
        self.assertIsInstance(spec.containers, list)
        self.assertEqual(0, len(spec.containers))
        self.assertIsInstance(spec.model, dict)
        self.assertEqual(len(spec.model), 4)
        self.assertIn('containers', spec.model)
        self.assertIsInstance(spec.model['containers'], list)
        self.assertIn('dnsPolicy', spec.model)
        self.assertIsInstance(spec.model['dnsPolicy'], str)
        self.assertIn('restartPolicy', spec.model)
        self.assertIsInstance(spec.model['restartPolicy'], str)
        self.assertIn('volumes', spec.model)
        self.assertIsInstance(spec.model['volumes'], list)

    def test_struct_with_model_rc_check_rcmeta(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='ReplicationController', name=name)
        self.assertIsNotNone(obj)
        obj.model = ReplicationController(name=name)
        meta = obj.model.rc_metadata
        self.assertIsNotNone(meta)
        self.assertIsInstance(meta, ObjectMeta)
        self.assertIsInstance(meta.model, dict)
        self.assertEqual(len(meta.model), 3)
        self.assertIn('labels', meta.model)
        self.assertIsInstance(meta.model['labels'], dict)
        self.assertIn('name', meta.model['labels'])
        self.assertEqual(meta.model['labels']['name'], name)
        self.assertIn('name', meta.model)
        self.assertIsInstance(meta.model['name'], str)
        self.assertEqual(meta.model['name'], name)
        self.assertIn('namespace', meta.model)
        self.assertIsInstance(meta.model['namespace'], str)

    # ------------------------------------------------------------------------------------- pod - add container

    def test_pod_add_container_invalid(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        c = object()
        try:
            obj.add_container(c)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, AssertionError)

    def test_pod_add_container(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        podspec = obj.model.model['spec']
        self.assertEqual(0, len(podspec['containers']))

        podspec = obj.model.pod_spec
        self.assertEqual(0, len(podspec.containers))
        self.assertEqual(0, len(podspec.model['containers']))

        name = "yomama"
        image = "busybox"
        c = K8sContainer(name=name, image=image)
        obj.add_container(c)

        podspec = obj.model.model['spec']
        self.assertEqual(1, len(podspec['containers']))

        podspec = obj.model.pod_spec
        self.assertEqual(1, len(podspec.containers))
        self.assertEqual(1, len(podspec.model['containers']))

    # ------------------------------------------------------------------------------------- pod - add host volume

    def test_pod_add_host_volume_none_args(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        volname = None
        volpath = None
        try:
            obj.add_host_volume(name=volname, path=volpath)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_host_volume_invalid_args(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        volname = 666
        volpath = 999
        try:
            obj.add_host_volume(name=volname, path=volpath)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_host_volume(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        volname = "devnull"
        volpath = "/dev/null"
        obj.add_host_volume(name=volname, path=volpath)

        podspec = obj.model.model['spec']
        self.assertEqual(1, len(podspec['volumes']))
        self.assertEqual(volname, podspec['volumes'][0]['name'])

        podspec = obj.model.pod_spec
        self.assertEqual(1, len(podspec.model['volumes']))
        self.assertEqual(volname, podspec.model['volumes'][0]['name'])

    # ------------------------------------------------------------------------------------- pod - add emptydir volume

    def test_pod_add_emptydir_volume_none_arg(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        volname = None
        try:
            obj.add_emptydir_volume(name=volname)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_emptydir_volume_invalid_arg(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        volname = 666
        try:
            obj.add_emptydir_volume(name=volname)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_emptydir_volume(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        volname = "emptydir"
        obj.add_emptydir_volume(name=volname)

        podspec = obj.model.model['spec']
        self.assertEqual(1, len(podspec['volumes']))
        self.assertEqual(volname, podspec['volumes'][0]['name'])

        podspec = obj.model.pod_spec
        self.assertEqual(volname, podspec.model['volumes'][0]['name'])

    # ------------------------------------------------------------------------------------- pod - add pull secret

    def test_pod_add_image_pull_secrets_none_arg(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        secretname = None
        try:
            obj.add_image_pull_secrets(name=secretname)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_image_pull_secrets_invalid_arg(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        secretname = 666
        try:
            obj.add_image_pull_secrets(name=secretname)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_image_pull_secrets(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        secretname = "yosecret"
        obj.add_image_pull_secrets(name=secretname)

        podspec = obj.model.model['spec']
        self.assertIn('imagePullSecrets', podspec)
        self.assertEqual(1, len(podspec['imagePullSecrets']))
        self.assertEqual(secretname, podspec['imagePullSecrets'][0]['name'])

        podspec = obj.model.pod_spec
        self.assertIn('imagePullSecrets', podspec.model)
        self.assertEqual(1, len(podspec.model['imagePullSecrets']))
        self.assertEqual(secretname, podspec.model['imagePullSecrets'][0]['name'])

    # ------------------------------------------------------------------------------------- pod - del pod node name

    def test_pod_del_pod_node_name(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        nodename = "yonodename"
        obj.set_pod_node_name(name=nodename)

        podspec = obj.model.model['spec']
        self.assertIn('nodeName', podspec)
        self.assertIsInstance(podspec['nodeName'], str)
        self.assertEqual(nodename, podspec['nodeName'])

        podspec = obj.model.pod_spec
        self.assertIn('nodeName', podspec.model)
        self.assertIsInstance(podspec.model['nodeName'], str)
        self.assertEqual(nodename, podspec.model['nodeName'])

        obj.del_pod_node_name()

        podspec = obj.model.model['spec']
        self.assertNotIn('nodeName', podspec)

        podspec = obj.model.pod_spec
        self.assertNotIn('nodeName', podspec.model)

    # ------------------------------------------------------------------------------------- pod - get pod containers

    def test_pod_get_pod_containers_empty(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        containers = obj.get_pod_containers()
        self.assertIsNotNone(containers)
        self.assertEqual(0, len(containers))

    def test_pod_get_pod_containers(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        count = 3
        for i in range(0, 3):
            name = "yocontainer_{0}".format(i)
            image = "busybox"
            c = K8sContainer(name=name, image=image)
            obj.add_container(c)

        containers = obj.get_pod_containers()
        self.assertIsNotNone(containers)
        self.assertEqual(count, len(containers))
        [self.assertIsInstance(x, dict) for x in containers]

    # ------------------------------------------------------------------------------------- pod - get pod node name

    def test_get_pod_node_name_none(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        name = obj.get_pod_node_name()
        self.assertIsNone(name)

    def test_get_pod_node_name(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        nodename = "yonodename"
        obj.set_pod_node_name(name=nodename)
        name = obj.get_pod_node_name()
        self.assertEqual(name, nodename)

    # ------------------------------------------------------------------------------------- pod - get pod node selector

    def test_get_pod_node_selector_none(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        s = obj.get_pod_node_selector()
        self.assertIsNone(s)

    def test_get_pod_node_selector(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        s_in = {"disktype": "ssd"}
        obj.set_pod_node_selector(new_dict=s_in)

        s_out = obj.get_pod_node_selector()
        self.assertEqual(s_in, s_out)

    # ------------------------------------------------------------------------------------- pod - set pod node name

    def test_pod_set_pod_node_name_none_arg(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        nodename = None
        try:
            obj.set_pod_node_name(name=nodename)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_pod_node_name_invalid_arg(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        nodename = 666
        try:
            obj.set_pod_node_name(name=nodename)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_pod_node_name(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        nodename = "yonodename"
        obj.set_pod_node_name(name=nodename)

        podspec = obj.model.model['spec']
        self.assertIn('nodeName', podspec)
        self.assertIsInstance(podspec['nodeName'], str)
        self.assertEqual(nodename, podspec['nodeName'])

        podspec = obj.model.pod_spec
        self.assertIn('nodeName', podspec.model)
        self.assertIsInstance(podspec.model['nodeName'], str)
        self.assertEqual(nodename, podspec.model['nodeName'])

    # ------------------------------------------------------------------------------------- pod - set pod node selector

    def test_pod_set_pod_node_selector_none_arg(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        s_in = None
        try:
            obj.set_pod_node_selector(new_dict=s_in)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_pod_node_selector_invalid_arg(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        s_in = "yoselector"
        try:
            obj.set_pod_node_selector(new_dict=s_in)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_pod_node_selector(self):
        name = "yomama"
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)

        s = {"disktype": "ssd"}
        obj.set_pod_node_selector(new_dict=s)

        podspec = obj.model.model['spec']
        self.assertIn('nodeSelector', podspec)
        self.assertIsInstance(podspec['nodeSelector'], dict)
        self.assertEqual(s, podspec['nodeSelector'])

        podspec = obj.model.pod_spec
        self.assertIn('nodeSelector', podspec.model)
        self.assertIsInstance(podspec.model['nodeSelector'], dict)
        self.assertEqual(s, podspec.model['nodeSelector'])
