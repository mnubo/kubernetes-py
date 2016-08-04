#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
import os
from kubernetes import K8sPodBasedObject, K8sContainer, K8sConfig
from kubernetes.models.v1 import Pod, ReplicationController, ObjectMeta, PodSpec
from tests.test_k8s_pod import K8sPodTest

kubeconfig_fallback = '{0}/.kube/config'.format(os.path.abspath(os.path.dirname(os.path.realpath(__file__))))


class K8sPodBasedObjectTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        K8sPodTest.cleanup_pods()

    # --------------------------------------------------------------------------------- util

    @staticmethod
    def _create_pod(config=None, name=None):
        if config is None:
            try:
                config = K8sConfig(kubeconfig=kubeconfig_fallback)
            except SyntaxError:
                config = K8sConfig()
            except IOError:
                config = K8sConfig()
        obj = K8sPodBasedObject(config=config, obj_type='Pod', name=name)
        obj.model = Pod(name=name)
        return obj

    @staticmethod
    def _create_rc(config=None, name=None):
        if config is None:
            try:
                config = K8sConfig(kubeconfig=kubeconfig_fallback)
            except SyntaxError:
                config = K8sConfig()
        obj = K8sPodBasedObject(config=config, obj_type='ReplicationController', name=name)
        obj.model = ReplicationController(name=name)
        return obj

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sPodBasedObject()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_invalid_config(self):
        config = object()
        try:
            K8sPodBasedObject(config=config)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_invalid_name(self):
        name = object()
        try:
            K8sPodBasedObject(name=name)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_object_type_pod(self):
        ot = "Pod"
        name = "yopod"
        obj = self._create_pod(name=name)
        self.assertIsNotNone(obj)
        self.assertIsInstance(obj, K8sPodBasedObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    def test_init_object_type_rc(self):
        ot = "ReplicationController"
        name = "yorc"
        obj = self._create_rc(name=name)
        self.assertIsNotNone(obj)
        self.assertIsInstance(obj, K8sPodBasedObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    # --------------------------------------------------------------------------------- init

    def test_init_with_model_pod(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        self.assertIsInstance(obj.model, Pod)
        self.assertIsInstance(obj.model.model, dict)
        self.assertIsInstance(obj.model.pod_metadata, ObjectMeta)
        self.assertIsInstance(obj.model.pod_spec, PodSpec)
        self.assertIsNone(obj.model.pod_status)

    def test_init_with_model_rc(self):
        name = "yoname"
        obj = self._create_rc(name=name)
        self.assertIsInstance(obj.model, ReplicationController)
        self.assertIsInstance(obj.model.model, dict)
        self.assertIsInstance(obj.model.pod_metadata, ObjectMeta)
        self.assertIsInstance(obj.model.pod_spec, PodSpec)
        self.assertIsNone(obj.model.pod_status)

    # --------------------------------------------------------------------------------- structure

    def test_struct_with_model_pod_check_podmeta(self):
        name = "yopod"
        obj = self._create_pod(name=name)
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
        name = "yoname"
        obj = self._create_pod(name=name)
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

    def test_struct_with_model_rc_check_podmeta(self):
        name = "yorc"
        obj = self._create_rc(name=name)
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
        name = "yorc"
        obj = self._create_rc(name=name)
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
        name = "yorc"
        obj = self._create_rc(name=name)
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

    # --------------------------------------------------------------------------------- add container

    def test_pod_add_container_invalid(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        c = object()
        try:
            obj.add_container(c)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, AssertionError)

    def test_rc_add_container_invalid(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        c = object()
        try:
            obj.add_container(c)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, AssertionError)

    def test_pod_add_container(self):
        name = "yoname"
        obj = self._create_pod(name=name)

        podspec = obj.model.model['spec']
        self.assertEqual(0, len(podspec['containers']))
        podspec = obj.model.pod_spec
        self.assertEqual(0, len(podspec.containers))
        self.assertEqual(0, len(podspec.model['containers']))

        name = "yopod"
        image = "redis"
        c = K8sContainer(name=name, image=image)
        obj.add_container(c)

        podspec = obj.model.model['spec']
        self.assertEqual(1, len(podspec['containers']))
        podspec = obj.model.pod_spec
        self.assertEqual(1, len(podspec.containers))
        self.assertEqual(1, len(podspec.model['containers']))

    def test_rc_add_container(self):
        name = "yoname"
        obj = self._create_rc(name=name)

        podspec = obj.model.model['spec']['template']['spec']
        self.assertEqual(0, len(podspec['containers']))
        podspec = obj.model.pod_spec
        self.assertEqual(0, len(podspec.containers))
        self.assertEqual(0, len(podspec.model['containers']))

        name = "yopod"
        image = "redis"
        c = K8sContainer(name=name, image=image)
        obj.add_container(c)

        podspec = obj.model.model['spec']['template']['spec']
        self.assertEqual(1, len(podspec['containers']))
        podspec = obj.model.pod_spec
        self.assertEqual(1, len(podspec.containers))
        self.assertEqual(1, len(podspec.model['containers']))

    # --------------------------------------------------------------------------------- add host volume

    def test_pod_add_host_volume_none_args(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        volname = None
        volpath = None
        try:
            obj.add_host_volume(name=volname, path=volpath)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_rc_add_host_volume_none_args(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        volname = None
        volpath = None
        try:
            obj.add_host_volume(name=volname, path=volpath)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_host_volume_invalid_args(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        volname = 666
        volpath = 999
        try:
            obj.add_host_volume(name=volname, path=volpath)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_rc_add_host_volume_invalid_args(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        volname = 666
        volpath = 999
        try:
            obj.add_host_volume(name=volname, path=volpath)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_host_volume(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        volname = "devnull"
        volpath = "/dev/null"
        obj.add_host_volume(name=volname, path=volpath)

        podspec = obj.model.model['spec']
        self.assertEqual(1, len(podspec['volumes']))
        self.assertEqual(volname, podspec['volumes'][0]['name'])

        podspec = obj.model.pod_spec
        self.assertEqual(1, len(podspec.model['volumes']))
        self.assertEqual(volname, podspec.model['volumes'][0]['name'])

    def test_rc_add_host_volume(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        volname = "devnull"
        volpath = "/dev/null"
        obj.add_host_volume(name=volname, path=volpath)

        podspec = obj.model.model['spec']['template']['spec']
        self.assertEqual(1, len(podspec['volumes']))
        self.assertEqual(volname, podspec['volumes'][0]['name'])
        podspec = obj.model.pod_spec
        self.assertEqual(1, len(podspec.model['volumes']))
        self.assertEqual(volname, podspec.model['volumes'][0]['name'])

    # --------------------------------------------------------------------------------- add emptydir volume

    def test_pod_add_emptydir_volume_none_arg(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        volname = None
        try:
            obj.add_emptydir_volume(name=volname)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_rc_add_emptydir_volume_none_arg(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        volname = None
        try:
            obj.add_emptydir_volume(name=volname)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_emptydir_volume_invalid_arg(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        volname = 666
        try:
            obj.add_emptydir_volume(name=volname)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_rc_add_emptydir_volume_invalid_arg(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        volname = 666
        try:
            obj.add_emptydir_volume(name=volname)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_emptydir_volume(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        volname = "emptydir"
        obj.add_emptydir_volume(name=volname)

        podspec = obj.model.model['spec']
        self.assertEqual(1, len(podspec['volumes']))
        self.assertEqual(volname, podspec['volumes'][0]['name'])
        podspec = obj.model.pod_spec
        self.assertEqual(volname, podspec.model['volumes'][0]['name'])

    def test_rc_add_emptydir_volume(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        volname = "emptydir"
        obj.add_emptydir_volume(name=volname)

        podspec = obj.model.model['spec']['template']['spec']
        self.assertEqual(1, len(podspec['volumes']))
        self.assertEqual(volname, podspec['volumes'][0]['name'])
        podspec = obj.model.pod_spec
        self.assertEqual(volname, podspec.model['volumes'][0]['name'])

    # --------------------------------------------------------------------------------- add pull secret

    def test_pod_add_image_pull_secrets_none_arg(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        secretname = None
        try:
            obj.add_image_pull_secrets(name=secretname)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_rc_add_image_pull_secrets_none_arg(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        secretname = None
        try:
            obj.add_image_pull_secrets(name=secretname)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_image_pull_secrets_invalid_arg(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        secretname = 666
        try:
            obj.add_image_pull_secrets(name=secretname)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_rc_add_image_pull_secrets_invalid_arg(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        secretname = 666
        try:
            obj.add_image_pull_secrets(name=secretname)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_image_pull_secrets(self):
        name = "yoname"
        obj = self._create_pod(name=name)
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

    def test_rc_add_image_pull_secrets(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        secretname = "yosecret"
        obj.add_image_pull_secrets(name=secretname)

        podspec = obj.model.model['spec']['template']['spec']
        self.assertIn('imagePullSecrets', podspec)
        self.assertEqual(1, len(podspec['imagePullSecrets']))
        self.assertEqual(secretname, podspec['imagePullSecrets'][0]['name'])
        podspec = obj.model.pod_spec
        self.assertIn('imagePullSecrets', podspec.model)
        self.assertEqual(1, len(podspec.model['imagePullSecrets']))
        self.assertEqual(secretname, podspec.model['imagePullSecrets'][0]['name'])

    # --------------------------------------------------------------------------------- del pod node name

    def test_pod_del_pod_node_name(self):
        name = "yoname"
        obj = self._create_pod(name=name)
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

    def test_rc_del_pod_node_name(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        nodename = "yonodename"
        obj.set_pod_node_name(name=nodename)

        podspec = obj.model.model['spec']['template']['spec']
        self.assertIn('nodeName', podspec)
        self.assertIsInstance(podspec['nodeName'], str)
        self.assertEqual(nodename, podspec['nodeName'])
        podspec = obj.model.pod_spec
        self.assertIn('nodeName', podspec.model)
        self.assertIsInstance(podspec.model['nodeName'], str)
        self.assertEqual(nodename, podspec.model['nodeName'])

        obj.del_pod_node_name()

        podspec = obj.model.model['spec']['template']['spec']
        self.assertNotIn('nodeName', podspec)
        podspec = obj.model.pod_spec
        self.assertNotIn('nodeName', podspec.model)

    # --------------------------------------------------------------------------------- get pod containers

    def test_pod_get_pod_containers_empty(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        containers = obj.get_pod_containers()
        self.assertIsNotNone(containers)
        self.assertEqual(0, len(containers))

    def test_rc_get_pod_containers_empty(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        containers = obj.get_pod_containers()
        self.assertIsNotNone(containers)
        self.assertEqual(0, len(containers))

    def test_pod_get_pod_containers(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        count = 3
        for i in range(0, 3):
            name = "yocontainer_{0}".format(i)
            image = "redis"
            c = K8sContainer(name=name, image=image)
            obj.add_container(c)

        containers = obj.get_pod_containers()
        self.assertIsNotNone(containers)
        self.assertEqual(count, len(containers))
        [self.assertIsInstance(x, dict) for x in containers]

    def test_rc_get_pod_containers(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        count = 3
        for i in range(0, 3):
            name = "yocontainer_{0}".format(i)
            image = "redis"
            c = K8sContainer(name=name, image=image)
            obj.add_container(c)

        containers = obj.get_pod_containers()
        self.assertIsNotNone(containers)
        self.assertEqual(count, len(containers))
        [self.assertIsInstance(x, dict) for x in containers]

    # --------------------------------------------------------------------------------- get pod node name

    def test_pod_get_pod_node_name_none(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        name = obj.get_pod_node_name()
        self.assertIsNone(name)

    def test_rc_get_pod_node_name_none(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        name = obj.get_pod_node_name()
        self.assertIsNone(name)

    def test_pod_get_pod_node_name(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        nodename = "yonodename"
        obj.set_pod_node_name(name=nodename)
        name = obj.get_pod_node_name()
        self.assertEqual(name, nodename)

    def test_rc_get_pod_node_name(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        nodename = "yonodename"
        obj.set_pod_node_name(name=nodename)
        name = obj.get_pod_node_name()
        self.assertEqual(name, nodename)

    # --------------------------------------------------------------------------------- get pod node selector

    def test_pod_get_pod_node_selector_none(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        s = obj.get_pod_node_selector()
        self.assertIsNone(s)

    def test_rc_get_pod_node_selector_none(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        s = obj.get_pod_node_selector()
        self.assertIsNone(s)

    def test_pod_get_pod_node_selector(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        s_in = {"disktype": "ssd"}
        obj.set_pod_node_selector(new_dict=s_in)
        s_out = obj.get_pod_node_selector()
        self.assertEqual(s_in, s_out)

    def test_rc_get_pod_node_selector(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        s_in = {"disktype": "ssd"}
        obj.set_pod_node_selector(new_dict=s_in)
        s_out = obj.get_pod_node_selector()
        self.assertEqual(s_in, s_out)

    # --------------------------------------------------------------------------------- get pod restart policy

    def test_pod_get_pod_restart_policy_none(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        rp = obj.get_pod_restart_policy()
        self.assertEqual('Always', rp)  # set to 'Always' by default

    def test_rc_get_pod_restart_policy_none(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        rp = obj.get_pod_restart_policy()
        self.assertEqual('Always', rp)  # set to 'Always' by default

    def test_pod_get_pod_restart_policy(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        p_in = 'OnFailure'
        obj.set_pod_restart_policy(p_in)
        p_out = obj.get_pod_restart_policy()
        self.assertEqual(p_in, p_out)

    def test_rc_get_pod_restart_policy(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        p_in = 'OnFailure'
        obj.set_pod_restart_policy(p_in)
        p_out = obj.get_pod_restart_policy()
        self.assertEqual(p_in, p_out)

    # --------------------------------------------------------------------------------- get service account

    def test_pod_get_service_account_none(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        acct = obj.get_service_account()
        self.assertIsNone(acct)

    def test_rc_get_service_account_none(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        acct = obj.get_service_account()
        self.assertIsNone(acct)

    def test_pod_get_service_account(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        name_in = "yoservice"
        obj.set_service_account(name_in)
        name_out = obj.get_service_account()
        self.assertEqual(name_in, name_out)

    def test_rc_get_service_account(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        name_in = "yoservice"
        obj.set_service_account(name_in)
        name_out = obj.get_service_account()
        self.assertEqual(name_in, name_out)

    # --------------------------------------------------------------------------------- set active deadline

    def test_pod_set_active_deadline_none_arg(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        d = None
        try:
            obj.set_active_deadline(d)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_rc_set_active_deadline_none_arg(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        d = None
        try:
            obj.set_active_deadline(d)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_active_deadline_invalid_arg(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        d = "yodeadline"
        try:
            obj.set_active_deadline(d)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_rc_set_active_deadline_invalid_arg(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        d = "yodeadline"
        try:
            obj.set_active_deadline(d)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_active_deadline(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        d = 600
        obj.set_active_deadline(d)

        podspec = obj.model.model['spec']
        self.assertIn('activeDeadlineSeconds', podspec)
        self.assertIsInstance(podspec['activeDeadlineSeconds'], int)
        self.assertEqual(d, podspec['activeDeadlineSeconds'])
        podspec = obj.model.pod_spec
        self.assertNotIn('nodeName', podspec.model)
        self.assertIn('activeDeadlineSeconds', podspec.model)
        self.assertIsInstance(podspec.model['activeDeadlineSeconds'], int)
        self.assertEqual(d, podspec.model['activeDeadlineSeconds'])

    def test_rc_set_active_deadline(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        d = 600
        obj.set_active_deadline(d)

        podspec = obj.model.model['spec']['template']['spec']
        self.assertIn('activeDeadlineSeconds', podspec)
        self.assertIsInstance(podspec['activeDeadlineSeconds'], int)
        self.assertEqual(d, podspec['activeDeadlineSeconds'])
        podspec = obj.model.pod_spec
        self.assertNotIn('nodeName', podspec.model)
        self.assertIn('activeDeadlineSeconds', podspec.model)
        self.assertIsInstance(podspec.model['activeDeadlineSeconds'], int)
        self.assertEqual(d, podspec.model['activeDeadlineSeconds'])

    # --------------------------------------------------------------------------------- set pod node name

    def test_pod_set_pod_node_name_none_arg(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        nodename = None
        try:
            obj.set_pod_node_name(name=nodename)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_rc_set_pod_node_name_none_arg(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        nodename = None
        try:
            obj.set_pod_node_name(name=nodename)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_pod_node_name_invalid_arg(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        nodename = 666
        try:
            obj.set_pod_node_name(name=nodename)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_rc_set_pod_node_name_invalid_arg(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        nodename = 666
        try:
            obj.set_pod_node_name(name=nodename)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_pod_node_name(self):
        name = "yoname"
        obj = self._create_pod(name=name)
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

    def test_rc_set_pod_node_name(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        nodename = "yonodename"
        obj.set_pod_node_name(name=nodename)

        podspec = obj.model.model['spec']['template']['spec']
        self.assertIn('nodeName', podspec)
        self.assertIsInstance(podspec['nodeName'], str)
        self.assertEqual(nodename, podspec['nodeName'])
        podspec = obj.model.pod_spec
        self.assertIn('nodeName', podspec.model)
        self.assertIsInstance(podspec.model['nodeName'], str)
        self.assertEqual(nodename, podspec.model['nodeName'])

    # --------------------------------------------------------------------------------- set pod node selector

    def test_pod_set_pod_node_selector_none_arg(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        s_in = None
        try:
            obj.set_pod_node_selector(new_dict=s_in)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_rc_set_pod_node_selector_none_arg(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        s_in = None
        try:
            obj.set_pod_node_selector(new_dict=s_in)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_pod_node_selector_invalid_arg(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        s_in = "yoselector"
        try:
            obj.set_pod_node_selector(new_dict=s_in)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_rc_set_pod_node_selector_invalid_arg(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        s_in = "yoselector"
        try:
            obj.set_pod_node_selector(new_dict=s_in)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_pod_node_selector(self):
        name = "yoname"
        obj = self._create_pod(name=name)
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

    def test_rc_set_pod_node_selector(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        s = {"disktype": "ssd"}
        obj.set_pod_node_selector(new_dict=s)

        podspec = obj.model.model['spec']['template']['spec']
        self.assertIn('nodeSelector', podspec)
        self.assertIsInstance(podspec['nodeSelector'], dict)
        self.assertEqual(s, podspec['nodeSelector'])
        podspec = obj.model.pod_spec
        self.assertIn('nodeSelector', podspec.model)
        self.assertIsInstance(podspec.model['nodeSelector'], dict)
        self.assertEqual(s, podspec.model['nodeSelector'])

    # --------------------------------------------------------------------------------- set pod restart policy

    def test_pod_set_pod_restart_policy_none_arg(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        try:
            obj.set_pod_restart_policy()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_rc_set_pod_restart_policy_none_arg(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        try:
            obj.set_pod_restart_policy()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_pod_restart_policy_not_a_string(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        policy = 666
        try:
            obj.set_pod_restart_policy(policy=policy)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_rc_set_pod_restart_policy_not_a_string(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        policy = 666
        try:
            obj.set_pod_restart_policy(policy=policy)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_pod_restart_policy_invalid_arg(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        policy = 'yopolicy'
        try:
            obj.set_pod_restart_policy(policy=policy)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_rc_set_pod_restart_policy_invalid_arg(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        policy = 'yopolicy'
        try:
            obj.set_pod_restart_policy(policy=policy)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_pod_restart_policy(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        policy = 'Always'
        obj.set_pod_restart_policy(policy=policy)
        p = obj.get_pod_restart_policy()
        self.assertEqual(policy, p)

    def test_rc_set_pod_restart_policy(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        policy = 'Always'
        obj.set_pod_restart_policy(policy=policy)
        p = obj.get_pod_restart_policy()
        self.assertEqual(policy, p)

    # --------------------------------------------------------------------------------- set pod service account

    def test_pod_set_service_account_none_arg(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        try:
            obj.set_service_account()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_rc_set_service_account_none_arg(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        try:
            obj.set_service_account()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_service_account_invalid_arg(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        name = 666
        try:
            obj.set_service_account(name)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_rc_set_service_account_invalid_arg(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        name = 666
        try:
            obj.set_service_account(name)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_service_account(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        name_in = "yoservice"
        obj.set_service_account(name_in)
        name_out = obj.get_service_account()
        self.assertEqual(name_in, name_out)

    def test_rc_set_service_account(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        name_in = "yoservice"
        obj.set_service_account(name_in)
        name_out = obj.get_service_account()
        self.assertEqual(name_in, name_out)

    # --------------------------------------------------------------------------------- set termination grace period

    def test_pod_set_termination_grace_period_none_arg(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        try:
            obj.set_termination_grace_period()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_rc_set_termination_grace_period_none_arg(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        try:
            obj.set_termination_grace_period()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_termination_grace_period_invalid_arg(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        secs = -666
        try:
            obj.set_termination_grace_period(secs)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_rc_set_termination_grace_period_invalid_arg(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        secs = -666
        try:
            obj.set_termination_grace_period(secs)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_termination_grace_period(self):
        name = "yoname"
        obj = self._create_pod(name=name)
        secs_in = 1234
        obj.set_termination_grace_period(secs_in)
        secs_out = obj.get_termination_grace_period()
        self.assertEqual(secs_in, secs_out)

    def test_rc_set_termination_grace_period(self):
        name = "yorc"
        obj = self._create_rc(name=name)
        secs_in = 1234
        obj.set_termination_grace_period(secs_in)
        secs_out = obj.get_termination_grace_period()
        self.assertEqual(secs_in, secs_out)
